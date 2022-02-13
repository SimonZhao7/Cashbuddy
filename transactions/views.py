from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateTransactionForm, ViewChoicesForm
from .models import Transaction
from .constants import SORT_CHOICES
from django.core.paginator import Paginator
# Create your views here.


@login_required
def create_transaction(request):
    form = CreateTransactionForm(user=request.user)
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Create Transaction', 'btn_text': 'Create'})


@login_required
def delete_transaction(request, slug):
    try:
        transaction = Transaction.objects.get(id=Transaction.get_id(slug))
    except Transaction.DoesNotExist:
        return render(request, '404.html')
    
    request.user.budget += transaction.amount
    request.user.save()
    transaction.delete() 
    return redirect('transactions:view', sort_by='all')


@login_required
def view(request, sort_by):
    try:
        choice_value = list(filter(lambda choice: choice[0] == sort_by, SORT_CHOICES))[0]
    except IndexError:
        return render(request, '404.html')

    if sort_by == 'all':  
        transactions = Transaction.objects.filter(user=request.user)
    elif sort_by == 'newest':
        transactions = Transaction.objects.filter(user=request.user).order_by('date_created').reverse()
    elif sort_by == 'oldest':
        transactions = Transaction.objects.filter(user=request.user).order_by('date_created')
    elif sort_by == 'price-lh':
        transactions = Transaction.objects.filter(user=request.user).order_by('amount')
    elif sort_by == 'price-hl':
        transactions = Transaction.objects.filter(user=request.user).order_by('amount').reverse()
    elif sort_by == 'category':
        transactions = Transaction.objects.filter(user=request.user).order_by('category')
    p = Paginator(transactions, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    
    form = ViewChoicesForm(initial={'sort_by': SORT_CHOICES[SORT_CHOICES.index(choice_value)]})
    if request.method == 'POST':
        form = ViewChoicesForm(request.POST)
        if form.is_valid():
            return redirect('transactions:view', sort_by=form.cleaned_data['sort_by'])
    return render(request, 'list_transactions.html', {'page_obj': page_obj, 'form': form})    


@login_required
def edit(request, slug):
    try:
        transaction = Transaction.objects.get(id=Transaction.get_id(slug))
    except Transaction.DoesNotExist:
        return render(request, '404.html')
    
    form = CreateTransactionForm(user=request.user, initial={
        'category': transaction.category,
        'title': transaction.title,
        'amount': transaction.amount,
        'description': transaction.description,
    })
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            form.update(transaction)
            return redirect('account:dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Edit Transaction', 'btn_text': 'Edit'})