from django.db import models
#from django.contrib.auth.models import User


class Blogtype(models.Model):
    title = models.CharField(max_length=32, verbose_name='类别')
    discription = models.CharField(max_length=64, verbose_name='描述')

    class Meta:
        verbose_name_plural = '博客分类'

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=32, verbose_name='标题')
    content = models.TextField()
    #author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    blogtype = models.ForeignKey(Blogtype, on_delete=models.DO_NOTHING, verbose_name='分类')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    #last_updated_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    views = models.IntegerField(default=0, verbose_name='阅读次数')
    stars = models.IntegerField(default=0, verbose_name='赞赏次数')

    class Meta:
        verbose_name_plural = '博客列表'

    def __str__(self):
        return self.title
