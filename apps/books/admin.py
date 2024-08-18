from django.contrib import admin

# Register your models here.
from .models import Rating, Reserve, ReserveQueue, Tag, Genre, Book, Borrow


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


class BookAdmin(admin.ModelAdmin):
    inlines = [RatingInline]


admin.site.register(Tag)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrow)
admin.site.register(Reserve)
admin.site.register(ReserveQueue)
