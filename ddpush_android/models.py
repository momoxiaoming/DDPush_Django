from django.db import models

# Create your models here.

from django.db import models

class DjangoTest(models.Model):
    name_text   = models.CharField(max_length=256)


# 设备注册模型
class DeviceModel(models.Model):
    dev_andId   = models.CharField(max_length=128)       #android id
    dev_imei    = models.CharField(max_length=128)        #imei
    dev_isRt    = models.CharField(max_length=10)        #设备root
    dev_name    = models.CharField(max_length=125)       #设备名称
    dev_sdk     = models.CharField(max_length=48)        #设备版本号
    app_ver     = models.CharField(max_length=48)        #app版本号
    dev_date    = models.CharField(max_length=48)        #注册时间
    dev_token   = models.CharField(max_length=128)       #绑定token值,世界唯一

# 任务下发模型
class TaskModel(models.Model):
    dev_token   = models.CharField(max_length=128)        #设备id,这里存储的是dev_token
    task_type   = models.CharField(max_length=20)         #任务类型,1001设备登录,1002 上班卡,1003 下班卡,1004早退下班,1005更新下班
    task_state  = models.CharField(max_length=10)         #任务状态 0是未完成,1是已完成,2已失败,3已下发
    task_cr_date= models.CharField(max_length=64)         #任务创建时间
    task_sh_date= models.CharField(max_length=64)         #任务完成时间
    task_desc   = models.CharField(max_length=64,null=True)         #任务描述

