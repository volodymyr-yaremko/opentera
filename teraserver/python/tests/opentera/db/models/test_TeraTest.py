from tests.opentera.db.models.BaseModelsTest import BaseModelsTest
from modules.FlaskModule.FlaskModule import flask_app


class TeraTestTest(BaseModelsTest):

    def test_defaults(self):
        with flask_app.app_context():
            pass
