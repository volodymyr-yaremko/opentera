from libtera.forms.TeraForm import *
from flask_babel import gettext
from libtera.db.DBManagerTeraUserAccess import DBManagerTeraUserAccess
from libtera.db.models.TeraSessionType import TeraSessionType


class TeraSessionTypeForm:

    @staticmethod
    def get_session_type_form(user_access: DBManagerTeraUserAccess):
        form = TeraForm("session_type")

        # Building lists
        # projects = user_access.get_accessible_projects()
        # project_list = []
        # for project in projects:
        #     project_list.append(TeraFormValue(value_id=project.id_project, value=project.project_name + ' [' +
        #                                                                          project.project_site.site_name +

        # Building lists
        categories = TeraSessionType.SessionCategoryEnum
        categories_list = []
        for category in categories:
            name = gettext(TeraSessionType.get_category_name(category))
            categories_list.append(TeraFormValue(value_id=category.value, value=name))

        # Sections
        section = TeraFormSection("informations", gettext("Informations"))
        form.add_section(section)

        # Items
        section.add_item(TeraFormItem("id_session_type", gettext("ID Type Séance"), "hidden", True))
        section.add_item(TeraFormItem("session_type_name", gettext("Nom du type de séance"), "text", True))
        section.add_item(TeraFormItem("session_type_prefix", gettext("Code du type de séance"), "text", True,
                                      item_options={'max_length': 10}))
        section.add_item(TeraFormItem("session_type_category", gettext("Catégorie"), "array", item_required=True,
                                      item_values=categories_list))
        section.add_item(TeraFormItem("session_type_online", gettext("Séance assistée?"), "boolean", True))
        section.add_item(TeraFormItem("session_type_multiusers", gettext("Séance de groupe?"), "boolean", True))
        section.add_item(TeraFormItem("session_type_color", gettext("Couleur d'affichage"), "color", True))
        section.add_item(TeraFormItem("session_type_config", gettext("Configuration spécifiques"), "longtext", False))

        return form.to_dict()
