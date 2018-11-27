#coding=utf-8

#本类是关于日期的工具类
from datetime import datetime


#-----------------------本地时间,一般是东八区时间(北京时间)-------
def get_loc_NowTimeFomatStr():
    """
    # 输出格式2018-11-11 00:00:00的当前字符串时间
    :return: 2018-11-11 00:00:00 时间字符串
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_loc_MillsForFomatStr(timeMills):
    """
    # 通过毫秒数获取时间字符串,格式2018-11-11 00:00:00
    :param timeMills: 毫秒数
    :return: 2018-11-11 00:00:00
    """
    return datetime.fromtimestamp(timeMills/1000).strftime('%Y-%m-%d %H:%M:%S')

def get_loc_NowTimeMills(timedlt=None):
    """
    # 默认获取当前时间的毫秒数,或者传入一个日期
    :param timedlt: dateTime类型
    :return: 毫秒数字符串
    """

    if timedlt==None :
        return int(datetime.now().timestamp()*1000)
    else:
        return int(datetime.timestamp(timedlt)*1000)

def get_loc_MillsForTimestr(timeStr):
    """
    传入日期字符串,得到毫秒数
    :param timeStr: 2018-11-11 00:00:00 格式日期字符串
    :return: 毫秒字符串
    """
    date_time=datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
    return get_loc_NowTimeMills(date_time)

# ------------------------------utc时间(时间标准时间,时差0,比北京时间少8小时)--------------------------------


def get_utc_NowTimeFomatStr():
    """
    # 输出格式2018-11-11 00:00:00的当前字符串时间
    :return: 2018-11-11 00:00:00 时间字符串
    """
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def get_utc_MillsForFomatStr(timeMills):
    """
    # 通过毫秒数获取时间字符串,格式2018-11-11 00:00:00
    :param timeMills: 毫秒数
    :return: 2018-11-11 00:00:00
    """
    return datetime.utcfromtimestamp(timeMills/1000).strftime('%Y-%m-%d %H:%M:%S')


def get_utc_NowTimeMills(timedlt=None):
    """
    # 默认获取当前时间的毫秒数,或者传入一个日期
    :param timedlt: dateTime类型utc时间
    :return: 毫秒数字符串
    """

    if timedlt==None :
        return int(datetime.utcnow().timestamp()*1000)
    else:
        return int(datetime.timestamp(timedlt)*1000)

def get_utc_MillsForTimestr(timeStr):
    """
    传入日期字符串,得到毫秒数
    :param timeStr: 2018-11-11 00:00:00 格式日期字符串
    :return: 毫秒字符串
    """
    date_time=datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
    return get_utc_NowTimeMills(date_time)

if __name__=='__main__':
    print(get_loc_NowTimeFomatStr())
    print(get_utc_NowTimeFomatStr())
