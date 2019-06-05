from libtera.db.Base import db

# Must include all Database objects here to be properly initialized and created if needed


# All at once to make sure all files ar registered.
from libtera.db.models import *

from libtera.db.models.TeraUser import TeraUser
from libtera.db.models.TeraSite import TeraSite
from libtera.db.models.TeraProject import TeraProject
from libtera.db.models.TeraParticipant import TeraParticipant
from libtera.db.models.TeraParticipantGroup import TeraParticipantGroup
from libtera.db.models.TeraDeviceType import TeraDeviceType
from libtera.db.models.TeraDevice import TeraDevice
from libtera.db.models.TeraKit import TeraKit
from libtera.db.models.TeraSession import TeraSession

# from libtera.db.models.TeraProjectAccess import TeraProjectAccess
# from libtera.db.models.TeraSiteAccess import TeraSiteAccess

from modules.FlaskModule.FlaskModule import flask_app

# User access with roles
from .DBManagerTeraUserAccess import DBManagerTeraUserAccess

class DBManager:
    """db_infos = {
        'user': '',
        'pw': '',
        'db': '',
        'host': '',
        'port': '',
        'type': ''
    }"""

    def __init__(self):
        pass

    @staticmethod
    def userAccess(user: TeraUser):
        access = DBManagerTeraUserAccess(user=user)
        return access

    @staticmethod
    def create_defaults():
        if TeraSite.get_count() == 0:
            print('No sites - creating defaults')
            TeraSite.create_defaults()

        if TeraProject.get_count() == 0:
            print("No projects - creating defaults")
            TeraProject.create_defaults()

        if TeraParticipantGroup.get_count() == 0:
            print("No participant groups - creating defaults")
            TeraParticipantGroup.create_defaults()

        if TeraParticipant.get_count() == 0:
            print("No participant - creating defaults")
            TeraParticipant.create_defaults()

        if TeraUser.get_count() == 0:
            print('No users - creating defaults')
            TeraUser.create_defaults()

        if TeraDeviceType.get_count() == 0:
            print('No device types - creating defaults')
            TeraDeviceType.create_defaults()

        if TeraKit.get_count() == 0:
            print('No kit - creating defaults')
            TeraKit.create_defaults()

        if TeraDevice.get_count() == 0:
            print('No device - creating defaults')
            TeraDevice.create_defaults()

        if TeraSession.get_count() == 0:
            print('No session - creating defaults')
            TeraSession.create_defaults()

    @staticmethod
    def open(db_infos, echo=False):
        db_uri = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % db_infos

        flask_app.config.update({
            'SQLALCHEMY_DATABASE_URI': db_uri,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ECHO': echo
        })

        # Create db engine
        db.init_app(flask_app)
        db.app = flask_app

        # Init tables
        db.drop_all()
        db.create_all()

    @staticmethod
    def open_local(db_infos, echo=False):
        db_uri = 'sqlite:///%(filename)s' % db_infos

        flask_app.config.update({
            'SQLALCHEMY_DATABASE_URI': db_uri,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ECHO': echo
        })

        # Create db engine
        db.init_app(flask_app)
        db.app = flask_app

        # Init tables
        db.create_all()
