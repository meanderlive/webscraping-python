from django.contrib import admin


from django.utils import timezone

from .models import Category, Listing , Paragraph , Heading


class ListingAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'content', 'created_by', 'slug','flagged', 'flagged_by', 'flagged_at')
    list_filter = ('flagged',)
    # exclude = ['slug', 'created_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        if obj.flagged:
            obj.flagged_by = request.user
            obj.flagged_at = timezone.now()
        else:
            obj.flagged_by = obj.flagged_at = None

        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site
admin.site.register(Listing, ListingAdmin)
admin.site.register(Heading)
admin.site.register(Paragraph)