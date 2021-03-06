import json
import uuid
from unittest.mock import patch

import pytest

from zconnectmqttauth.brokers.vernemq import app
from zconnectmqttauth.brokers.util import WORKER_USERNAME
from zconnectmqttauth.auth.mongodb.vmq import MQTTUser
# FIXME
from zconnectmqttauth.auth.mongodb.overlock import Project


@pytest.fixture(name="test_client")
def fix_test_client():
    yield app.test_client()


def _getjson(response):
    try:
        return json.loads(response.data.decode("utf8"))
    except:
        return {}


PROJECTID = "3b32154818bccbde03cfea45"


class TestAuthRegisterByProject:

    def test_no_project(self, test_client):
        """no project in db - error"""
        response = test_client.post(
            "/auth_on_register",
            data=json.dumps({
                "username": "v1:009a5ee11a2c6fd8393535d1:aircon:0xbeef",
                "password": "p:abc",
                "client_id": "2of3opf23",
            }),
            content_type="application/json",
        )

        assert {"result": "error"} == _getjson(response)
        assert response._status_code == 200

    def test_with_project(self, test_client):
        """project exists, key doesn't match"""

        Project.objects().delete()
        p = Project(
            name="Project 123",
            id=PROJECTID,
            project_keys=["p:{}".format(uuid.uuid4())],
        )
        p.save()

        response = test_client.post(
            "/auth_on_register",
            data=json.dumps({
                "username": "v1:{}:aircon:0xbeef".format(PROJECTID),
                "password": "p:abc",
                "client_id": "2of3opf23",
            }),
            content_type="application/json",
        )

        assert {"result": "error"} == _getjson(response)
        assert response._status_code == 200

    def test_with_project_key(self, test_client):
        """project exists, key matches"""

        Project.objects().delete()
        p = Project(
            name="Project 123",
            id=PROJECTID,
            project_keys=["p:{}".format(uuid.uuid4())],
        )
        p.save()

        response = test_client.post(
            "/auth_on_register",
            data=json.dumps({
                "username": "v1:{}:aircon:0xbeef".format(PROJECTID),
                "password": p.project_keys[0],
                "client_id": "2of3opf23",
            }),
            content_type="application/json",
        )

        assert {"result": "ok"} == _getjson(response)
        assert response._status_code == 200


class TestAuthRegisterByUser:

    @pytest.fixture(autouse=True)
    def fix_seed_db(self):
        MQTTUser(
          **{
            "username": "v1:pid123:aircon:0xbeef",
            "passhash": "$2a$12$G9/ZxPAMyPwiLCslezywge5WlHSHEU40XSV8ISPp04IN4K/rH4egW",
            "client_id": "fk4opgk4pokwep4otk490tk34t"
          }
        ).save()

        yield

        MQTTUser.objects().delete()

    @pytest.mark.xfail(reason="needs changing to do thiss tuff on pub/sub, not auth")
    def test_not_blacklisted(self, test_client):
        response = test_client.post(
            "/auth_on_register",
            data=json.dumps({
                "username": "v1:pid123:aircon:0xbeef",
                "password": "p:abc",
                "client_id": "2of3opf23",
            }),
            content_type="application/json",
        )

        assert {"result": "ok"} == _getjson(response)
        assert response._status_code == 200

    def test_not_authed(self, test_client):
        response = test_client.post(
            "/auth_on_register",
            data=json.dumps({
                "username": "v1:{}:blep:0xbeef".format(PROJECTID),
                "password": "p:abc",
                "client_id": "2of3opf23",
            }),
            content_type="application/json",
        )

        assert {"result": "error"} == _getjson(response)
        assert response._status_code == 200


class TestAuthPublish:

    def test_can_publish(self, test_client):
        response = test_client.post(
            "/auth_on_publish",
            data=json.dumps({
                "username": "v1:pid123:aircon:0xbeef",
                "password": "p:abc",
                "client_id": "2of3opf23",
                "topic": "/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/evt/boom/fmt/json",
            }),
            content_type="application/json",
        )

        assert {"result": "ok"} == _getjson(response)
        assert response._status_code == 200

    def test_cant_publish_cmd(self, test_client):
        response = test_client.post(
            "/auth_on_publish",
            data=json.dumps({
                "username": "v1:pid123:aircon:0xbeef",
                "password": "p:abc",
                "client_id": "2of3opf23",
                "topic": "/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/cmd/boom/fmt/json",
            }),
            content_type="application/json",
        )

        assert {'result': {'error': 'Topic did not match regex'}} == _getjson(response)
        assert response._status_code == 200


class TestAuthSubscribe:

    def test_can_subscribe(self, test_client):
        response = test_client.post(
            "/auth_on_subscribe",
            data=json.dumps({
                "username": "v1:pid123:aircon:0xbeef",
                "password": "p:abc",
                "client_id": "2of3opf23",
                "topics": [
                    {
                        "topic": "/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/cmd/boom/fmt/json",
                    },
                ],
            }),
            content_type="application/json",
        )

        assert {"result": "ok"} == _getjson(response)
        assert response._status_code == 200

    def test_cant_subscribe_evt(self, test_client):
        response = test_client.post(
            "/auth_on_subscribe",
            data=json.dumps({
                "username": "v1:pid123:aircon:0xbeef",
                "password": "p:abc",
                "client_id": "2of3opf23",
                "topics": [
                    {
                        "topic": "/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/evt/boom/fmt/json",
                    },
                ]
            }),
            content_type="application/json",
        )

        assert {'result': {'error': 'Topic did not match regex'}} == _getjson(response)
        assert response._status_code == 200


class TestWorkerConnect:

    def test_worker_register(self, test_client):
        password = "abc123"

        with patch("zconnectmqttauth.brokers.vernemq.WORKER_PASSWORD", password):
            response = test_client.post(
                "/auth_on_register",
                data=json.dumps({
                    "username": WORKER_USERNAME,
                    "password": password,
                    "client_id": "2of3opf23",
                    "topics": [
                        {
                            "topic": "/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/evt/boom/fmt/json",
                        },
                    ]
                }),
                content_type="application/json",
            )

        assert {"result": "ok"} == _getjson(response)
        assert response._status_code == 200

    @pytest.mark.parametrize("endpoint", (
        "/auth_on_subscribe",
        "/auth_on_publish",
    ))
    def test_worker_pubsub(self, test_client, endpoint):
        password = "abc123"

        with patch("zconnectmqttauth.brokers.util.WORKER_PASSWORD", password):
            response = test_client.post(
                endpoint,
                data=json.dumps({
                    "username": WORKER_USERNAME,
                    "password": password,
                    "client_id": "2of3opf23",
                    "topics": [
                        {
                            "topic": "/iot-2/type/gateway/id/v1:pid123:aircon:0xbeef/evt/boom/fmt/json",
                        },
                    ]
                }),
                content_type="application/json",
            )

        assert {"result": "ok"} == _getjson(response)
        assert response._status_code == 200
