#coding=utf-8
import datetime,random
from django.utils import timezone
from pycommon import timeUtil
import binascii





def errorResDict(resMsg_str):
    resJson = {"resCode": 1, "resMsg": resMsg_str, "resData": ""}
    return str(resJson)

def sucResDict(resMsg_str,resData_str=""):
    resJson = {"resCode": 0, "resMsg": resMsg_str, "resData": resData_str}
    return str(resJson)

# 获取当前时间,格式2018-09-06 11:11:11
def getTime_str():
    time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")

    return time
# 获取当前时间的小时数
def getTimeHours():
    time = timezone.localtime(timezone.now()).strftime("%H")

    return int(time)

def getTimeHourAndMin():
    #获取小时分钟
    time = timezone.localtime(timezone.now()).strftime("%H:%M")

    return str(time)

def baseN(num, b):
    return ((num == 0) and "0") or \
           (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])



def getSoleNumStr():
    dt='2018-11-11 00:00:00'    #光棍节这天作为时间起点

    temp_mills=timeUtil.get_utc_MillsForTimestr(dt)
    now_mills=timeUtil.get_utc_NowTimeMills()
    jlt=int(now_mills)-int(temp_mills)
    jlt=jlt  #添加一个随机数jlt
    print(jlt)
    rlt_num=baseN(jlt,32) #转32进制
    return str(rlt_num)

if __name__=='__main__':
    getSoleNumStr()