from flask import Blueprint

msgapi_bp = Blueprint('msg_api', __name__, url_prefix='/api')

from app.msg_api import msg_routes
