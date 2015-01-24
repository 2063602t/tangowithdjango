from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

# Create your views here.
def index(request):
    # Query the database (via the object-model) for a list of ALL categories
    # Order the response by the no. of likes in descending order.
    # Retrieve the top 5 or all if there are fewer than five
    category_list = Category.objects.order_by('-likes')[:5]
    # Construct a dictionary to pass the template engine as its context.
    context_dict = {'categories': category_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'boldmessage': "about page!"}
    return render(request, 'rango/about.html', context_dict)