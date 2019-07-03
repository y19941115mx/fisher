from flask import Blueprint
from app.api.v1 import auth, tcl


def create_blueprint_web():
    blueprint = Blueprint('v1', __name__, url_prefix='/v1')
    auth.api.register(blueprint)
    tcl.api.register(blueprint)
    return blueprint


bp = create_blueprint_web()
