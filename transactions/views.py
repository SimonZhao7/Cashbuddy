from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateTransactionForm

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