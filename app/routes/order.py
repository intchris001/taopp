from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mail import Message
from app import db, mail
from app.models import Order, OrderItem, Cart, CartItem

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user=current_user).order_by(Order.created_at.desc()).all()
    return render_template('order/list.html', orders=orders)

@order_bp.route('/orders/<int:id>')
@login_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    if order.user != current_user:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('order.orders'))
    return render_template('order/detail.html', order=order)

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = current_user.cart
    if not cart or not cart.items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('product.products'))
    
    if request.method == 'POST':
        # Create order
        order = Order(user=current_user)
        db.session.add(order)
        
        # Create order items from cart items
        for cart_item in cart.items:
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
        
        # Clear cart
        for item in cart.items:
            db.session.delete(item)
        db.session.delete(cart)
        
        db.session.commit()
        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('order.order_detail', id=order.id))
    
    return render_template('order/checkout.html', cart=cart)

def send_order_confirmation_email(order):
    msg = Message(
        'Order Confirmation - TAOPP',
        recipients=[current_user.email]
    )
    msg.body = f'''
Dear {current_user.username},

Thank you for your order! Your order number is: {order.id}

Order Details:
{chr(10).join(f'- {item.product.name} x {item.quantity} = ${item.price * item.quantity}' for item in order.items)}

Total Amount: ${order.total_amount}

If you have any questions, please feel free to contact us.

Best Regards,
TAOPP Team
'''
    mail.send(msg) 