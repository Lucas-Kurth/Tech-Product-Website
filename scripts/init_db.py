"""
Database initialization script
Run this file to create all database tables
Usage: python scripts/init_db.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from backend.models import User, Product, WishlistItem


def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

        # Optionally add some sample products
        add_sample_products()


def add_sample_products():
    """Add sample products from the homepage to the database"""

    # Check if products already exist
    if Product.query.first() is not None:
        print("Products already exist in database. Skipping sample data insertion.")
        return

    sample_products = [
        {
            'name': 'Apple iPad Air M3',
            'description': 'Powerful M3 chip with stunning Liquid Retina display. Perfect for creative work, multitasking, and entertainment on the go.',
            'price': 599.00,
            'image_url': 'icons/ipad.png',
            'external_link': 'https://www.apple.com/ipad-air/',
            'category': 'Tablets'
        },
        {
            'name': 'Lenovo ThinkPad',
            'description': 'Reliable business laptop with legendary keyboard and all-day battery. Built for professionals who demand performance.',
            'price': 1299.00,
            'image_url': 'icons/lenovo.png',
            'external_link': 'https://www.lenovo.com/thinkpad',
            'category': 'Laptops'
        },
        {
            'name': 'Apple Watch Series 10',
            'description': 'Advanced health sensors with always-on display. Your ultimate fitness companion with seamless iPhone integration.',
            'price': 399.00,
            'image_url': 'icons/applewatch.png',
            'external_link': 'https://www.apple.com/apple-watch-series-10/',
            'category': 'Wearables'
        },
        {
            'name': 'iPhone 17 Pro',
            'description': 'Most powerful iPhone with A18 Pro chip and 48MP camera. Titanium design meets cutting-edge mobile technology.',
            'price': 999.00,
            'image_url': 'icons/iphone.png',
            'external_link': 'https://www.apple.com/iphone-16-pro/',
            'category': 'Smartphones'
        },
        {
            'name': 'Samsung Galaxy Z Flip 6',
            'description': 'Iconic foldable design with FlexMode and powerful cameras. Stand out with this compact and innovative device.',
            'price': 1099.00,
            'image_url': 'icons/samsungFlip.png',
            'external_link': 'https://www.samsung.com/galaxy-z-flip6/',
            'category': 'Smartphones'
        },
        {
            'name': 'Alienware Laptop',
            'description': 'High-refresh display with NVIDIA graphics and advanced cooling. Dominate every game with serious power.',
            'price': 1799.00,
            'image_url': 'icons/gamingLaptop.png',
            'external_link': 'https://rog.asus.com/laptops/',
            'category': 'Laptops'
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Industry-leading noise cancellation with exceptional sound. 30-hour battery and ultra-comfortable all-day design.',
            'price': 349.00,
            'image_url': 'icons/headphones.png',
            'external_link': 'https://www.sony.com/headphones/',
            'category': 'Audio'
        },
        {
            'name': 'NVIDIA RTX 4080',
            'description': 'Next-gen gaming with ray tracing and DLSS 3 technology. Unlock ultimate graphics power for your PC build.',
            'price': 1199.00,
            'image_url': 'icons/graphic.png',
            'external_link': 'https://www.nvidia.com/geforce/',
            'category': 'PC Components'
        }
    ]

    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()
    print(f"Added {len(sample_products)} sample products to the database!")


if __name__ == '__main__':
    init_database()
