from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateTransactionForm
from .models import Transaction

# Create your views here.


@login_required
def create_transaction(request):
    form = CreateTransactionForm(user=request.user)
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:home')
    return render(request, 'create_transaction.html', {'form': form})


@login_required
def delete_transaction(request, slug):
    try:
        transaction = Transaction.objects.get(id=Transaction.get_id(slug))
    except Transaction.DoesNotExist:
        return render(request, '404.html')
    
    transaction.delete()
    return redirect('transactions:view')


@login_required
def view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('date_created').reverse()
    return render(request, 'list_transactions.html', {'transactions': transactions})    