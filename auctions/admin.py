from django.contrib import admin
from .models import User, Bid, Listing, Comment
# Register your models here.

class BidAdmin(admin.ModelAdmin):
	list_display = ("listing", "bidder", "bid")

admin.site.register(Listing)
admin.site.register(Bid, BidAdmin)
admin.site.register(User)
admin.site.register(Comment)