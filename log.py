# coding=utf-8

import requests
from PyQt4 import QtGui, uic
import sys, urllib2, time

PATH = '' #两个ui文件所在路径

username = '********' #学号
password = '********' #密码
max_data_usage = 25 #流量上限，目前只有25和50

info = []

def show(data_usage, data_percent, money_left, suggest):
    qtDialogFile = "success.ui"
    Ui_DialogWindow, QtBaseClass2 = uic.loadUiType(qtDialogFile)

    class MyApp(QtGui.QDialog, Ui_DialogWindow):
        def __init__(self):
            QtGui.QDialog.__init__(self)
            Ui_DialogWindow.__init__(self)
            self.setupUi(self)
            self.setFixedSize(400, 300)
            self.data_usage.setText(data_usage)
            self.data_percent.setText(data_percent)
            self.money_left.setText(money_left)
            self.suggest.setText(suggest)

    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()

def check(info):
    data_usage = int(info[0]) / 1024.0 / 1024.0 / 1024.0
    data_percent = data_usage / 25 * 100
    data_usage = '%.2fG' % data_usage
    data_percent = '%.2f%%' % data_percent
    money_left = info[2] + u'元'
    localtime = time.localtime(time.time())
    day = localtime[2]
    suggest = 25.0 * day / max_data_usage
    suggest = '%.2fG' % suggest
    show(data_usage, data_percent, money_left, suggest)


def error():
    qtDialogFile = PATH + "./fail.ui"
    Ui_DialogWindow, QtBaseClass2 = uic.loadUiType(qtDialogFile)

    class MyApp(QtGui.QDialog, Ui_DialogWindow):
        def __init__(self):
            QtGui.QDialog.__init__(self)
            Ui_DialogWindow.__init__(self)
            self.setupUi(self)
            self.setFixedSize(440, 200)
            self.Retry.clicked.connect(self.retry)
            self.Exit.clicked.connect(self.exit)

        def retry(self):
            try:
                requests.post("https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1", headers=headers,
                              data=payload_logout, timeout=2)
                session = requests.Session()
                session.post("https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1", headers=headers,
                              data=payload_login, timeout=2)
                r = session.post('https://ipgw.neu.edu.cn/include/auth_action.php?k=6666', headers=headers,
                                 data=payload_getinfo, timeout=2)
                global info
                info = r.content.split(',')
                urllib2.urlopen('https://www.baidu.com/', timeout=2)
            except:
                QtGui.QMessageBox.about(self, u"错误", u"无法登陆")
            else:
                QtGui.QWidget.close(self)

        def exit(self):
            QtGui.QWidget.close(self)

    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    return info

payload_logout = {'action':'logout', 'username':username, 'password':password, 'ajax':'1'}
payload_login = {'action':'login', 'ac_id':'1', 'username':username, 'password':password, 'save_me':'0'}
payload_getinfo = {'action':'get_online_info', 'key':'6666'}

headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}

try:
    session = requests.Session()
    session.post("https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1", headers=headers,
                 data=payload_login, timeout=1)
    r = session.post('https://ipgw.neu.edu.cn/include/auth_action.php?k=6666', headers=headers,
                     data=payload_getinfo, timeout=1)
    info = r.content.split(',')
    urllib2.urlopen('https://www.baidu.com/', timeout=2)
except:
    try:
        requests.post("https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1", headers=headers,
                      data=payload_logout, timeout=1)
        session = requests.Session()
        session.post("https://ipgw.neu.edu.cn/srun_portal_pc.php?url=&ac_id=1", headers=headers,
                     data=payload_login, timeout=1)
        r = session.post('https://ipgw.neu.edu.cn/include/auth_action.php?k=6666', headers=headers,
                         data=payload_getinfo, timeout=1)
        info = r.content.split(',')
        urllib2.urlopen('https://www.baidu.com/', timeout=2)
    except:
        info = error()
        if info:
            check(info)
    else:
        check(info)
else:
    check(info)
