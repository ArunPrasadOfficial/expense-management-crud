from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum

from .models import Expense
from .serializers import ExpenseSerializer
from .filters import ExpenseFilter


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, partial_update, destroy
    for the Expense model.

    Filtering:  /api/expenses/?category=Food
                /api/expenses/?date=2025-01-20
                /api/expenses/?date_from=2025-01-01&date_to=2025-01-31
    Searching:  /api/expenses/?search=grocery
    Ordering:   /api/expenses/?ordering=-amount
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'amount', 'created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Expense created successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Validation failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Expense updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Validation failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Expense deleted successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Extra endpoint: /api/expenses/summary/ -> total amount + count."""
        qs = self.filter_queryset(self.get_queryset())
        total = qs.aggregate(total=Sum('amount'))['total'] or 0
        return Response({"count": qs.count(), "total_amount": total})
