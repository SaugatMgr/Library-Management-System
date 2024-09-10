from django.contrib import admin
from .models import Genre, Book, Borrow, Reserve, ReserveQueue, Notification, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created_on", "modified_on")
    search_fields = ("name",)
    ordering = ("-created_on",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "isbn",
        "availability_status",
        "quantity",
        "price",
    )
    list_filter = ("availability_status", "genres", "section", "shelf")
    search_fields = ("title", "author", "isbn")
    ordering = ("-created_on",)
    filter_horizontal = ("genres",)
    inlines = [RatingInline]


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "get_borrower_name",
        "borrowed_date",
        "due_date",
        "returned_date",
        "borrow_status",
    )
    list_filter = ("borrow_status", "borrowed_date", "due_date")
    search_fields = (
        "book__title",
        "borrower__first_name",
        "borrower__middle_name",
        "borrower__last_name",
    )
    ordering = ("-borrowed_date",)

    def get_borrower_name(self, obj):
        return f"{obj.borrower.first_name} {obj.borrower.middle_name or ''} {obj.borrower.last_name}".strip()

    get_borrower_name.short_description = "Borrower"


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ("book", "get_reserver_name", "reserved_date", "reserve_status")
    list_filter = ("reserve_status", "reserved_date")
    search_fields = (
        "book__title",
        "reserver__first_name",
        "reserver__middle_name",
        "reserver__last_name",
    )
    ordering = ("-reserved_date",)

    def get_reserver_name(self, obj):
        return f"{obj.reserver.first_name} {obj.reserver.middle_name or ''} {obj.reserver.last_name}".strip()

    get_reserver_name.short_description = "Reserver"


@admin.register(ReserveQueue)
class ReserveQueueAdmin(admin.ModelAdmin):
    list_display = ("book", "users")
    search_fields = ("book__title",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "timestamp", "is_read")
    list_filter = ("is_read", "timestamp")
    search_fields = (
        "user__first_name",
        "user__middle_name",
        "user__last_name",
        "message",
    )
    ordering = ("-timestamp",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("get_user_name", "book", "rating")
    list_filter = ("rating",)
    search_fields = (
        "user__first_name",
        "user__middle_name",
        "user__last_name",
        "book__title",
    )
    ordering = ("-created_on",)

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.middle_name or ''} {obj.user.last_name}".strip()

    get_user_name.short_description = "User"
