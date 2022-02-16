import os
from datetime import timedelta

from flask_cors import CORS
from random import randint

from flask import Flask, jsonify, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder="../../dist/static",
                template_folder="../../dist")
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.debug = True
    app.permanent_session_lifetime = timedelta(days=30)
    CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/api/random')
    def random_number():
        response = {
            'randomNumber': randint(1, 100)
        }
        return jsonify(response)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        # if app.debug:
        #     return requests.get('http://localhost:8080/{}'.format(path)).text
        return render_template("index.html")

    # 初始化数据库
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import comment
    app.register_blueprint(comment.bp)

    return app
