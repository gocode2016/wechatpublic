from flask import Flask
from flask import request
import hashlib
import xml.etree.ElementTree as ET
import re
import time
import random
import urllib
import json
import threading
import os
app = Flask(__name__)

g_xmlForm = '''
<xml>
<ToUserName><![CDATA[{ToUserName}]]></ToUserName>
<FromUserName><![CDATA[{FromUserName}]]></FromUserName>
<CreateTime>{CreateTime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{Content}]]></Content>
</xml>'''

class TokenManager(threading.Thread):
    '''
    '''
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            self.resetToken()
            time.sleep(7000)
    def resetToken(self):
        appid = os.getenv('APPID')
        appsecret = os.getenv('APPSECRET')
        url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid, appsecret))
        resp = urllib.urlopen(url)
        jsonResp = json.loads(resp.read())
        self.token = jsonResp['access_token']
        print(self.token)
    def getToken(self):
        return self.token

g_tokenManager = TokenManager()

class Lottery(object):
    def __init__(self):
        self.userList = list()
    def addUser(self,userName):
        '''增加用户:判断用户是否已经存在,添加用户到list
        '''
        if self.userList.count(userName) == 0:
            self.userList.append(userName)
    def draw(self):
        '''抽奖:产生随机下标,保存用户,重置,将用户返回
        '''
        index = random.randint(0,len(self.userList)-1)
        luckyUser = self.userList[index]
        self.reset()
        return luckyUser
    def reset(self):
        del self.userList[:]
    def count(self):
        return len(self.userList)

g_lottery = Lottery()

class Msg(object):
    def __init__(self):
        pass
    def __init__(self,msgHead):
        self.msgHead = msgHead
    def reply(self):
        return 'success'

class TextMsg(Msg):
    def __init__(self,xmlElement,msgHead):
        self.content = xmlElement.text.encode('raw_unicode_escape').decode('utf-8')
        self.msgHead = msgHead
    def isDefined(self):
        pattern = re.compile(r'\[[A-Z]+\]')
        match = pattern.search(self.content)
        if match:
            self.define = match.group()
            return True
        else:
            print("It's an undefined msg")
            return False
    def reply(self):
        if self.isDefined():
            if self.define == '[CJ]':
                msgDict = dict()
                msgDict['ToUserName'] = self.msgHead.getFromUserName()
                msgDict['FromUserName'] = self.msgHead.getToUserName()
                msgDict['CreateTime'] = int(time.time())
                g_lottery.addUser(msgDict['ToUserName'])
                msgDict['Content'] = '感谢参与,目前共有%s人,我们将在稍后开奖' % g_lottery.count()
                print(msgDict['Content'])
                return g_xmlForm.format(**msgDict)
        return 'success'

class MsgHead(object):
    def __init__(self,xmlData,):
        self.xmlData = xmlData
        self.toUserName = xmlData.find('ToUserName').text
        self.fromUserName = xmlData.find('FromUserName').text
        self.createTime = xmlData.find('CreateTime').text
        self.msgType = xmlData.find('MsgType').text
        self.msgId = xmlData.find('MsgId').text
    def getToUserName(self):
        return self.toUserName
    def getFromUserName(self):
        return self.fromUserName
    def getCreateTime(self):
        return self.createTime
    def getMsgType(self):
        return self.msgType
    def getMsgId(self):
        return self.msgId
    def getMsg(self):
        if self.msgType == 'text':
            return TextMsg(self.xmlData.find('Content'),self)

@app.route("/draw_lottery")
def drawLottery():
    if g_lottery.count() > 0:
        return g_lottery.draw()
    else:
        return 'no participator'
        
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/wx", methods=['POST'])
def wx_post():
    data = request.data
    msgHead = MsgHead(ET.fromstring(data))
    msg = msgHead.getMsg()
    return msg.reply()
    
@app.route("/wx", methods=['GET'])
def handle():
    args = request.args
    signature = args['signature']
    print(signature)
    timestamp = args['timestamp']
    print(timestamp)
    nonce = args['nonce']
    print(nonce)
    echostr = args['echostr']
    print(echostr)
    token = 'yelloworange'

    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    print(hashcode)
    if hashcode == signature:
        print('hello wx')
        return echostr
    else:
        print('unknow host')
        return echostr
    
if __name__ == '__main__':
    g_tokenManager.start()
    app.run(host='0.0.0.0',port=80)
