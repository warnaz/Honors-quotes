from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Count, F
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, blank=True)
    image = models.ImageField(upload_to='media/', default='image/gosling.jpg')
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_sum_category(self):
        if self.quotes_author:
            sum_cat = self.quotes_author.aggregate(quant=Count('category'))
            query_cat = self.quotes_author.all().values(
                'category__title').annotate(
                total=(Count('category')))

            aggr = {}

            for i in query_cat:
                key = i['category__title']
                caun = (i['total'] / sum_cat['quant']) * 100
                aggr[key] = [round(caun, 2), i['total']]

            return aggr

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.user}'

    def save(self, *args, **kwargs):
        self.slug = str(self.user)
        return super().save(*args, **kwargs)
