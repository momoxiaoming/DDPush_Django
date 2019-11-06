#coding=utf-8
import smtplib
import threading

from email.mime.text import MIMEText
from email.header import Header
class emailUtil:

    __qqEmail=''
    __qqPwd=''

    _reciveEmail=''
    def __init__(self):
        self.__qqEmail='xxxx'
        self.__qqPwd='xxxx'
        self._reciveEmail='xxxx'
    def sendEmail(self,content,receiveremail=None):
        if receiveremail==None:
            receiveremail=self._reciveEmail
        t = threading.Thread(target=self.__sendQQemail, args=(content, receiveremail,))
        t.start()


    def __sendQQemail(self,content,receiveremail):
        try:
            message = MIMEText(content, 'plain', 'utf-8')
            message['From'] = Header('张小明小号<'+self.__qqEmail+'>', 'utf-8').encode()
            message['To'] = Header('张小明大号<'+self._reciveEmail+'>', 'utf-8').encode()

            message['Subject'] = Header(u'主题:'+content, 'utf-8').encode()

            s=smtplib.SMTP_SSL('smtp.qq.com',465)
            s.login(self.__qqEmail,self.__qqPwd)
            s.sendmail(self.__qqEmail,receiveremail,message.as_string())
            s.quit()
            print('send sucess')
        except BaseException:
            print('邮件发送出错')


if __name__ =='__main__':
    e=emailUtil()
    e.sendEmail('打卡成功')
