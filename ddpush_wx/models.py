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


# 定时任务
class UserTask(models.Model):
    wx_appId       = models.CharField(max_length=124)      # 微信appid
    wx_up_time     = models.CharField(max_length=32,null=True)  # 上班定时任务时间
    wx_down_time   = models.CharField(max_length=32,null=True)  # 下班定时任务时间
    wx_status_date = models.CharField(max_length=124,null=True) #时间


