from django.forms import ModelForm
from .models import Category


class CreateCategoryForm(ModelForm):
    class Meta: 
        model = Category
        fields = ['name']
        
    def save(self, request, commit=True):
        instance = super().save(commit=False)
        instance.user = request.user
        
        if commit:
            instance.save()
        return instance
    
    def update(self, instance):
        instance.name = self.cleaned_data['name']
        instance.save()
        return instance