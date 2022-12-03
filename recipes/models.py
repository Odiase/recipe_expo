import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from embed_video.fields import EmbedVideoField
from embed_video.backends import *

# Create your models here

class Recipe(models.Model):
    '''Recipe Table Schema'''

    recipe_categories = (
        ('Dessert','Dessert'),
        ('Drinks','Drinks'),
        ('Healthy and Tasty', 'Healthy and Tasty'),
        ('Native', 'Native'),
        ('Pastries', 'Pastries'),
        ('Soup','Soup'),
        ('Veggies', 'Veggies'),
    )
    servings  = (
        ("1 to 3","1 to 3"),
        ("3 to 5","3 to 5"),
        ("5 to 7","5 to 7"),
        ("more Than 7", "more Than 7"),
    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL, related_name = "my_recipes", null = True)
    recipe_name = models.CharField(max_length=200)
    recipe_info = models.TextField(max_length=1000, help_text="Give Some Information About This recipe", blank=True, null = True)
    recipe_image = ResizedImageField(size = [600,600],upload_to = "uploads/recipe_images", force_format = "jpeg", quality = 100)
    recipe_preparation = RichTextField()
    preparation_time = models.IntegerField(help_text="Time to prepare the ingredients, e.g 10 (for 10 minutes)")
    cooking_time = models.IntegerField(help_text="Time to cook the ingredients, e.g 10 (for 10 minutes)")
    category = models.CharField(choices=recipe_categories, max_length=20)
    serving = models.CharField(choices = servings, max_length=15)
    created = models.DateTimeField(auto_now_add=True, blank = True, null = True, editable=False)
    updated = models.DateTimeField(auto_now = True, blank = True, null = True, editable=False)
    youtube_video_url = EmbedVideoField(blank = True, null =True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True)
    slug = models.SlugField(unique = True, max_length = 200)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.recipe_name
    
    def get_absolute_url(self):
        '''returns the link to a single recipe view'''
        return reverse('single_recipe', args=[str(self.slug),str(self.id)])

    def get_recent_comments(self):
        '''Returns 5 comments from a recipe'''
        comments = self.comments.all()[0:5]
        return comments
    
    def added_to_recipe_book(self,user):
        '''checking if the current recipe instance is added to a user's recipe book'''
        if RecipeBook.objects.filter(user=user, recipes=self).exists():
            return True
        else:
            return False

    def num_of_likes(self):
        '''Returns Number Of Likes On A Recipe'''

        likes = self.recipe_likes
        likes = likes.count()
        return likes
    
    def already_liked_recipe(self,user):
        '''Checks if a recipe has been liked by a user'''

        if Like.objects.filter(user = user, recipe = self).exists():
            return True
        else:
            return False
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.recipe_name)
        return super(Recipe,self).save(*args, **kwargs)


class ApiRecipe(models.Model):
    '''ApiRecipe Table Schema'''

    id = models.CharField(max_length=200, primary_key=True, unique = True)
    recipe_url = models.URLField()
    image_url = models.URLField(blank=True, null = True)
    name = models.CharField(max_length=200, blank=True, null = True)
    time_to_prepare = models.CharField(max_length=10, blank=True, null = True)
    recipe_link = models.URLField(blank=True, null = True)
    type = "api_recipe"

    def __str__(self):
        return f"{self.name} has an id of {self.id}"


class RecipeBook(models.Model):
    '''RecipeBook Table Schema'''

    recipes = models.ManyToManyField(Recipe)
    api_recipes = models.ManyToManyField(ApiRecipe)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="my_recipe_book")

    def __str__(self):
        return f"{self.user.username} Recipes"


class Comment(models.Model):
    '''Comment Table Schema'''

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="my_comments")
    recipe = models.ForeignKey('Recipe', on_delete = models.CASCADE, related_name="comments")
    message = models.CharField(max_length = 200,help_text="Write A Comment On This Recipe")
    created = models.DateTimeField(auto_now_add = True,blank = True, null = True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.recipe.recipe_name} comment {self.id}"


class Like(models.Model):
    '''Like Table Schema'''
    
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name="recipe_likes")

    class Meta:
        ordering = ['recipe']
    
    def __str__(self):
        return f"{self.recipe.recipe_name} like"