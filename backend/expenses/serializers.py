from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'amount', 'category', 'date',
            'payment_method', 'description', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_amount(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_category(self, value):
        valid_categories = [c[0] for c in Expense.CATEGORY_CHOICES]
        if value not in valid_categories:
            raise serializers.ValidationError(
                f"Category must be one of {valid_categories}."
            )
        return value

    def validate_date(self, value):
        import datetime
        if value > datetime.date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value
