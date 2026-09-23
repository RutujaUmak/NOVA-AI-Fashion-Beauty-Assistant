
import streamlit as st
from google import genai
import re


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GEMINI
# ============================================================

def get_client():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if api_key:
            return genai.Client(api_key=api_key)

    except Exception:
        pass

    return None


# ============================================================
# 50 PRODUCT CATALOG
# ============================================================

PRODUCTS = [

    # ---------------- WOMEN ----------------

    {
        "id": 1,
        "name": "Floral Printed Kurta Set",
        "cat": "Women",
        "type": "Ethnic Wear",
        "price": 1499,
        "old": 2499,
        "rating": 4.5,
        "image": "https://images.pexels.com/photos/35504999/pexels-photo-35504999.jpeg"
    },

    {
        "id": 2,
        "name": "Pastel Oversized Shirt",
        "cat": "Women",
        "type": "Western Wear",
        "price": 899,
        "old": 1599,
        "rating": 4.3,
        "image": "https://images.pexels.com/photos/36899306/pexels-photo-36899306.jpeg"
    },

    {
        "id": 3,
        "name": "Women's Casual Denim Jacket",
        "cat": "Women",
        "type": "Jacket",
        "price": 1299,
        "old": 2199,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=700"
    },

    {
        "id": 4,
        "name": "Elegant Party Dress",
        "cat": "Women",
        "type": "Party Wear",
        "price": 1899,
        "old": 2999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700"
    },

    {
        "id": 5,
        "name": "Cotton Straight Kurta",
        "cat": "Women",
        "type": "Ethnic Wear",
        "price": 799,
        "old": 1299,
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700"
    },

    {
        "id": 6,
        "name": "High Waist Blue Jeans",
        "cat": "Women",
        "type": "Jeans",
        "price": 1199,
        "old": 1999,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=700"
    },

    {
        "id": 7,
        "name": "Women Floral Top",
        "cat": "Women",
        "type": "Top",
        "price": 699,
        "old": 1199,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?w=700"
    },

    {
        "id": 8,
        "name": "Elegant Anarkali Suit",
        "cat": "Women",
        "type": "Ethnic Wear",
        "price": 2199,
        "old": 3499,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700"
    },

    {
        "id": 9,
        "name": "Women's Black Blazer",
        "cat": "Women",
        "type": "Formal Wear",
        "price": 1699,
        "old": 2599,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=700"
    },

    {
        "id": 10,
        "name": "Printed Summer Dress",
        "cat": "Women",
        "type": "Casual Wear",
        "price": 999,
        "old": 1699,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=700"
    },


    # ---------------- MEN ----------------

    {
        "id": 11,
        "name": "Classic Men's Casual Shirt",
        "cat": "Men",
        "type": "Western Wear",
        "price": 999,
        "old": 1799,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=700"
    },

    {
        "id": 12,
        "name": "Relaxed Fit Denim Jeans",
        "cat": "Men",
        "type": "Jeans",
        "price": 1299,
        "old": 2299,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=700"
    },

    {
        "id": 13,
        "name": "Men's Black T-Shirt",
        "cat": "Men",
        "type": "T-Shirt",
        "price": 599,
        "old": 999,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=700"
    },

    {
        "id": 14,
        "name": "Men's Formal Shirt",
        "cat": "Men",
        "type": "Formal Wear",
        "price": 899,
        "old": 1499,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=700"
    },

    {
        "id": 15,
        "name": "Slim Fit Chinos",
        "cat": "Men",
        "type": "Trousers",
        "price": 1199,
        "old": 1999,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=700"
    },

    {
        "id": 16,
        "name": "Men's Denim Jacket",
        "cat": "Men",
        "type": "Jacket",
        "price": 1499,
        "old": 2499,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=700"
    },

    {
        "id": 17,
        "name": "Men's Polo T-Shirt",
        "cat": "Men",
        "type": "T-Shirt",
        "price": 799,
        "old": 1299,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1625910513413-5fc45b7d7eae?w=700"
    },

    {
        "id": 18,
        "name": "Men's Casual Hoodie",
        "cat": "Men",
        "type": "Hoodie",
        "price": 1099,
        "old": 1899,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=700"
    },

    {
        "id": 19,
        "name": "Men's Linen Shirt",
        "cat": "Men",
        "type": "Casual Wear",
        "price": 1199,
        "old": 1999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=700"
    },

    {
        "id": 20,
        "name": "Men's Premium Blazer",
        "cat": "Men",
        "type": "Formal Wear",
        "price": 2499,
        "old": 3999,
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=700"
    },


    # ---------------- BEAUTY ----------------

    {
        "id": 21,
        "name": "Hydrating Glow Serum",
        "cat": "Beauty",
        "type": "Skincare",
        "price": 799,
        "old": 1299,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700"
    },

    {
        "id": 22,
        "name": "Velvet Matte Lipstick",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 599,
        "old": 899,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=700"
    },

    {
        "id": 23,
        "name": "Soft Blush Makeup Palette",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 899,
        "old": 1399,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=700"
    },

    {
        "id": 24,
        "name": "Vitamin C Face Serum",
        "cat": "Beauty",
        "type": "Skincare",
        "price": 699,
        "old": 1199,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1556229010-aa3c1c2c7c4a?w=700"
    },

    {
        "id": 25,
        "name": "Hydrating Face Moisturizer",
        "cat": "Beauty",
        "type": "Skincare",
        "price": 549,
        "old": 899,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=700"
    },

    {
        "id": 26,
        "name": "Waterproof Mascara",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 499,
        "old": 799,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=700"
    },

    {
        "id": 27,
        "name": "Liquid Foundation",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 749,
        "old": 1199,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=700"
    },

    {
        "id": 28,
        "name": "Rose Face Toner",
        "cat": "Beauty",
        "type": "Skincare",
        "price": 399,
        "old": 699,
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=700"
    },

    {
        "id": 29,
        "name": "Nude Lip Gloss",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 349,
        "old": 599,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=700"
    },

    {
        "id": 30,
        "name": "Daily Sunscreen SPF 50",
        "cat": "Beauty",
        "type": "Skincare",
        "price": 599,
        "old": 899,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=700"
    },


    # ---------------- ACCESSORIES ----------------

    {
        "id": 31,
        "name": "Minimal Gold Necklace",
        "cat": "Accessories",
        "type": "Jewellery",
        "price": 699,
        "old": 1199,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=700"
    },

    {
        "id": 32,
        "name": "Structured Women's Handbag",
        "cat": "Accessories",
        "type": "Bags",
        "price": 1199,
        "old": 1999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700"
    },

    {
        "id": 33,
        "name": "Classic Leather Wallet",
        "cat": "Accessories",
        "type": "Wallet",
        "price": 499,
        "old": 899,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=700"
    },

    {
        "id": 34,
        "name": "Elegant Pearl Earrings",
        "cat": "Accessories",
        "type": "Jewellery",
        "price": 599,
        "old": 999,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=700"
    },

    {
        "id": 35,
        "name": "Women's Fashion Watch",
        "cat": "Accessories",
        "type": "Watch",
        "price": 1299,
        "old": 2199,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=700"
    },

    {
        "id": 36,
        "name": "Men's Classic Watch",
        "cat": "Accessories",
        "type": "Watch",
        "price": 1499,
        "old": 2499,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=700"
    },

    {
        "id": 37,
        "name": "Fashion Sunglasses",
        "cat": "Accessories",
        "type": "Sunglasses",
        "price": 399,
        "old": 699,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700"
    },

    {
        "id": 38,
        "name": "Leather Crossbody Bag",
        "cat": "Accessories",
        "type": "Bags",
        "price": 999,
        "old": 1699,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=700"
    },

    {
        "id": 39,
        "name": "Statement Bracelet",
        "cat": "Accessories",
        "type": "Jewellery",
        "price": 449,
        "old": 799,
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=700"
    },

    {
        "id": 40,
        "name": "Classic Leather Belt",
        "cat": "Accessories",
        "type": "Belt",
        "price": 599,
        "old": 999,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=700"
    },


    # ---------------- FOOTWEAR ----------------

    {
        "id": 41,
        "name": "Everyday Sneakers",
        "cat": "Footwear",
        "type": "Shoes",
        "price": 1299,
        "old": 2199,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700"
    },

    {
        "id": 42,
        "name": "Women's Casual Sneakers",
        "cat": "Footwear",
        "type": "Shoes",
        "price": 999,
        "old": 1699,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=700"
    },

    {
        "id": 43,
        "name": "Men's Running Shoes",
        "cat": "Footwear",
        "type": "Sports Shoes",
        "price": 1599,
        "old": 2599,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=700"
    },

    {
        "id": 44,
        "name": "Women's Flat Sandals",
        "cat": "Footwear",
        "type": "Sandals",
        "price": 499,
        "old": 899,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=700"
    },

    {
        "id": 45,
        "name": "Men's Casual Loafers",
        "cat": "Footwear",
        "type": "Loafers",
        "price": 1099,
        "old": 1799,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=700"
    },

    {
        "id": 46,
        "name": "Women's Heeled Sandals",
        "cat": "Footwear",
        "type": "Heels",
        "price": 899,
        "old": 1499,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=700"
    },

    {
        "id": 47,
        "name": "Classic White Sneakers",
        "cat": "Footwear",
        "type": "Shoes",
        "price": 1199,
        "old": 1999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1495555961986-6d4c1ecb7be3?w=700"
    },

    {
        "id": 48,
        "name": "Women's Ballet Flats",
        "cat": "Footwear",
        "type": "Flats",
        "price": 699,
        "old": 1099,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=700"
    },

    {
        "id": 49,
        "name": "Men's Sports Sneakers",
        "cat": "Footwear",
        "type": "Sports Shoes",
        "price": 1399,
        "old": 2299,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=700"
    },

    {
        "id": 50,
        "name": "Premium Party Heels",
        "cat": "Footwear",
        "type": "Heels",
        "price": 1499,
        "old": 2499,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1515347619252-60a4bf4fff4f?w=700"
    }
]


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wish" not in st.session_state:
    st.session_state.wish = []

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm **NOVA AI** ✨\n\n"
                "I can help you find fashion, beauty, "
                "accessories and footwear based on "
                "your budget and preferences."
            ),
            "products": []
        }
    ]


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
);

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f7f7f8;
    color: #222;
}

#MainMenu, header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1250px;
    padding: 1.2rem 1rem 3rem;
}

.top {
    background: white;
    padding: 20px 25px;
    border-radius: 18px;
    box-shadow: 0 4px 20px #0000000c;
    margin-bottom: 20px;
}

.logo {
    font: 700 36px 'Playfair Display';
}

.logo span {
    color: #d63384;
}

.sub {
    color: #666;
}

.hero {
    padding: 38px;
    border-radius: 24px;
    margin-bottom: 25px;
    background: linear-gradient(
        120deg,
        #fff0f6,
        #f5efff,
        #fff8ef
    );
}

.pill {
    display: inline-block;
    background: #171717;
    color: white;
    padding: 7px 14px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 600;
}

.hero h1 {
    font: 700 44px/1.1 'Playfair Display';
    margin: 18px 0 10px;
}

.hero p {
    color: #555;
    font-size: 17px;
}

.title {
    font: 700 28px 'Playfair Display';
    margin: 25px 0 15px;
}

.ai {
    background: linear-gradient(
        135deg,
        #fff0f7,
        #f7efff
    );
    padding: 22px;
    border: 1px solid #efd9e7;
    border-radius: 20px;
}

.chat-product {
    background: white;
    border: 1px solid #eeeeee;
    border-radius: 16px;
    padding: 10px;
    margin-top: 10px;
}

.chat-product img {
    width: 100%;
    height: 190px;
    object-fit: cover;
    border-radius: 12px;
}

.chat-name {
    font-weight: 700;
    margin-top: 8px;
}

.chat-price {
    font-size: 18px;
    font-weight: 700;
}

.chat-old {
    color: #999;
    text-decoration: line-through;
    font-size: 12px;
}

.chat-rating {
    color: #087f5b;
    font-size: 12px;
}

.card {
    background: white;
    border: 1px solid #eee;
    border-radius: 15px;
    overflow: hidden;
}

.card img {
    width: 100%;
    height: 210px;
    object-fit: cover;
}

.body {
    padding: 13px;
}

.name {
    font-weight: 600;
}

.type {
    font-size: 12px;
    color: #777;
}

.price {
    font-size: 18px;
    font-weight: 700;
    margin-top: 7px;
}

.old {
    text-decoration: line-through;
    color: #999;
    font-size: 12px;
}

.rate {
    color: #087f5b;
    font-size: 12px;
    margin-top: 5px;
}

.stButton > button {
    border-radius: 9px;
    color: #222 !important;
    background: white;
    border: 1px solid #ddd;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #d63384;
    color: #d63384 !important;
}

[data-testid="stChatMessage"],
[data-testid="stChatMessage"] * {
    color: #222 !important;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
    background: #272932 !important;
    caret-color: white !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #d5d5d5 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# BASIC HELPERS
# ============================================================

def get_product(product_id):

    return next(
        (
            p for p in PRODUCTS
            if p["id"] == product_id
        ),
        None
    )


def catalog_text():

    return "\n".join(
        f"""
ID: {p['id']}
Name: {p['name']}
Category: {p['cat']}
Type: {p['type']}
Price: ₹{p['price']}
Rating: {p['rating']}
"""
        for p in PRODUCTS
    )


# ============================================================
# EXTRACT BUDGET
# ============================================================

def extract_budget(question):

    q = question.lower()

    patterns = [

        r"under\s*[₹rs.]?\s*(\d+)",
        r"below\s*[₹rs.]?\s*(\d+)",
        r"within\s*[₹rs.]?\s*(\d+)",
        r"upto\s*[₹rs.]?\s*(\d+)",
        r"up to\s*[₹rs.]?\s*(\d+)",
        r"budget\s*(?:of)?\s*[₹rs.]?\s*(\d+)",
        r"₹\s*(\d+)",
        r"rs\.?\s*(\d+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            q
        )

        if match:

            return int(
                match.group(1)
            )

    return None


# ============================================================
# CATEGORY DETECTION
# ============================================================

def detect_category(question):

    q = question.lower()

    if any(
        word in q
        for word in [
            "makeup",
            "lipstick",
            "mascara",
            "foundation",
            "cosmetic"
        ]
    ):
        return "Beauty"

    if any(
        word in q
        for word in [
            "skin",
            "skincare",
            "serum",
            "moisturizer",
            "sunscreen"
        ]
    ):
        return "Beauty"

    if any(
        word in q
        for word in [
            "men",
            "male",
            "boy",
            "mens"
        ]
    ):
        return "Men"

    if any(
        word in q
        for word in [
            "women",
            "woman",
            "girl",
            "womens"
        ]
    ):
        return "Women"

    if any(
        word in q
        for word in [
            "shoe",
            "shoes",
            "sneaker",
            "footwear",
            "heels",
            "sandals",
            "flats"
        ]
    ):
        return "Footwear"

    if any(
        word in q
        for word in [
            "bag",
            "jewellery",
            "jewelry",
            "necklace",
            "watch",
            "wallet",
            "sunglasses",
            "accessory"
        ]
    ):
        return "Accessories"

    return None


# ============================================================
# PRODUCT SEARCH ENGINE
# ============================================================

def recommend_products(question):

    q = question.lower()

    budget = extract_budget(question)
    category = detect_category(question)

    products = PRODUCTS.copy()

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if category:

        category_products = [
            p for p in products
            if p["cat"].lower()
            == category.lower()
        ]

        if category_products:

            products = category_products

    # --------------------------------------------------------
    # BUDGET
    # --------------------------------------------------------

    if budget:

        budget_products = [
            p for p in products
            if p["price"] <= budget
        ]

        if budget_products:

            products = budget_products

    # --------------------------------------------------------
    # KEYWORD MATCH
    # --------------------------------------------------------

    keywords = re.findall(
        r"[a-zA-Z]+",
        q
    )

    keywords = [
        word for word in keywords
        if len(word) >= 3
    ]

    scored = []

    for p in products:

        searchable = (
            p["name"]
            + " "
            + p["cat"]
            + " "
            + p["type"]
        ).lower()

        score = 0

        for word in keywords:

            if word in searchable:
                score += 2

        scored.append(
            (score, p)
        )

    matched = [
        p for score, p in scored
        if score > 0
    ]

    # Only use keyword filtering when
    # we actually found meaningful matches.

    if matched:

        products = matched

    # --------------------------------------------------------
    # CHEAPEST
    # --------------------------------------------------------

    cheapest_words = [
        "cheapest",
        "cheap",
        "lowest",
        "lowest price",
        "lowest priced",
        "affordable",
        "least expensive"
    ]

    if any(
        word in q
        for word in cheapest_words
    ):

        return sorted(
            products,
            key=lambda p: p["price"]
        )[:4]

    # --------------------------------------------------------
    # BEST RATED
    # --------------------------------------------------------

    if any(
        word in q
        for word in [
            "best rated",
            "highest rated",
            "top rated",
            "best product",
            "best"
        ]
    ):

        return sorted(
            products,
            key=lambda p: p["rating"],
            reverse=True
        )[:4]

    # --------------------------------------------------------
    # EXPENSIVE
    # --------------------------------------------------------

    if any(
        word in q
        for word in [
            "expensive",
            "premium",
            "luxury"
        ]
    ):

        return sorted(
            products,
            key=lambda p: p["price"],
            reverse=True
        )[:4]

    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    return products[:4]


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(question, selected_products):

    client = get_client()

    if not client:

        return fallback_answer(
            question,
            selected_products
        )

    selected_text = "\n".join(
        f"""
Product: {p['name']}
Category: {p['cat']}
Type: {p['type']}
Price: ₹{p['price']}
Rating: {p['rating']}
"""
        for p in selected_products
    )

    # Last few messages provide conversation memory.

    history = st.session_state.messages[-8:]

    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history
    )

    prompt = f"""
You are NOVA AI, a friendly Indian fashion,
beauty and shopping assistant.

You have access to a product catalog.

CATALOG:
{catalog_text()}

PRODUCTS SELECTED BY THE SEARCH ENGINE:
{selected_text}

RECENT CONVERSATION:
{history_text}

CURRENT USER QUESTION:
{question}

RULES:

1. Answer the user's actual question.
2. Never invent products.
3. Never invent prices.
4. Use only products from the catalog.
5. Use ₹ for Indian prices.
6. Be concise but helpful.
7. If products are selected, mention their names and prices.
8. If the user asks for cheapest, clearly identify the lowest-priced
   matching product.
9. If the user asks for a budget, respect the budget.
10. If the user asks a general fashion or beauty question,
    give useful styling advice.
11. If the user asks something unrelated to shopping,
    answer normally but briefly.
12. Do not output product image URLs.
13. Product cards and images will be displayed by the application.
14. Maintain conversational context.

Answer naturally like a premium shopping assistant.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:

            return response.text

    except Exception:

        pass

    return fallback_answer(
        question,
        selected_products
    )


# ============================================================
# FALLBACK
# ============================================================

def fallback_answer(
    question,
    selected_products
):

    if not selected_products:

        return (
            "✨ I couldn't find an exact match. "
            "Try asking for a product category, "
            "budget, or style."
        )

    cheapest = min(
        selected_products,
        key=lambda p: p["price"]
    )

    q = question.lower()

    if "cheapest" in q or "lowest" in q:

        return (
            f"✨ I found the cheapest matching option: "
            f"**{cheapest['name']}** at "
            f"**₹{cheapest['price']:,}** "
            f"with a **{cheapest['rating']}★ rating**."
        )

    if "best" in q:

        best = max(
            selected_products,
            key=lambda p: p["rating"]
        )

        return (
            f"⭐ A highly rated option is "
            f"**{best['name']}** at "
            f"₹{best['price']:,}, "
            f"rated **{best['rating']}★**."
        )

    names = ", ".join(
        p["name"]
        for p in selected_products[:3]
    )

    return (
        f"✨ I found these options for you: "
        f"{names}."
    )


# ============================================================
# PRODUCT CARD INSIDE CHAT
# ============================================================

def show_chat_products(products):

    if not products:

        return

    st.markdown(
        "### 🛍 Recommended for you"
    )

    columns = st.columns(
        min(
            len(products),
            3
        )
    )

    for column, product in zip(
        columns,
        products
    ):

        with column:

            discount = round(
                (
                    (
                        product["old"]
                        - product["price"]
                    )
                    / product["old"]
                )
                * 100
            )

            st.image(
                product["image"],
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class="chat-product">

                    <div class="chat-name">
                        {product['name']}
                    </div>

                    <div class="type">
                        {product['cat']} •
                        {product['type']}
                    </div>

                    <div class="chat-price">
                        ₹{product['price']:,}

                        <span class="chat-old">
                            ₹{product['old']:,}
                        </span>
                    </div>

                    <div class="chat-rating">
                        ★ {product['rating']}
                        • {discount}% OFF
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(
                    "🛍 Add",
                    key=f"chat_add_{product['id']}",
                    use_container_width=True
                ):

                    if product["id"] not in st.session_state.cart:

                        st.session_state.cart.append(
                            product["id"]
                        )

                    st.toast(
                        "Added to cart!"
                    )

            with c2:

                heart = (
                    "❤️"
                    if product["id"]
                    in st.session_state.wish
                    else "♡"
                )

                if st.button(
                    heart,
                    key=f"chat_wish_{product['id']}",
                    use_container_width=True
                ):

                    if product["id"] in st.session_state.wish:

                        st.session_state.wish.remove(
                            product["id"]
                        )

                    else:

                        st.session_state.wish.append(
                            product["id"]
                        )

                    st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="top">

        <div class="logo">
            NOVA<span>AI</span>
        </div>

        <div class="sub">
            Fashion • Beauty • Lifestyle • AI Shopping
        </div>

    </div>

    <div class="hero">

        <span class="pill">
            AI SHOPPING ASSISTANT
        </span>

        <h1>
            Discover your style.<br>
            Find your product.<br>
            Shop with NOVA. ✨
        </h1>

        <p>
            Ask naturally about products, prices,
            categories, budgets and styling.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.markdown(
    '<div class="title">Try NOVA</div>',
    unsafe_allow_html=True
)

quick_questions = [

    "💰 Cheapest product",

    "💄 Cheapest makeup",

    "🧴 Skincare under ₹800",

    "👔 Men's fashion under ₹1500",

    "👗 Wedding outfit",

    "⭐ Best rated product"
]

quick_cols = st.columns(6)

for i, text in enumerate(
    quick_questions
):

    with quick_cols[i]:

        if st.button(
            text,
            key=f"quick_{i}",
            use_container_width=True
        ):

            question = text.split(
                " ",
                1
            )[1]

            selected = recommend_products(
                question
            )

            answer = ask_gemini(
                question,
                selected
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                    "products": []
                }
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "products": [
                        p["id"]
                        for p in selected
                    ]
                }
            )

            st.rerun()


# ============================================================
# CHAT HEADER
# ============================================================

st.markdown(
    """
    <div class="ai">

        <div class="title" style="margin:0">
            ✨ NOVA AI Assistant
        </div>

        <p>
            Ask anything about our fashion,
            beauty and lifestyle catalog.
        </p>

        <p>
            Example:
            <b>
            "Show me the cheapest makeup product under ₹700"
            </b>
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            products = [
                get_product(pid)
                for pid in message.get(
                    "products",
                    []
                )
            ]

            products = [
                p for p in products
                if p
            ]

            show_chat_products(
                products
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask NOVA anything..."
)


if question:

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "products": []
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    # --------------------------------------------------------
    # PRODUCT ENGINE
    # --------------------------------------------------------

    selected_products = recommend_products(
        question
    )

    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "NOVA is thinking..."
        ):

            answer = ask_gemini(
                question,
                selected_products
            )

        st.markdown(
            answer
        )

        show_chat_products(
            selected_products
        )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "products": [
                p["id"]
                for p in selected_products
            ]
        }
    )


# ============================================================
# EXPLORE PRODUCTS
# ============================================================

st.markdown(
    '<div class="title">✨ Explore 50 Products</div>',
    unsafe_allow_html=True
)

categories = [
    "All",
    "Women",
    "Men",
    "Beauty",
    "Accessories",
    "Footwear"
]

category = st.radio(
    "Category",
    categories,
    horizontal=True,
    label_visibility="collapsed"
)

if category == "All":

    items = PRODUCTS

else:

    items = [
        p for p in PRODUCTS
        if p["cat"] == category
    ]


# ============================================================
# PRODUCT GRID
# ============================================================

for start in range(
    0,
    len(items),
    4
):

    cols = st.columns(4)

    for column, product in zip(
        cols,
        items[start:start + 4]
    ):

        with column:

            discount = round(
                (
                    (
                        product["old"]
                        - product["price"]
                    )
                    / product["old"]
                )
                * 100
            )

            st.markdown(
                f"""
                <div class="card">

                    <img
                        src="{product['image']}"
                    >

                    <div class="body">

                        <div class="name">
                            {product['name']}
                        </div>

                        <div class="type">
                            {product['cat']} •
                            {product['type']}
                        </div>

                        <div class="price">

                            ₹{product['price']:,}

                            <span class="old">
                                ₹{product['old']:,}
                            </span>

                            <span style="
                                color:#087f5b;
                                font-size:12px
                            ">
                                {discount}% OFF
                            </span>

                        </div>

                        <div class="rate">
                            ★ {product['rating']}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(
                    "🛍 Add",
                    key=f"grid_add_{product['id']}",
                    use_container_width=True
                ):

                    if product["id"] not in st.session_state.cart:

                        st.session_state.cart.append(
                            product["id"]
                        )

                    st.toast(
                        f"{product['name']} added!"
                    )

            with c2:

                heart = (
                    "❤️"
                    if product["id"]
                    in st.session_state.wish
                    else "♡"
                )

                if st.button(
                    heart,
                    key=f"grid_wish_{product['id']}",
                    use_container_width=True
                ):

                    if product["id"] in st.session_state.wish:

                        st.session_state.wish.remove(
                            product["id"]
                        )

                    else:

                        st.session_state.wish.append(
                            product["id"]
                        )

                    st.rerun()


# ============================================================
# SHOPPING SPACE
# ============================================================

st.markdown(
    '<div class="title">🛍 Shopping Space</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)


# ============================================================
# CART
# ============================================================

with left:

    st.subheader(
        "🛒 Your Cart"
    )

    cart = [
        get_product(pid)
        for pid in st.session_state.cart
    ]

    cart = [
        p for p in cart
        if p
    ]

    if cart:

        for product in cart:

            st.write(
                f"**{product['name']}** — "
                f"₹{product['price']:,}"
            )

        total = sum(
            p["price"]
            for p in cart
        )

        st.success(
            f"Total: ₹{total:,}"
        )

    else:

        st.info(
            "Your cart is empty."
        )


# ============================================================
# WISHLIST
# ============================================================

with right:

    st.subheader(
        "❤️ Wishlist"
    )

    wishlist = [
        get_product(pid)
        for pid in st.session_state.wish
    ]

    wishlist = [
        p for p in wishlist
        if p
    ]

    if wishlist:

        for product in wishlist:

            st.write(
                f"**{product['name']}** — "
                f"₹{product['price']:,}"
            )

    else:

        st.info(
            "Your wishlist is empty."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:45px;
        background:#171717;
        color:white;
        padding:28px;
        border-radius:18px;
        text-align:center
    ">

        <div style="
            font:700 28px 'Playfair Display'
        ">
            NOVA<span style="color:#ff72ad">
                AI
            </span>
        </div>

        <div style="
            color:#bbb;
            margin-top:5px
        ">
            AI Fashion • AI Beauty • Smart Shopping
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
```
