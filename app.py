import re
import streamlit as st

# Optional Gemini support. The app still works without a Gemini API key.
try:
    from google import genai
except Exception:
    genai = None


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 50-PRODUCT CATALOG
# ============================================================

PRODUCTS = [
    # Women
    {"id": 1, "name": "Floral Printed Kurta Set", "category": "Women", "type": "Ethnic Wear", "price": 1499, "mrp": 2499, "rating": 4.5, "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800"},
    {"id": 2, "name": "Pastel Oversized Shirt", "category": "Women", "type": "Shirt", "price": 899, "mrp": 1599, "rating": 4.3, "image": "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?w=800"},
    {"id": 3, "name": "Women's Denim Jacket", "category": "Women", "type": "Jacket", "price": 1299, "mrp": 2199, "rating": 4.4, "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=800"},
    {"id": 4, "name": "Elegant Party Dress", "category": "Women", "type": "Dress", "price": 1899, "mrp": 2999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=800"},
    {"id": 5, "name": "Cotton Straight Kurta", "category": "Women", "type": "Ethnic Wear", "price": 799, "mrp": 1299, "rating": 4.2, "image": "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=800"},
    {"id": 6, "name": "High Waist Blue Jeans", "category": "Women", "type": "Jeans", "price": 1199, "mrp": 1999, "rating": 4.5, "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800"},
    {"id": 7, "name": "Floral Casual Top", "category": "Women", "type": "Top", "price": 699, "mrp": 1199, "rating": 4.3, "image": "https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?w=800"},
    {"id": 8, "name": "Elegant Anarkali Suit", "category": "Women", "type": "Ethnic Wear", "price": 2199, "mrp": 3499, "rating": 4.7, "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=800"},
    {"id": 9, "name": "Women's Black Blazer", "category": "Women", "type": "Formal Wear", "price": 1699, "mrp": 2599, "rating": 4.4, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800"},
    {"id": 10, "name": "Printed Summer Dress", "category": "Women", "type": "Dress", "price": 999, "mrp": 1699, "rating": 4.5, "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=800"},

    # Men
    {"id": 11, "name": "Classic Men's Casual Shirt", "category": "Men", "type": "Shirt", "price": 999, "mrp": 1799, "rating": 4.4, "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800"},
    {"id": 12, "name": "Relaxed Fit Denim Jeans", "category": "Men", "type": "Jeans", "price": 1299, "mrp": 2299, "rating": 4.3, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800"},
    {"id": 13, "name": "Men's Black T-Shirt", "category": "Men", "type": "T-Shirt", "price": 599, "mrp": 999, "rating": 4.4, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800"},
    {"id": 14, "name": "Men's Formal Shirt", "category": "Men", "type": "Formal Wear", "price": 899, "mrp": 1499, "rating": 4.5, "image": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=800"},
    {"id": 15, "name": "Slim Fit Chinos", "category": "Men", "type": "Trousers", "price": 1199, "mrp": 1999, "rating": 4.3, "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800"},
    {"id": 16, "name": "Men's Denim Jacket", "category": "Men", "type": "Jacket", "price": 1499, "mrp": 2499, "rating": 4.6, "image": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=800"},
    {"id": 17, "name": "Men's Polo T-Shirt", "category": "Men", "type": "T-Shirt", "price": 799, "mrp": 1299, "rating": 4.5, "image": "https://images.unsplash.com/photo-1625910513413-5fc45b7d7eae?w=800"},
    {"id": 18, "name": "Men's Casual Hoodie", "category": "Men", "type": "Hoodie", "price": 1099, "mrp": 1899, "rating": 4.4, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800"},
    {"id": 19, "name": "Men's Linen Shirt", "category": "Men", "type": "Shirt", "price": 1199, "mrp": 1999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800"},
    {"id": 20, "name": "Men's Premium Blazer", "category": "Men", "type": "Formal Wear", "price": 2499, "mrp": 3999, "rating": 4.8, "image": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800"},

    # Beauty
    {"id": 21, "name": "Hydrating Glow Serum", "category": "Beauty", "type": "Skincare", "price": 799, "mrp": 1299, "rating": 4.7, "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800"},
    {"id": 22, "name": "Velvet Matte Lipstick", "category": "Beauty", "type": "Makeup", "price": 599, "mrp": 899, "rating": 4.5, "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800"},
    {"id": 23, "name": "Soft Blush Makeup Palette", "category": "Beauty", "type": "Makeup", "price": 899, "mrp": 1399, "rating": 4.6, "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800"},
    {"id": 24, "name": "Vitamin C Face Serum", "category": "Beauty", "type": "Skincare", "price": 699, "mrp": 1199, "rating": 4.5, "image": "https://images.unsplash.com/photo-1556229010-aa3c1c2c7c4a?w=800"},
    {"id": 25, "name": "Hydrating Face Moisturizer", "category": "Beauty", "type": "Skincare", "price": 549, "mrp": 899, "rating": 4.4, "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800"},
    {"id": 26, "name": "Waterproof Mascara", "category": "Beauty", "type": "Makeup", "price": 499, "mrp": 799, "rating": 4.3, "image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=800"},
    {"id": 27, "name": "Liquid Foundation", "category": "Beauty", "type": "Makeup", "price": 749, "mrp": 1199, "rating": 4.5, "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800"},
    {"id": 28, "name": "Rose Face Toner", "category": "Beauty", "type": "Skincare", "price": 399, "mrp": 699, "rating": 4.2, "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=800"},
    {"id": 29, "name": "Nude Lip Gloss", "category": "Beauty", "type": "Makeup", "price": 349, "mrp": 599, "rating": 4.3, "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800"},
    {"id": 30, "name": "Daily Sunscreen SPF 50", "category": "Beauty", "type": "Skincare", "price": 599, "mrp": 899, "rating": 4.6, "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800"},

    # Accessories
    {"id": 31, "name": "Minimal Gold Necklace", "category": "Accessories", "type": "Jewellery", "price": 699, "mrp": 1199, "rating": 4.6, "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800"},
    {"id": 32, "name": "Structured Women's Handbag", "category": "Accessories", "type": "Bags", "price": 1199, "mrp": 1999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800"},
    {"id": 33, "name": "Classic Leather Wallet", "category": "Accessories", "type": "Wallet", "price": 499, "mrp": 899, "rating": 4.4, "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800"},
    {"id": 34, "name": "Elegant Pearl Earrings", "category": "Accessories", "type": "Jewellery", "price": 599, "mrp": 999, "rating": 4.5, "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800"},
    {"id": 35, "name": "Women's Fashion Watch", "category": "Accessories", "type": "Watch", "price": 1299, "mrp": 2199, "rating": 4.6, "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800"},
    {"id": 36, "name": "Men's Classic Watch", "category": "Accessories", "type": "Watch", "price": 1499, "mrp": 2499, "rating": 4.7, "image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=800"},
    {"id": 37, "name": "Fashion Sunglasses", "category": "Accessories", "type": "Sunglasses", "price": 399, "mrp": 699, "rating": 4.3, "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800"},
    {"id": 38, "name": "Leather Crossbody Bag", "category": "Accessories", "type": "Bags", "price": 999, "mrp": 1699, "rating": 4.5, "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=800"},
    {"id": 39, "name": "Statement Bracelet", "category": "Accessories", "type": "Jewellery", "price": 449, "mrp": 799, "rating": 4.2, "image": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800"},
    {"id": 40, "name": "Classic Leather Belt", "category": "Accessories", "type": "Belt", "price": 599, "mrp": 999, "rating": 4.4, "image": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=800"},

    # Footwear
    {"id": 41, "name": "Everyday Sneakers", "category": "Footwear", "type": "Shoes", "price": 1299, "mrp": 2199, "rating": 4.4, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"},
    {"id": 42, "name": "Women's Casual Sneakers", "category": "Footwear", "type": "Shoes", "price": 999, "mrp": 1699, "rating": 4.5, "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800"},
    {"id": 43, "name": "Men's Running Shoes", "category": "Footwear", "type": "Sports Shoes", "price": 1599, "mrp": 2599, "rating": 4.7, "image": "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800"},
    {"id": 44, "name": "Women's Flat Sandals", "category": "Footwear", "type": "Sandals", "price": 499, "mrp": 899, "rating": 4.3, "image": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=800"},
    {"id": 45, "name": "Men's Casual Loafers", "category": "Footwear", "type": "Loafers", "price": 1099, "mrp": 1799, "rating": 4.5, "image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=800"},
    {"id": 46, "name": "Women's Heeled Sandals", "category": "Footwear", "type": "Heels", "price": 899, "mrp": 1499, "rating": 4.4, "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800"},
    {"id": 47, "name": "Classic White Sneakers", "category": "Footwear", "type": "Shoes", "price": 1199, "mrp": 1999, "rating": 4.6, "image": "https://images.unsplash.com/photo-1495555961986-6d4c1ecb7be3?w=800"},
    {"id": 48, "name": "Women's Ballet Flats", "category": "Footwear", "type": "Flats", "price": 699, "mrp": 1099, "rating": 4.3, "image": "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=800"},
    {"id": 49, "name": "Men's Sports Sneakers", "category": "Footwear", "type": "Sports Shoes", "price": 1399, "mrp": 2299, "rating": 4.5, "image": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=800"},
    {"id": 50, "name": "Premium Party Heels", "category": "Footwear", "type": "Heels", "price": 1499, "mrp": 2499, "rating": 4.7, "image": "https://images.unsplash.com/photo-1515347619252-60a4bf4fff4f?w=800"},
]


# ============================================================
# CSS - NO HTML UI IS REQUIRED FOR THE MAIN LAYOUT
# ============================================================

st.markdown(
    """
    <style>
