from django.contrib import admin
from .models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'amount', 'category', 'date']
    list_filter = ['category', 'date']
    search_fields = ['title', 'user__username']

admin.site.register(Expense, ExpenseAdmin)
