"""
Project 2: Data Analysis Example
"""
import sys
import os
import json

# Add the parent directory to sys.path to import the lib package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.utils import calculate_average
from lib.data_processing import transform_dict, filter_data

def analyze_product_data(products):
    """Analyze product data"""
    # Filter out products with no price or 0 price
    valid_products = filter_data(products, lambda p: p.get('price', 0) > 0)
    
    # Calculate average price by category
    by_category = {}
    for product in valid_products:
        category = product.get('category', 'uncategorized')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(product['price'])
    
    # Transform to get average prices
    avg_prices = transform_dict(by_category, calculate_average)
    
    # Find products above average price in their category
    premium_products = filter_data(
        valid_products,
        lambda p: p['price'] > avg_prices.get(p.get('category', 'uncategorized'), 0)
    )
    
    return {
        "average_by_category": avg_prices,
        "premium_products": premium_products
    }

if __name__ == "__main__":
    # Example data
    products = [
        {"name": "Laptop", "price": 1200, "category": "electronics"},
        {"name": "Smartphone", "price": 800, "category": "electronics"},
        {"name": "Tablet", "price": 300, "category": "electronics"},
        {"name": "Chair", "price": 150, "category": "furniture"},
        {"name": "Desk", "price": 250, "category": "furniture"},
        {"name": "Lamp", "price": 50, "category": "furniture"},
        {"name": "T-shirt", "price": 20, "category": "clothing"},
        {"name": "Jeans", "price": 60, "category": "clothing"},
    ]
    
    result = analyze_product_data(products)
    
    # Display results
    print("Average prices by category:")
    for category, avg in result["average_by_category"].items():
        print(f"  {category}: ${avg:.2f}")
    
    print("\nPremium products:")
    for product in result["premium_products"]:
        print(f"  {product['name']} (${product['price']}) - {product['category']}")
