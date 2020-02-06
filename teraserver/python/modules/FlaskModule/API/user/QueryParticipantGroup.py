from flask import jsonify, session, request
from flask_restplus import Resource, reqparse
from modules.LoginModule.LoginModule import multi_auth
from modules.FlaskModule.FlaskModule import user_api_ns as api
from libtera.db.models.TeraUser import TeraUser
from libtera.db.models.TeraParticipantGroup import TeraParticipantGroup
from libtera.db.DBManager import DBManager
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import exc

# Parser definition(s)
get_parser = api.parser()
get_parser.add_argument('id_group', type=int, help='ID of the participant group to query'
                        )
get_parser.add_argument('id_project', type=int, help='ID of the project from which to get all participant groups')
get_parser.add_argument('id', type=int, help='Alias for "id_group"')
get_parser.add_argument('list', type=bool, help='Flag that limits the returned data to minimal information')

post_parser = reqparse.RequestParser()
post_parser.add_argument('group', type=str, location='json', help='Participant group to create / update', required=True)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('id', type=int, help='Participant Group ID to delete', required=True)


class QueryParticipantGroup(Resource):

    def __init__(self, _api, *args, **kwargs):
        Resource.__init__(self, _api, *args, **kwargs)
        self.module = kwargs.get('flaskModule', None)

    @multi_auth.login_required
    @api.expect(get_parser)
    @api.doc(description='Get participant groups information. Only one of the ID parameter is supported at once. '
                         'If no ID is specified, returns all accessible groups for the logged user',
             responses={200: 'Success - returns list of participant groups',
                        500: 'Database error'})
    def get(self):
        current_user = TeraUser.get_user_by_uuid(session['user_id'])
        user_access = DBManager.userAccess(current_user)

        parser = get_parser

        args = parser.parse_args()

        groups = []
        # If we have no arguments, return all accessible participants
        if args['id']:
            args['id_group'] = args['id']

        if not any(args.values()):
            groups = user_access.get_accessible_groups()
        elif args['id_group']:
            if args['id_group'] in user_access.get_accessible_groups_ids():
                groups = [TeraParticipantGroup.get_participant_group_by_id(args['id_group'])]
        elif args['id_project']:
            if args['id_project'] in user_access.get_accessible_projects_ids():
                groups = TeraParticipantGroup.get_participant_group_for_project(args['id_project'])

        try:
            group_list = []
            for group in groups:
                if args['list'] is None:
                    group_json = group.to_json()
                    group_list.append(group_json)
                else:
                    group_json = group.to_json(minimal=True)
                    group_json['group_participant_count'] = len(user_access.query_participants_for_group(
                        group.id_participant_group))
                    group_list.append(group_json)
            return jsonify(group_list)

        except InvalidRequestError:
            return '', 500

    @multi_auth.login_required
    @api.expect(post_parser)
    @api.doc(description='Create / update participant groups. id_participant_group must be set to "0" to create a new '
                         'group. A group can be created/modified if the user has admin rights to the project.',
             responses={200: 'Success',
                        403: 'Logged user can\'t create/update the specified device',
                        400: 'Badly formed JSON or missing fields(id_participant_group or id_project) in the JSON body',
                        500: 'Internal error occured when saving device'})
    def post(self):
        # parser = post_parser

        current_user = TeraUser.get_user_by_uuid(session['user_id'])
        user_access = DBManager.userAccess(current_user)
        # Using request.json instead of parser, since parser messes up the json!
        if 'group' not in request.json:
            return '', 400

        json_group = request.json['group']

        # Validate if we have an id
        if 'id_participant_group' not in json_group or 'id_project' not in json_group:
            return '', 400

        # Check if current user can modify the posted group
        # User can modify or add a group if it has admin access to that project
        if json_group['id_project'] not in user_access.get_accessible_projects_ids(admin_only=True):
            return '', 403

        # Do the update!
        if json_group['id_participant_group'] > 0:
            # Already existing
            try:
                TeraParticipantGroup.update(json_group['id_participant_group'], json_group)
            except exc.SQLAlchemyError:
                import sys
                print(sys.exc_info())
                return '', 500
        else:
            # New
            try:
                new_group = TeraParticipantGroup()
                new_group.from_json(json_group)
                TeraParticipantGroup.insert(new_group)
                # Update ID for further use
                json_group['id_participant_group'] = new_group.id_participant_group
            except exc.SQLAlchemyError:
                import sys
                print(sys.exc_info())
                return '', 500

        # TODO: Publish update to everyone who is subscribed to sites update...
        update_group = TeraParticipantGroup.get_participant_group_by_id(json_group['id_participant_group'])

        return jsonify([update_group.to_json()])

    @multi_auth.login_required
    @api.expect(delete_parser)
    @api.doc(description='Delete a specific participant group',
             responses={200: 'Success',
                        403: 'Logged user can\'t delete participant group (only project admin can delete)',
                        500: 'Database error.'})
    def delete(self):
        parser = delete_parser
        current_user = TeraUser.get_user_by_uuid(session['user_id'])
        user_access = DBManager.userAccess(current_user)

        args = parser.parse_args()
        id_todel = args['id']

        # Check if current user can delete
        # Only projects admins can delete a group
        group = TeraParticipantGroup.get_participant_group_by_id(id_todel)

        if user_access.get_project_role(group.id_project) != 'admin':
            return '', 403

        # If we are here, we are allowed to delete. Do so.
        try:
            TeraParticipantGroup.delete(id_todel=id_todel)
        except exc.SQLAlchemyError:
            import sys
            print(sys.exc_info())
            return 'Database error', 500

        return '', 200
