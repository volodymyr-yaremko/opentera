from tests.opentera.db.models.BaseModelsTest import BaseModelsTest


class TeraServiceAccessTest(BaseModelsTest):

    def test_defaults(self):
        with self._flask_app.app_context():
            pass