# -*- coding: utf-8 -*-

from plone import api
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import base64
import json
import requests


class RemoteProceduresVocabularyFactory:
    def __call__(self, context):
        # sample : "https://olln-formulaires.guichet-citoyen.be/api/formdefs/"
        url = api.portal.get_registry_record("procedures.url_formdefs_api")
        # sample : "568DGess2x8j8twv7x2Y2MApjn789xfG7jM27r399q4xSD27Jz"
        key = api.portal.get_registry_record("procedures.secret_key_api")
        orig = "ia.smartweb"
        if not url:
            return SimpleVocabulary([])
        auth = "{}:{}".format(orig, key)
        b64val = base64.b64encode(auth.encode()).decode()
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic {}".format(b64val),
        }
        payload = {}
        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=False
            )
        except Exception:
            return SimpleVocabulary([])

        if response.status_code != 200:
            return SimpleVocabulary([])

        json_procedures = json.loads(response.text)
        return SimpleVocabulary(
            [
                SimpleTerm(value=elem["url"], title=elem["title"])
                for elem in json_procedures.get("data", [])
            ]
        )


RemoteProceduresVocabulary = RemoteProceduresVocabularyFactory()
