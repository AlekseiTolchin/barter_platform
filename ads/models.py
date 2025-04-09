from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Ad(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='ads',
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    image_url = models.URLField(
        verbose_name='URL изображения',
        blank=True,
        null=True,
    )
    category = models.CharField(
        verbose_name='Категория',
        max_length=50,
    )
    condition = models.CharField(
        verbose_name='Состояние',
        max_length=50,
        choices=(('new', 'Новый'), ('used', 'Б/У')),
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ads:ad_detail', kwargs={'pk': self.pk})


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        Ad,
        verbose_name='Объявление отправителя',
        on_delete=models.CASCADE,
        related_name='sent_proposals'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        verbose_name='Объявление получателя',
        on_delete=models.CASCADE,
        related_name='received_proposals'
    )
    comment = models.TextField(
        verbose_name='Коментарий',
    )
    status = models.CharField(
        verbose_name='Статус предложения',
        max_length=50,
        choices=(
            ('pending', 'Ожидает'),
            ('accepted', 'Принята'),
            ('rejected', 'Отклонена')
        ),
        default='pending',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
        ordering = ['-created_at']

    def __str__(self):
        return f'Предложение обмена от {self.ad_sender} - {self.ad_receiver}'

    def get_absolute_url(self):
        return reverse('ads:proposal_detail', kwargs={'pk': self.pk})
