from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, UserProfile, User
from rango.forms import CategoryForm, PageForm, UserProfileForm
from datetime import datetime
from rango.bing_search import run_query


# Create your views here.
def index(request):
    # Query the database (via the object-model) for a list of ALL categories
    # Order the response by the no. of likes in descending order.
    # Retrieve the top 5 or all if there are fewer than five
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Construct a dictionary to pass the template engine as its context.
    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits', 0)
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits += 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    # Return response back to user, updating any cookies that need changed.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    visits = request.session.get('visits', 0)
    # if visits >= 1:
    # first_visit = False
    # else:
    #     first_visit = True

    context_dict = {'boldmessage': "Rango's about page!", 'visits': visits}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = dict()
    context_dict['result_list'] = None
    context_dict['query'] = None

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() Method raises a DoesNotExist exception.
        # So th .get() method returns one model instance, or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that the filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name "pages".
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists
        context_dict['category'] = category

        # Increment view count
        category.views += 1
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            try:
                # Save the new category to the database.
                form.save(commit=True)

                # Now call the index() view.
                # The user will be shown the homepage.
                return index(request)
            except IntegrityError as e:
                return form.errors.add_error('name', 'This category already exists.')
        else:
            # The supplied form contained errors - just print them to the terminal
            print form.errors
    else:
        # If the request was not a POST display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    # A HTTP POST?
    if request.method == 'POST':
        form = PageForm(request.POST)

        # a valid form?
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


@login_required
def register_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            new_profile = profile_form.save(commit=False)
            current_profile = UserProfile.objects.get_or_create(user=User.objects.get_by_natural_key(user.username))[0]
            current_profile.website = new_profile.website
            current_profile.picture = new_profile.picture
            current_profile.save()

    else:
        profile_form = UserProfileForm

    return render(request, 'rango/profile_registration.html', {'profile_form': profile_form})


def profile(request, username):
    user = User.objects.get_by_natural_key(username)
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    website = user_profile.website
    picture = user_profile.picture
    return render(request, 'rango/profile.html',
                  {'picture': picture.name, 'website': website, 'user_name': user.username})


def track_url(request):
    url = '/rango/'
    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            url = page.url
    return redirect(url)