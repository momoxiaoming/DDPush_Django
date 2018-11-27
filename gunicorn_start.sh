#!/bin/sh
#service name
#项目的目录
SERVICE_DIR=/data/web/momoxiaoming_django
#gunicorn的名字
SERVICE_NAME=gunicorn
#gunicorn的配置文件名
SERVICE_CONF=gunicorn.conf
#虚拟环境的路径
VIRTUAL_DIR=/data/web/momoxiaoming_django/venv/bin/activate
#pid存放的位置
PID=gunicorn\.pid
#项目启动入口
OBJECT_APP=momoxiaoming_django.wsgi

cd $SERVICE_DIR

source $VIRTUAL_DIR

case "$1" in

    start)
        gunicorn $OBJECT_APP -c $SERVICE_DIR/$SERVICE_CONF >/dev/null 2>&1 &
        echo $! > $SERVICE_DIR/$PID
        echo "*** start $SERVICE_NAME ***"
        ;;
    stop)
        kill `cat $SERVICE_DIR/$PID`
        rm -rf $SERVICE_DIR/$PID
        echo "*** stop $SERVICE_NAME ***"

        sleep 2
        P_ID=`ps -ef | grep -w "$SERVICE_NAME" | grep -v "grep" | awk '{print $2}'`
        if [ "$P_ID" == "" ]; then
            echo "*** $SERVICE_NAME process not exists or stop success ***"
        else
            echo "*** $SERVICE_NAME process pid is:$P_ID ***"
            echo "*** begin kill $SERVICE_NAME process,kill is:$P_ID ***"
            kill -9 $P_ID
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        echo "*** restart $SERVICE_NAME ***"
        ;;

    *)
        ## restart
        $0 stop
        sleep 2
        $0 start
        ;;
esac
exit 0