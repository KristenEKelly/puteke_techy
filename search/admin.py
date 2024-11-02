from django.contrib import admin
from .models import Show, Season, Episode, Subtitle, Actor

# Registering models to make them accessible in the admin panel
admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Subtitle)
admin.site.register(Actor)