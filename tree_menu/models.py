from django.db import models
from django.urls import reverse, NoReverseMatch

class MenuItem(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название пункта')
    named_url = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Named URL',
        help_text='Именованный URL из urls.py'
    )
    explicit_url = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Явный URL',
        help_text='Явный URL (если нет named URL)'
    )
    menu_name = models.CharField(
        max_length=50, 
        verbose_name='Название меню',
        help_text='Название меню, к которому относится этот пункт'
    )
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='children',
        verbose_name='Родительский пункт'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
        help_text='Порядок сортировки пунктов меню'
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                url = reverse(self.named_url)
            except NoReverseMatch:
                url = self.explicit_url if self.explicit_url else '#'
            return url
        return self.explicit_url if self.explicit_url else '#'