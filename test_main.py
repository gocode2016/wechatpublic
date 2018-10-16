import pytest
import main

@pytest.fixture
def client(request):
    main.app.config['TESTING'] = True
    client = main.app.test_client()

    def teardown(): #清理工作放在这里
        pass
    request.addfinalizer(teardown)

    return client

def test_hello(client):
    rv = client.get("/");
    assert b'Hello World' in rv.data

def test_msg(client):
    rv = client.post("/wx?signature=7895274204367b506b5c27ed540972c3552a5e53&timestamp=1539091653&nonce=1841256615&openid=oTwo10dnoDY35gK5APNGWfdPzuU0",data='<xml><ToUserName><![CDATA[gh_0f708d1d8ace]]></ToUserName>\n<FromUserName><![CDATA[oTwo10dnoDY35gK5APNGWfdPzuU0]]></FromUserName>\n<CreateTime>1539091653</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[\xe4\xbd\xa0\xe5\xa5\xbd]]></Content>\n<MsgId>6610348315604941314</MsgId>\n</xml>')
    assert b'success' in rv.data

def test_msg_cj(client):
    rv = client.post("/wx?signature=7895274204367b506b5c27ed540972c3552a5e53&timestamp=1539091653&nonce=1841256615&openid=oTwo10dnoDY35gK5APNGWfdPzuU0",data='<xml><ToUserName><![CDATA[gh_0f708d1d8ace]]></ToUserName>\n<FromUserName><![CDATA[oTwo10dnoDY35gK5APNGWfdPzuU0]]></FromUserName>\n<CreateTime>1539091653</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[[CJ]\xe4\xbd\xa0\xe5\xa5\xbd]]></Content>\n<MsgId>6610348315604941314</MsgId>\n</xml>')
    assert b'\xe6\x88\x91\xe4\xbb\xac\xe5\xb0\x86\xe5\x9c\xa8\xe7\xa8\x8d\xe5\x90\x8e\xe5\xbc\x80\xe5\xa5\x96' in rv.data
