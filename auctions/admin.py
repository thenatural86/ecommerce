from django.contrib import admin
from .models import User, Listing, Bid, Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "image", "category")


# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
