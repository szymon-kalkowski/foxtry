from typing import List
from django.contrib import admin
from main.models import *

admin.site.register(Workers)
admin.site.register(Service)
admin.site.register(Customer)

class OrderItemAdmin(admin.StackedInline):
    model = OrderItem

class PortfolioRowAdmin(admin.StackedInline):
    model = PortfolioRow

class PortfolioVideoAdmin(admin.StackedInline):
    model = PortfolioVideo

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioRowAdmin, PortfolioVideoAdmin]

    class Meta:
        model = Portfolio

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]

    class Meta:
        model = Order