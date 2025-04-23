from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from app import db
from app.models.product import Product, Category
from sqlalchemy import or_, desc, asc

product_bp = Blueprint('product', __name__)

def get_sorted_categories():
    """Retrieve categories in alphabetical order"""
    return Category.query.order_by(asc(Category.name)).all()

def build_product_query(category_id=None, search_term=None):
    """Construct product query based on filters"""
    base_query = Product.query
    
    if category_id:
        base_query = base_query.filter_by(category_id=category_id)
    
    if search_term:
        search_filter = or_(
            Product.name.ilike(f'%{search_term}%'),
            Product.description.ilike(f'%{search_term}%')
        )
        base_query = base_query.filter(search_filter)
    
    return base_query.order_by(asc(Product.name))

@product_bp.route('/products')
def products():
    """Display products with optional category filtering and pagination"""
    page_number = request.args.get('page', 1, type=int)
    selected_category = request.args.get('category_id', None, type=int)
    items_per_page = 12
    
    # Get available categories
    available_categories = get_sorted_categories()
    
    # Build and execute product query
    product_query = build_product_query(category_id=selected_category)
    paginated_products = product_query.paginate(
        page=page_number, 
        per_page=items_per_page
    )
    
    template_data = {
        'products': paginated_products,
        'categories': available_categories,
        'category_id': selected_category
    }
    
    return render_template('product/products.html', **template_data)

@product_bp.route('/products/category/<int:category_id>')
def products_by_category(category_id):
    """Redirect to products view with category filter"""
    return redirect(url_for('product.products', category_id=category_id))

@product_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    """Display detailed product information and related items"""
    selected_product = Product.query.get_or_404(product_id)
    
    # Find related products from the same category
    related_items = []
    if selected_product.category_id:
        related_items = Product.query.filter(
            Product.category_id == selected_product.category_id,
            Product.id != selected_product.id
        ).order_by(asc(Product.name)).limit(4).all()
    
    return render_template(
        'product/detail.html',
        product=selected_product,
        related_products=related_items
    )

@product_bp.route('/products/search')
def search():
    """Search products by name or description"""
    search_query = request.args.get('q', '').strip()
    
    if not search_query:
        return redirect(url_for('product.products'))
    
    # Execute search query
    search_results = build_product_query(search_term=search_query).all()
    
    return render_template(
        'product/search.html',
        products=search_results,
        query=search_query
    ) 