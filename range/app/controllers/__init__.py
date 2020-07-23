import os
from flask import Blueprint, current_app
from flask_bootstrap import Bootstrap


from app.controllers.analytics_controller import index as analytics_index



template_dir = os.path.abspath('app/views/analytics')

analytics_blueprints = Blueprint('analytics', 'api', template_folder=template_dir)
analytics_blueprints.add_url_rule('/', view_func=analytics_index, methods=['GET', 'POST'])



