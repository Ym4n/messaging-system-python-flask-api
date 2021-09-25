from app.pages import pages_bp
from flask import render_template 

@pages_bp.route('/')
def main_page():
    return render_template('mainPage.html')