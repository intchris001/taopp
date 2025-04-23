from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = Product.query.limit(8).all()
    return render_template('index.html', products=products)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html') 