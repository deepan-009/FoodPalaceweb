from django.contrib import admin

from .models import Award, Booking, MenuCategory, MenuItem, Review


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 3
    fields = ("name", "price", "description", "is_veg", "is_signature", "order")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kitchen", "order", "item_count")
    list_filter = ("kitchen",)
    search_fields = ("name",)
    inlines = [MenuItemInline]

    @admin.display(description="items")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_veg", "is_signature")
    list_filter = ("category__kitchen", "is_veg", "is_signature", "category")
    list_editable = ("price", "is_veg", "is_signature")
    search_fields = ("name", "description")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Paste Google reviews straight in here, one at a time."""

    list_display = ("user_name", "rating", "time_ago", "is_local_guide", "is_featured", "likes")
    list_filter = ("rating", "is_local_guide", "is_featured")
    list_editable = ("is_featured",)
    search_fields = ("user_name", "text")
    fieldsets = (
        ("Reviewer", {
            "fields": ("user_name", "profile_pic_url", "is_local_guide",
                       "review_count", "photo_count"),
        }),
        ("Review", {
            "fields": ("rating", "time_ago", "is_edited", "text"),
        }),
        ("Optional detail block", {
            "classes": ("collapse",),
            "fields": ("order_type", "meal_type", "price_range",
                       "food_rating", "service_rating", "atmosphere_rating"),
        }),
        ("Placement", {"fields": ("is_featured", "order", "likes")}),
    )


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "year", "is_highlight", "order")
    list_editable = ("is_highlight", "order")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "occasion", "guests", "preferred_date", "is_handled", "created_at")
    list_filter = ("occasion", "is_handled")
    list_editable = ("is_handled",)
    search_fields = ("name", "phone", "email")
    readonly_fields = ("created_at",)


admin.site.site_header = "Food Palace Family Restaurant"
admin.site.site_title = "Food Palace admin"
admin.site.index_title = "Kitchen, menu and reviews"
