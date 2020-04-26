from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from redis import Redis

from project.config import ConfigFlask, ConfigDB, ConfigRedis, ConfigJWT

# Create app
app = Flask(__name__)

# Config app requirements (backend, database, redis, JWT keys)
app.config.from_object(ConfigFlask)
app.config.from_object(ConfigDB)
app.config.from_object(ConfigJWT)

# Create database connection
db = SQLAlchemy(app)

# Persists object as json
ma = Marshmallow(app)

# Establish migration path
migrate_dir = ConfigDB.MIGRATION_PATH
migrate = Migrate(app, db, directory=migrate_dir) if migrate_dir != '' else Migrate(app, db)

jwt = JWTManager(app)

manager = Manager(app)


redis = Redis(host=ConfigRedis.HOST, port=ConfigRedis.PORT, password=ConfigRedis.PASSWORD,
              decode_responses=ConfigRedis.DECODE_RESPONSES)

# --------------------------
# Register all blueprints
# --------------------------
from project.blueprints.user_blueprint import user_blueprint
from project.blueprints.profile_blueprint import profile_blueprint
from project.blueprints.product_blueprint import product_blueprint
from project.blueprints.auth_blueprint import auth_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(auth_blueprint)

# --------------------------
# Error handlers
# --------------------------
@app.errorhandler(500)
def internal_error(ex):
    app.logger.error(ex)
    return 'bad request', 400
