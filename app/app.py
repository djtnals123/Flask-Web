from app import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import MetaData
#

# naming_convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(column_0_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }
# db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/static')
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from app.models.account_model import Account

    # ORM
    # db.init_app(app)
    # if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
    #     migrate.init_app(app, db, render_as_batch=True)
    # else:
    #     migrate.init_app(app, db)
    # from . import models

    # 블루프린트
    from app.views import index_views, account_views, board_views, admin_views
    app.register_blueprint(index_views.bp)
    app.register_blueprint(account_views.bp)
    app.register_blueprint(board_views.bp)
    app.register_blueprint(admin_views.bp)

    # 필터
    from app.filter import first_error, format_datetime
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['first_error'] = first_error

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    return app
