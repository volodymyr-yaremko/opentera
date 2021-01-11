from flask import jsonify, session, request
from flask_restx import Resource

from services.BureauActif import Globals
from services.shared.ServiceAccessManager import ServiceAccessManager, current_login_type, current_device_client, \
    current_participant_client, current_user_client, LoginType
from services.BureauActif.FlaskModule import default_api_ns as api, flask_app

# Parser definition(s)
get_parser = api.parser()
get_parser.add_argument('id_project', type=str, help='First day of the month for the data to query')
get_parser.add_argument('id_site', type=str, help='First day of the month for the data to query')


class QueryLoginType(Resource):

    def __init__(self, _api, *args, **kwargs):
        Resource.__init__(self, _api, *args, **kwargs)
        self.module = kwargs.get('flaskModule', None)

    @api.expect(get_parser)
    @api.doc(description='Gets current login type: device, participant or user and associated informations',
             responses={200: 'Success'})
    @ServiceAccessManager.token_required
    def get(self):
        parser = get_parser
        args = parser.parse_args()
        login_infos = {
            'login_type': 'unknown',
            'login_id': 0,
            'is_super_admin': False
        }

        if current_login_type == LoginType.DEVICE_LOGIN:
            login_infos['login_type'] = 'device'
            login_infos['login_id'] = current_device_client.id_device

        if current_login_type == LoginType.PARTICIPANT_LOGIN:
            login_infos['login_type'] = 'participant'
            login_infos['login_id'] = current_participant_client.id_participant

        if current_login_type == LoginType.USER_LOGIN:
            login_infos['login_type'] = 'user'
            login_infos['login_id'] = current_user_client.id_user
            login_infos['is_super_admin'] = current_user_client.user_superadmin

        # If reservation has a session associated to it, get it from OpenTera
        if args['id_project'] or args['id_site']:
            if args['id_project']:
                params = {'id_project': args['id_project'], 'uuid_user': current_user_client.user_uuid}
            if args['id_site']:
                params = {'id_site': args['id_site'], 'uuid_user': current_user_client.user_uuid}

            endpoint = '/api/service/user_role'
            response = Globals.service.get_from_opentera(endpoint, params)

            if response.status_code == 200:
                permission_info = response.json()
                login_infos.update(permission_info)

        return login_infos
