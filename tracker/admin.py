from django.contrib import admin
from .models import User, Asset, CheckoutLog

# This tells Django to show these tables in the Admin panel!
admin.site.register(User)
admin.site.register(Asset)
admin.site.register(CheckoutLog)