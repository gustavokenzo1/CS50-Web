from django.contrib import admin

from .models import Auction, Bid, Comment, User, Watchlist


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starting_bid',
                    'current_price', 'is_active')


class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'price')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'text')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction')


# Register your models here.
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
