import click
from app import create_app, db
from app.models.product import Category, Product

app = create_app()

@click.group()
def cli():
    """Management script for the application."""
    pass

@cli.command()
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

@cli.command()
def clean_db():
    """Clean the database."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database cleaned successfully!")

def create_sample_data():
    """Create sample categories and products."""
    with app.app_context():
        # Create main categories
        frozen = Category(name='Frozen', description='Frozen food products')
        fresh = Category(name='Fresh', description='Fresh produce and meat')
        beverages = Category(name='Beverages', description='Drinks and beverages')
        home = Category(name='Home', description='Home essentials')
        pet_food = Category(name='Pet Food', description='Pet food and treats')

        db.session.add_all([frozen, fresh, beverages, home, pet_food])
        db.session.commit()

        # Create products for each category
        products = [
            # Frozen products
            Product(name='Ice Cream - Vanilla', description='Creamy vanilla ice cream made with real vanilla beans',
                   price=4.99, image_url='/static/images/products/Ice Cream - Vanilla.jpeg', stock=50, category_id=frozen.id),
            Product(name='Frozen Pizza', description='Ready to bake pepperoni pizza with extra cheese',
                   price=6.99, image_url='/static/images/products/Frozen Pizza.jpeg', stock=30, category_id=frozen.id),
            Product(name='Frozen Mixed Vegetables', description='A mix of corn, peas, carrots, and green beans',
                   price=3.49, image_url='/static/images/products/Frozen Mixed Vegetables.jpeg', stock=45, category_id=frozen.id),
            
            # Fresh products
            Product(name='Organic Bananas', description='Farm-fresh organic bananas',
                   price=1.99, image_url='/static/images/products/Organic Bananas.jpeg', stock=100, category_id=fresh.id),
            Product(name='Chicken Breast', description='Fresh boneless, skinless chicken breasts',
                   price=8.99, image_url='/static/images/products/Chicken Breast.jpeg', stock=35, category_id=fresh.id),
            Product(name='Fresh Spinach', description='Organic baby spinach leaves',
                   price=3.99, image_url='/static/images/products/Fresh Spinach.jpeg', stock=40, category_id=fresh.id),
            
            # Beverage products
            Product(name='Cola', description='Classic cola in a 12-pack',
                   price=5.99, image_url='/static/images/products/Cola .jpeg', stock=60, category_id=beverages.id),
            Product(name='Premium Coffee', description='Whole bean premium roast coffee',
                   price=9.99, image_url='/static/images/products/Premium Coffee.jpeg', stock=25, category_id=beverages.id),
            Product(name='Orange Juice', description='100% freshly squeezed orange juice',
                   price=4.49, image_url='/static/images/products/Orange Juice.jpeg', stock=35, category_id=beverages.id),
            
            # Home products
            Product(name='All-Purpose Cleaner', description='Effective cleaner for all surfaces',
                   price=3.99, image_url='/static/images/products/All-Purpose Cleaner.jpeg', stock=40, category_id=home.id),
            Product(name='Kitchen Towels', description='Pack of 4 absorbent kitchen towels',
                   price=7.99, image_url='/static/images/products/Kitchen Towels.jpeg', stock=30, category_id=home.id),
            Product(name='Shower Gel', description='Refreshing scented shower gel',
                   price=5.49, image_url='/static/images/products/Shower Gel.jpeg', stock=45, category_id=home.id),
            
            # Pet food products
            Product(name='Premium Dog Food', description='High-quality dry dog food for all breeds',
                   price=12.99, image_url='/static/images/products/Premium Dog Food.jpeg', stock=50, category_id=pet_food.id),
            Product(name='Cat Food - Salmon', description='Salmon flavored cat food for adult cats',
                   price=9.99, image_url='/static/images/products/Cat Food - Salmon.jpeg', stock=35, category_id=pet_food.id),
            Product(name='Pet Treats', description='Delicious treats for your furry friends',
                   price=4.99, image_url='/static/images/products/Pet Treats.jpeg', stock=60, category_id=pet_food.id)
        ]

        db.session.add_all(products)
        db.session.commit()
        return len(products), db.session.query(Category).count()

@cli.command()
def seed_db():
    """Seed the database with initial data."""
    num_products, num_categories = create_sample_data()
    print(f"Successfully added {num_products} products to {num_categories} categories")

@cli.command()
def show_db():
    """Show database contents."""
    with app.app_context():
        print("\n=== Categories in Database ===")
        categories = Category.query.all()
        for category in categories:
            print(f"\nCategory ID: {category.id}")
            print(f"Name: {category.name}")
            print(f"Description: {category.description}")
            
        print("\n\n=== Products in Database ===")
        products = Product.query.all()
        for product in products:
            print(f"\nProduct ID: {product.id}")
            print(f"Name: {product.name}")
            print(f"Description: {product.description}")
            print(f"Price: ${product.price}")
            print(f"Stock: {product.stock}")
            print(f"Category ID: {product.category_id}")
            print(f"Image URL: {product.image_url}")

@cli.command()
def run():
    """Run the application."""
    app.run(debug=True)

if __name__ == '__main__':
    cli() 