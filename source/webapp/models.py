from django.db import models

# Create your models here.
class Section(models.Model): #the same as categories in the lab
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title', unique=True)
    description = models.CharField(max_length=50, null=True, blank=True, verbose_name='Description')

    def __str__(self): #with self.id
        return f"{self.pk}. {self.title}"
    class Meta:
        db_table = 'sections'
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
class Article(models.Model): #id is there by default
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title')
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name='Author', default="Unknown")
    content = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Created at')
    section = models.ForeignKey("webapp.Section", on_delete=models.RESTRICT, verbose_name='Section', related_name='articles', null=True)

    def __str__(self): #with self.id
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
