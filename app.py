import streamlit as st
import os
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NOVA | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


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
        "old": 2499,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 2,
        "name": "Pastel Oversized Shirt",
        "category": "Women",
        "type": "Shirt",
        "price": 899,
        "old": 1599,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 3,
        "name": "Women's Denim Jacket",
        "category": "Women",
        "type": "Jacket",
        "price": 1299,
        "old": 2199,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 4,
        "name": "Elegant Party Dress",
        "category": "Women",
        "type": "Dress",
        "price": 1899,
        "old": 2999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 5,
        "name": "Cotton Straight Kurta",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 799,
        "old": 1299,
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1583391733981-8498403d1f96?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 6,
        "name": "High Waist Blue Jeans",
        "category": "Women",
        "type": "Jeans",
        "price": 1199,
        "old": 1999,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 7,
        "name": "Floral Casual Top",
        "category": "Women",
        "type": "Top",
        "price": 699,
        "old": 1199,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 8,
        "name": "Elegant Anarkali Suit",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 2199,
        "old": 3499,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1610189012906-3c9c9f9e8d9d?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 9,
        "name": "Women's Black Blazer",
        "category": "Women",
        "type": "Formal Wear",
        "price": 1699,
        "old": 2599,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 10,
        "name": "Printed Summer Dress",
        "category": "Women",
        "type": "Dress",
        "price": 999,
        "old": 1699,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=85"
    },

    # MEN

    {
        "id": 11,
        "name": "Classic Men's Casual Shirt",
        "category": "Men",
        "type": "Shirt",
        "price": 999,
        "old": 1799,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 12,
        "name": "Relaxed Fit Denim Jeans",
        "category": "Men",
        "type": "Jeans",
        "price": 1299,
        "old": 2299,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 13,
        "name": "Men's Black T-Shirt",
        "category": "Men",
        "type": "T-Shirt",
        "price": 599,
        "old": 999,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 14,
        "name": "Men's Formal Shirt",
        "category": "Men",
        "type": "Formal Wear",
        "price": 899,
        "old": 1499,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1603252110481-7ba873bf42ab?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 15,
        "name": "Slim Fit Chinos",
        "category": "Men",
        "type": "Trousers",
        "price": 1199,
        "old": 1999,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 16,
        "name": "Men's Denim Jacket",
        "category": "Men",
        "type": "Jacket",
        "price": 1499,
        "old": 2499,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 17,
        "name": "Men's Polo T-Shirt",
        "category": "Men",
        "type": "T-Shirt",
        "price": 799,
        "old": 1299,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1586363104868-3a5e2ab60d99?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 18,
        "name": "Men's Casual Hoodie",
        "category": "Men",
        "type": "Hoodie",
        "price": 1099,
        "old": 1899,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=800&q=85"
    },

    # BEAUTY

    {
        "id": 19,
        "name": "Hydrating Glow Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 799,
        "old": 1299,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 20,
        "name": "Velvet Matte Lipstick",
        "category": "Beauty",
        "type": "Makeup",
        "price": 599,
        "old": 899,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 21,
        "name": "Vitamin C Face Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 699,
        "old": 1199,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 22,
        "name": "Daily Sunscreen SPF 50",
        "category": "Beauty",
        "type": "Skincare",
        "price": 599,
        "old": 899,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?auto=format&fit=crop&w=800&q=85"
    },

    # ACCESSORIES

    {
        "id": 23,
        "name": "Minimal Gold Necklace",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 699,
        "old": 1199,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 24,
        "name": "Structured Women's Handbag",
        "category": "Accessories",
        "type": "Bags",
        "price": 1199,
        "old": 1999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 25,
        "name": "Fashion Sunglasses",
        "category": "Accessories",
        "type": "Sunglasses",
        "price": 399,
        "old": 699,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=85"
    },

    # FOOTWEAR

    {
        "id": 26,
        "name": "Everyday Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 1299,
        "old": 2199,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 27,
        "name": "Women's Casual Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 999,
        "old": 1699,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=85"
    },

    {
        "id": 28,
        "name": "Men's Running Shoes",
        "category": "Footwear",
        "type": "Sports Shoes",
        "price": 1599,
        "old": 2599,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=800&q=85"
    },

]


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* GLOBAL */

    .stApp {
        background: #f8f8f8;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }


    /* NAVBAR */

    .navbar {
        background: white;
        padding: 16px 25px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 22px;
        border: 1px solid #eeeeee;
    }

    .brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .brand span {
        color: #e91e63;
    }

    .navtext {
        color: #666;
        font-size: 14px;
    }


    /* HERO */

    .hero {
        background:
        linear-gradient(
            90deg,
            rgba(20,20,20,.90),
            rgba(20,20,20,.35)
        ),
        url("https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1800&q=90");

        background-size: cover;
        background-position: center;

        min-height: 380px;

        border-radius: 25px;

        padding: 70px 60px;

        display: flex;
        align-items: center;

        color: white;

        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 48px;
        line-height: 1.05;
        margin-bottom: 15px;
    }

    .hero p {
        font-size: 17px;
        color: #eeeeee;
        max-width: 520px;
    }

    .hero-tag {
        display: inline-block;
        background: #e91e63;
        padding: 7px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin-bottom: 15px;
    }


    /* SECTION */

    .section-title {
        font-size: 26px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 15px;
    }


    /* CATEGORY */

    .category-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        border: 1px solid #eeeeee;
        transition: .2s;
    }

    .category-icon {
        font-size: 34px;
        margin-bottom: 8px;
    }

    .category-name {
        font-weight: 700;
    }

    .category-sub {
        font-size: 12px;
        color: #888;
    }


    /* PRODUCTS */

    .product-card {
        background: white;
        border-radius: 18px;
        padding: 10px;
        border: 1px solid #eeeeee;
        margin-bottom: 15px;
    }

    .product-image {
        width: 100%;
        height: 280px;
        object-fit: cover;
        border-radius: 14px;
    }

    .product-name {
        font-size: 15px;
        font-weight: 700;
        margin-top: 10px;
    }

    .product-type {
        font-size: 12px;
        color: #888;
    }

    .price {
        font-size: 18px;
        font-weight: 800;
        margin-top: 5px;
    }

    .old-price {
        color: #999;
        text-decoration: line-through;
        font-size: 12px;
        margin-left: 5px;
    }

    .rating {
        color: #087f5b;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ASSISTANT */

    .assistant-box {
        background: white;
        border: 1px solid #eeeeee;
        border-radius: 22px;
        padding: 30px;
        margin-top: 35px;
    }

    .assistant-title {
        font-size: 28px;
        font-weight: 800;
    }

    .assistant-sub {
        color: #777;
        margin-bottom: 20px;
    }


    /* FOOTER */

    .footer {
        text-align: center;
        color: #999;
        padding: 40px;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    """
    <div class="navbar">

        <div class="brand">
            NOVA<span>AI</span>
        </div>

        <div class="navtext">
            Women &nbsp;&nbsp; Men &nbsp;&nbsp; Beauty
            &nbsp;&nbsp; Accessories &nbsp;&nbsp; Footwear
        </div>

        <div class="navtext">
            🛍️ Cart
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div>

            <div class="hero-tag">
                NEW SEASON
            </div>

            <h1>
                Style that<br>
                feels like you.
            </h1>

            <p>
                Discover fashion, beauty and everyday
                essentials with NOVA.
            </p>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CATEGORY SECTION
# ============================================================

st.markdown(
    '<div class="section-title">Shop by Category</div>',
    unsafe_allow_html=True
)


categories = [
    ("👗", "Women", "Fashion & ethnic wear"),
    ("👔", "Men", "Everyday essentials"),
    ("💄", "Beauty", "Makeup & skincare"),
    ("👜", "Accessories", "Complete your look"),
    ("👟", "Footwear", "Shoes & sneakers"),
]


cols = st.columns(5)


for i, (icon, name, sub) in enumerate(categories):

    with cols[i]:

        st.markdown(
            f"""
            <div class="category-card">

                <div class="category-icon">
                    {icon}
                </div>

                <div class="category-name">
                    {name}
                </div>

                <div class="category-sub">
                    {sub}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FEATURED PRODUCTS
# ============================================================

st.markdown(
    '<div class="section-title">Trending Now</div>',
    unsafe_allow_html=True
)


featured = PRODUCTS[:8]


for start in range(
    0,
    len(featured),
    4
):

    row = featured[
        start:start + 4
    ]

    cols = st.columns(4)


    for i, product in enumerate(row):

        with cols[i]:

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )


            # IMPORTANT:
            # Direct URL image display

            try:

                st.image(
                    product["image"],
                    use_container_width=True
                )

            except Exception:

                st.info(
                    "Product image unavailable"
                )


            st.markdown(
                f"""
                <div class="product-name">
                    {product['name']}
                </div>

                <div class="product-type">
                    {product['category']} • {product['type']}
                </div>

                <div class="price">
                    ₹{product['price']:,}

                    <span class="old-price">
                        ₹{product['old']:,}
                    </span>
                </div>

                <div class="rating">
                    ⭐ {product['rating']}
                </div>
                """,
                unsafe_allow_html=True
            )


            b1, b2 = st.columns(2)


            with b1:

                if st.button(
                    "Add to Bag",
                    key=f"add_{product['id']}",
                    use_container_width=True
                ):

                    if product["id"] not in st.session_state.cart:

                        st.session_state.cart.append(
                            product["id"]
                        )

                    st.toast(
                        "Added to bag 🛍️"
                    )


            with b2:

                if st.button(
                    "♡",
                    key=f"wish_{product['id']}",
                    use_container_width=True
                ):

                    if product["id"] not in st.session_state.wishlist:

                        st.session_state.wishlist.append(
                            product["id"]
                        )

                    else:

                        st.session_state.wishlist.remove(
                            product["id"]
                        )

                    st.rerun()


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# ============================================================
# NOVA SHOPPING ASSISTANT
# ============================================================

st.markdown(
    """
    <div class="assistant-box">

        <div class="assistant-title">
            ✨ Ask NOVA
        </div>

        <div class="assistant-sub">
            Tell me what you're shopping for.
            I'll help you find something from the collection.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUICK SEARCH
# ============================================================

quick = st.columns(4)


questions = [
    "Show me kurtas under ₹1500",
    "Women's shirts",
    "Men's fashion",
    "Beauty under ₹800",
]


def find_products(query):

    q = query.lower()

    budget = None

    match = re.search(
        r"(?:under|below|upto|up to)\s*₹?(\d+)",
        q
    )

    if match:
        budget = int(match.group(1))


    result = []


    for product in PRODUCTS:

        searchable = (
            product["name"]
            + " "
            + product["category"]
            + " "
            + product["type"]
        ).lower()


        matches = False


        if "kurta" in q and "kurta" in searchable:
            matches = True

        elif "shirt" in q and "shirt" in searchable:
            matches = True

        elif "men" in q and product["category"] == "Men":
            matches = True

        elif "women" in q and product["category"] == "Women":
            matches = True

        elif "beauty" in q and product["category"] == "Beauty":
            matches = True

        elif "makeup" in q and product["type"] == "Makeup":
            matches = True

        elif "skincare" in q and product["type"] == "Skincare":
            matches = True


        if budget and product["price"] > budget:
            matches = False


        if matches:
            result.append(product)


    return result[:4]


for i, q in enumerate(questions):

    with quick[i]:

        if st.button(
            q,
            key=f"quick_{i}",
            use_container_width=True
        ):

            products = find_products(q)

            st.session_state.messages.append(
                {
                    "question": q,
                    "products": products
                }
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "What are you looking for?"
)


if question:

    products = find_products(
        question
    )

    st.session_state.messages.append(
        {
            "question": question,
            "products": products
        }
    )


# ============================================================
# RESULTS
# ============================================================

for item in st.session_state.messages:

    st.markdown(
        f"### You searched for: `{item['question']}`"
    )


    products = item["products"]


    if products:

        cols = st.columns(
            min(4, len(products))
        )


        for i, product in enumerate(products):

            with cols[i]:

                st.markdown(
                    '<div class="product-card">',
                    unsafe_allow_html=True
                )


                try:

                    st.image(
                        product["image"],
                        use_container_width=True
                    )

                except Exception:

                    st.info(
                        "Image unavailable"
                    )


                st.markdown(
                    f"""
                    <div class="product-name">
                        {product['name']}
                    </div>

                    <div class="product-type">
                        {product['category']} •
                        {product['type']}
                    </div>

                    <div class="price">
                        ₹{product['price']:,}
                    </div>

                    <div class="rating">
                        ⭐ {product['rating']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if st.button(
                    "Add to Bag",
                    key=f"result_{product['id']}_{item['question']}",
                    use_container_width=True
                ):

                    if product["id"] not in st.session_state.cart:

                        st.session_state.cart.append(
                            product["id"]
                        )

                    st.toast(
                        "Added to bag 🛍️"
                    )


                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No matching products found. "
            "Try another category or budget."
        )


# ============================================================
# CART SUMMARY
# ============================================================

if st.session_state.cart:

    st.divider()

    st.markdown(
        f"### 🛍️ Your Bag — "
        f"{len(st.session_state.cart)} item(s)"
    )


    total = 0


    for pid in st.session_state.cart:

        product = next(
            (
                p for p in PRODUCTS
                if p["id"] == pid
            ),
            None
        )

        if product:

            total += product["price"]

            st.write(
                f"**{product['name']}** — "
                f"₹{product['price']:,}"
            )


    st.success(
        f"Total: ₹{total:,}"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        NOVA AI • Fashion & Beauty Assistant
        <br>
        Discover your style. Shop smarter.
    </div>
    """,
    unsafe_allow_html=True
)
