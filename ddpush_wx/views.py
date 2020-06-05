#coding=utf-8

from django.shortcuts import render
import json
from django.http import HttpResponse,Http404
from .models import UserModel,UserTask
from ddpush_android.models import DeviceModel,TaskModel
import requests

from common import ResUtil
# Create your views here.

APPID ='xxx'   #小程序appid
SECRET='xxxx' #小程序scret


#通过前端login之后得到code,发送到微信后台换区openid
def getWxUserInfo(request):
    if request.method=='POST':
        reqParam=json.loads(request.body)
        if request == '' or request == None:
            return HttpResponse(ResUtil.errorResDict('请求参数不合法'))
        wxCode=reqParam['wxCode']
        if wxCode==None or wxCode=='':
            return HttpResponse(ResUtil.errorResDict('appid不合法'))
        # 拼接参数
        wxOpenReqUrl = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + APPID + '&secret=' + SECRET + '&js_code='+wxCode+'&grant_type=authorization_code'
        # 换取appid
        rlt = requests.request("GET", wxOpenReqUrl)
        json_rlt = json.loads(rlt.text)
        print(json_rlt)


        openId = json_rlt['openid']
        print(openId)

        if openId==None or openId =='':
            return HttpResponse(ResUtil.errorResDict('openid 获取失败'))

        return HttpResponse(ResUtil.sucResDict("获取成功",{"wxOpenId":openId}))


    else:
        return HttpResponse(ResUtil.errorResDict('请求方式不对'))




#查询appid是否已在绑定表里面
def quryWxBind(request):
    if request.method=='POST':
        reqParam=json.loads(request.body)
        if request == '' or request == None:
            return HttpResponse(ResUtil.errorResDict('请求参数不合法'))
        wxAppid=reqParam['wxAppId']
        if wxAppid==None or wxAppid=='':
            return HttpResponse(ResUtil.errorResDict('appid不合法'))

        #查询绑定表里是否含有这个微信绑定的设备
        de_rlt=UserModel.objects.filter(wx_appId=wxAppid)

        if de_rlt.count()>0:
            ##
            devToken=de_rlt[0].wx_devToken
            return HttpResponse(ResUtil.sucResDict('suc',{"bindState":0,"devToken":devToken}))

        else:
            return HttpResponse(ResUtil.errorResDict('绑定失败'))
    else:
        return HttpResponse(ResUtil.errorResDict('请求方式不对'))


# 绑定设备
def bindDev(request):

    if request.method== 'POST':
        #获取参数中的devToken和微信用户名
        reqParam=json.loads(request.body)

        if request=='' or request==None:
            return HttpResponse(ResUtil.errorResDict('请求参数不合法'))

        devToken=reqParam['devToken']
        wxName=reqParam['wxName']
        bindEmail=reqParam['userEmail']
        wxAppId=reqParam['wxAppId']

        if devToken=='' or devToken ==None:
            return HttpResponse(ResUtil.errorResDict('设备码不存在'))

        #查询token是否存在,先查绑定表,再查设备表
        db_cur=UserModel.objects.filter(wx_appId=wxAppId)
        if db_cur.count() > 0:
            #更新绑定信息
            user=db_cur[0]
            user.wx_userName=wxName
            user.wx_devToken=devToken
            user.wx_bindEmail=bindEmail
            user.save()
            return HttpResponse(ResUtil.sucResDict('绑定成功',{"bindState":0}))

        db_cur=DeviceModel.objects.filter(dev_token=devToken)
        if db_cur.count()>0:
            #能查询到此token,添加绑定,新增绑定表
            userModel=UserModel(wx_devToken=devToken,wx_userName=wxName,wx_bindEmail=bindEmail,wx_appId=wxAppId,wx_bindDate=ResUtil.getTime_str())
            userModel.save()
            return HttpResponse(ResUtil.sucResDict('绑定成功',{"bindState":0}))

        else:
            return HttpResponse(ResUtil.errorResDict('绑定失败,无此设备'))

    else:
        return HttpResponse(ResUtil.errorResDict('请使用post方式请求'))


# 下发任务
def addTask(request):
    if request.method=='POST':
        resParam=json.loads(request.body)

        #获取devToken,taskType
        if resParam=='' or resParam==None:
            return HttpResponse(ResUtil.errorResDict('请求参数为空'))

        devToken=resParam['devToken']
        taskType=resParam['taskType']

        if devToken=='' or devToken==None:
            return HttpResponse(ResUtil.errorResDict('设备码为空,请前往设置重新绑定'))

        # if
        # #这里的任务类型由服务器来判断,
        # if ResUtil.getTimeHours()>12:
        #     #下班卡
        #     taskType='1003'
        # else:
        #     #上班卡
        #     taskType='1002'

        if taskType=='1001':
            #判断该用户是否绑定了钉钉
            rlt=UserModel.objects.filter(wx_devToken=devToken)
            if rlt.count()>0:
                userName=rlt[0].wx_bindAccount
                userPwd=rlt[0].wx_bindpwd
                if userName=='' or  userName==None or userPwd=='' or userPwd==None:
                    return HttpResponse(ResUtil.errorResDict('发送失败,请前往设置绑定钉钉账号'))


        taskModel=TaskModel(dev_token=devToken,task_type=taskType,task_state='0',task_cr_date=ResUtil.getTime_str())
        taskModel.save()
        return HttpResponse(ResUtil.sucResDict('发送成功',''))

    else:

        return HttpResponse(ResUtil.errorResDict('请使用post方式请求'))

def queryData(request):
    if request.method=='POST':
        resParam=json.loads(request.body)
        #获取devToken,taskType
        if resParam=='' or resParam==None:
            return HttpResponse(ResUtil.errorResDict('请求参数为空'))
        devToken=resParam['devToken']
        page=resParam['page']
        pagesize=resParam['pageSize']

        page=int(page)-1
        pagesize=int(pagesize)
        #查询这个设备下的所有任务
        rlt=TaskModel.objects.filter(dev_token=devToken).order_by('-task_cr_date')[int(pagesize)*int(page):int(pagesize)]  # - 表降序,无- 表升序
        if rlt.count()>0:
            #有相关的任务数据
            listData=[]
            for item in rlt:
                dev_token=item.dev_token
                task_type=item.task_type
                task_state=item.task_state
                task_cr_date=item.task_cr_date
                task_sh_date=item.task_sh_date
                task_desc=item.task_desc

                if task_desc==None or task_desc=='':
                    task_desc="无"

                if task_type=="1003":
                    task_type="下班打卡"
                elif task_type=="1002":
                    task_type="上班打卡"
                elif task_type == "1004":
                    task_type = "早退下班卡"
                elif task_type == "1005":
                    task_type = "更新下班卡"
                elif task_type == "1001":
                    task_type = "设备登录"

                if task_state=="0":
                    task_state="任务未完成"
                elif task_state=="1":
                    task_state="任务成功"
                elif task_state=="2":
                    task_state="任务失败"

                model={"dev_token":dev_token,"task_type":task_type,"task_state":task_state,"task_cr_date":task_cr_date,"task_sh_date":task_sh_date,"task_desc":task_desc}

                listData.append(model)

            return HttpResponse(ResUtil.sucResDict("数据获取成功",{"listData":listData}))

        else:

            return HttpResponse(ResUtil.errorResDict("该设备无相关任务"))


def bindDingAccount(request):
    """
    绑定钉钉账号密码
    :param request:
    :return:
    """
    if request.method=='POST':
        resParam=json.loads(request.body)
        #获取devToken,taskType
        if resParam=='' or resParam==None:
            return HttpResponse(ResUtil.errorResDict('请求参数为空'))
        
        devToken=resParam['devToken']
        account=resParam['account']
        pwd=resParam['pwd']


        if devToken==None or devToken=='':
            return HttpResponse(ResUtil.errorResDict('设备码不存在'))

        #查询设备码
        db_cur=UserModel.objects.filter(wx_devToken=devToken)
        if db_cur.count()>0:
            userModel=db_cur[0]
            userModel.wx_bindAccount=account
            userModel.wx_bindpwd=pwd
            userModel.save()
            return HttpResponse(ResUtil.sucResDict('绑定成功'))

    else:

        return HttpResponse(ResUtil.errorResDict("请使用post方式请求"))


def qurTask(request):
    """
    定时任务
    :param request:
    :return:
    """
    if request.method == 'POST':
        resParam = json.loads(request.body)
        # 获取devToken,taskType
        if resParam == '' or resParam == None:
            return HttpResponse(ResUtil.errorResDict('请求参数为空'))

        wxAppid = resParam['wxAppId']

        if wxAppid == None or wxAppid == '':
            return HttpResponse(ResUtil.errorResDict('appId不存在'))

        # 查询定时任务
        db_cur = UserTask.objects.filter(wx_appId=wxAppid)

        if db_cur.count() > 0:
            userTask = db_cur[0]
            wx_up_time=userTask.wx_up_time
            wx_down_time=userTask.wx_down_time

            up_check=True
            down_check=True

            if wx_up_time==None or wx_up_time =='':
                up_check=True
                wx_up_time='00:00'

            if wx_down_time == None or wx_down_time =='':
                down_check = True
                wx_down_time='00:00'


            resDa={"up":{"ischeck":up_check ,"time": wx_up_time},"down":{"ischeck": down_check,"time": wx_down_time}}

            return HttpResponse(ResUtil.sucResDict('获取成功',resDa))


        else:



            return HttpResponse(ResUtil.sucResDict('获取成功'))

    else:

        return HttpResponse(ResUtil.errorResDict("请使用post方式请求"))

from .DsTask import task
def saveTask(request):
    """
    定时任务
    :param request:
    :return:
    """




    if request.method == 'POST':
        resParam = json.loads(request.body)
        # 获取devToken,taskType
        if resParam == '' or resParam == None:
            return HttpResponse(ResUtil.errorResDict('请求参数为空'))

        wxAppId = resParam['wxAppId']
        up_check = resParam['task']['up']['ischeck']
        down_check = resParam['task']['up']['ischeck']

        up_time=resParam['task']['up']['time']
        down_time=resParam['task']['down']['time']

        if up_check==False:
            up_time=''

        if down_check==False:
            down_time=''


        if wxAppId == None or wxAppId == '':
            return HttpResponse(ResUtil.errorResDict('appid不存在'))

        db_cur = UserTask.objects.filter(wx_appId=wxAppId)

        if db_cur.count() > 0:
            # 更新绑定信息
            user = db_cur[0]
            user.wx_up_time = up_time
            user.wx_down_time = down_time
            user.wx_status_date= ResUtil.getTime_str()
            user.save()
        else:

            userModel = UserTask(wx_appId=wxAppId, wx_up_time=up_time, wx_down_time=down_time,
                                 wx_status_date=ResUtil.getTime_str())
            userModel.save()

        return HttpResponse(ResUtil.sucResDict('保存成功', {}))



    else:

        return HttpResponse(ResUtil.errorResDict("请使用post方式请求"))


