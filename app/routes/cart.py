from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Cart, CartItem, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart = current_user.cart
    if not cart:
        cart = Cart(user=current_user)
        db.session.add(cart)
        db.session.commit()
    return render_template('cart/view.html', cart=cart)

@cart_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
        
    product = Product.query.get_or_404(product_id)
    
    if quantity > product.stock:
        return jsonify({'error': 'Not enough stock available'}), 400
    
    cart = current_user.cart
    if not cart:
        cart = Cart(user=current_user)
        db.session.add(cart)
    
    cart_item = CartItem.query.filter_by(cart=cart, product=product).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart successfully'})

@cart_bp.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    cart_item_id = request.form.get('cart_item_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    if not cart_item_id or not quantity:
        return jsonify({'error': 'Cart item ID and quantity are required'}), 400
        
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.cart.user != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if quantity > cart_item.product.stock:
        return jsonify({'error': 'Not enough stock available'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({'message': 'Cart updated successfully'})

@cart_bp.route('/cart/remove/<int:cart_item_id>')
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.cart.user != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(cart_item)
    db.session.commit()
    
    return redirect(url_for('cart.view_cart')) 