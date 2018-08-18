from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<int:blog_id>/', views.blog, name='blog'),
    path('blogtype/<int:blogtype_id>/', views.blogtype, name='blogtype'),
    path('blogtypes/', views.blogtypes, name='blogtypes'),#小屏幕分类展示
]
