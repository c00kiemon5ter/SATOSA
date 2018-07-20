import responses
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import satosa.config
from satosa.proxy_server import make_app


class TestAccountLinking:
    def test_full_flow(self, satosa_config_dict, account_linking_module_config):
        api_url = "https://alservice.example.com/api"
        redirect_url = "https://alservice.examle.com/redirect"
        account_linking_module_config["config"]["api_url"] = api_url
        account_linking_module_config["config"]["redirect_url"] = redirect_url
        satosa_config_dict["MICRO_SERVICES"].insert(0, account_linking_module_config)

        # application
        configuration = satosa.config.parse(satosa_config_dict)
        app = make_app(configuration)
        test_client = Client(app, BaseResponse)

        # incoming auth req
        http_resp = test_client.get("/{}/{}/request".format(satosa_config_dict["BACKEND_MODULES"][0]["name"],
                                                            satosa_config_dict["FRONTEND_MODULES"][0]["name"]))
        assert http_resp.status_code == 200

        with responses.RequestsMock() as rsps:
            # fake no previous account linking
            rsps.add(responses.GET, "{}/get_id".format(api_url), "test_ticket", status=404)

            # incoming auth resp
            http_resp = test_client.get("/{}/response".format(satosa_config_dict["BACKEND_MODULES"][0]["name"]))
            assert http_resp.status_code == 302
            assert http_resp.headers["Location"].startswith(redirect_url)

        with responses.RequestsMock() as rsps:
            # fake previous account linking
            rsps.add(responses.GET, "{}/get_id".format(api_url), "test_userid", status=200)

            # incoming account linking response
            http_resp = test_client.get("/account_linking/handle_account_linking")
            assert http_resp.status_code == 200
