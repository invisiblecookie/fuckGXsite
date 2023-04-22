from django.contrib import admin
from .models import *
# Register your models here.




class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'set','description')

admin.site.register(Book, BookAdmin)


class AutherAdmin(admin.ModelAdmin):
    list_display = ('name','book','subtitle', 'comment')

admin.site.register(Author, AutherAdmin)

class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'book')

admin.site.register(Subtitle, SubtitleAdmin)