from app import create_app, db
from app.models import User, Product

def seed_data():
    app = create_app()
    with app.app_context():
        # Create admin user
        admin = User(
            username='admin',
            email='admin@taopp.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create sample products
        products = [
            Product(
                name='Fresh Apples',
                description='Crisp and juicy apples from local farms',
                price=2.99,
                image_url='images/products/apples.jpg',
                stock=100
            ),
            Product(
                name='Organic Milk',
                description='Fresh organic milk from grass-fed cows',
                price=3.49,
                image_url='images/products/milk.jpg',
                stock=50
            ),
            Product(
                name='Whole Wheat Bread',
                description='Freshly baked whole wheat bread',
                price=2.49,
                image_url='images/products/bread.jpg',
                stock=30
            ),
            Product(
                name='Free Range Eggs',
                description='Farm fresh free range eggs',
                price=4.99,
                image_url='images/products/eggs.jpg',
                stock=40
            ),
            Product(
                name='Organic Spinach',
                description='Fresh organic spinach leaves',
                price=3.99,
                image_url='images/products/spinach.jpg',
                stock=25
            ),
            Product(
                name='Greek Yogurt',
                description='Creamy Greek yogurt with live cultures',
                price=2.99,
                image_url='images/products/yogurt.jpg',
                stock=35
            ),
            Product(
                name='Almond Butter',
                description='Smooth and creamy almond butter',
                price=5.99,
                image_url='images/products/almond-butter.jpg',
                stock=20
            ),
            Product(
                name='Quinoa',
                description='Organic quinoa grains',
                price=4.49,
                image_url='images/products/quinoa.jpg',
                stock=15
            )
        ]
        db.session.add_all(products)
        db.session.commit()

if __name__ == '__main__':
    seed_data() 