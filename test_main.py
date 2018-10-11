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
