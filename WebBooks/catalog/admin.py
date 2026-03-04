from django.contrib import admin

from .models import Book, Author, Genre, Language, Status, BookInstance

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)
class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInLine]
@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_field = ('book', 'status')
    list_display = ('book', 'status','borrower','due_back', 'id')
    fieldsets = [
        ('Book', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Status', {
            'fields': ('status', 'due_back', 'borrower')
        })
    ]