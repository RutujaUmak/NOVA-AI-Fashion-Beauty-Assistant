
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
