import json


def test_ping(client, helpers):
    response = client.get('/healthz/ping')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert "OK" == data["status"]
    assert "PONG!" == data["data"]


def test_secured_helloworld(client, helpers):
    response = client.get('/healthz/helloworld')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert 1 == len(data["data"])
    assert "OK" == data["status"]
    assert "hello, world!" == data["data"][0]["saying"]
