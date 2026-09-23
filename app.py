```python
import os
import re
import streamlit as st

# ============================================================
# OPTIONAL GEMINI
# ============================================================

try:
    from google import genai
except Exception:
    genai = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PRODUCT CATALOG
# IMPORTANT:
# Put your verified images inside the assets folder.
# Example:
# assets/floral_kurta.jpg
# assets/pastel_shirt.jpg
# ============================================================

PRODUCTS = [

    # =========================
    # WOMEN
    # =========================

    {
        "id": 1,
        "name": "Floral Printed Kurta Set",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 1499,
        "mrp": 2499,
        "rating": 4.5,
        "image": "assets/floral_kurta.jpg",
    },

    {
        "id": 2,
        "name": "Pastel Oversized Shirt",
        "category": "Women",
        "type": "Shirt",
        "price": 899,
        "mrp": 1599,
        "rating": 4.3,
        "image": "assets/pastel_shirt.jpg",
    },

    {
        "id": 3,
        "name": "Women's Denim Jacket",
        "category": "Women",
        "type": "Jacket",
        "price": 1299,
        "mrp": 2199,
        "rating": 4.4,
        "image": "assets/womens_denim_jacket.jpg",
    },

    {
        "id": 4,
        "name": "Elegant Party Dress",
        "category": "Women",
        "type": "Dress",
        "price": 1899,
        "mrp": 2999,
        "rating": 4.6,
        "image": "assets/party_dress.jpg",
    },

    {
        "id": 5,
        "name": "Cotton Straight Kurta",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 799,
        "mrp": 1299,
        "rating": 4.2,
        "image": "assets/cotton_kurta.jpg",
    },

    {
        "id": 6,
        "name": "High Waist Blue Jeans",
        "category": "Women",
        "type": "Jeans",
        "price": 1199,
        "mrp": 1999,
        "rating": 4.5,
        "image": "assets/womens_blue_jeans.jpg",
    },

    {
        "id": 7,
        "name": "Floral Casual Top",
        "category": "Women",
        "type": "Top",
        "price": 699,
        "mrp": 1199,
        "rating": 4.3,
        "image": "assets/floral_top.jpg",
    },

    {
        "id": 8,
        "name": "Elegant Anarkali Suit",
        "category": "Women",
        "type": "Ethnic Wear",
        "price": 2199,
        "mrp": 3499,
        "rating": 4.7,
        "image": "assets/anarkali.jpg",
    },

    {
        "id": 9,
        "name": "Women's Black Blazer",
        "category": "Women",
        "type": "Formal Wear",
        "price": 1699,
        "mrp": 2599,
        "rating": 4.4,
        "image": "assets/womens_black_blazer.jpg",
    },

    {
        "id": 10,
        "name": "Printed Summer Dress",
        "category": "Women",
        "type": "Dress",
        "price": 999,
        "mrp": 1699,
        "rating": 4.5,
        "image": "assets/summer_dress.jpg",
    },


    # =========================
    # MEN
    # =========================

    {
        "id": 11,
        "name": "Classic Men's Casual Shirt",
        "category": "Men",
        "type": "Shirt",
        "price": 999,
        "mrp": 1799,
        "rating": 4.4,
        "image": "assets/mens_casual_shirt.jpg",
    },

    {
        "id": 12,
        "name": "Relaxed Fit Denim Jeans",
        "category": "Men",
        "type": "Jeans",
        "price": 1299,
        "mrp": 2299,
        "rating": 4.3,
        "image": "assets/mens_jeans.jpg",
    },

    {
        "id": 13,
        "name": "Men's Black T-Shirt",
        "category": "Men",
        "type": "T-Shirt",
        "price": 599,
        "mrp": 999,
        "rating": 4.4,
        "image": "assets/mens_black_tshirt.jpg",
    },

    {
        "id": 14,
        "name": "Men's Formal Shirt",
        "category": "Men",
        "type": "Formal Wear",
        "price": 899,
        "mrp": 1499,
        "rating": 4.5,
        "image": "assets/mens_formal_shirt.jpg",
    },

    {
        "id": 15,
        "name": "Slim Fit Chinos",
        "category": "Men",
        "type": "Trousers",
        "price": 1199,
        "mrp": 1999,
        "rating": 4.3,
        "image": "assets/slim_chinos.jpg",
    },

    {
        "id": 16,
        "name": "Men's Denim Jacket",
        "category": "Men",
        "type": "Jacket",
        "price": 1499,
        "mrp": 2499,
        "rating": 4.6,
        "image": "assets/mens_denim_jacket.jpg",
    },

    {
        "id": 17,
        "name": "Men's Polo T-Shirt",
        "category": "Men",
        "type": "T-Shirt",
        "price": 799,
        "mrp": 1299,
        "rating": 4.5,
        "image": "assets/mens_polo.jpg",
    },

    {
        "id": 18,
        "name": "Men's Casual Hoodie",
        "category": "Men",
        "type": "Hoodie",
        "price": 1099,
        "mrp": 1899,
        "rating": 4.4,
        "image": "assets/mens_hoodie.jpg",
    },

    {
        "id": 19,
        "name": "Men's Linen Shirt",
        "category": "Men",
        "type": "Shirt",
        "price": 1199,
        "mrp": 1999,
        "rating": 4.6,
        "image": "assets/mens_linen_shirt.jpg",
    },

    {
        "id": 20,
        "name": "Men's Premium Blazer",
        "category": "Men",
        "type": "Formal Wear",
        "price": 2499,
        "mrp": 3999,
        "rating": 4.8,
        "image": "assets/mens_blazer.jpg",
    },


    # =========================
    # BEAUTY
    # =========================

    {
        "id": 21,
        "name": "Hydrating Glow Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 799,
        "mrp": 1299,
        "rating": 4.7,
        "image": "assets/glow_serum.jpg",
    },

    {
        "id": 22,
        "name": "Velvet Matte Lipstick",
        "category": "Beauty",
        "type": "Makeup",
        "price": 599,
        "mrp": 899,
        "rating": 4.5,
        "image": "assets/matte_lipstick.jpg",
    },

    {
        "id": 23,
        "name": "Soft Blush Makeup Palette",
        "category": "Beauty",
        "type": "Makeup",
        "price": 899,
        "mrp": 1399,
        "rating": 4.6,
        "image": "assets/blush_palette.jpg",
    },

    {
        "id": 24,
        "name": "Vitamin C Face Serum",
        "category": "Beauty",
        "type": "Skincare",
        "price": 699,
        "mrp": 1199,
        "rating": 4.5,
        "image": "assets/vitamin_c_serum.jpg",
    },

    {
        "id": 25,
        "name": "Hydrating Face Moisturizer",
        "category": "Beauty",
        "type": "Skincare",
        "price": 549,
        "mrp": 899,
        "rating": 4.4,
        "image": "assets/moisturizer.jpg",
    },

    {
        "id": 26,
        "name": "Waterproof Mascara",
        "category": "Beauty",
        "type": "Makeup",
        "price": 499,
        "mrp": 799,
        "rating": 4.3,
        "image": "assets/mascara.jpg",
    },

    {
        "id": 27,
        "name": "Liquid Foundation",
        "category": "Beauty",
        "type": "Makeup",
        "price": 749,
        "mrp": 1199,
        "rating": 4.5,
        "image": "assets/foundation.jpg",
    },

    {
        "id": 28,
        "name": "Rose Face Toner",
        "category": "Beauty",
        "type": "Skincare",
        "price": 399,
        "mrp": 699,
        "rating": 4.2,
        "image": "assets/rose_toner.jpg",
    },

    {
        "id": 29,
        "name": "Nude Lip Gloss",
        "category": "Beauty",
        "type": "Makeup",
        "price": 349,
        "mrp": 599,
        "rating": 4.3,
        "image": "assets/lip_gloss.jpg",
    },

    {
        "id": 30,
        "name": "Daily Sunscreen SPF 50",
        "category": "Beauty",
        "type": "Skincare",
        "price": 599,
        "mrp": 899,
        "rating": 4.6,
        "image": "assets/sunscreen.jpg",
    },


    # =========================
    # ACCESSORIES
    # =========================

    {
        "id": 31,
        "name": "Minimal Gold Necklace",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 699,
        "mrp": 1199,
        "rating": 4.6,
        "image": "assets/gold_necklace.jpg",
    },

    {
        "id": 32,
        "name": "Structured Women's Handbag",
        "category": "Accessories",
        "type": "Bags",
        "price": 1199,
        "mrp": 1999,
        "rating": 4.6,
        "image": "assets/womens_handbag.jpg",
    },

    {
        "id": 33,
        "name": "Classic Leather Wallet",
        "category": "Accessories",
        "type": "Wallet",
        "price": 499,
        "mrp": 899,
        "rating": 4.4,
        "image": "assets/leather_wallet.jpg",
    },

    {
        "id": 34,
        "name": "Elegant Pearl Earrings",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 599,
        "mrp": 999,
        "rating": 4.5,
        "image": "assets/pearl_earrings.jpg",
    },

    {
        "id": 35,
        "name": "Women's Fashion Watch",
        "category": "Accessories",
        "type": "Watch",
        "price": 1299,
        "mrp": 2199,
        "rating": 4.6,
        "image": "assets/womens_watch.jpg",
    },

    {
        "id": 36,
        "name": "Men's Classic Watch",
        "category": "Accessories",
        "type": "Watch",
        "price": 1499,
        "mrp": 2499,
        "rating": 4.7,
        "image": "assets/mens_watch.jpg",
    },

    {
        "id": 37,
        "name": "Fashion Sunglasses",
        "category": "Accessories",
        "type": "Sunglasses",
        "price": 399,
        "mrp": 699,
        "rating": 4.3,
        "image": "assets/sunglasses.jpg",
    },

    {
        "id": 38,
        "name": "Leather Crossbody Bag",
        "category": "Accessories",
        "type": "Bags",
        "price": 999,
        "mrp": 1699,
        "rating": 4.5,
        "image": "assets/crossbody_bag.jpg",
    },

    {
        "id": 39,
        "name": "Statement Bracelet",
        "category": "Accessories",
        "type": "Jewellery",
        "price": 449,
        "mrp": 799,
        "rating": 4.2,
        "image": "assets/bracelet.jpg",
    },

    {
        "id": 40,
        "name": "Classic Leather Belt",
        "category": "Accessories",
        "type": "Belt",
        "price": 599,
        "mrp": 999,
        "rating": 4.4,
        "image": "assets/leather_belt.jpg",
    },


    # =========================
    # FOOTWEAR
    # =========================

    {
        "id": 41,
        "name": "Everyday Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 1299,
        "mrp": 2199,
        "rating": 4.4,
        "image": "assets/everyday_sneakers.jpg",
    },

    {
        "id": 42,
        "name": "Women's Casual Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 999,
        "mrp": 1699,
        "rating": 4.5,
        "image": "assets/womens_sneakers.jpg",
    },

    {
        "id": 43,
        "name": "Men's Running Shoes",
        "category": "Footwear",
        "type": "Sports Shoes",
        "price": 1599,
        "mrp": 2599,
        "rating": 4.7,
        "image": "assets/mens_running_shoes.jpg",
    },

    {
        "id": 44,
        "name": "Women's Flat Sandals",
        "category": "Footwear",
        "type": "Sandals",
        "price": 499,
        "mrp": 899,
        "rating": 4.3,
        "image": "assets/flat_sandals.jpg",
    },

    {
        "id": 45,
        "name": "Men's Casual Loafers",
        "category": "Footwear",
        "type": "Loafers",
        "price": 1099,
        "mrp": 1799,
        "rating": 4.5,
        "image": "assets/mens_loafers.jpg",
    },

    {
        "id": 46,
        "name": "Women's Heeled Sandals",
        "category": "Footwear",
        "type": "Heels",
        "price": 899,
        "mrp": 1499,
        "rating": 4.4,
        "image": "assets/heeled_sandals.jpg",
    },

    {
        "id": 47,
        "name": "Classic White Sneakers",
        "category": "Footwear",
        "type": "Shoes",
        "price": 1199,
        "mrp": 1999,
        "rating": 4.6,
        "image": "assets/white_sneakers.jpg",
    },

    {
        "id": 48,
        "name": "Women's Ballet Flats",
        "category": "Footwear",
        "type": "Flats",
        "price": 699,
        "mrp": 1099,
        "rating": 4.3,
        "image": "assets/ballet_flats.jpg",
    },

    {
        "id": 49,
        "name": "Men's Sports Sneakers",
        "category": "Footwear",
        "type": "Sports Shoes",
        "price": 1399,
        "mrp": 2299,
        "rating": 4.5,
        "image": "assets/mens_sports_sneakers.jpg",
    },

    {
        "id": 50,
        "name": "Premium Party Heels",
        "category": "Footwear",
        "type": "Heels",
        "price": 1499,
        "mrp": 2499,
        "rating": 4.7,
        "image": "assets/party_heels.jpg",
    },
]


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background: #fafafa;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }


    /* Header */

    .nova-logo {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .nova-pink {
        color: #e91e63;
    }

    .nova-subtitle {
        color: #777;
        font-size: 14px;
        margin-top: -8px;
        margin-bottom: 25px;
    }


    /* Welcome */

    .welcome {
        text-align: center;
        padding: 55px 20px 35px 20px;
    }

    .welcome h1 {
        font-size: 40px;
        margin-bottom: 10px;
    }

    .welcome p {
        color: #777;
        font-size: 16px;
    }


    /* Product card */

    .product-card {
        border: 1px solid #eeeeee;
        border-radius: 16px;
        padding: 10px;
        background: white;
        margin-bottom: 10px;
    }

    .product-title {
        font-size: 15px;
        font-weight: 700;
        min-height: 42px;
        margin-top: 8px;
    }

    .product-type {
        color: #777;
        font-size: 12px;
    }

    .product-price {
        font-size: 18px;
        font-weight: 800;
        margin-top: 5px;
    }

    .product-mrp {
        color: #999;
        text-decoration: line-through;
        font-size: 12px;
    }

    .product-rating {
        color: #087f5b;
        font-size: 13px;
        font-weight: 600;
    }


    /* Chat */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
    }

    [data-testid="stChatInput"] {
        border-radius: 18px;
    }

    [data-testid="stChatInput"] textarea {
        background: white !important;
        color: #222 !important;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []


# ============================================================
# HELPERS
# ============================================================

def get_product(product_id):
    return next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None
    )


def extract_budget(text):

    patterns = [
        r"(?:under|below|within|upto|up to)\s*(?:₹|rs\.?|inr)?\s*(\d[\d,]*)",
        r"(?:₹|rs\.?|inr)\s*(\d[\d,]*)",
        r"budget\s*(?:of)?\s*(?:₹|rs\.?|inr)?\s*(\d[\d,]*)",
    ]

    for pattern in patterns:

        match = re.search(pattern, text.lower())

        if match:
            return int(
                match.group(1).replace(",", "")
            )

    return None


def detect_category(text):

    q = text.lower()

    if any(x in q for x in [
        "makeup",
        "lipstick",
        "mascara",
        "foundation",
        "cosmetic",
        "beauty",
        "skincare",
        "skin care",
        "serum",
        "moisturizer",
        "sunscreen",
        "toner",
    ]):
        return "Beauty"

    if any(x in q for x in [
        "men",
        "mens",
        "male",
        "boy",
    ]):
        return "Men"

    if any(x in q for x in [
        "women",
        "womens",
        "woman",
        "girl",
        "ladies",
    ]):
        return "Women"

    if any(x in q for x in [
        "shoe",
        "shoes",
        "sneaker",
        "sneakers",
        "footwear",
        "heel",
        "heels",
        "sandals",
        "flats",
        "loafers",
    ]):
        return "Footwear"

    if any(x in q for x in [
        "bag",
        "jewellery",
        "jewelry",
        "necklace",
        "watch",
        "wallet",
        "sunglasses",
        "accessory",
        "accessories",
        "belt",
        "bracelet",
        "earrings",
    ]):
        return "Accessories"

    return None


def detect_type(text):

    q = text.lower()

    groups = {

        "Makeup": [
            "makeup",
            "lipstick",
            "mascara",
            "foundation",
            "lip gloss",
            "blush",
        ],

        "Skincare": [
            "skincare",
            "skin care",
            "serum",
            "moisturizer",
            "sunscreen",
            "toner",
        ],

        "Shoes": [
            "shoe",
            "shoes",
            "sneaker",
            "sneakers",
        ],

        "Heels": [
            "heel",
            "heels",
        ],

        "Sandals": [
            "sandal",
            "sandals",
        ],

        "Jeans": [
            "jeans",
            "denim jeans",
        ],

        "Jacket": [
            "jacket",
        ],

        "Dress": [
            "dress",
        ],

        "Shirt": [
            "shirt",
        ],

        "T-Shirt": [
            "t-shirt",
            "tshirt",
            "t shirt",
        ],

        "Bags": [
            "bag",
            "handbag",
        ],

        "Jewellery": [
            "jewellery",
            "jewelry",
            "necklace",
            "earrings",
            "bracelet",
        ],

        "Watch": [
            "watch",
        ],

        "Ethnic Wear": [
            "kurta",
            "anarkali",
            "ethnic",
            "ethnic wear",
        ],
    }

    for product_type, words in groups.items():

        if any(word in q for word in words):
            return product_type

    return None


# ============================================================
# PRODUCT SEARCH
# ============================================================

def recommend_products(question):

    q = question.lower()

    budget = extract_budget(question)

    category = detect_category(question)

    product_type = detect_type(question)

    candidates = PRODUCTS[:]


    # Category filter

    if category:

        candidates = [
            p for p in candidates
            if p["category"] == category
        ]


    # Product type filter

    if product_type:

        type_matches = [
            p for p in candidates
            if product_type.lower()
            in p["type"].lower()
        ]

        if type_matches:
            candidates = type_matches


    # Budget filter

    if budget is not None:

        candidates = [
            p for p in candidates
            if p["price"] <= budget
        ]

        if not candidates:
            return []


    # Cheapest

    if any(word in q for word in [
        "cheapest",
        "lowest price",
        "lowest priced",
        "least expensive",
        "most affordable",
    ]):

        return sorted(
            candidates,
            key=lambda p: (
                p["price"],
                -p["rating"]
            )
        )[:4]


    # Highest rated

    if any(word in q for word in [
        "best rated",
        "highest rated",
        "top rated",
        "highest rating",
    ]):

        return sorted(
            candidates,
            key=lambda p: (
                -p["rating"],
                p["price"]
            )
        )[:4]


    # Keyword matching

    words = re.findall(
        r"[a-zA-Z]+",
        q
    )

    stop_words = {
        "show",
        "me",
        "the",
        "a",
        "an",
        "for",
        "under",
        "below",
        "within",
        "please",
        "find",
        "want",
        "need",
        "give",
        "some",
        "product",
        "products",
        "best",
        "good",
        "can",
        "you",
        "something",
        "what",
        "is",
        "are",
        "with",
        "price",
        "cheap",
    }

    words = [
        w for w in words
        if len(w) >= 3
        and w not in stop_words
    ]


    scored = []

    for product in candidates:

        searchable = (
            f"{product['name']} "
            f"{product['category']} "
            f"{product['type']}"
        ).lower()

        score = sum(
            1
            for word in words
            if word in searchable
        )

        scored.append(
            (score, product)
        )


    matches = [
        p
        for score, p in scored
        if score > 0
    ]

    if matches:

        return sorted(
            matches,
            key=lambda p: (
                -next(
                    score
                    for score, item
                    in scored
                    if item["id"] == p["id"]
                ),
                p["price"],
            )
        )[:4]


    return sorted(
        candidates,
        key=lambda p: (
            -p["rating"],
            p["price"]
        )
    )[:4]


# ============================================================
# LOCAL AI RESPONSE
# ============================================================

def local_answer(question, products):

    if not products:

        budget = extract_budget(question)

        if budget is not None:

            return (
                f"I couldn't find a matching product "
                f"within ₹{budget:,}. "
                "Try increasing your budget or changing "
                "the category."
            )

        return (
            "I couldn't find an exact match. "
            "Try asking for dresses, kurtas, shirts, "
            "makeup, skincare, shoes or bags."
        )


    q = question.lower()


    if any(x in q for x in [
        "cheapest",
        "lowest price",
        "most affordable",
    ]):

        p = min(
            products,
            key=lambda x: x["price"]
        )

        return (
            f"The most affordable option is "
            f"**{p['name']}** at **₹{p['price']:,}** "
            f"with a **{p['rating']}★** rating."
        )


    if any(x in q for x in [
        "best rated",
        "highest rated",
        "top rated",
    ]):

        p = max(
            products,
            key=lambda x: x["rating"]
        )

        return (
            f"One of the highest-rated matching options "
            f"is **{p['name']}** at **₹{p['price']:,}** "
            f"with a **{p['rating']}★** rating."
        )


    names = ", ".join(
        p["name"]
        for p in products[:3]
    )

    return (
        f"I found these options for you: "
        f"**{names}**."
    )


# ============================================================
# GEMINI
# ============================================================

def ask_ai(question, products):

    api_key = st.secrets.get(
        "GEMINI_API_KEY",
        ""
    )

    if not api_key or genai is None:

        return local_answer(
            question,
            products
        )


    selected_text = "\n".join(
        f"- {p['name']} | "
        f"{p['category']} | "
        f"{p['type']} | "
        f"₹{p['price']} | "
        f"{p['rating']}★"
        for p in products
    )


    catalog_text = "\n".join(
        f"ID {p['id']} | "
        f"{p['name']} | "
        f"{p['category']} | "
        f"{p['type']} | "
        f"₹{p['price']} | "
        f"{p['rating']}★"
        for p in PRODUCTS
    )


    history = []

    for msg in st.session_state.messages[-8:]:

        history.append(
            f"{msg['role']}: "
            f"{msg['content']}"
        )

    history_text = "\n".join(history)


    prompt = f"""
You are NOVA AI, a fashion and beauty shopping assistant.

PRODUCT CATALOG:
{catalog_text}

PRODUCTS SELECTED:
{selected_text}

RECENT CHAT:
{history_text}

CUSTOMER QUESTION:
{question}

RULES:

1. Be natural and conversational.
2. Help the customer find products.
3. Use only products from the catalog.
4. Never invent products.
5. Never invent prices.
6. Never invent ratings.
7. Never invent discounts.
8. Use Indian rupees.
9. Keep responses short and useful.
10. Do not output image URLs.
11. When products are relevant, mention their names and prices.
12. Do not claim an image shows something that is not in the product catalog.
"""


    try:

        client = genai.Client(
            api_key=api_key
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if response and response.text:

            return response.text

    except Exception:

        pass


    return local_answer(
        question,
        products
    )


# ============================================================
# CART / WISHLIST
# ============================================================

def add_to_cart(product_id):

    if product_id not in st.session_state.cart:

        st.session_state.cart.append(
            product_id
        )

        st.toast(
            "Added to cart 🛍️"
        )

    else:

        st.toast(
            "Already in cart."
        )


def toggle_wishlist(product_id):

    if product_id in st.session_state.wishlist:

        st.session_state.wishlist.remove(
            product_id
        )

        st.toast(
            "Removed from wishlist."
        )

    else:

        st.session_state.wishlist.append(
            product_id
        )

        st.toast(
            "Added to wishlist ❤️"
        )


# ============================================================
# PRODUCT CARD
# ============================================================

def display_product(product, prefix):

    image_path = product["image"]


    # --------------------------------------------------------
    # IMAGE CHECK
    # --------------------------------------------------------

    if os.path.exists(image_path):

        st.image(
            image_path,
            use_container_width=True
        )

    else:

        st.warning(
            f"Image missing: {image_path}"
        )


    st.markdown(
        f"""
        <div class="product-title">
            {product['name']}
        </div>

        <div class="product-type">
            {product['category']} • {product['type']}
        </div>

        <div class="product-price">
            ₹{product['price']:,}
            <span class="product-mrp">
                ₹{product['mrp']:,}
            </span>
        </div>

        <div class="product-rating">
            ⭐ {product['rating']}
        </div>
        """,
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    with c1:

        if st.button(
            "🛍 Add",
            key=f"{prefix}_cart_{product['id']}",
            use_container_width=True,
        ):

            add_to_cart(
                product["id"]
            )


    with c2:

        if product["id"] in st.session_state.wishlist:

            icon = "❤️"

        else:

            icon = "♡"


        if st.button(
            icon,
            key=f"{prefix}_wish_{product['id']}",
            use_container_width=True,
        ):

            toggle_wishlist(
                product["id"]
            )

            st.rerun()


# ============================================================
# PRODUCT DISPLAY
# ============================================================

def display_products(products, prefix):

    if not products:
        return


    st.markdown(
        "#### Recommended for you"
    )


    cols = st.columns(
        min(len(products), 4)
    )


    for i, product in enumerate(products):

        with cols[i % len(cols)]:

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )

            display_product(
                product,
                f"{prefix}_{i}"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="nova-logo">NOVA<span class="nova-pink">AI</span></div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Fashion • Beauty • Smart Shopping"
    )


    st.divider()


    st.markdown("### 🛍️ Shopping")


    category = st.selectbox(
        "Browse category",
        [
            "All",
            "Women",
            "Men",
            "Beauty",
            "Accessories",
            "Footwear",
        ]
    )


    st.divider()


    st.markdown("### Your shopping")


    st.write(
        f"🛒 Cart: **{len(st.session_state.cart)}**"
    )

    st.write(
        f"❤️ Wishlist: **{len(st.session_state.wishlist)}**"
    )


    st.divider()


    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    st.markdown("### Try asking")


    st.caption(
        "• Show me kurtas under ₹1500\n\n"
        "• Women's shirts under ₹1000\n\n"
        "• Men's fashion under ₹1500\n\n"
        "• Show me makeup\n\n"
        "• Best rated skincare\n\n"
        "• Show me shoes"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="nova-logo">NOVA<span class="nova-pink">AI</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="nova-subtitle">'
    'Your personal fashion & beauty shopping assistant'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome">

        <h1>✨ What are you looking for?</h1>

        <p>
        Ask NOVA to discover fashion, beauty,
        accessories and footwear.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    quick_cols = st.columns(4)


    quick_questions = [
        "Women's ethnic wear",
        "Women's shirts",
        "Men's fashion",
        "Beauty under ₹800",
    ]


    for i, question in enumerate(
        quick_questions
    ):

        with quick_cols[i]:

            if st.button(
                question,
                key=f"welcome_{i}",
                use_container_width=True,
            ):

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": question,
                        "products": [],
                    }
                )

                products = recommend_products(
                    question
                )

                answer = ask_ai(
                    question,
                    products
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "products": [
                            p["id"]
                            for p in products
                        ],
                    }
                )

                st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for i, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


        product_ids = message.get(
            "products",
            []
        )


        if product_ids:

            products = [
                get_product(pid)
                for pid in product_ids
            ]

            products = [
                p for p in products
                if p
            ]

            display_products(
                products,
                f"chat_{i}"
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask NOVA about fashion, beauty or products..."
)


if question:

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "products": [],
        }
    )


    # Find products

    products = recommend_products(
        question
    )


    # AI response

    answer = ask_ai(
        question,
        products
    )


    # Assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "products": [
                p["id"]
                for p in products
            ],
        }
    )


    st.rerun()


# ============================================================
# CATEGORY BROWSE
# ============================================================

if category != "All":

    st.divider()

    st.subheader(
        f"Browse {category}"
    )


    visible_products = [
        p
        for p in PRODUCTS
        if p["category"] == category
    ]


    for start in range(
        0,
        len(visible_products),
        4
    ):

        row = visible_products[
            start:start + 4
        ]

        cols = st.columns(4)


        for i, product in enumerate(row):

            with cols[i]:

                st.markdown(
                    '<div class="product-card">',
                    unsafe_allow_html=True
                )

                display_product(
                    product,
                    f"browse_{category}_{start}_{i}"
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# ============================================================
# CART
# ============================================================

if st.session_state.cart:

    st.divider()

    with st.expander(
        f"🛒 Cart ({len(st.session_state.cart)})"
    ):

        cart_products = [
            get_product(pid)
            for pid in st.session_state.cart
        ]

        cart_products = [
            p for p in cart_products
            if p
        ]


        total = sum(
            p["price"]
            for p in cart_products
        )


        for product in cart_products:

            st.write(
                f"**{product['name']}** — "
                f"₹{product['price']:,}"
            )


        st.success(
            f"Cart total: ₹{total:,}"
        )


# ============================================================
# WISHLIST
# ============================================================

if st.session_state.wishlist:

    st.divider()

    with st.expander(
        f"❤️ Wishlist ({len(st.session_state.wishlist)})"
    ):

        wish_products = [
            get_product(pid)
            for pid in st.session_state.wishlist
        ]

        wish_products = [
            p for p in wish_products
            if p
        ]


        for product in wish_products:

            st.write(
                f"**{product['name']}** — "
                f"₹{product['price']:,}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NOVA AI • Fashion • Beauty • Smart Shopping"
)
```
