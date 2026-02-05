from django import forms
from rango.models import Page, Category

MAX_LEN = 128
MAX_URL = 200

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=MAX_LEN, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=MAX_LEN,help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=MAX_URL,help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")
        # if url not empty and doesn't start with http:// add it. also allow https because why isnt it there
        if url and not (url.startswith("http://") or url.startswith("https://")):
            url = f"http://{url}"
            cleaned_data["url"] = url

        return cleaned_data
