from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad  # Указываем модель, связанную с формой
        fields = ['title', 'description', 'image_url', 'category', 'condition']  # Поля, которые будут доступны в форме
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'image_url': 'URL изображения',
            'category': 'Категория',
            'condition': 'Состояние',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Введите URL изображения'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Укажите категорию'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }
