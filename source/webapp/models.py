from django.contrib.auth import get_user_model
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Created at')

    class Meta:
        abstract = True

# Create your models here.
class Article(BaseModel): #id is there by default
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title')
    content = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Content')
    author = models.ForeignKey(
        get_user_model(),
        related_name='articles',
        on_delete=models.SET_DEFAULT,
        default=1)
    tags = models.ManyToManyField(
        "webapp.Tag",
        related_name="articles",
        verbose_name="Tags",
        blank=True,
        through='webapp.ArticleTag',
        through_fields=("article", "tag"),
    )

    def __str__(self): #with self.id
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

class Comment(BaseModel):
   article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE, verbose_name='Статья')
   text = models.TextField(max_length=400, verbose_name='Комментарий')
   author = models.ForeignKey(
       get_user_model(),
       related_name='comments',
       on_delete=models.SET_DEFAULT,
       default=1)


   def __str__(self):
       return self.text[:20]

   class Meta:
       db_table = 'comments'
       verbose_name = 'Comment'
       verbose_name_plural = 'Comments'

class Tag(BaseModel):
    name = models.CharField(max_length=31, verbose_name='Tag')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class ArticleTag(BaseModel):
    article = models.ForeignKey('webapp.Article', related_name='tags_articles', on_delete=models.CASCADE, verbose_name='Article')
    tag = models.ForeignKey('webapp.Tag', related_name='articles_tags', on_delete=models.CASCADE, verbose_name='Tag')
