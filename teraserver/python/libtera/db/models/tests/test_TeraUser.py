import unittest
from libtera.db.DBManager import DBManager
from libtera.db.models.TeraUser import TeraUser, TeraUserTypes
from libtera.db.models.TeraSite import TeraSite
from libtera.db.models.TeraProject import TeraProject
from libtera.db.models.TeraSiteAccess import TeraSiteAccess
from libtera.db.Base import db
import uuid
import os
from passlib.hash import bcrypt


class TeraUserTest(unittest.TestCase):

    filename = 'TeraUserTest.db'

    SQLITE = {
        'filename': filename
    }

    db_man = DBManager()

    def setUp(self):
        if os.path.isfile(self.filename):
            print('removing database')
            os.remove(self.filename)

        self.db_man.open_local(self.SQLITE)
        # Creating default users / tests.
        self.db_man.create_defaults()

    def tearDown(self):
        pass

    def test_superadmin(self):
        # Superadmin should have access to everything.
        admin = TeraUser.get_user_by_username('admin')
        self.assertNotEqual(admin, None, 'admin user not None')
        self.assertEqual(True, isinstance(admin, TeraUser), 'admin user is a TeraUser')
        self.assertTrue(admin.user_superadmin, 'admin user is superadmin')
        self.assertTrue(TeraUser.verify_password('admin', 'admin'), 'admin user default password is admin')

        # Verify that superadmin can access all sites
        sites = self.db_man.get_user_sites(admin)
        self.assertEqual(len(sites), TeraSite.get_count(), 'admin user can access all sites')

        # Verify that superadmin can access all projects
        projects = self.db_man.get_user_projects(admin)
        self.assertEqual(len(projects), TeraProject.get_count())
