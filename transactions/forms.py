from django import forms
from django.forms import ModelChoiceField, ModelForm
from categories.models import Category
from transactions.models import Transaction


class CreateTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'] = ModelChoiceField(queryset=Category.objects.filter(user=self.user))
        
    class Meta:
        model = Transaction
        fields = ['category', 'title', 'date_created', 'amount', 'description']
        widgets = {
            'date_created': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 10, 'col': 20})
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        
        if commit:
            instance.save()
        return instance

    def update(self, instance):
        data = self.cleaned_data
        instance.title = data['title']
        instance.category = data['category']
        instance.date_created = data['date_created']
        instance.amount = data['amount']
        instance.description = data['description']
        instance.save()
        return instance