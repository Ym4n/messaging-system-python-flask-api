from flask import Blueprint

pages_bp = Blueprint('pages', __name__,template_folder='templates')

from app.pages import Main_Page_Route