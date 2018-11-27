#coding=utf-8
# Register your models here.
from django.contrib import admin
from .models import DjangoTest

admin.site.register(DjangoTest)    #将djanTest表加入用户管理界面