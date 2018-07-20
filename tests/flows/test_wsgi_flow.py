"""
Complete test for a SAML to SAML proxy.
"""
import json

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import satosa.config
from satosa.proxy_server import make_app
from satosa.response import NotFound


class TestProxy:
    """
    Performs a complete flow test for the proxy.
    Verifies client <-> PROXY.
    """

    def test_flow(self, satosa_config_dict):
        """
        Performs the test.
        """
        configuration = satosa.config.parse(satosa_config_dict)
        app = make_app(configuration)
        test_client = Client(app, BaseResponse)

        # Make request to frontend
        resp = test_client.get('/{}/{}/request'.format("backend", "frontend"))
        assert resp.status == '200 OK'
        headers = dict(resp.headers)
        assert headers["Set-Cookie"]

        # Fake response coming in to backend
        resp = test_client.get('/{}/response'.format("backend"), headers=[("Cookie", headers["Set-Cookie"])])
        assert resp.status == '200 OK'
        assert resp.data.decode('utf-8') == "Auth response received, passed to test frontend"

    def test_unknown_request_path(self, satosa_config_dict):
        configuration = satosa.config.parse(satosa_config_dict)
        app = make_app(configuration)
        test_client = Client(app, BaseResponse)

        resp = test_client.get('/unknown')
        assert resp.status == NotFound._status
