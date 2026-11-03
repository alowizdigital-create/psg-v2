from unittest import mock

import pytest

from notifications.sms import SmsError, envoyer_sms


def reponse(code=200, json=None):
    r = mock.Mock(status_code=code, text=str(json))
    r.json.return_value = json if json is not None else {}
    return r


@pytest.fixture
def techsoft(settings):
    settings.SMS_PROVIDER = "techsoft"
    settings.TECHSOFT_API_TOKEN = "jeton-test"
    settings.SMS_SENDER_ID = "PSGROUP"


def test_techsoft_format_de_la_requete(techsoft):
    with mock.patch("notifications.sms.requests.post", return_value=reponse(200, {"status": "success"})) as post:
        envoyer_sms("6 53 83 43 02", "Bonjour")
    url, = post.call_args.args
    assert url == "https://app.techsoft-sms.com/api/http/sms/send"
    assert post.call_args.kwargs["json"] == {
        "api_token": "jeton-test", "recipient": "237653834302", "sender_id": "PSGROUP",
        "type": "plain", "message": "Bonjour"}


@pytest.mark.parametrize("r", [reponse(401, {"message": "Unauthenticated"}),
                               reponse(200, {"status": "error", "message": "Solde insuffisant"})])
def test_techsoft_erreurs(techsoft, r):
    with mock.patch("notifications.sms.requests.post", return_value=r), pytest.raises(SmsError):
        envoyer_sms("653834302", "Bonjour")


def test_techsoft_sans_jeton(settings):
    settings.SMS_PROVIDER = "techsoft"
    settings.TECHSOFT_API_TOKEN = ""
    with pytest.raises(SmsError):
        envoyer_sms("653834302", "Bonjour")
