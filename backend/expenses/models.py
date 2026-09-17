from django.db import models
from django.core.validators import MinValueValidator


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Education', 'Education'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Health', 'Health'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=150)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash'
    )
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.category})"
