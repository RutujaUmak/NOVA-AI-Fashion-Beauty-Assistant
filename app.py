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
    .stApp {
        background: #f7f7f8;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .pink {
        color: #d63384;
    }

    .hero-box {
        padding: 28px;
        border-radius: 22px;
        background: linear-gradient(135deg, #fff0f6, #f3efff, #fff8ed);
        margin: 12px 0 22px 0;
        border: 1px solid #f0dce8;
    }

    .product-name {
        font-weight: 700;
        font-size: 16px;
        min-height: 44px;
    }

    .muted {
        color: #777;
        font-size: 13px;
    }

    .price {
        font-size: 20px;
        font-weight: 800;
    }

    .old-price {
        color: #999;
        text-decoration: line-through;
        font-size: 13px;
        margin-left: 6px;
    }

    .rating {
        color: #087f5b;
        font-weight: 600;
        font-size: 13px;
    }

    .footer-note {
        text-align: center;
        color: #777;
        padding: 28px 0 10px 0;
    }

    [data-testid="stChatInput"] textarea {
        color: white !important;
        background: #272932 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #dddddd !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm **NOVA AI** ✨\n\n"
                "Ask me about fashion, beauty, footwear, "
                "accessories, prices, budgets or styling."
            ),
            "products": [],
        }
    ]

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []


# ============================================================
# HELPERS
# ============================================================

def get_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def extract_budget(text):
    patterns = [
        r"(?:under|below|within|upto|up to)\s*(?:₹|rs\.?|inr)?\s*(\d[\d,]*)",
        r"(?:₹|rs\.?|inr)\s*(\d[\d,]*)",
        r"budget\s*(?:of)?\s*(?:₹|rs\.?|inr)?\s*(\d[\d,]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1).replace(",", ""))

    return None


def detect_category(text):
    q = text.lower()

    if any(x in q for x in ["makeup", "lipstick", "mascara", "foundation", "cosmetic"]):
        return "Beauty"

    if any(x in q for x in ["skincare", "skin care", "serum", "moisturizer", "sunscreen", "toner"]):
        return "Beauty"

    if any(x in q for x in ["men", "mens", "male", "boy"]):
        return "Men"

    if any(x in q for x in ["women", "womens", "woman", "girl", "ladies"]):
        return "Women"

    if any(x in q for x in ["shoe", "shoes", "sneaker", "sneakers", "footwear", "heel", "heels", "sandals", "flats", "loafers"]):
        return "Footwear"

    if any(x in q for x in ["bag", "jewellery", "jewelry", "necklace", "watch", "wallet", "sunglasses", "accessory", "accessories", "belt", "bracelet", "earrings"]):
        return "Accessories"

    return None


def detect_type_keywords(text):
    q = text.lower()

    groups = {
        "Makeup": ["makeup", "lipstick", "mascara", "foundation", "lip gloss", "blush"],
        "Skincare": ["skincare", "skin care", "serum", "moisturizer", "sunscreen", "toner"],
        "Shoes": ["shoe", "shoes", "sneaker", "sneakers"],
        "Heels": ["heel", "heels"],
        "Sandals": ["sandal", "sandals"],
        "Jeans": ["jeans", "denim jeans"],
        "Jacket": ["jacket"],
        "Dress": ["dress"],
        "Shirt": ["shirt"],
        "T-Shirt": ["t-shirt", "tshirt", "t shirt"],
        "Bags": ["bag", "handbag"],
        "Jewellery": ["jewellery", "jewelry", "necklace", "earrings", "bracelet"],
        "Watch": ["watch"],
    }

    for product_type, words in groups.items():
        if any(word in q for word in words):
            return product_type

    return None


def recommend_products(question):
    q = question.lower()
    budget = extract_budget(question)
    category = detect_category(question)
    product_type = detect_type_keywords(question)

    candidates = PRODUCTS[:]

    if category:
        candidates = [p for p in candidates if p["category"] == category]

    if product_type:
        type_matches = [p for p in candidates if product_type.lower() in p["type"].lower()]
        if type_matches:
            candidates = type_matches

    if budget is not None:
        budget_matches = [p for p in candidates if p["price"] <= budget]
        if budget_matches:
            candidates = budget_matches
        else:
            return []

    cheapest_words = ["cheapest", "lowest price", "lowest priced", "least expensive", "most affordable", "cheaper"]
    highest_rating_words = ["best rated", "highest rated", "top rated", "highest rating"]

    if any(word in q for word in cheapest_words):
        return sorted(candidates, key=lambda p: (p["price"], -p["rating"]))[:4]

    if any(word in q for word in highest_rating_words):
        return sorted(candidates, key=lambda p: (-p["rating"], p["price"]))[:4]

    # Search by meaningful product words.
    words = re.findall(r"[a-zA-Z]+", q)
    stop_words = {
        "show", "me", "the", "a", "an", "for", "under", "below",
        "within", "please", "find", "want", "need", "give", "some",
        "product", "products", "best", "good", "can", "you", "something",
        "what", "is", "are", "with", "price", "cheap", "cheapest"
    }
    words = [w for w in words if len(w) >= 3 and w not in stop_words]

    scored = []
    for product in candidates:
        searchable = (
            f"{product['name']} {product['category']} {product['type']}"
        ).lower()
        score = sum(1 for word in words if word in searchable)
        scored.append((score, product))

    matches = [p for score, p in scored if score > 0]
    if matches:
        return sorted(matches, key=lambda p: (-next(
            score for score, item in scored if item["id"] == p["id"]
        ), p["price"]))[:4]

    return sorted(candidates, key=lambda p: (-p["rating"], p["price"]))[:4]


def catalog_for_ai():
    return "\n".join(
        f"ID {p['id']} | {p['name']} | {p['category']} | {p['type']} | ₹{p['price']} | rating {p['rating']}"
        for p in PRODUCTS
    )


def local_answer(question, products):
    q = question.lower()

    if not products:
        budget = extract_budget(question)
        if budget is not None:
            return (
                f"I couldn't find a matching product within ₹{budget:,}. "
                "Try increasing the budget or changing the category."
            )
        return "I couldn't find an exact match. Try asking for men's fashion, makeup, skincare, shoes, bags, or a budget."

    if any(x in q for x in ["cheapest", "lowest price", "lowest priced", "most affordable"]):
        p = min(products, key=lambda x: x["price"])
        return f"The cheapest matching option is **{p['name']}** at **₹{p['price']:,}**, rated **{p['rating']}★**."

    if any(x in q for x in ["best rated", "highest rated", "top rated"]):
        p = max(products, key=lambda x: x["rating"])
        return f"A top-rated matching option is **{p['name']}** at **₹{p['price']:,}**, rated **{p['rating']}★**."

    names = ", ".join(p["name"] for p in products[:3])
    return f"I found these options for you: **{names}**."


def ask_ai(question, products):
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key or genai is None:
        return local_answer(question, products)

    client = genai.Client(api_key=api_key)

    selected_text = "\n".join(
        f"- {p['name']} | {p['category']} | {p['type']} | ₹{p['price']} | {p['rating']}★"
        for p in products
    )

    history = []
    for msg in st.session_state.messages[-8:]:
        history.append(f"{msg['role']}: {msg['content']}")
    history_text = "\n".join(history)

    prompt = f"""
You are NOVA AI, a shopping assistant for a fashion and beauty store.

PRODUCT CATALOG:
{catalog_for_ai()}

PRODUCTS SELECTED BY THE PYTHON SEARCH ENGINE:
{selected_text}

RECENT CHAT:
{history_text}

CURRENT QUESTION:
{question}

Rules:
- Answer naturally and helpfully.
- Use only catalog products when recommending products.
- Never invent a product, price, rating, or discount.
- If the user asks a general question, answer it normally.
- If products are relevant, mention the product names and prices.
- For cheapest/lowest-price questions, trust the Python-selected products.
- Use Indian rupees.
- Do not output image URLs.
- Keep the answer concise.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        if response and response.text:
            return response.text
    except Exception:
        pass

    return local_answer(question, products)


def add_to_cart(product_id):
    if product_id not in st.session_state.cart:
        st.session_state.cart.append(product_id)


def toggle_wishlist(product_id):
    if product_id in st.session_state.wishlist:
        st.session_state.wishlist.remove(product_id)
    else:
        st.session_state.wishlist.append(product_id)


def display_product(product, prefix):
    st.image(product["image"], use_container_width=True)

    discount = round((1 - product["price"] / product["mrp"]) * 100)

    st.markdown(f"**{product['name']}**")
    st.caption(f"{product['category']} • {product['type']}")
    st.markdown(
        f"**₹{product['price']:,}**  ~~₹{product['mrp']:,}~~  • **{discount}% OFF**"
    )
    st.markdown(f"⭐ **{product['rating']}**")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("🛍 Add", key=f"{prefix}_add_{product['id']}", use_container_width=True):
            add_to_cart(product["id"])
            st.toast(f"{product['name']} added to cart.")

    with c2:
        icon = "❤️" if product["id"] in st.session_state.wishlist else "♡"
        if st.button(icon, key=f"{prefix}_wish_{product['id']}", use_container_width=True):
            toggle_wishlist(product["id"])
            st.rerun()


def display_products(products, prefix):
    if not products:
        return

    st.markdown("### 🛍 Recommended products")

    for start in range(0, len(products), 3):
        cols = st.columns(3)
        for col, product in zip(cols, products[start:start + 3]):
            with col:
                display_product(product, f"{prefix}_{start}")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("✨ NOVA AI")
    st.caption("Fashion • Beauty • Smart Shopping")

    st.divider()

    st.metric("Products", len(PRODUCTS))
    st.metric("Cart items", len(st.session_state.cart))
    st.metric("Wishlist", len(st.session_state.wishlist))

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. What would you like to find? ✨",
                "products": [],
            }
        ]
        st.rerun()

    st.info(
        "Tip: Ask questions like:\n\n"
        "• Cheapest makeup\n"
        "• Shoes under ₹1000\n"
        "• Men's fashion under ₹1500\n"
        "• Best rated skincare"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">NOVA<span class="pink">AI</span></div>',
    unsafe_allow_html=True,
)
st.caption("AI Fashion • AI Beauty • Lifestyle • Smart Shopping")

st.markdown(
    """
    <div class="hero-box">
        <h2>Discover your style. Find your product. Shop with NOVA. ✨</h2>
        <p>Ask naturally about products, prices, categories, budgets and styling.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# QUICK PROMPTS
# ============================================================

st.subheader("Try NOVA")

quick_questions = [
    "Show me the cheapest product",
    "Show me the cheapest makeup",
    "Skincare under ₹800",
    "Men's fashion under ₹1500",
    "Show me shoes under ₹1000",
    "Show me the best rated product",
]

quick_cols = st.columns(3)

for i, prompt in enumerate(quick_questions):
    with quick_cols[i % 3]:
        if st.button(prompt, key=f"quick_{i}", use_container_width=True):
            selected = recommend_products(prompt)
            answer = ask_ai(prompt, selected)

            st.session_state.messages.append(
                {"role": "user", "content": prompt, "products": []}
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "products": [p["id"] for p in selected],
                }
            )
            st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

st.subheader("💬 NOVA AI Assistant")

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        product_ids = message.get("products", [])
        if product_ids:
            products = [get_product(pid) for pid in product_ids]
            products = [p for p in products if p]
            display_products(products, f"history_{i}")


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input("Ask NOVA anything...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question, "products": []}
    )

    products = recommend_products(question)
    answer = ask_ai(question, products)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "products": [p["id"] for p in products],
        }
    )

    st.rerun()


# ============================================================
# PRODUCT EXPLORER
# ============================================================

st.divider()
st.subheader("✨ Explore 50 Products")

category = st.radio(
    "Choose category",
    ["All", "Women", "Men", "Beauty", "Accessories", "Footwear"],
    horizontal=True,
)

if category == "All":
    visible_products = PRODUCTS
else:
    visible_products = [p for p in PRODUCTS if p["category"] == category]

for start in range(0, len(visible_products), 4):
    cols = st.columns(4)

    for col, product in zip(cols, visible_products[start:start + 4]):
        with col:
            display_product(product, f"grid_{category}_{start}")


# ============================================================
# CART + WISHLIST
# ============================================================

st.divider()
st.subheader("🛍 Shopping Space")

cart_col, wish_col = st.columns(2)

with cart_col:
    st.markdown("### 🛒 Your Cart")

    cart_products = [get_product(pid) for pid in st.session_state.cart]
    cart_products = [p for p in cart_products if p]

    if not cart_products:
        st.info("Your cart is empty.")
    else:
        total = sum(p["price"] for p in cart_products)
        for p in cart_products:
            st.write(f"**{p['name']}** — ₹{p['price']:,}")
        st.success(f"Cart total: ₹{total:,}")

with wish_col:
    st.markdown("### ❤️ Wishlist")

    wish_products = [get_product(pid) for pid in st.session_state.wishlist]
    wish_products = [p for p in wish_products if p]

    if not wish_products:
        st.info("Your wishlist is empty.")
    else:
        for p in wish_products:
            st.write(f"**{p['name']}** — ₹{p['price']:,}")


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    "<div class='footer-note'>NOVA AI • 50 Products • Smart Recommendations • AI Shopping Assistant</div>",
    unsafe_allow_html=True,
)
