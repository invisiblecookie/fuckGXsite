from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.text import slugify
from slugger import AutoSlugField

# Create your models here.

'''
# 目录
class TableOfContent(models.Model):
    page = models.IntegerField()
'''



# 书目 or 文章
class Book(models.Model):
    SETS = (
    ('经', '经'),
    ('史', '史'),
    ('子', '子'),
    ('集', '集'),
    )
    title = models.CharField(max_length=200)
    #author =  models.ForeignKey(Author, null=True, blank=True, on_delete=SET_NULL)
    #slug = AutoSlugField(populate_from='title')
    slug = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    set = models.CharField(max_length=10, choices=SETS)
    
    def __str__(self):
        return self.title
        '''
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Book, self).save(*args, **kwargs)
    '''

# 小标题
class Subtitle(models.Model):
    title = models.CharField(max_length=200)
    #TOC = models.ForeignKey(TableOfContent, on_delete=models.CASCADE)
    #author =  models.ForeignKey(Author, null=True, blank=True, on_delete=SET_NULL)
    #slug = AutoSlugField(populate_from='title')
    slug = models.CharField(max_length=200, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    dynasty = models.CharField(max_length=100, null=True, blank=True)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=SET_NULL)
    subtitle = models.ForeignKey(Subtitle, null=True, blank=True, on_delete=SET_NULL)
    comment = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
    

