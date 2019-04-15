from django.urls import path
from . import views
urlpatterns = [
    path('bindDev/', views.bindDev, name='bindDev'),
    path('addTask/', views.addTask, name='addTask'),
    path('quryWxBind/', views.quryWxBind, name='quryWxBind'),
    path('queryData/', views.queryData, name='queryData'),
    path('getWxUserInfo/', views.getWxUserInfo, name='getWxUserInfo'),
    path('bindDingAccount/', views.bindDingAccount, name='bindDingAccount'),
    path('qurTask/', views.qurTask, name='qurTask'),
    path('saveTask/', views.saveTask, name='saveTask'),

]