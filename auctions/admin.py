from django.contrib import admin
from .models import Comment, User, Listing, Bid

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
