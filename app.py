```python
import streamlit as st
import random
from typing import List, Dict

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# OPTIONAL GEMINI AI
# ============================================================

try:
    from google import genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def get_gemini_client():
    """Create Gemini client only when an API key is available."""

    if not GEMINI_AVAILABLE:
        return None

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            return None

        return genai.Client(api_key=api_key)

    except Exception:
        return None


# ============================================================
# PRODUCT DATA
# ============================================================

PRODUCTS = [
    {
        "id": 1,
        "name": "Floral Printed Kurta Set",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 1499,
        "old_price": 2499,
        "rating": 4.5,
        "reviews": 1280,
        "image": "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=700",
        "badge": "BESTSELLER",
        "description": "Elegant floral kurta set perfect for festive and casual occasions.",
    },
    {
        "id": 2,
        "name": "Pastel Oversized Shirt",
        "category": "Women",
        "type": "Western Wear",
        "price": 899,
        "old_price": 1599,
        "rating": 4.3,
        "reviews": 840,
        "image": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=700",
        "badge": "TRENDING",
        "description": "Relaxed oversized shirt in a soft pastel shade.",
    },
    {
        "id": 3,
        "name": "Classic Men's Casual Shirt",
        "category": "Men",
        "type": "Western Wear",
        "price": 999,
        "old_price": 1799,
        "rating": 4.4,
        "reviews": 960,
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=700",
        "badge": "HOT",
        "description": "Smart casual shirt for everyday styling.",
    },
    {
        "id": 4,
        "name": "Minimal Gold Necklace",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 699,
        "old_price": 1199,
        "rating": 4.6,
        "reviews": 540,
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=700",
        "badge": "NEW",
        "description": "Minimal necklace designed for everyday elegance.",
    },
    {
        "id": 5,
        "name": "Hydrating Glow Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 799,
        "old_price": 1299,
        "rating": 4.7,
        "reviews": 2150,
        "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700",
        "badge": "TOP RATED",
        "description": "Lightweight hydrating serum for a fresh-looking glow.",
    },
    {
        "id": 6,
        "name": "Velvet Matte Lipstick",
        "category": "Beauty",
        "type": "Makeup",
        "price": 599,
        "old_price": 899,
        "rating": 4.5,
        "reviews": 1760,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=700",
        "badge": "TRENDING",
        "description": "Smooth matte lipstick with rich colour payoff.",
    },
    {
        "id": 7,
        "name": "Everyday Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 1299,
        "old_price": 2199,
        "rating": 4.4,
        "reviews": 1120,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700",
        "badge": "POPULAR",
        "description": "Comfortable everyday sneakers for casual outfits.",
    },
    {
        "id": 8,
        "name": "Structured Women's Handbag",
        "category": "Accessories",
        "type": "Bags",
        "price": 1199,
        "old_price": 1999,
        "rating": 4.6,
        "reviews": 730,
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700",
        "badge": "EDITOR'S PICK",
        "description": "Elegant structured handbag for office and casual looks.",
    },
    {
        "id": 9,
        "name": "Floral Eau De Parfum",
        "category": "Beauty",
        "type": "Fragrance",
        "price": 999,
        "old_price": 1599,
        "rating": 4.4,
        "reviews": 630,
        "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=700",
        "badge": "NEW",
        "description": "Soft floral fragrance designed for everyday wear.",
    },
    {
        "id": 10,
        "name": "Relaxed Fit Denim Jeans",
        "category": "Men",
        "type": "Jeans",
        "price": 1299,
        "old_price": 2299,
        "rating": 4.3,
        "reviews": 890,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=700",
        "badge": "BESTSELLER",
        "description": "Relaxed-fit denim for effortless everyday styling.",
    },
    {
        "id": 11,
        "name": "Soft Blush Makeup Palette",
        "category": "Beauty",
        "type": "Makeup",
        "price": 899,
        "old_price": 1399,
        "rating": 4.6,
        "reviews": 1440,
        "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=700",
        "badge": "TOP RATED",
        "description": "Versatile shades for natural and party makeup looks.",
    },
    {
        "id": 12,
        "name": "Classic Analog Watch",
        "category": "Accessories",
        "type": "Watches",
        "price": 1499,
        "old_price": 2499,
        "rating": 4.5,
        "reviews": 580,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700",
        "badge": "TRENDING",
        "description": "Minimal classic watch suitable for everyday styling.",
    },
]


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm NOVA ✨ Your personal fashion & beauty assistant. "
                "Tell me what you're looking for and I'll help you find the right style."
            ),
        }
    ]


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f7f7f8;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main container */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Brand */
.nova-brand {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 700;
    letter-spacing: -1px;
}

.nova-brand span {
    color: #d63384;
}

/* Header */
.top-header {
    background: white;
    padding: 18px 24px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Hero */
.hero {
    background: linear-gradient(
        120deg,
        #fff0f6,
        #f7f0ff,
        #fff8ef
    );
    border-radius: 24px;
    padding: 38px;
    margin-bottom: 26px;
    min-height: 260px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 46px;
    font-weight: 700;
    line-height: 1.1;
    color: #171717;
}

.hero-subtitle {
    color: #666;
    font-size: 17px;
    margin-top: 12px;
}

.hero-pill {
    display: inline-block;
    background: #171717;
    color: white;
    padding: 7px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Section */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 29px;
    font-weight: 700;
    margin: 28px 0 15px;
}

/* Product card */
.product-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #eeeeee;
    transition: all .2s ease;
    margin-bottom: 10px;
}

.product-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,.10);
}

.product-image {
    width: 100%;
    height: 265px;
    object-fit: cover;
}

.product-body {
    padding: 14px;
}

.product-name {
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 6px;
}

.product-type {
    color: #888;
    font-size: 12px;
}

.product-price {
    font-size: 19px;
    font-weight: 700;
    margin-top: 8px;
}

.old-price {
    color: #999;
    text-decoration: line-through;
    font-size: 13px;
    margin-left: 5px;
}

.discount {
    color: #00875a;
    font-size: 12px;
    font-weight: 600;
    margin-left: 5px;
}

.rating {
    display: inline-block;
    background: #00875a;
    color: white;
    border-radius: 5px;
    padding: 3px 6px;
    font-size: 11px;
    margin-top: 7px;
}

/* Badge */
.badge {
    position: absolute;
    margin: 10px;
    background: #171717;
    color: white;
    padding: 5px 9px;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
}

/* AI box */
.ai-box {
    background: linear-gradient(135deg, #fff0f7, #f7efff);
    border: 1px solid #f0d8e8;
    border-radius: 22px;
    padding: 25px;
    margin-top: 10px;
}

.ai-title {
    font-family: 'Playfair Display', serif;
    font-size: 27px;
    font-weight: 700;
}

/* Category */
.category-card {
    background: white;
    border: 1px solid #eee;
    border-radius: 15px;
    padding: 18px 10px;
    text-align: center;
}

/* Cart */
.cart-box {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #eee;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    font-weight: 600;
    border: 1px solid #e2e2e2;
    min-height: 40px;
}

.stButton > button:hover {
    border-color: #d63384;
    color: #d63384;
}

/* Chat */
[data-testid="stChatMessage"] {
    border-radius: 15px;
}

/* Footer */
.nova-footer {
    margin-top: 50px;
    background: #171717;
    color: white;
    border-radius: 20px;
    padding: 35px;
    text-align: center;
}

.small-muted {
    color: #888;
    font-size: 12px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def discount_percent(product):
    return round(
        ((product["old_price"] - product["price"]) / product["old_price"]) * 100
    )


def add_to_cart(product):
    if product["id"] not in st.session_state.cart:
        st.session_state.cart.append(product["id"])


def toggle_wishlist(product):
    if product["id"] in st.session_state.wishlist:
        st.session_state.wishlist.remove(product["id"])
    else:
        st.session_state.wishlist.append(product["id"])


def get_product(product_id):
    return next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None,
    )


def search_products(query):
    if not query:
        return PRODUCTS

    query = query.lower()

    return [
        p
        for p in PRODUCTS
        if query in p["name"].lower()
        or query in p["category"].lower()
        or query in p["type"].lower()
        or query in p["description"].lower()
    ]


def product_context():
    return "\n".join(
        [
            f"{p['name']} | Category: {p['category']} | "
            f"Type: {p['type']} | Price: ₹{p['price']} | "
            f"Rating: {p['rating']}"
            for p in PRODUCTS
        ]
    )


# ============================================================
# AI RESPONSE
# ============================================================

def generate_ai_response(user_message):

    client = get_gemini_client()

    # --------------------------------------------------------
    # GEMINI
    # --------------------------------------------------------

    if client:

        prompt = f"""
You are NOVA, a sophisticated fashion and beauty shopping assistant.

Your job is to help customers discover products, create outfits,
suggest beauty products and answer shopping questions.

Available products:

{product_context()}

Customer:
{user_message}

Rules:
- Be friendly and concise.
- Use Indian Rupees.
- Recommend products from the available catalog when appropriate.
- Do not invent product names that are not in the catalog.
- For outfit requests, combine products logically.
- Ask a short follow-up question if the request is unclear.
- Do not make medical diagnoses.
- For skincare concerns, provide general cosmetic guidance and recommend
  consulting a qualified professional for medical concerns.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return response.text

        except Exception:
            pass

    # --------------------------------------------------------
    # FALLBACK RESPONSE
    # --------------------------------------------------------

    text = user_message.lower()

    if "wedding" in text or "party" in text:

        recommendations = [
            p
            for p in PRODUCTS
            if p["category"] in ["Women", "Accessories", "Beauty"]
        ][:4]

        names = ", ".join(p["name"] for p in recommendations)

        return (
            "✨ For a wedding or party look, I'd suggest building the look "
            f"around these pieces: {names}. "
            "For a more traditional look, choose ethnic wear with minimal "
            "gold jewellery. For a modern look, try a statement outfit with "
            "soft glam makeup."
        )

    if "skincare" in text or "skin" in text:

        return (
            "🧴 For a simple beauty routine, start with a gentle cleanser, "
            "hydrating product and sunscreen during the day. "
            "From our catalog, the **Hydrating Glow Serum** is a popular "
            "choice. If you tell me your skin type and budget, I can narrow "
            "down the suggestions."
        )

    if "makeup" in text:

        return (
            "💄 For an everyday makeup look, try a soft base, blush, "
            "defined brows and a comfortable lip colour. "
            "Our **Velvet Matte Lipstick** and **Soft Blush Makeup Palette** "
            "are good options from the catalog."
        )

    if "men" in text:

        return (
            "👔 For men's fashion, you can explore our casual shirts, "
            "denim and sneakers. Tell me the occasion and your budget, "
            "and I'll create a complete outfit."
        )

    if "under" in text or "budget" in text:

        return (
            "💰 Absolutely! Tell me your budget, for example "
            "\"outfit under ₹2000\" or \"beauty products under ₹1000\", "
            "and I'll suggest suitable products."
        )

    return (
        "✨ I can help with fashion, beauty, skincare, makeup, outfits, "
        "accessories and budget-based shopping. Try asking me something like "
        "\"Suggest a wedding outfit under ₹3000\"."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="top-header">
    <div class="nova-brand">
        NOVA<span>AI</span>
    </div>
    <div style="color:#777; margin-top:3px;">
        Fashion • Beauty • Lifestyle
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SEARCH
# ============================================================

search = st.text_input(
    "Search",
    placeholder="Search for dresses, makeup, skincare, shoes, bags...",
    label_visibility="collapsed",
)

st.session_state.search_query = search


# ============================================================
# NAVIGATION
# ============================================================

categories = [
    "All",
    "Women",
    "Men",
    "Beauty",
    "Accessories",
    "Footwear",
]

cols = st.columns(len(categories))

for i, category in enumerate(categories):

    with cols[i]:

        if st.button(
            category,
            key=f"cat_{category}",
            use_container_width=True,
        ):
            st.session_state.selected_category = category
            st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

    <div class="hero-pill">NOVA AI STYLE STUDIO</div>

    <div class="hero-title">
        Your style.<br>
        Your beauty.<br>
        Your NOVA. ✨
    </div>

    <div class="hero-subtitle">
        Discover fashion, beauty and lifestyle products curated
        around your personal style.
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# QUICK CATEGORY BUTTONS
# ============================================================

st.markdown(
    '<div class="section-title">Shop by Category</div>',
    unsafe_allow_html=True,
)

quick_categories = [
    ("👗", "Fashion", "Women"),
    ("👔", "Men", "Men"),
    ("💄", "Makeup", "Beauty"),
    ("🧴", "Skincare", "Beauty"),
    ("👜", "Accessories", "Accessories"),
    ("👟", "Footwear", "Footwear"),
]

qcols = st.columns(6)

for i, (emoji, label, value) in enumerate(quick_categories):

    with qcols[i]:

        st.markdown(
            f"""
            <div class="category-card">
                <div style="font-size:30px">{emoji}</div>
                <b>{label}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"Explore {label}",
            key=f"quick_{label}",
            use_container_width=True,
        ):
            st.session_state.selected_category = value
            st.rerun()


# ============================================================
# FILTER PRODUCTS
# ============================================================

selected = st.session_state.selected_category

if selected == "All":
    filtered_products = PRODUCTS
else:
    filtered_products = [
        p for p in PRODUCTS
        if p["category"] == selected
    ]

if search:
    filtered_products = search_products(search)


# ============================================================
# PRODUCT SECTION
# ============================================================

st.markdown(
    f'<div class="section-title">Trending Now ✨</div>',
    unsafe_allow_html=True,
)

st.caption(
    f"{len(filtered_products)} products available"
)


# ============================================================
# PRODUCT GRID
# ============================================================

for row_start in range(0, len(filtered_products), 4):

    row_products = filtered_products[row_start:row_start + 4]

    cols = st.columns(4)

    for col, product in zip(cols, row_products):

        with col:

            st.markdown(
                f"""
                <div class="product-card">

                    <div style="position:relative;">
                        <div class="badge">
                            {product["badge"]}
                        </div>

                        <img
                            src="{product["image"]}"
                            class="product-image"
                        />
                    </div>

                    <div class="product-body">

                        <div class="product-name">
                            {product["name"]}
                        </div>

                        <div class="product-type">
                            {product["type"]}
                        </div>

                        <div class="product-price">
                            ₹{product["price"]}
                            <span class="old-price">
                                ₹{product["old_price"]}
                            </span>

                            <span class="discount">
                                {discount_percent(product)}% OFF
                            </span>
                        </div>

                        <div class="rating">
                            ★ {product["rating"]}
                        </div>

                        <span class="small-muted">
                            ({product["reviews"]:,} reviews)
                        </span>

                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(
                    "🛍 Add",
                    key=f"cart_{product['id']}",
                    use_container_width=True,
                ):

                    add_to_cart(product)
                    st.toast(
                        f"{product['name']} added to cart"
                    )

            with c2:

                heart = (
                    "❤️"
                    if product["id"]
                    in st.session_state.wishlist
                    else "♡"
                )

                if st.button(
                    heart,
                    key=f"wish_{product['id']}",
                    use_container_width=True,
                ):

                    toggle_wishlist(product)
                    st.rerun()


# ============================================================
# AI STYLE ASSISTANT
# ============================================================

st.markdown(
    """
<div class="ai-box">

<div class="ai-title">
✨ Ask NOVA — Your AI Stylist
</div>

<p style="color:#666;">
Get personalized fashion and beauty recommendations.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# Display messages

for message in st.session_state.chat_messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input(
    "Ask NOVA: e.g. Suggest a wedding outfit under ₹3000..."
)

if prompt:

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("NOVA is styling your look... ✨"):

            answer = generate_ai_response(prompt)

        st.markdown(answer)

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# ============================================================
# CART + WISHLIST
# ============================================================

st.markdown(
    '<div class="section-title">Your Shopping Space</div>',
    unsafe_allow_html=True,
)

cart_products = [
    get_product(product_id)
    for product_id in st.session_state.cart
]

wishlist_products = [
    get_product(product_id)
    for product_id in st.session_state.wishlist
]

c1, c2 = st.columns(2)

with c1:

    st.markdown(
        '<div class="cart-box"><h3>🛍 Your Cart</h3>',
        unsafe_allow_html=True,
    )

    if not cart_products:

        st.info("Your cart is empty.")

    else:

        total = 0

        for p in cart_products:

            total += p["price"]

            st.write(
                f"**{p['name']}** — ₹{p['price']}"
            )

        st.divider()

        st.markdown(
            f"### Total: ₹{total:,}"
        )

with c2:

    st.markdown(
        '<div class="cart-box"><h3>❤️ Wishlist</h3>',
        unsafe_allow_html=True,
    )

    if not wishlist_products:

        st.info("Your wishlist is empty.")

    else:

        for p in wishlist_products:

            st.write(
                f"**{p['name']}** — ₹{p['price']}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="nova-footer">

    <div style="font-family:'Playfair Display';font-size:30px;">
        NOVA<span style="color:#ff72ad;">AI</span>
    </div>

    <p>
        Fashion • Beauty • Lifestyle • AI Styling
    </p>

    <div style="color:#aaa;font-size:13px;">
        AI-powered shopping experience
    </div>

</div>
""",
    unsafe_allow_html=True,
)
```
