from django.contrib import admin

from .models import Film

# Configures the Django admin panel. Useful during development.
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'location')
    search_fields = ('title', 'release_year', 'location')

admin.site.register(Film, FilmAdmin)
