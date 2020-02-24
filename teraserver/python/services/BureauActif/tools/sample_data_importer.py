import sys
from requests import get, post
import json
from datetime import datetime

from services.BureauActif.tools.sample_data_loader import load_data_from_path


class Config:
    hostname = 'localhost'
    port = 4040

    # User endpoints
    user_login_endpoint = '/api/user/login'
    user_participant_endpoint = '/api/user/participants'
    user_site_endpoint = '/api/user/sites'
    user_project_endpoint = '/api/user/projects'
    user_device_endpoint = '/api/user/devices'
    user_device_project_endpoint = '/api/user/deviceprojects'
    user_device_participant_endpoint = '/api/user/deviceparticipants'

    # Device endpoints
    device_login_endpoint = '/api/device/login'
    device_session_endpoint = '/api/device/sessions'


    username = 'admin'
    password = 'admin'


def _make_url(hostname, port, endpoint):
    return 'https://' + hostname + ':' + str(port) + endpoint


def login_user(config: Config):
    url = _make_url(config.hostname, config.port, config.user_login_endpoint)
    response = get(url=url, verify=False, auth=(config.username, config.password))
    if response.status_code == 200:
        return response.json()
    return {}


def create_site(config: Config, name):
    url = _make_url(config.hostname, config.port, config.user_site_endpoint)

    site_dict = {'site': {'id_site': 0,
                          'site_name': name}
                 }
    try:
        response = post(url=url, json=site_dict, verify=False, auth=(config.username, config.password))
    except:
        return {}

    if response.status_code == 200:
        return response.json().pop()
    return {}


def create_project(config: Config, name: str, site_id: int):

    url = _make_url(config.hostname, config.port, config.user_project_endpoint)

    project_dict = {'project': {'id_project': 0,
                                'project_name': name,
                                'id_site': site_id}
                 }
    try:
        response = post(url=url, json=project_dict, verify=False, auth=(config.username, config.password))
    except:
        return {}

    if response.status_code == 200:
        return response.json().pop()
    return {}


def create_participant(config: Config, name: str, id_project: int):
    url = _make_url(config.hostname, config.port, config.user_participant_endpoint)

    try:

        participant_dict = {'participant': {'id_participant': 0,
                                            'id_project': id_project,
                                            'participant_name': name}}

        response = post(url=url, json=participant_dict, verify=False, auth=(config.username, config.password))

    except:
        return {}

    if response.status_code == 200:
        return response.json().pop()
    return {}


def create_device(config: Config, name: str):
    url = _make_url(config.hostname, config.port, config.user_device_endpoint)
    try:
        device_dict = {'device': {'id_device': 0, 'device_name': name, 'device_type': 4, 'device_enabled': True}}
        response = post(url=url, json=device_dict, verify=False, auth=(config.username, config.password))

    except:
        return {}

    if response.status_code == 200:
        return response.json().pop()
    return {}


def add_device_project(config: Config, id_project: int, id_device: int):
    url = _make_url(config.hostname, config.port, config.user_device_project_endpoint)
    try:
        device_project_dict = {'device_project': {'id_device': id_device, 'id_project': id_project}}
        response = post(url=url, json=device_project_dict, verify=False, auth=(config.username, config.password))
    except:
        return {}
    if response.status_code == 200:
        return response.json().pop()
    return {}


def add_device_participant(config: Config, id_participant: int, id_device: int):
    url = _make_url(config.hostname, config.port, config.user_device_participant_endpoint)
    try:
        device_participant_dict = {'device_participant': {'id_device': id_device, 'id_participant': id_participant}}
        response = post(url=url, json=device_participant_dict, verify=False, auth=(config.username, config.password))
    except:
        return {}

    if response.status_code == 200:
        return response.json().pop()
    return {}


def create_device_session(config: Config, session_participants: list, id_session_type: int):
    url = _make_url(config.hostname, config.port, config.device_session_endpoint)
    try:
        session_dict = {'session': {'id_session': 0,
                                    'id_session_type': 2,  # TODO get session types from server
                                    'session_participants': session_participants}}

        response = post(url=url, json=session_dict, verify=False, auth=(config.username, config.password))
    except:
        return {}

    if response.status_code == 200:
        return response.json().pop()
    return {}


if __name__ == '__main__':

    config = Config()

    # Get data from files
    result = load_data_from_path('/Users/dominic/Downloads/Rasp8')

    # Login admin
    admin_info = login_user(config)

    # create_participant(config1, 'PartBA_1')
    site_info = create_site(config, 'Bureau Actif Site ' + str(datetime.now()))
    project_info = create_project(config, 'Projet Bureau Actif', site_info['id_site'])
    participant_info = create_participant(config, 'MyParticipant', project_info['id_project'])
    device_info = create_device(config, 'MonBureau')
    device_project_info = add_device_project(config, project_info['id_project'], device_info['id_device'])
    device_participant_info = add_device_participant(config, participant_info['id_participant'],
                                                     device_info['id_device'])

    print(site_info, project_info, participant_info, device_info, device_project_info, device_participant_info)


