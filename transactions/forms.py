from django.forms import ModelChoiceField, ModelForm
from django.utils import timezone
from categories.models import Category
from transactions.models import Transaction


class CreateTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'] = ModelChoiceField(queryset=Category.objects.filter(user=self.user))
        
    class Meta:
        model = Transaction
        fields = ['category', 'title', 'amount', 'description']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_created = timezone.now()
        instance.user = self.user
        
        if commit:
            instance.save()
        return instance