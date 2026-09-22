import streamlit as st
from google import genai

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
# GEMINI AI
# ============================================================

def get_gemini_client():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            return None

        return genai.Client(api_key=api_key)

    except Exception:
        return None


# ============================================================
# PRODUCT CATALOG
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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm **NOVA AI** ✨\n\n"
                "Your personal Fashion & Beauty Assistant.\n\n"
                "Ask me about outfits, makeup, skincare, accessories, "
                "shopping budgets or product recommendations."
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

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Header */

.top-header {
    background: white;
    padding: 20px 25px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.nova-brand {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 700;
}

.nova-brand span {
    color: #d63384;
}

.brand-subtitle {
    color: #777;
    margin-top: 3px;
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
    margin-bottom: 28px;
}

.hero-pill {
    display: inline-block;
    background: #171717;
    color: white;
    padding: 7px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 45px;
    font-weight: 700;
    line-height: 1.1;
    margin-top: 15px;
}

.hero-subtitle {
    color: #666;
    font-size: 17px;
    margin-top: 12px;
}

/* Section */

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 29px;
    font-weight: 700;
    margin: 28px 0 15px;
}

/* Product */

.product-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #eeeeee;
    margin-bottom: 10px;
}

.product-image {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

.product-body {
    padding: 14px;
}

.product-name {
    font-weight: 600;
    font-size: 15px;
}

.product-type {
    color: #888;
    font-size: 12px;
    margin-top: 4px;
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
    margin-left: 5px;
}

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

.rating {
    display: inline-block;
    background: #00875a;
    color: white;
    border-radius: 5px;
    padding: 3px 6px;
    font-size: 11px;
    margin-top: 7px;
}

/* AI */

.ai-box {
    background: linear-gradient(135deg, #fff0f7, #f7efff);
    border: 1px solid #f0d8e8;
    border-radius: 22px;
    padding: 25px;
    margin-top: 35px;
}

.ai-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
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
    padding: 20px;
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

/* Footer */

.nova-footer {
    margin-top: 50px;
    background: #171717;
    color: white;
    border-radius: 20px;
    padding: 35px;
    text-align: center;
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
        ((product["old_price"] - product["price"])
         / product["old_price"]) * 100
    )


def add_to_cart(product_id):
    if product_id not in st.session_state.cart:
        st.session_state.cart.append(product_id)


def toggle_wishlist(product_id):
    if product_id in st.session_state.wishlist:
        st.session_state.wishlist.remove(product_id)
    else:
        st.session_state.wishlist.append(product_id)


def get_product(product_id):
    return next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None
    )


def product_context():
    return "\n".join(
        [
            f"""
Product: {p['name']}
Category: {p['category']}
Type: {p['type']}
Price: ₹{p['price']}
Rating: {p['rating']}
Description: {p['description']}
"""
            for p in PRODUCTS
        ]
    )


# ============================================================
# AI RESPONSE
# ============================================================

def generate_ai_response(user_message):

    client = get_gemini_client()

    if client:

        prompt = f"""
You are NOVA AI, a professional Fashion & Beauty shopping assistant.

You help customers with:

- Fashion
- Women's fashion
- Men's fashion
- Makeup
- Skincare
- Haircare
- Accessories
- Shoes
- Bags
- Fragrance
- Outfit styling
- Occasion-based styling
- Budget shopping
- Product recommendations

PRODUCT CATALOG:

{product_context()}

CUSTOMER MESSAGE:

{user_message}

RULES:

1. Be friendly, stylish and concise.
2. Use Indian Rupees (₹).
3. Recommend products from the catalog when relevant.
4. Never invent products that are not in the catalog.
5. If the user gives a budget, respect it.
6. If the user asks for an outfit, combine suitable products.
7. If the request is unclear, ask one short follow-up question.
8. Give practical fashion and beauty suggestions.
9. Do not provide medical diagnoses.
10. For medical skin/hair problems, suggest consulting a qualified professional.
11. Use emojis naturally but don't overuse them.
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

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    text = user_message.lower()

    if "wedding" in text or "party" in text:

        return """
✨ **Wedding / Party Look**

For a stylish look, I recommend:

👗 Floral Printed Kurta Set  
💎 Minimal Gold Necklace  
💄 Soft Blush Makeup Palette  
🌸 Floral Eau De Parfum

Tell me your **budget** and whether you want a **traditional or modern look**.
"""

    if "makeup" in text:

        return """
💄 **Makeup Recommendation**

For an everyday soft-glam look:

• Soft Blush Makeup Palette
• Velvet Matte Lipstick
• Keep the base light and natural

Tell me your budget and the occasion, and I'll create a complete makeup look.
"""

    if "skin" in text or "skincare" in text:

        return """
🧴 **Skincare Recommendation**

For a simple routine:

1. Gentle cleanser
2. Hydrating product
3. Sunscreen during the day

Our catalog includes **Hydrating Glow Serum — ₹799**.

Tell me your skin type and budget for a more specific recommendation.
"""

    if "men" in text or "mens" in text:

        return """
👔 **Men's Fashion**

You can build a casual look with:

• Classic Men's Casual Shirt — ₹999
• Relaxed Fit Denim Jeans — ₹1,299
• Everyday Sneakers — ₹1,299

Tell me the occasion and your budget and I'll create a complete outfit.
"""

    if "under" in text or "budget" in text:

        return """
💰 **Budget Shopping**

Absolutely! Tell me something like:

• "Fashion under ₹2000"
• "Makeup under ₹1000"
• "Wedding outfit under ₹3000"
• "Men's outfit under ₹2500"

I'll suggest products from our catalog.
"""

    return """
✨ I can help you with:

👗 Fashion & outfits  
💄 Makeup  
🧴 Skincare  
💇 Beauty  
👜 Accessories  
👟 Footwear  
💰 Budget shopping  
🎉 Occasion styling  

Try asking:

**"Suggest a wedding outfit under ₹3000"**
"""


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="top-header">

<div class="nova-brand">
NOVA<span>AI</span>
</div>

<div class="brand-subtitle">
Fashion • Beauty • Lifestyle • AI Styling
</div>

</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

<div class="hero-pill">
NOVA AI STYLE STUDIO
</div>

<div class="hero-title">
Your style.<br>
Your beauty.<br>
Your NOVA. ✨
</div>

<div class="hero-subtitle">
Your personal AI assistant for fashion, beauty and shopping.
</div>

</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# QUICK CHAT PROMPTS
# ============================================================

st.markdown(
    '<div class="section-title">What can NOVA help with?</div>',
    unsafe_allow_html=True,
)

quick_prompts = [
    "👗 Wedding outfit",
    "💄 Makeup",
    "🧴 Skincare",
    "👔 Men's fashion",
    "👜 Accessories",
    "💰 Budget shopping",
]

prompt_cols = st.columns(6)

for i, prompt_text in enumerate(quick_prompts):

    with prompt_cols[i]:

        if st.button(
            prompt_text,
            key=f"quick_prompt_{i}",
            use_container_width=True,
        ):
            clean_prompt = prompt_text.split(" ", 1)[1]

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": clean_prompt,
                }
            )

            answer = generate_ai_response(clean_prompt)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()

# ============================================================
# AI CHAT
# ============================================================

st.markdown(
    """
<div class="ai-box">

<div class="ai-title">
✨ Ask NOVA — Your AI Fashion & Beauty Assistant
</div>

<p style="color:#666;">
Chat with NOVA for personalized fashion, beauty and shopping recommendations.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# Display chat history

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_prompt = st.chat_input(
    "Ask NOVA... e.g. Suggest a wedding outfit under ₹3000"
)

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("NOVA is styling your look... ✨"):

            answer = generate_ai_response(user_prompt)

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

# ============================================================
# PRODUCT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">✨ Explore Products</div>',
    unsafe_allow_html=True,
)

categories = [
    "All",
    "Women",
    "Men",
    "Beauty",
    "Accessories",
    "Footwear",
]

category_cols = st.columns(len(categories))

for i, category in enumerate(categories):

    with category_cols[i]:

        if st.button(
            category,
            key=f"category_{category}",
            use_container_width=True,
        ):
            st.session_state.selected_category = category
            st.rerun()


selected_category = st.session_state.selected_category

if selected_category == "All":

    filtered_products = PRODUCTS

else:

    filtered_products = [
        p for p in PRODUCTS
        if p["category"] == selected_category
    ]

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

<span style="color:#888;font-size:12px;">
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
                    key=f"add_{product['id']}",
                    use_container_width=True,
                ):

                    add_to_cart(product["id"])

                    st.toast(
                        f"{product['name']} added to cart"
                    )

            with c2:

                is_wishlisted = (
                    product["id"]
                    in st.session_state.wishlist
                )

                heart = "❤️" if is_wishlisted else "♡"

                if st.button(
                    heart,
                    key=f"wish_{product['id']}",
                    use_container_width=True,
                ):

                    toggle_wishlist(product["id"])
                    st.rerun()

# ============================================================
# CART + WISHLIST
# ============================================================

st.markdown(
    '<div class="section-title">🛍 Your Shopping Space</div>',
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

cart_col, wish_col = st.columns(2)

# CART

with cart_col:

    st.markdown(
        '<div class="cart-box"><h3>🛍 Your Cart</h3>',
        unsafe_allow_html=True,
    )

    if not cart_products:

        st.info("Your cart is empty.")

    else:

        total = 0

        for product in cart_products:

            total += product["price"]

            st.write(
                f"**{product['name']}** — ₹{product['price']}"
            )

        st.divider()

        st.markdown(
            f"### Total: ₹{total:,}"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# WISHLIST

with wish_col:

    st.markdown(
        '<div class="cart-box"><h3>❤️ Wishlist</h3>',
        unsafe_allow_html=True,
    )

    if not wishlist_products:

        st.info("Your wishlist is empty.")

    else:

        for product in wishlist_products:

            st.write(
                f"**{product['name']}** — ₹{product['price']}"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="nova-footer">

<div style="
font-family:'Playfair Display';
font-size:30px;
font-weight:700;
">
NOVA<span style="color:#ff72ad;">AI</span>
</div>

<p>
Fashion • Beauty • Lifestyle • AI Styling
</p>

<div style="color:#aaa;font-size:13px;">
AI-powered fashion and beauty assistant
</div>

</div>
""",
    unsafe_allow_html=True,
)
