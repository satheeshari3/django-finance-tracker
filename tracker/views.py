from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum  # Don't forget this import

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, "tracker/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_income = transactions.filter(category="Income").aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(category="Expense").aggregate(Sum('amount'))['amount__sum'] or 0
    net_savings = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_savings': net_savings,
    }
    return render(request, 'tracker/dashboard.html', context)

#--------------------------------------------MAIN LOGIC FOR THE APP--------------------------------------------

# List transactions (only the logged-in user's)
@login_required
def list_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_income = transactions.filter(category="Income").aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(category="Expense").aggregate(Sum('amount'))['amount__sum'] or 0
    net_savings = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_savings': net_savings,
    }

    return render(request, 'tracker/transaction_list.html', context)


# Add new transaction
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # attach logged-in user
            transaction.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm()

    return render(request, 'tracker/add_transaction.html', {'form': form})


# Edit transaction
@login_required
def edit_transaction(request, pk):
    # ensure user can only edit their own transaction
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            edited_transaction = form.save(commit=False)
            edited_transaction.user = request.user  # ensure user stays same
            edited_transaction.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'tracker/edit_transaction.html', {'form': form})


# Delete transaction
@login_required
def delete_transaction(request, pk):
    # ensure user can only delete their own transaction
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        return redirect('list_transactions')

    return render(request, 'tracker/delete_transaction.html', {'transaction': transaction})