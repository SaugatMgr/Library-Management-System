from django.contrib import admin

# Register your models here.
from .models import Reserve, ReserveQueue, Tag, Genre, Book, Borrow

admin.site.register(Tag)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Reserve)
admin.site.register(ReserveQueue)
