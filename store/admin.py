from django.contrib import admin
from .models import Blog, Product
from .forms import ProductForm

# Register your models here.
@admin.register(Blog)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
