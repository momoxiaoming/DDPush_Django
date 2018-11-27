#coding=utf-8
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),  #自动打卡应用地址导入主项目
    path('regDev/', views.regDev, name='regDev'),
    path('taskQury/', views.taskQury, name='taskQury'),
    path('taskSubmt/', views.taskSubmt, name='taskSubmt'),
    path('updateApk/', views.updateApk, name='updateApk'),

]