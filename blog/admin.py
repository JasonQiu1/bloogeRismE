from django.contrib import admin

from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title_text',)}
    fieldsets = [
        (None,                  {'fields':['title_text', 'slug']}),
        ('Date information',    {'fields':['pub_date', 'hidden']}),
        (None,                  {'fields':['body']}),
    ]
    list_display = ('title_text', 'pub_date', 'hidden')
    list_filter = ['pub_date']
    search_fields = ['title_text']

admin.site.register(Post, PostAdmin)
