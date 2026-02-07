# PYTHON IMPORTS
from datetime import datetime

# DJANGO IMPORTS
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# RANGO IMPORTS
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# ----------------------
# AUTHLESS VIEWS GO HERE
# ----------------------

def index(request):
    # query the db for all categories then return the top 5 liked ones
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    visitor_cookie_handler(request)
    # now pass that to something the template can use
    context_dict = {
      "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!",
      "categories": category_list,
      "pages": page_list,
    }
    # render the response BEFORE returning it so we can do cookie stuff
    return render(request, 'rango/index.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict["pages"] = pages
        context_dict["category"] = category
    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, 'rango/category.html', context=context_dict) 

def about(request):
    visitor_cookie_handler(request)
    context_dict = {
      "your_name": "Insert Name",
      "visits": request.session["visits"]
    }
    return render(request, 'rango/about.html', context=context_dict)

# --------------------------------------
# VIEWS THAT REQUIRE AUTH TO USE GO HERE
# --------------------------------------

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/rango/")
        else:
            print(form.errors)
    return render(request, "rango/add_category.html", {"form": form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # can't add a page to category that doesn't exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_category", kwargs = {"category_name_slug": category_name_slug}))
        else:
            print(form.errors)
    context_dict = {"form": form, "category":category}
    return render(request, "rango/add_page.html", context=context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# ------------------------------------------------
# VIEWS RELATING TO AUTHENTICATION PROCESS GO HERE
# ------------------------------------------------

def register(request):
    registered = False
    # for a user who is sending in their form
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # django user stuff first
            user = user_form.save()
            user.set_password(user.password) # this hashes the password
            user.save()
            # and now our specific user profile stuff
            profile = profile_form.save(commit=False) # hold on, don't save to the db quite yet!
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save() # now save the userprofile model instance
            registered = True # the user is now registered!
        else: # if the stuff in the POST is invalid
            print(user_form.errors, profile_form.errors)
    # for a regular access of the url (non-post)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    # now render the site, with the specified context
    context_dict = {
        "user_form": user_form,
        "profile_form": profile_form,
        "registered": registered,
    }
    return render(request, 'rango/register.html', context=context_dict)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active: # make sure the account isn't frozen
                login(request, user) # log the user in if acc active
                return redirect(reverse('rango:index')) # send user back to homepage
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username} {password}")
            return HttpResponse("Invalid login details supplied.")
    # request isn't POST, it's probably a GET, so display login form
    else:
        return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

# ------------
# cookie stuff
# -------------

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val: val = default_val
    return val

def visitor_cookie_handler(request):
    # get number of visits from user's cookie; if there are none set to 1
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    # check WHEN the last visit was from the cookie
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # now, if the last visit was over one day ago..
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    # update the visit counter in the cookie
    request.session['visits'] = visits
    return visits
