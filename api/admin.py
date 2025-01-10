from django.contrib import admin
from .models import Book , Author , Favorite
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','genre')

admin.site.register(Book,BookAdmin)
admin.site.register(Author)
admin.site.register(Favorite)