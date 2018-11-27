#coding=utf-8
from django.db import models

# Create your models here.

# 微信用户绑定模型
class UserModel(models.Model):
    wx_devToken    = models.CharField(max_length=128)      #设备绑定token
    wx_bindDate    = models.CharField(max_length=50)
    wx_userName    = models.CharField(max_length=125)      #微信用户名
    wx_appId       = models.CharField(max_length=124)      #微信appid
    wx_bindEmail   = models.CharField(max_length=125)      #通知邮箱
    wx_bindAccount = models.CharField(max_length=32,null=True)      #绑定的钉钉手机号
    wx_bindpwd     = models.CharField(max_length=32,null=True)      #绑定的钉钉密码

