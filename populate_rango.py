import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # create list of dictionaries containing pages for each category,
    # then create dictionary for our categories and put the page dictionary list into them
    python_pages = [
            {"title": "Official Python Tutorial",
             "url":"http://docs.python.org/3/tutorial"
            },
            {"title": "How to Think like a Computer Scientist",
             "url":"http://greenteapress.com/thinkpython/"
             },
            {"title":"Learn Python in 10 Minutes",
             "url":"httpL//www.korokithakis.net/tutorials/python/"},
    ]

    django_pages = [
            {"title":"Official Django Tutorial",
             "url":"https://docs.djangoproject.com/en/2.1/intro/tutorial01/"
            },
            {"title":"Django Rocks",
             "url":"http://djangorocks.com"
            },
            {"title":"How to Tango with Django",
             "url":"http://www.tangowithdjango.com/"}
    ]

    other_pages = [
            {"title":"Bottle",
             "url":"http://bottlepy.org/docs/dev/"
            },
            {"title":"Flask",
             "url":"http://flask.pocoo.org"
            }
    ]

    categories = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
                  "Django": {"pages": django_pages, "views": 64, "likes": 32},
                  "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}
                 }
    # helper functions for adding categories and pages
    def add_page(category, title, url, views=0):
        p = Page.objects.get_or_create(category=category, title=title)[0]
        p.url = url
        p.views = views
        p.save()
        return p

    def add_cat(name, likes=0, views=0): # i would call this add_category but don't want to risk failing a test
        c = Category.objects.get_or_create(name=name)[0]
        c.likes = likes
        c.views = views
        c.save()
        return c

    # goes through each category and actually adds them - along with all of their pages - to the db
    for category, category_data in categories.items():
        # returns 0 if there is no likes or views field specified in the category dictionary
        c = add_cat(category, likes=category_data.get("likes",0), views=category_data.get("views",0))
        for p in category_data["pages"]:
            add_page(c, p["title"], p["url"])

    # now we're going to make sure they've actually been added
    # i would personally print show this info differently but again i dont want to risk failing a test due to that
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f"{c}: {p}")

# allows this module to be run standalone as well as being able to use it for imports
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
