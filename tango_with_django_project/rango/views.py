from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page


# Create your views here.
def index(request):
    # Query the database (via the object-model) for a list of ALL categories
    # Order the response by the no. of likes in descending order.
    # Retrieve the top 5 or all if there are fewer than five
    category_list = Category.objects.order_by('-likes')[:5]
    # Construct a dictionary to pass the template engine as its context.
    context_dict = {'categories': category_list}

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'boldmessage': "about page!"}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() Method raises a DoesNotExist exception.
        # So th .get() method returns one model instance, or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict = {'category_name': category.name}

        # Retrieve all of the associated pages.
        # Note that the filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name "pages".
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)
