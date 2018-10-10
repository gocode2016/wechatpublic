from flask import Flask
from flask import request
import hashlib
import xml.etree.ElementTree as ET
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/wx", methods=['POST'])
def wx_post():
    args = request.args
    print(args)
    data = request.data
    print(data)
    root = ET.fromstring(data)
    msgtype = root.find('MsgType').text
    if msgtype == 'text':
        print('收到文本消息:'+ root.find('Content').text)
    return 'success'
    
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
