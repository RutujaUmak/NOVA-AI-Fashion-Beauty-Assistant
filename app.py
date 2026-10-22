
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
)

# --------------------------------------------------
# NOVA AI - PRODUCT CATALOGUE
# Replace image_url with the actual image URL
# for each product before publishing.
# --------------------------------------------------

PRODUCTS = [
    {
        "id": 1,
        "name": "Floral Printed Kurta Set",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 1499,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700",
    },
    {
        "id": 2,
        "name": "Pastel Oversized Shirt",
        "category": "Women",
        "type": "Shirt",
        "price": 899,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?w=700",
    },
    {
        "id": 3,
        "name": "Women's Denim Jacket",
        "category": "Women",
        "type": "Jacket",
        "price": 1299,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=700",
    },
    {
        "id": 4,
        "name": "Elegant Party Dress",
        "category": "Women",
        "type": "Dress",
        "price": 1899,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700",
    },
    {
        "id": 5,
        "name": "Cotton Straight Kurta",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 799,
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=700",
    },
    {
        "id": 6,
        "name": "High Waist Blue Jeans",
        "category": "Women",
        "type": "Jeans",
        "price": 1199,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=700",
    },
    {
        "id": 7,
        "name": "Floral Casual Top",
        "category": "Women",
        "type": "Top",
        "price": 699,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?w=700",
    },
    {
        "id": 8,
        "name": "Elegant Anarkali Suit",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 2199,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700",
    },
    {
        "id": 9,
        "name": "Women's Black Blazer",
        "category": "Women",
        "type": "Formal Wear",
        "price": 1699,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=700",
    },
    {
        "id": 10,
        "name": "Printed Summer Dress",
        "category": "Women",
        "type": "Dress",
        "price": 999,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=700",
    },
    {
        "id": 11,
        "name": "Classic Men's Casual Shirt",
        "category": "Men",
        "type": "Shirt",
        "price": 999,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=700",
    },
    {
        "id": 12,
        "name": "Relaxed Fit Denim Jeans",
        "category": "Men",
        "type": "Jeans",
        "price": 1299,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=700",
    },
    {
        "id": 13,
        "name": "Men's Black T-Shirt",
        "category": "Men",
        "type": "T-Shirt",
        "price": 599,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=700",
    },
    {
        "id": 14,
        "name": "Men's Formal Shirt",
        "category": "Men",
        "type": "Formal Wear",
        "price": 899,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=700",
    },
    {
        "id": 15,
        "name": "Slim Fit Chinos",
        "category": "Men",
        "type": "Trousers",
        "price": 1199,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=700",
    },
    {
        "id": 16,
        "name": "Men's Denim Jacket",
        "category": "Men",
        "type": "Jacket",
        "price": 1499,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=700",
    },
    {
        "id": 17,
        "name": "Men's Polo T-Shirt",
        "category": "Men",
        "type": "T-Shirt",
        "price": 799,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1625910513413-5fc45b7d7eae?w=700",
    },
    {
        "id": 18,
        "name": "Men's Casual Hoodie",
        "category": "Men",
        "type": "Hoodie",
        "price": 1099,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=700",
    },
    {
        "id": 19,
        "name": "Men's Linen Shirt",
        "category": "Men",
        "type": "Shirt",
        "price": 1199,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=700",
    },
    {
        "id": 20,
        "name": "Men's Premium Blazer",
        "category": "Men",
        "type": "Formal Wear",
        "price": 2499,
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=700",
    },
    {
        "id": 21,
        "name": "Hydrating Glow Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 799,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700",
    },
    {
        "id": 22,
        "name": "Velvet Matte Lipstick",
        "category": "Beauty",
        "type": "Makeup",
        "price": 599,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=700",
    },
    {
        "id": 23,
        "name": "Soft Blush Makeup Palette",
        "category": "Beauty",
        "type": "Makeup",
        "price": 899,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=700",
    },
    {
        "id": 24,
        "name": "Vitamin C Face Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 699,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1556229010-aa3c1c2c7c4a?w=700",
    },
    {
        "id": 25,
        "name": "Hydrating Face Moisturizer",
        "category": "Beauty",
        "type": "Skincare",
        "price": 549,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=700",
    },
    {
        "id": 26,
        "name": "Waterproof Mascara",
        "category": "Beauty",
        "type": "Makeup",
        "price": 499,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=700",
    },
    {
        "id": 27,
        "name": "Liquid Foundation",
        "category": "Beauty",
        "type": "Makeup",
        "price": 749,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=700",
    },
    {
        "id": 28,
        "name": "Rose Face Toner",
        "category": "Beauty",
        "type": "Skincare",
        "price": 399,
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=700",
    },
    {
        "id": 29,
        "name": "Nude Lip Gloss",
        "category": "Beauty",
        "type": "Makeup",
        "price": 349,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=700",
    },
    {
        "id": 30,
        "name": "Daily Sunscreen SPF 50",
        "category": "Beauty",
        "type": "Skincare",
        "price": 599,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=700",
    },
    {
        "id": 31,
        "name": "Minimal Gold Necklace",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 699,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=700",
    },
    {
        "id": 32,
        "name": "Structured Women's Handbag",
        "category": "Accessories",
        "type": "Bags",
        "price": 1199,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700",
    },
    {
        "id": 33,
        "name": "Classic Leather Wallet",
        "category": "Accessories",
        "type": "Wallet",
        "price": 499,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=700",
    },
    {
        "id": 34,
        "name": "Elegant Pearl Earrings",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 599,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=700",
    },
    {
        "id": 35,
        "name": "Women's Fashion Watch",
        "category": "Accessories",
        "type": "Watch",
        "price": 1299,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=700",
    },
    {
        "id": 36,
        "name": "Men's Classic Watch",
        "category": "Accessories",
        "type": "Watch",
        "price": 1499,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=700",
    },
    {
        "id": 37,
        "name": "Fashion Sunglasses",
        "category": "Accessories",
        "type": "Sunglasses",
        "price": 399,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700",
    },
    {
        "id": 38,
        "name": "Leather Crossbody Bag",
        "category": "Accessories",
        "type": "Bags",
        "price": 999,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=700",
    },
    {
        "id": 39,
        "name": "Statement Bracelet",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 449,
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=700",
    },
    {
        "id": 40,
        "name": "Classic Leather Belt",
        "category": "Accessories",
        "type": "Belt",
        "price": 599,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=700",
    },
    {
        "id": 41,
        "name": "Everyday Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 1299,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700",
    },
    {
        "id": 42,
        "name": "Women's Casual Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 999,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=700",
    },
    {
        "id": 43,
        "name": "Men's Running Shoes",
        "category": "Footwear",
        "type": "Sports Shoes",
        "price": 1599,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=700",
    },
    {
        "id": 44,
        "name": "Women's Flat Sandals",
        "category": "Footwear",
        "type": "Sandals",
        "price": 499,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=700",
    },
    {
        "id": 45,
        "name": "Men's Casual Loafers",
        "category": "Footwear",
        "type": "Loafers",
        "price": 1099,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=700",
    },
    {
        "id": 46,
        "name": "Women's Heeled Sandals",
        "category": "Footwear",
        "type": "Heels",
        "price": 899,
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=700",
    },
    {
        "id": 47,
        "name": "Classic White Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 1199,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1495555961986-6d4c1ecb7be3?w=700",
    },
    {
        "id": 48,
        "name": "Women's Ballet Flats",
        "category": "Footwear",
        "type": "Flats",
        "price": 699,
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=700",
    },
    {
        "id": 49,
        "name": "Men's Sports Sneakers",
        "category": "Footwear",
        "type": "Sports Shoes",
        "price": 1399,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=700",
    },
    {
        "id": 50,
        "name": "Premium Party Heels",
        "category": "Footwear",
        "type": "Heels",
        "price": 1499,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1515347619252-60a4bf4fff4f?w=700",
    },
]

# --------------------------------------------------
# STYLE
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff7fb, #f8f5ff);
    }
    h1, h2, h3 {
        color: #8e245f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("✨ NOVA AI")
st.subheader("Your Fashion, Beauty & Personal Style Assistant")
st.write(
    "Discover products, compare prices, explore style ideas, "
    "and get recommendations from our catalogue."
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "chat" not in st.session_state:
    st.session_state.chat = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Explore NOVA AI")

page = st.sidebar.radio(
    "Choose a feature",
    [
        "Product Catalogue",
        "AI Style Assistant",
        "Virtual Try-On",
        "My Cart",
        "My Wishlist",
    ],
)

# --------------------------------------------------
# PRODUCT CARD
# --------------------------------------------------

def show_product(product):
    with st.container(border=True):
        st.image(
            product["image_url"],
            caption=product["name"],
            use_container_width=True,
        )

        st.markdown(f"**{product['name']}**")
        st.write(f"Category: {product['category']}")
        st.write(f"₹{product['price']:,}")
        st.write(f"⭐ {product['rating']} / 5")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Add to Cart",
                key=f"cart_{product['id']}",
                use_container_width=True,
            ):
                st.session_state.cart.append(product["id"])
                st.success("Added to cart!")

        with col2:
            if st.button(
                "♡ Wishlist",
                key=f"wish_{product['id']}",
                use_container_width=True,
            ):
                if product["id"] not in st.session_state.wishlist:
                    st.session_state.wishlist.append(product["id"])
                st.success("Added to wishlist!")

# --------------------------------------------------
# PRODUCT CATALOGUE
# --------------------------------------------------

if page == "Product Catalogue":
    st.header("🛍️ Explore Products")

    categories = ["All"] + sorted(
        {product["category"] for product in PRODUCTS}
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "Search products",
            placeholder="Try dress, lipstick, shoes, serum...",
        ).strip().lower()

    with col2:
        category = st.selectbox("Category", categories)

    max_price = st.slider(
        "Maximum price (₹)",
        min_value=300,
        max_value=5000,
        value=5000,
        step=100,
    )

    filtered = [
        p for p in PRODUCTS
        if (category == "All" or p["category"] == category)
        and p["price"] <= max_price
        and (
            search in p["name"].lower()
            or search in p["category"].lower()
            or search in p["type"].lower()
        )
    ]

    sort_by = st.selectbox(
        "Sort products",
        ["Recommended", "Price: Low to High", "Price: High to Low", "Top Rated"],
    )

    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda p: p["price"])
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda p: p["price"], reverse=True)
    elif sort_by == "Top Rated":
        filtered.sort(key=lambda p: p["rating"], reverse=True)

    st.caption(f"{len(filtered)} products found")

    if not filtered:
        st.info("No products found. Try a different search or price range.")
    else:
        for start in range(0, len(filtered), 3):
            cols = st.columns(3)
            for col, product in zip(cols, filtered[start:start + 3]):
                with col:
                    show_product(product)

# --------------------------------------------------
# AI STYLE ASSISTANT - RULE-BASED, NO API REQUIRED
# --------------------------------------------------

elif page == "AI Style Assistant":
    st.header("💬 NOVA Style Assistant")
    st.write(
        "Ask about products, affordable options, outfits, "
        "occasions, beauty products, or colour combinations."
    )

    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input(
            "Your question",
            placeholder="Example: Show me the cheapest dress",
        )
        submitted = st.form_submit_button("Get Recommendation")

    if submitted and question.strip():
        q = question.lower()

        if any(word in q for word in ["cheap", "cheapest", "affordable", "budget", "low price"]):
            results = sorted(PRODUCTS, key=lambda p: p["price"])[:5]
            answer = "Here are five affordable products from the catalogue."

        elif any(word in q for word in ["dress", "kurta", "outfit", "wear", "clothes"]):
            results = [
                p for p in PRODUCTS
                if p["category"] in ["Women", "Men"]
                and any(
                    word in (p["name"] + " " + p["type"]).lower()
                    for word in ["dress", "kurta", "shirt", "jeans", "blazer"]
                )
            ][:5]
            answer = "Here are some clothing options you can explore."

        elif any(word in q for word in ["beauty", "skin", "makeup", "lipstick", "serum"]):
            results = [p for p in PRODUCTS if p["category"] == "Beauty"][:5]
            answer = "Here are beauty and skincare products from the catalogue."

        elif any(word in q for word in ["shoe", "sneaker", "sandal", "heel", "footwear"]):
            results = [p for p in PRODUCTS if p["category"] == "Footwear"][:5]
            answer = "Here are footwear options from the catalogue."

        else:
            matching = [
                p for p in PRODUCTS
                if any(
                    word in (p["name"] + " " + p["category"] + " " + p["type"]).lower()
                    for word in q.split()
                    if len(word) > 2
                )
            ]
            results = matching[:5]
            answer = (
                "Here are products matching your question."
                if results
                else "Try asking about dresses, shirts, beauty products, "
                     "footwear, accessories, or affordable products."
            )

        st.markdown(f"**NOVA AI:** {answer}")

        if results:
            cols = st.columns(min(3, len(results)))
            for i, product in enumerate(results):
                with cols[i % len(cols)]:
                    show_product(product)

# --------------------------------------------------
# VIRTUAL TRY-ON - UPLOAD AND PREVIEW
# --------------------------------------------------

elif page == "Virtual Try-On":
    st.header("👗 Virtual Try-On")
    st.write(
        "Upload a photo and select a catalogue item. "
        "This starter feature previews your photo and the selected product; "
        "it does not yet generate a realistic outfit replacement."
    )

    uploaded = st.file_uploader(
        "Upload a selfie or full-body photo",
        type=["jpg", "jpeg", "png"],
    )

    clothing = [
        p for p in PRODUCTS
        if p["category"] in ["Women", "Men"]
    ]

    selected_name = st.selectbox(
        "Choose an outfit",
        [p["name"] for p in clothing],
    )
    selected = next(
        p for p in clothing if p["name"] == selected_name
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Your Photo")
        if uploaded:
            st.image(uploaded, use_container_width=True)
        else:
            st.info("Upload a photo to see it here.")

    with right:
        st.subheader("Selected Product")
        st.image(
            selected["image_url"],
            caption=selected["name"],
            use_container_width=True,
        )
        st.write(f"Price: ₹{selected['price']:,}")

    st.warning(
        "A real virtual try-on requires a compatible image-generation "
        "model or API. This preview does not claim that you are wearing "
        "the selected outfit."
    )

# --------------------------------------------------
# CART
# --------------------------------------------------

elif page == "My Cart":
    st.header("🛒 My Cart")

    cart_items = [
        p for product_id in st.session_state.cart
        for p in PRODUCTS if p["id"] == product_id
    ]

    if not cart_items:
        st.info("Your cart is empty.")
    else:
        total = 0
        for product in cart_items:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(product["image_url"], use_container_width=True)
            with col2:
                st.markdown(f"**{product['name']}**")
                st.write(f"₹{product['price']:,}")
                total += product["price"]

        st.subheader(f"Total: ₹{total:,}")

        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

# --------------------------------------------------
# WISHLIST
# --------------------------------------------------

elif page == "My Wishlist":
    st.header("♡ My Wishlist")

    wishlist_items = [
        p for p in PRODUCTS
        if p["id"] in st.session_state.wishlist
    ]

    if not wishlist_items:
        st.info("Your wishlist is empty.")
    else:
        cols = st.columns(3)
        for i, product in enumerate(wishlist_items):
            with cols[i % 3]:
                show_product(product)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "NOVA AI | Fashion & Beauty — Product images and prices are "
    "catalogue examples. Verify image accuracy and prices before publishing."
)
