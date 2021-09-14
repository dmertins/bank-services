from pathlib import Path

from flask import Flask


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=str(Path(app.instance_path, 'contract.sqlite')),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    Path(app.instance_path).mkdir(exist_ok=True)

    return app
