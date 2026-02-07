from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# User model
class UserProfile(models.Model):
    # links our model user to a django User model. not done via inheritance in order to allow other parts of rango to access users
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional attributes that our site's users will have on top of the pre-defined django ones
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username

    
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
