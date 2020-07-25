from django.contrib import admin
from .models import gadget,chat,messenger,chat_unseen
from seatbooking.models import notification,new_notes

admin.site.register(gadget)
admin.site.register(chat)
admin.site.register(messenger)
admin.site.register(chat_unseen)
admin.site.register(notification)
admin.site.register(new_notes)