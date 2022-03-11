""" Work in progress; not ready for use.
Models: https://pyrat.uniklinik-bonn.de/pyrat-test/api/v2/specification/ui#/models
Updates:
    Currently, SFB team does not expect to query the pyrat database for updates
    If this changes, we should add a table that takes a hash of the item in the payload
    and references a lookup table before updating
Regularity:
    Currently, SFB team expects to manually enter subjects.
    In the future, we could make adjustments to run a chronjob on a set of IDs
Post to pyrat: future updates may include posting deathdate information
    Currently, we do not have write permissions to do so
Issues that required changes to schema:
    1. subject.User lab has no clear corresponding item in pyrat. We propose to make
       this nullable, and then update as users are added.
    2. subject.User user - because pyrat does not permit us to query the user table
       with unique IDs, and because adamacs may want to track users not associated with
       the animal management facility, we propose assigning an int as adamacs user_id,
       which can be projected up to the animal table as either owner or responsible.
    3. by projecting up from user_id, we eliminate the need for a separate user_role
       table that would have handled 'responsible' and 'owner' - Are there any other
       roles we'd like to keep track of? roles as unique pairing of subject and user
       seem unqiue to the pyrat owner/responsible definitions.
    4. Project is not available via pyrat, so could not be linked to subject
Issues with pyrat test database:
    1. None of the available animals have generation information, making it hard to see
       potential variability in this info.
    2. A number of test subjects are missing crucial data like birthdate. For now,
       these variables have been set as nullable, but should be enforced when we have
       access to the real server.

Example payload= (note( HSC prefix has mutation data))
    [{'eartag_or_id': 'ROE-0221', 'labid': None, 'sex': 'f', 'generation': None,
      'dateborn': '2017-04-10T00:00:00', 'strain_name': 'Test_2',
      'mutations': [{'animalid': 17984, 'mutation_id': 66,
                     'mutationname': 'cbl-b', 'grade_id': 3,'mutationgrade': '+/+'}],
      'parents': [{'animalid': 17888, 'parent_id': 14816,
                   'parent_eartag': 'ROE-0138', 'parent_sex': 'm'},
                  {'animalid': 17888,'parent_id': 17199,
                   'parent_eartag': 'ROE-0182', 'parent_sex': 'f'}],
      'licence_number': None, 'licence_title': None,
      'owner_fullname': 'Röll Wilhelm', 'responsible_fullname': None}]
"""

import datajoint as dj
import json
import requests
from requests.auth import HTTPBasicAuth
from ..pipeline import subject

# Constants
url = 'https://pyrat.uniklinik-bonn.de/pyrat-test/api/v2/'


class PyratIngestion:
    def __init__(self):
        # Ensure credentials
        assert dj.config['custom']['pyrat_client_token'], \
            'Need pyrat client/user tokens in dj.config'

        # Establish Authentication
        global auth
        auth = HTTPBasicAuth(dj.config['custom']['pyrat_client_token'],
                             dj.config['custom']['pyrat_user_token'])

        # Establish Connection
        test_connection = requests.get(url + 'version', auth=auth)
        if test_connection.status_code == 200:
            print('Connected')
        else:
            print(f'Connection error {test_connection.status_code}')

    def get_animal(self, SubjectID: str, prompt=True):
        """Import subject info from pyrat into adamacs subject schema
        :param SubjectID: accepts wildcards (e.g., KOF* for IDs beginning w/KOF)
        example use: PyratIngestion().get_animal('KOF*')


        """
        requested_params = {'_key': ['eartag_or_id', 'labid', 'sex', 'dateborn',
                                     'strain_id', 'strain_name', 'mutations',
                                     'generation', 'parents', 'licence_number',
                                     'licence_title', 'owner_fullname',
                                     'responsible_fullname'],
                            'eartag': SubjectID}
        payload = json.loads(requests.get(url+'animals', auth=auth,
                                          params=requested_params
                                          ).content)

        print('Gathering users...')
        user_list = [{'user_id': 0, 'name': 'default_id'}]
        # needed default else err on max_list_val - should initialize as empty
        owner_id = None
        max_db_user_id = int((dj.U().aggr(subject.User, n='max(user_id)'
                                          ).fetch('n') or 0) + 1)
        for owner in restrict_by(payload, 'owner_fullname', user_list, 'user_id'):
            owner_query = subject.User & {'name': owner['owner_fullname']}
            if owner_query:
                owner_id = (owner_query).fetch1('user_id')
            else:
                max_list_val = max([val["user_id"] for val in user_list]) + 1
                owner_id = max(max_db_user_id, max_list_val)
            user_list.append({'user_id': owner_id, 'name': owner['owner_fullname']})
        responsible_id = None
        for resp in restrict_by(payload, 'responsible_fullname'):
            responsible_query = subject.User & {'name': resp['responsible_fullname']}
            if responsible_query:
                responsible_id = responsible_query.fetch1('user_id')
            else:
                max_list_val = max([val["user_id"] for val in user_list]) + 1
                responsible_id = max(max_db_user_id, max_list_val)
                user_list.append({'user_id': responsible_id,
                                  'name': resp['responsible_fullname']})
        user_list = [d for d in user_list if d['user_id'] != 0]

        print('Gathering protocols...')
        protocol_list = []
        for protocol in restrict_by(payload, 'licence_number'):
            # protocol_list, 'protocol'):
            if not subject.Protocol & {'protocol': protocol['licence_number']}:
                protocol_list.append({'protocol': protocol['licence_number'],
                                      'protocol_description': protocol['licence_title']
                                      })
        print('Gathering lines/mutations...')
        line_list = []
        for line in restrict_by(payload, 'strain_id'):
        #  ERROR - this is overly restrictive, not caputring all items that are in genotype_list
            if not subject.Line & {'line': line['strain_id']}:
                is_active = self.strain_status(line['strain_id'])
                line_list.append({'line': line['strain_id'],
                                  'line_name': line['strain_name'],
                                  'is_active': is_active})
        mutation_list = []
        for animal in [d for d in payload if d['mutations']]:
            for mutation in animal['mutations']:  # one of multiple mutations
                if (not subject.Mutation & {'mutation_id': mutation['mutation_id']}
                    and mutation['mutation_id'] not in [val['mutation_id']
                                                        for val in mutation_list]):
                    mutation_list.append({'line': animal['strain_id'],
                                          'mutation_id': mutation['mutation_id'],
                                          'description': mutation['mutationname']})

        print('Gathering subjects...')
        subject_list = []
        genotype_list = []
        for animal in restrict_by(payload, 'eartag_or_id'):  # subject_list,'subject'):
            if not (subject.Subject & {'subject': animal['eartag_or_id']}):
                parents = animal['parents']
                if parents:
                    parent_ids = {parents[0]['parent_sex']: parents[0]['parent_eartag'],
                                  parents[1]['parent_sex']: parents[1]['parent_eartag']}
                else:
                    parent_ids = None
                subject_list.append({'subject': animal['eartag_or_id'],
                                     'earmark': animal['labid'],
                                     'sex': animal['sex'],
                                     'birth_date': animal['dateborn'] or None,
                                     # 'subject_description': ??, # pyrat animal_color?
                                     'generation': animal['generation'] or None,
                                     'parent_ids': parent_ids or None,
                                     'owner_id': owner_id,
                                     'responsible_id': responsible_id,
                                     'line': animal['strain_id'],
                                     'protocol': animal['licence_number'] or None})
                for mutation in animal['mutations']:
                    genotype_list.append({'subject': animal['eartag_or_id'],
                                          'line': animal['strain_id'],
                                          'mutation_id': mutation['mutation_id'],
                                          'genotype': mutation['mutationgrade']})

        # --- User Confirmation ---
        print('--- PyRAT items to be inserted ---')
        inserts = [user_list, protocol_list, line_list, mutation_list, subject_list]
        print_key = ['name', 'protocol_description', 'line_name', 'description',
                     'subject']
        titles = ['User(s)', 'Protocol(s)', 'Line(s)', 'Mutation(s)', 'Subjects']
        for insert, key, title in zip(inserts, print_key, titles):
            print(f'{title}: ', list(i[key] for i in insert), '\n')
        if prompt and dj.utils.user_choice('Proceed with new subject schema insert?'
                                           ) != 'yes':
            print('Canceled insert.')
            return

        # --- Inserts ---
        subject.User.insert(user_list)
        subject.Protocol.insert(protocol_list)
        subject.Line.insert(line_list)
        subject.Mutation.insert(mutation_list)
        subject.Subject.insert(subject_list)
        # subject.SubjectGenotype.insert(genotype_list) # foreign key contstraint fail bc line_list is missing items

    def strain_status(self, strain_id: str):
        """For a given a given strain_id, return 'active'
        is_active is the only info uniquely within the strains table

        :param strain_id: strain id from the animal table
        """
        requested_params = {'_key': ['id', 'active'], 'id': strain_id}
        payload = json.loads(requests.get(url+'strains', auth=auth,
                                          params=requested_params
                                          ).content)
        return payload[0]['active']


def restrict_by(payload, pkey, built_list=None, lkey=None):
    """
    First, restrict the list of dicts payload by unique instances of a payload key
    Second, remove items where the payload key is already in the list we're building
    """
    unique_payload = list({v[pkey]: v for v in payload if v[pkey] is not None}.values())
    if built_list:
        existing_ids = [str(val[lkey]) for val in built_list]
        return [d for d in unique_payload if str(d[pkey]) not in existing_ids]
    else:
        return unique_payload
