from django.db import models
from django.urls import reverse, NoReverseMatch

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    named_url = models.CharField(max_length=100, blank=True)
    explicit_url = models.CharField(max_length=100, blank=True)
    menu_name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.explicit_url or '#'
        return self.explicit_url or '#'