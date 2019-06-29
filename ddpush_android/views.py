# coding=utf-8
# Create your views here.
from django.http import HttpResponse,Http404
from ddpush_android.models import DeviceModel,TaskModel
from ddpush_wx.models import UserModel
from django.utils import timezone
from common import ResUtil,emailUtl
import json

def index(request):


    return HttpResponse("hello momoxiaoming")




#---------------------------------android端相关注册接口------------------
# 设备注册接口
def regDev(request):
    if (request.method == 'POST'):
        req_body=json.loads(request.body)
        if(req_body==None):
            return HttpResponse(ResUtil.errorResDict('请求参数不合法'))

        dev_andId = req_body['dev_andId']
        if(dev_andId=='' or dev_andId==None):
            return HttpResponse(ResUtil.errorResDict('android 不能为空!'))

        # 查询后台是否存在该设备
        qurResult = DeviceModel.objects.filter(dev_andId=dev_andId)

        devToken=''

        if qurResult.count()==0: # 没有,直接插入
            devMod = DeviceModel()
            devMod.dev_andId = req_body['dev_andId']
            devMod.dev_date = ResUtil.getTime_str()
            devMod.dev_imei = req_body['dev_imei']
            devMod.dev_isRt = req_body['dev_isRt']
            devMod.dev_name = req_body['dev_name']
            devMod.dev_sdk = req_body['dev_sdk']
            devMod.app_ver = req_body['app_ver']
            token=ResUtil.getSoleNumStr()
            devMod.dev_token=token
            devMod.save()

            devToken=token



        else: #查询该设备 token
            qurResult=qurResult[0]
            devToken=qurResult.dev_token

        resData={'devToken':devToken}
        resData=str(resData)

        return HttpResponse(ResUtil.sucResDict('设备注册成功',resData))
    else:

        return HttpResponse(ResUtil.errorResDict('请使用POST方式请求!'))



# 任务查询接口,设备只会拉取未完成的任务
def taskQury(request):
    if request.method=='POST':
        req_body=json.loads(request.body)
        if req_body=='' or req_body is None:
            return HttpResponse()

        devToken=req_body['devToken']

        if devToken=='' or devToken is None:
            return HttpResponse(ResUtil.errorResDict('设备devToken为空!'))
        # 查询未完成任务
        qurTask=TaskModel.objects.filter(task_state='0',dev_token=devToken,task_cr_date__gt=ResUtil.getCurDayTime_str())

        if qurTask.count()==0:
            #无任务
            return HttpResponse(ResUtil.errorResDict("该设备当前无任务"))

        else:

            taskDict=qurTask[0]
            if taskDict.task_state=='3':
                return HttpResponse(ResUtil.sucResDict('无设备任务'))

            if taskDict.task_type=='1001':
                #设备登录,组装账号密码
                rlt=UserModel.objects.filter(wx_devToken=devToken)
                if rlt.count()>0:
                    userModel=rlt[0]
                    taskData={"account":userModel.wx_bindAccount,"pwd":userModel.wx_bindpwd}
                    resDict = {"taskType": taskDict.task_type, "taskId": taskDict.id, "taskData": taskData}
                    return HttpResponse(ResUtil.sucResDict('任务拉取成功', str(resDict)))

                else:
                    return HttpResponse(ResUtil.errorResDict('未绑定钉钉账号密码,无法登陆'))
            else:
                resDict = {"taskType": taskDict.task_type, "taskId": taskDict.id, "taskData": {}}
                taskDict.task_state='3'
                taskDict.save()
                return HttpResponse(ResUtil.sucResDict('任务拉取成功', str(resDict)))
    else:
        return HttpResponse(ResUtil.errorResDict('请求方式错误'))


# 任务提交接口
def taskSubmt(request):
    if request.method=='POST':
        req_body=json.loads(request.body)
        if req_body=='' or req_body is None:
            return HttpResponse(ResUtil.errorResDict('请求参数不合法'))

        taskId=req_body['taskId']
        taskState=req_body['taskState']
        taskDesc=req_body['taskDesc']

        if taskId=='' or taskId is None:
            return HttpResponse(ResUtil.errorResDict('taskId为空!'))

        devToken=''
        # 查询未完成任务
        qurTask=TaskModel.objects.filter(id=taskId)
        if qurTask.count()>0:
            qurTask=qurTask[0]
            devToken = qurTask.dev_token
            task_type=qurTask.task_type
            qurTask.task_state = taskState
            qurTask.task_sh_date=ResUtil.getTime_str()
            qurTask.task_desc=taskDesc
            qurTask.save()

            usermodel = UserModel.objects.filter(wx_devToken=devToken)
            # 成功后发送邮件
            if usermodel.count() > 0:
                email = usermodel[0].wx_bindEmail

                if email != '' and email != None:
                    eu = emailUtl.emailUtil()
                    sendMsg = ''
                    typeMsg=''
                    if task_type=='1001':
                        typeMsg='登陆任务'
                    else:
                        typeMsg='打卡任务'

                    if taskState == '1':

                        sendMsg = '恭喜'+typeMsg+'执行成功_'+ResUtil.getTime_str()
                    else:
                        sendMsg = '很遗憾'+typeMsg+'执行失败_'+ResUtil.getTime_str()

                    eu.sendEmail(sendMsg, email)

            return HttpResponse(ResUtil.sucResDict('任务提交成功', ''))
        else:

            return HttpResponse(ResUtil.errorResDict('提交的任务id不存在'))



    else:
        return HttpResponse(ResUtil.errorResDict('请求方式错误'))



def updateApk(request):
    if request.method=='POST':
        req_body=json.loads(request.body)
        if req_body=='' or req_body is None:
            return HttpResponse()

        devToken=req_body['dev_token']
        app_ver=req_body['app_ver']

        if app_ver==None or app_ver =='':
            return HttpResponse(ResUtil.errorResDict('版本号不存在'))

        if devToken=='' or devToken is None:
            return HttpResponse(ResUtil.errorResDict('设备devToken为空!'))

        app_ver=int(app_ver)

        if app_ver<2:
            #需要更新,组装参数

            return HttpResponse(ResUtil.sucResDict('检查到新版本', str({"apkUrl":"http://api.momoxiaoming.com:9102/static/app-release_v2.apk","apkVer":"2"})))

        else:
            return HttpResponse(ResUtil.errorResDict('无需更新'))


    else:
        return HttpResponse(ResUtil.errorResDict('请求方式错误'))














