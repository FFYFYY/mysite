from django.shortcuts import render
from .models import Blog, Blogtype
from django.db.models import Count
import markdown


def blogs(request):
    blogs = Blog.objects.all().order_by('-views')
    blog_count = Blog.objects.all().count()
    blogtypes = Blogtype.objects.annotate(blog_count=Count('blog'))  # 加入计数
    context = {
        'blogs': blogs,
        'blog_count': blog_count,
        'blogtypes': blogtypes,
    }
    return render(request, 'blog/blogs.html', context)


def blogtype(request, blogtype_id):
    try:
        blogtype = Blogtype.objects.get(id=blogtype_id)
    except:
        return render(request, 'error.html')
    blog_count = Blog.objects.all().count()
    blogtypes = Blogtype.objects.annotate(blog_count=Count('blog'))
    blogs = Blog.objects.filter(blogtype=blogtype).order_by('-views')
    context = {
        'blogs': blogs,
        'blogtype_title': blogtype.title,
        'blogtypes': blogtypes,
        'blog_count': blog_count,
    }
    return render(request, 'blog/class.html', context)


def blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except:
        return render(request, 'error.html')
    blog.views += 1
    blog.save()
    blog_count = Blog.objects.all().count()
    blogtypes = Blogtype.objects.annotate(blog_count=Count('blog'))
    blog.content = markdown.markdown(
        blog.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ],
    )
    context = {
        'blog': blog,
        'blogtypes': blogtypes,
        'blog_count': blog_count,
    }
    return render(request, 'blog/blog.html', context)


def blogtypes(request):
    blog_count = Blog.objects.all().count()
    blogtypes = Blogtype.objects.annotate(blog_count=Count('blog'))
    context = {
        'blogtypes': blogtypes,
        'blog_count': blog_count,
    }
    return render(request, 'blog/blogtype.html', context)
