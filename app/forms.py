from django import forms
from .models import DesignRequest, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]
        labels = { "title": "Название категории" }

class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        exclude = ['user']
        fields = ['title', 'content', 'image', 'category', 'status', 'comment', 'image_after']
        labels = {"status": "Статус", "title": "Название", "content": "Контент", "image": "Изображение", "category": "Категория", "comment": "Комментарий", "image_after": "Изображение после работы" }
        widgets = {
            "category": forms.Select(attrs={'class': "form-control"}),
            "comment": forms.Textarea(attrs={'class': "form-control"}),
            "status": forms.Select(attrs={'class': "form-control"}),
        }