from app import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event

class Product(db.Model):
    """Product model representing items available for purchase"""
    
    __tablename__ = 'product'
    
    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    # Foreign keys and relationships
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Media and assets
    image_url = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @hybrid_property
    def is_available(self):
        """Check if product is available for purchase"""
        return self.stock > 0
    
    @hybrid_property
    def price_display(self):
        """Format price for display"""
        return f"${self.price:.2f}"
    
    def update_stock(self, quantity):
        """Update product stock"""
        if self.stock + quantity < 0:
            return False
        self.stock += quantity
        return True
    
    def to_dict(self):
        """Convert product to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Category(db.Model):
    """Category model for organizing products"""
    
    __tablename__ = 'category'
    
    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    
    # Relationships
    products = db.relationship(
        'Product',
        backref='category',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    @hybrid_property
    def product_count(self):
        """Get number of products in category"""
        return self.products.count()
    
    def to_dict(self):
        """Convert category to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'product_count': self.product_count
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

# Event listeners
@event.listens_for(Product, 'before_insert')
def set_default_timestamps(mapper, connection, target):
    """Set default timestamps for new products"""
    target.created_at = datetime.utcnow()
    target.updated_at = datetime.utcnow()

@event.listens_for(Product, 'before_update')
def update_timestamp(mapper, connection, target):
    """Update timestamp when product is modified"""
    target.updated_at = datetime.utcnow() 