from flask import Flask
from flask import request
import hashlib
import xml.etree.ElementTree as ET
import re
import time
import random
app = Flask(__name__)

g_xmlForm = '''
<xml>
<ToUserName><![CDATA[{ToUserName}]]></ToUserName>
<FromUserName><![CDATA[{FromUserName}]]></FromUserName>
<CreateTime>{CreateTime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{Content}]]></Content>
</xml>'''

class Lottery(object):
    def __init__(self):
        self.userList = list()
    def addUser(self,userName):
        if self.userList.cout(userName) == 0:
            self.userList.append(userName)
    def draw(self):
        index = random.randint(0,len(self.userList)-1)
        return self.userList[index]
    def clear(self):
        del self.userList[:]

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
            print("It's a defined msg")
            return True
        else:
            print("It's a undefined msg")
            return False
    def reply(self):
        if self.isDefined():
            if self.define == '[CJ]':
                msgDict = dict()
                msgDict['ToUserName'] = self.msgHead.getFromUserName()
                msgDict['FromUserName'] = self.msgHead.getToUserName()
                msgDict['CreateTime'] = int(time.time())
                msgDict['Content'] = '感谢您的参与,我们将在稍后开奖'
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

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/wx", methods=['POST'])
def wx_post():
    data = request.data
    msgHead = MsgHead(ET.fromstring(data))
    msg = msgHead.getMsg()
    return msg.reply();
    
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
    app.run(host='0.0.0.0',port=80)
