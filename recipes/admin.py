from django.contrib import admin
from .models import Recipe, Comment, RecipeBook, Like, ApiRecipe
# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields ={"slug": ("recipe_name",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
    )


admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(RecipeBook)
admin.site.register(Like)
admin.site.register(ApiRecipe)