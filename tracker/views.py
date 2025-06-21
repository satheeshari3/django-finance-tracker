from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum  # Don't forget this import


def list_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')

    total_income = Transaction.objects.filter(category="Income").aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(category="Expense").aggregate(Sum('amount'))['amount__sum'] or 0
    net_savings = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_savings': net_savings,
    }
    return render(request, 'tracker/transaction_list.html', context)


def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})
from django.shortcuts import get_object_or_404

# Edit transaction
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/edit_transaction.html', {'form': form})

# Delete transaction
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('list_transactions')
    return render(request, 'tracker/delete_transaction.html', {'transaction': transaction})