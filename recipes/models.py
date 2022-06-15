import uuid
from click import help_option
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

# Create your models here

class Recipe(models.Model):
    recipe_categories = (
        ('Dessert','Dessert'),
        ('Drinks','Drinks'),
        ('Healthy and Tasty', 'Healthy and Tasty'),
        ('Native', 'Native'),
        ('Pastries', 'Pastries'),
        ('Soup','Soup'),
    )
    servings  = (
        ("1 to 3","1 to 3"),
        ("3 to 5","3 to 5"),
        ("5 to 7","5 to 7"),
        ("more Than 7", "more Than 7"),
    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL, related_name = "my_recipes", null = True)
    recipe_name = models.CharField(max_length=200, help_text="Name Of Recipe")
    recipe_info = models.TextField(max_length=1000, help_text="Give Some Information About This recipe", blank=True, null = True)
    recipe_image = ResizedImageField(size = [500,500],upload_to = "uploads/recipe_images", force_format = "jpeg", quality = 100)
    recipe_details = RichTextField()
    preparation_time = models.IntegerField(help_text="Time to prepare the ingredients, e.g 10 (for 10 minutes)")
    cooking_time = models.IntegerField(help_text="Time to cook the ingredients, e.g 10 (for 10 minutes)")
    category = models.CharField(choices=recipe_categories, max_length=20)
    serving = models.CharField(choices = servings, max_length=15)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True)
    slug = models.SlugField(unique = True, max_length = 200)

    def __str__(self):
        return self.recipe_name
    
    def get_absolute_url(self):
        return reverse('single_recipe',args = [str(self.slug),str(self.id)])
    
    def get_recent_comments(self):
        comments = self.comments.all()[0:10]
        return comments
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.recipe_name)
        return super(Recipe,self).save(*args, **kwargs)


class RecipeBook(models.Model):
    recipes = models.ManyToManyField(Recipe)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="my_recipe_book")

    def __str__(self):
        return f"{self.user.username} Recipes"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="my_comments")
    recipe = models.ForeignKey('Recipe', on_delete = models.CASCADE, related_name="comments")
    message = models.CharField(max_length = 200,help_text="Write A Comment On This Recipe")
    created = models.DateTimeField(auto_now_add = True,blank = True, null = True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.recipe.recipe_name} comment {self.id}"