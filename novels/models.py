from django.db import models


class Booktype(models.Model):
    booktype = models.CharField(max_length=120, verbose_name='类型')

    class Meta:
        verbose_name_plural = '书本分类'

    def __str__(self):
        return self.booktype


class Novel(models.Model):
    bookname = models.CharField(max_length=120, verbose_name='书名')
    summary = models.CharField(max_length=120, verbose_name='简介', default='暂无')
    author = models.CharField(max_length=120, verbose_name='作者', default='暂无')
    booktype = models.ForeignKey(Booktype, on_delete=models.DO_NOTHING,
                                 verbose_name='类型')
    read_count = models.IntegerField('阅读量', default=0)
    search_count = models.IntegerField('搜索量', default=0)

    class Meta:
        verbose_name_plural = '书本信息'

    def __str__(self):
        return self.bookname



class Chapter(models.Model):
    bookname = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='书名')
    chapter_num = models.IntegerField(default='**', verbose_name='章节数')
    chapter_title = models.CharField(max_length=120, verbose_name='章节')
    text = models.TextField(verbose_name='内容')

    class Meta:
        verbose_name_plural = '章节内容'

    def __str__(self):
        return self.chapter_title
