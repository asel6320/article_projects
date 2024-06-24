from django.db import models

# Create your models here.
class Article(models.Model): #id is there by default
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title')
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name='Author', default="Unknown")
    content = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Created at')

    def __str__(self): #with self.id
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
