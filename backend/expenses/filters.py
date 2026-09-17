import django_filters
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    payment_method = django_filters.CharFilter(field_name='payment_method', lookup_expr='iexact')

    class Meta:
        model = Expense
        fields = ['category', 'date', 'date_from', 'date_to', 'payment_method']
