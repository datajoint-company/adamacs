""" Work in progress; not ready for use.
Methods below outline how to establish a connection and request a payload
More work needs to be done to map the adamacs.schemas field onto the pyrat 'models'
Models: https://pyrat.uniklinik-bonn.de/pyrat-test/api/v2/specification/ui#/models

Specifically, which fields should be directly loaded from pyrat and which fields
should serve as primary keys for selecting which pyrat entries to ingest?
"""

import datajoint as dj
import json
import requests
from requests.auth import HTTPBasicAuth

# Constants
url = 'https://pyrat.uniklinik-bonn.de/pyrat-test/api/v2/'


class PyratIngestion:
    """Work in progress; not ready for use"""
    def __init__(self):
        # Ensure credentials
        assert dj.config['custom']['pyrat_client_token'], \
            'Need pyrat client/user tokens in dj.config'

        # Establish Authentication
        auth = HTTPBasicAuth(dj.config['custom']['pyrat_client_token'],
                             dj.config['custom']['pyrat_user_token'])
        global auth

        # Establish Connection
        test_connection = requests.get(url + 'version', auth=auth)
        if test_connection.status_code == 200:
            print('Connected')
        else:
            print(f'Connection error {test_connection.status_code}')

    def get_animal(self, SubjectID=None):
        requested_params = {'_key': ['animalid', 'age_days']}  # TODO: add fields

        # TODO - ingestigate restricting request to SubjectID
        payload = requests.get(url+'animals', auth=auth, params=requested_params)
        animal = json.loads(payload.content)

        if SubjectID:
            animal = [d for d in animal if d['animalid'] == SubjectID]

        # TODO - ingest resulting payload into relevant schema

    def get_strain(self):
        # requested_params = {'_key': ['id', 'status']}
        # payload = requests.get(url+'strains', auth=auth, params=requested_params)
        # strain = json.loads(payload.content)
        pass
