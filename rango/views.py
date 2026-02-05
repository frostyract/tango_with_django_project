from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

# views go here
def index(request):
    # query the db for all categories then return the top 5 liked ones
    category_list = Category.objects.order_by('-likes')[:5]
    # now pass that to something the template can use
    context_dict = {
      "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!",
      "categories": category_list,
    }
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {
      "your_name": "Insert Name", 
    }
    return render(request, 'rango/about.html', context=context_dict)
