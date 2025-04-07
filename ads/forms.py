from django import forms

from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
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


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        labels = {
            'ad_sender': 'Ваше объявление',
            'ad_receiver': 'Объявление получателя',
            'comment': 'Коментарий',
        }
        widgets = {
            'ad_sender': forms.Select(attrs={'class': 'form-control'}),
            'ad_receiver': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Коментарий'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
            self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)


class ExchangeProposalStatusForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = [ 'status']
        labels = {
            'status': 'Статус предложения',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
