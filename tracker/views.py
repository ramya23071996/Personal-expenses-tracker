from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm, RegisterForm
from django.db.models import Sum
from django.contrib.auth import login

from django.db.models.functions import TruncMonth
from django.db.models import F

from datetime import date

@login_required
def dashboard(request):
    today = date.today()
    expenses = Expense.objects.filter(user=request.user, date__month=today.month)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    by_category = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
    return render(request, 'tracker/dashboard.html', {'total': total, 'by_category': by_category})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('expense_list')
    return render(request, 'tracker/expense_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'tracker/expense_form.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/expense_confirm_delete.html', {'expense': expense})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
