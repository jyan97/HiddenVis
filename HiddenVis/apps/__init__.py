# -*- coding: utf-8 -*-

from flask import Flask, render_template

from apps.configs import config
# from apps.models import db

# from apps.manager.density.views import density
# from apps.manager.select_data.views import select_data


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # with app.app_context():
    #     db.init_app(app)
    #     db.create_all()
    return app
