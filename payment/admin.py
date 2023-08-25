from django.contrib import admin

from .models import Payment, Transactions


admin.site.register(Payment)
admin.site.register(Transactions)