
from .models import UserTask,UserModel
from common import ResUtil
from ddpush_android.models import TaskModel
#定时任务核心方法
@task
def task():

    #查询任务数据库,找到所有的任务,挨个执行
    db_cur = UserTask.objects.filter()

    nowTime=ResUtil.getTimeHourAndMin()
    print('...定时任务执行....',nowTime)

    print(db_cur.count())
    if db_cur.count()>0:
        for item in db_cur:
             #取出每条定时数据
            wx_appId=item.wx_appId
            wx_up_time=item.wx_up_time
            wx_down_time=item.wx_down_time
            print(wx_appId)
            print(wx_up_time)
            print(wx_down_time)
            print(nowTime)

            if wx_up_time != None and wx_up_time != '' and wx_up_time == nowTime:
                 # 该账号需要上班任务已到,添加任务
                 devToken = qurDevToken(wx_appId)

                 print('上班任务')
                 if devToken != None:
                     taskModel = TaskModel(dev_token=devToken, task_type='1002', task_state='0',
                                           task_cr_date=ResUtil.getTime_str())
                     taskModel.save()

            if wx_down_time != None and wx_down_time != '' and wx_down_time == nowTime:
                 # 该账号需要下班任务已到
                 devToken = qurDevToken(wx_appId)
                 print('下班任务')
                 if devToken != None:
                     taskModel = TaskModel(dev_token=devToken, task_type='1003', task_state='0',
                                           task_cr_date=ResUtil.getTime_str())
                     taskModel.save()

    else:
        print('没有查到任务')


def qurDevToken(wxappid):
    db_cur = UserModel.objects.filter(wx_appId=wxappid)
    if db_cur.count() > 0:
        user=db_cur[0]

        return user.wx_devToken

    return None






