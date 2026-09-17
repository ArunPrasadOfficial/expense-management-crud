from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'category', 'date', 'payment_method')
    list_filter = ('category', 'payment_method', 'date')
    search_fields = ('title', 'description')
