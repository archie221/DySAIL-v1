from django.contrib import admin
from .models import book_student, timedetails,authenticate

admin.site.register(authenticate)
admin.site.register(book_student)
admin.site.register(timedetails)