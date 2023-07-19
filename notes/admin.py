from django.contrib import admin

from .models import Note, Image, DisplayMode
# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class NotesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Created by', {'fields': ['user']}),
        ('Note Text', {'fields': ['note_text']}),
        ('Date Information', {'fields': ['date_created']}),
        ('Colour Theme', {'fields': ['colour_theme']})
    ]

    list_display = ('user', 'pk', 'note_text', 'date_created', 'colour_theme', 'has_excess_images')
    list_filter = ['last_updated', 'user']
    search_fields = ['note_text']
    inlines = [ImageInline]

class NoteInline(admin.TabularInline):
    model = Note
    extra = 2

class UsersAdmin(admin.ModelAdmin):
    inlines = [NoteInline]

admin.site.register(Note, NotesAdmin)

admin.site.register(DisplayMode)