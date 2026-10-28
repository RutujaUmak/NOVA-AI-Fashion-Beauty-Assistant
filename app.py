
import os
import uuid
import requests
import streamlit as st
from supabase import create_client
from groq import Groq

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="🛍️",
    layout="wide",
)

# -------------------- CONFIGURATION --------------------

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name, default)
        if value:
            return value
    except Exception:
        pass
    return os.getenv(name, default)


SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")
GROQ_API_KEY = get_secret("GROQ_API_KEY")
GROQ_MODEL = get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")
VTON_API_KEY = get_secret("VTON_API_KEY")

# TryOnLabs documented API endpoints.
VTON_GENERATE_URL = "https://api.tryonlabs.ai/api/v1/vton/generate/"
VTON_DOWNLOAD_URL = "https://api.tryonlabs.ai/api/v1/vton/download/"

# -------------------- DEMO PRODUCT CATALOGUE --------------------
# These are illustrative listings. Replace sample photos/details
# with verified product information and images you have permission to use.

DEMO_PRODUCTS = [
    {
        "id": "NOVA001",
        "name": "Floral Printed Kurti",
        "category": "Women Ethnic",
        "price": 399, "mrp": 899, "rating": 4.2,
        "color": "Pink", "sizes": "S, M, L, XL",
        "image_url": "https://images.unsplash.com/photo-1583391733956-6c78276477e3?auto=format&fit=crop&w=700&q=85",
        "description": "Everyday ethnic fashion",
    },
    {
        "id": "NOVA002",
        "name": "Elegant Festive Saree",
        "category": "Women Ethnic",
        "price": 799, "mrp": 1599, "rating": 4.4,
        "color": "Wine", "sizes": "Free Size",
        "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=85",
        "description": "Festive and traditional wear",
    },
    {
        "id": "NOVA003",
        "name": "Casual Everyday Top",
        "category": "Women Western",
        "price": 249, "mrp": 599, "rating": 4.1,
        "color": "White", "sizes": "XS, S, M, L, XL",
        "image_url": "https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=700&q=85",
        "description": "Casual college and office wear",
    },
    {
        "id": "NOVA004",
        "name": "Floral Summer Dress",
        "category": "Women Western",
        "price": 499, "mrp": 999, "rating": 4.3,
        "color": "Blue", "sizes": "S, M, L, XL",
        "image_url": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=700&q=85",
        "description": "Colourful daytime outfit",
    },
    {
        "id": "NOVA005",
        "name": "Men's Casual Shirt",
        "category": "Men Fashion",
        "price": 449, "mrp": 899, "rating": 4.0,
        "color": "Blue", "sizes": "M, L, XL, XXL",
        "image_url": "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=700&q=85",
        "description": "Classic everyday shirt",
    },
    {
        "id": "NOVA006",
        "name": "Basic Cotton T-shirt",
        "category": "Men Fashion",
        "price": 229, "mrp": 499, "rating": 4.1,
        "color": "Black", "sizes": "S, M, L, XL, XXL",
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=700&q=85",
        "description": "Comfortable everyday basic",
    },
    {
        "id": "NOVA007",
        "name": "Everyday Shoulder Bag",
        "category": "Bags & Accessories",
        "price": 549, "mrp": 1199, "rating": 4.3,
        "color": "Tan", "sizes": "One Size",
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=700&q=85",
        "description": "Compact everyday handbag",
    },
    {
        "id": "NOVA008",
        "name": "Statement Earrings",
        "category": "Jewellery",
        "price": 179, "mrp": 399, "rating": 4.0,
        "color": "Gold", "sizes": "One Size",
        "image_url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=700&q=85",
        "description": "Statement jewellery",
    },
    {
        "id": "NOVA009",
        "name": "Skincare Essentials",
        "category": "Beauty",
        "price": 349, "mrp": 699, "rating": 4.1,
        "color": "Mixed", "sizes": "Set",
        "image_url": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=700&q=85",
        "description": "Demo skincare bundle; check ingredients",
    },
    {
        "id": "NOVA010",
        "name": "Makeup Essentials Kit",
        "category": "Beauty",
        "price": 399, "mrp": 899, "rating": 4.0,
        "color": "Mixed", "sizes": "Kit",
        "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=700&q=85",
        "description": "Beauty and makeup collection",
    },
    {
        "id": "NOVA011",
        "name": "Comfortable Women's Flats",
        "category": "Footwear",
        "price": 299, "mrp": 699, "rating": 4.1,
        "color": "Beige", "sizes": "36–41",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=700&q=85",
        "description": "Everyday casual footwear",
    },
    {
        "id": "NOVA012",
        "name": "Minimal Home Cushion Covers",
        "category": "Home & Living",
        "price": 199, "mrp": 499, "rating": 4.0,
        "color": "Multicolor", "sizes": "Set of 2",
        "image_url": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=700&q=85",
        "description": "Simple home decor update",
    },
]

# -------------------- DATABASE --------------------

@st.cache_resource
def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def load_products():
    db = get_supabase()
    if db:
        try:
            result = (
                db.table("products")
                .select("*")
                .eq("active", True)
                .execute()
            )
            if result.data:
                return result.data
        except Exception as exc:
            st.warning(
                "Supabase product query failed. Showing demo catalogue. "
                f"Check schema and permissions. Details: {exc}"
            )
    return DEMO_PRODUCTS


def save_cart_item(product_id, quantity):
    db = get_supabase()
    session_id = st.session_state.session_id
    if db:
        try:
            if quantity <= 0:
                db.table("cart_items").delete().eq(
                    "session_id", session_id
                ).eq("product_id", product_id).execute()
            else:
                db.table("cart_items").upsert(
                    {
                        "session_id": session_id,
                        "product_id": product_id,
                        "quantity": quantity,
                    },
                    on_conflict="session_id,product_id",
                ).execute()
        except Exception as exc:
            st.error(f"Could not save cart to Supabase: {exc}")
            return False
    return True


def save_wishlist_item(product_id, should_add):
    db = get_supabase()
    session_id = st.session_state.session_id
    if db:
        try:
            if should_add:
                db.table("wishlist_items").upsert(
                    {
                        "session_id": session_id,
                        "product_id": product_id,
                    },
                    on_conflict="session_id,product_id",
                ).execute()
            else:
                db.table("wishlist_items").delete().eq(
                    "session_id", session_id
                ).eq("product_id", product_id).execute()
        except Exception as exc:
            st.error(f"Could not save wishlist to Supabase: {exc}")
            return False
    return True


def load_saved_items(table):
    db = get_supabase()
    if not db:
        return []
    try:
        result = (
            db.table(table)
            .select("*")
            .eq("session_id", st.session_state.session_id)
            .execute()
        )
        return result.data or []
    except Exception:
        return []


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "cart" not in st.session_state:
    st.session_state.cart = {}
    for item in load_saved_items("cart_items"):
        st.session_state.cart[item["product_id"]] = item["quantity"]
if "wishlist" not in st.session_state:
    st.session_state.wishlist = {
        item["product_id"] for item in load_saved_items("wishlist_items")
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

products = load_products()
product_by_id = {p["id"]: p for p in products}
categories = ["All"] + sorted({p["category"] for p in products})

# -------------------- STYLE --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:#fffafd;}
.block-container {padding-top:1.2rem;max-width:1500px;}
.nova-banner {
  background:linear-gradient(115deg,#70164d,#bd2676,#f3a1c7);
  color:white;padding:25px;border-radius:18px;margin-bottom:18px;
}
.nova-logo {font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:700;}
.nova-tagline {font-size:1rem;opacity:.96;}
.promo {background:#fff0f6;border:1px solid #f5c5da;padding:12px 16px;
border-radius:12px;margin:10px 0 20px;color:#79234f;}
.price {font-weight:750;font-size:1.12rem;color:#1e1720;}
.old-price {text-decoration:line-through;color:#938895;font-size:.85rem;}
.product-name {font-weight:650;min-height:2.8rem;}
div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:14px;}
button[kind="primary"] {background:#a21caf;border-color:#a21caf;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nova-banner">
  <div class="nova-logo">NOVA AI</div>
  <div style="font-size:1.08rem;font-weight:600">FASHION & BEAUTY</div>
  <div class="nova-tagline">
    Discover your style · Affordable finds · AI-powered shopping
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------- NAVIGATION AND FILTERS --------------------

with st.sidebar:
    st.markdown("## 🛍️ NOVA AI")
    page = st.radio(
        "Navigate",
        ["Shop", "AI Style Studio", "NOVA Chatbot", "My Cart", "Wishlist"],
    )
    st.divider()
    search = st.text_input("🔎 Search products", placeholder="Kurti, saree, makeup...")
    category = st.selectbox("Category", categories)
    max_price = st.slider("Maximum price (₹)", 100, 5000, 2000, 50)
    min_rating = st.selectbox("Minimum rating", ["Any", "3.5", "4.0", "4.5"])
    sort_by = st.selectbox(
        "Sort products",
        ["Recommended", "Price: Low to High", "Price: High to Low", "Top Rated"],
    )

def filtered_products():
    items = products.copy()
    query = search.strip().lower()
    if query:
        items = [
            p for p in items
            if query in (
                str(p.get("name", "")) + " " +
                str(p.get("category", "")) + " " +
                str(p.get("description", "")) + " " +
                str(p.get("color", ""))
            ).lower()
        ]
    if category != "All":
        items = [p for p in items if p.get("category") == category]
    items = [p for p in items if float(p.get("price", 0)) <= max_price]
    if min_rating != "Any":
        items = [
            p for p in items
            if float(p.get("rating", 0)) >= float(min_rating)
        ]
    if sort_by == "Price: Low to High":
        items.sort(key=lambda p: float(p.get("price", 0)))
    elif sort_by == "Price: High to Low":
        items.sort(key=lambda p: float(p.get("price", 0)), reverse=True)
    elif sort_by == "Top Rated":
        items.sort(key=lambda p: float(p.get("rating", 0)), reverse=True)
    return items


def product_card(p):
    pid = p["id"]
    price = float(p.get("price", 0))
    mrp = float(p.get("mrp", price))
    discount = round((1 - price / mrp) * 100) if mrp else 0

    with st.container(border=True):
        try:
            st.image(p["image_url"], use_container_width=True)
        except Exception:
            st.info("Product image unavailable")
        st.markdown(
            f'<div class="product-name">{p["name"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<span class="price">₹{price:.0f}</span> '
            f'<span class="old-price">₹{mrp:.0f}</span> '
            f'<span style="color:#16803d">{discount}% off</span>',
            unsafe_allow_html=True,
        )
        st.caption(
            f'⭐ {p.get("rating", "N/A")} · {p.get("category", "")}'
        )
        st.caption(p.get("description", ""))

        left, right = st.columns(2)
        with left:
            if st.button("♡ Wishlist", key=f"wish_{pid}", use_container_width=True):
                adding = pid not in st.session_state.wishlist
                if save_wishlist_item(pid, adding):
                    if adding:
                        st.session_state.wishlist.add(pid)
                    else:
                        st.session_state.wishlist.discard(pid)
                    st.rerun()
        with right:
            if st.button("Add to cart", key=f"add_{pid}",
                         type="primary", use_container_width=True):
                qty = st.session_state.cart.get(pid, 0) + 1
                if save_cart_item(pid, qty):
                    st.session_state.cart[pid] = qty
                    st.toast("Added to your NOVA cart!")
                    st.rerun()


# -------------------- SHOP --------------------

if page == "Shop":
    st.markdown(
        '<div class="promo">✨ <b>NOVA Style Days</b> — '
        'Discover fashion, beauty and lifestyle favourites.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Shop by category")
    category_columns = st.columns(min(6, len(categories) - 1 or 1))
    for col, cat in zip(category_columns, categories[1:]):
        with col:
            st.markdown(
                f"<div style='background:#fff0f6;border-radius:12px;"
                f"padding:12px;text-align:center;font-weight:600'>{cat}</div>",
                unsafe_allow_html=True,
            )

    items = filtered_products()
    st.markdown(f"### ✨ Products for you ({len(items)})")
    if not items:
        st.info("No matches. Try a different search or price range.")
    else:
        for start in range(0, len(items), 4):
            cols = st.columns(4, gap="medium")
            for col, p in zip(cols, items[start:start + 4]):
                with col:
                    product_card(p)

# -------------------- CART --------------------

elif page == "My Cart":
    st.markdown("## 🛒 My Cart")
    cart_items = [
        (product_by_id[pid], qty)
        for pid, qty in st.session_state.cart.items()
        if pid in product_by_id and qty > 0
    ]
    if not cart_items:
        st.info("Your cart is empty. Add products from the Shop page.")
    else:
        total = 0
        for p, qty in cart_items:
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                st.image(p["image_url"], width=90)
            with c2:
                st.markdown(f"**{p['name']}**")
                st.write(f"₹{p['price']} × {qty}")
            with c3:
                st.write(f"**₹{float(p['price']) * qty:.0f}**")
                new_qty = st.number_input(
                    "Quantity", min_value=0, max_value=20, value=qty,
                    key=f"quantity_{p['id']}",
                )
                if new_qty != qty:
                    if save_cart_item(p["id"], new_qty):
                        if new_qty == 0:
                            st.session_state.cart.pop(p["id"], None)
                        else:
                            st.session_state.cart[p["id"]] = new_qty
                        st.rerun()
            total += float(p["price"]) * qty
        st.divider()
        st.subheader(f"Subtotal: ₹{total:.0f}")
        st.caption("Demo only: payment and real order placement are not enabled.")

# -------------------- WISHLIST --------------------

elif page == "Wishlist":
    st.markdown("## ♡ My Wishlist")
    items = [p for p in products if p["id"] in st.session_state.wishlist]
    if not items:
        st.info("Your wishlist is empty.")
    else:
        for start in range(0, len(items), 4):
            cols = st.columns(4)
            for col, p in zip(cols, items[start:start + 4]):
                with col:
                    product_card(p)

# -------------------- AI STYLE STUDIO / VIRTUAL TRY-ON --------------------

elif page == "AI Style Studio":
    st.markdown("## 📸 NOVA AI Style Studio")
    st.write(
        "Upload a photo, select an outfit and generate a virtual try-on "
        "preview using a configured AI provider."
    )
    st.warning(
        "Use a photo you have permission to process. Style suggestions "
        "cannot guarantee a perfect fit or determine personal traits "
        "with 100% accuracy."
    )

    person_photo = st.file_uploader(
        "Upload your photo", type=["jpg", "jpeg", "png"]
    )
    outfit_products = [
        p for p in products
        if p.get("category") in ["Women Ethnic", "Women Western", "Men Fashion"]
    ]
    if not outfit_products:
        outfit_products = products

    chosen = st.selectbox(
        "Choose a garment",
        outfit_products,
        format_func=lambda p: f'{p["name"]} — ₹{p["price"]}',
    )
    occasion = st.selectbox(
        "Occasion", ["Everyday", "College", "Office", "Festive", "Party", "Travel"]
    )
    preference = st.selectbox(
        "Style preference",
        ["Comfortable", "Traditional", "Modern", "Minimal", "Bold colours"],
    )

    if person_photo:
        st.image(person_photo, caption="Your uploaded photo", width=220)

    if st.button("✨ Generate virtual try-on", type="primary"):
        if not person_photo:
            st.error("Please upload a photo first.")
        elif not VTON_API_KEY:
            st.error(
                "VTON_API_KEY is missing. Add a valid TryOnLabs API token "
                "to Streamlit Secrets."
            )
        else:
            try:
                # Fetch the selected catalogue garment as bytes.
                garment_response = requests.get(
                    chosen["image_url"], timeout=30
                )
                garment_response.raise_for_status()

                person_photo.seek(0)
                files = {
                    "person_image": (
                        person_photo.name,
                        person_photo.getvalue(),
                        person_photo.type,
                    ),
                    "garment_image": (
                        f'{chosen["id"]}.jpg',
                        garment_response.content,
                        "image/jpeg",
                    ),
                }
                response = requests.post(
                    VTON_GENERATE_URL,
                    headers={"Authorization": f"Bearer {VTON_API_KEY}"},
                    files=files,
                    data={
                        "resolution": "2k",
                        "generation_mode": "quality",
                    },
                    timeout=180,
                )
                response.raise_for_status()

                content_type = response.headers.get("content-type", "")
                if content_type.startswith("image/"):
                    st.image(response.content, caption="Virtual try-on result")
                else:
                    result = response.json()
                    experiment_id = result.get("id") or result.get("experiment_id")

                    if not experiment_id and isinstance(result.get("experiment"), dict):
                        experiment_id = (
                            result["experiment"].get("id")
                            or result["experiment"].get("experiment_id")
                        )

                    if not experiment_id:
                        st.error(
                            "The provider did not return an experiment ID. "
                            f"Response: {json_safe(result)}"
                        )
                    else:
                        with st.spinner("Generating your outfit preview..."):
                            download = requests.get(
                                VTON_DOWNLOAD_URL,
                                headers={
                                    "Authorization": f"Bearer {VTON_API_KEY}"
                                },
                                params={"experiment_id": experiment_id},
                                timeout=180,
                            )
                            download.raise_for_status()
                            if download.headers.get("content-type", "").startswith("image/"):
                                st.image(
                                    download.content,
                                    caption=f'AI try-on: {chosen["name"]}',
                                )
                            else:
                                st.error(
                                    "The download endpoint did not return an image. "
                                    "Check the provider response and API documentation."
                                )
                st.caption(
                    f"Selected occasion: {occasion}. Style preference: {preference}."
                )
            except requests.RequestException as exc:
                st.error(f"Virtual try-on API request failed: {exc}")
            except Exception as exc:
                st.error(f"Virtual try-on failed: {exc}")

# -------------------- CHATGPT-STYLE CHATBOT --------------------

elif page == "NOVA Chatbot":
    st.markdown("## 🤖 Chat with NOVA AI")
    st.caption("Ask for outfit ideas, products, categories and budget recommendations.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask NOVA AI anything about fashion or beauty...")
    if prompt:
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        catalogue_context = "\n".join(
            f'{p["id"]}: {p["name"]}, ₹{p["price"]}, '
            f'{p["category"]}, rating {p.get("rating", "N/A")}, '
            f'image {p["image_url"]}'
            for p in products
        )
        system_prompt = (
            "You are NOVA AI, a friendly Indian fashion and beauty shopping "
            "assistant. Give concise, useful answers. Use INR. Recommend only "
            "catalogue products when discussing NOVA inventory. Do not claim "
            "that prices, stock or reviews are live. Do not claim 100% accurate "
            "face analysis or medical/skin diagnoses. Catalogue:\n"
            + catalogue_context
        )

        answer = None
        if GROQ_API_KEY:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.chat_history[-12:])
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    temperature=0.4,
                    max_tokens=700,
                )
                answer = completion.choices[0].message.content
            except Exception as exc:
                st.warning(f"AI service is unavailable: {exc}")

        # Fallback if no Groq key is configured or the API call fails.
        if not answer:
            query = prompt.lower()
            matches = [
                p for p in products
                if any(
                    word in (
                        p["name"] + " " + p["category"] + " "
                        + p.get("description", "")
                    ).lower()
                    for word in query.split() if len(word) > 2
                )
            ]
            if "cheap" in query or "under" in query or "budget" in query:
                matches = sorted(
                    [p for p in products if float(p["price"]) <= 500],
                    key=lambda p: float(p["price"]),
                )[:5]
            if matches:
                answer = "Here are some catalogue matches:\n\n" + "\n".join(
                    f'- **{p["name"]}** — ₹{p["price"]} '
                    f'({p["category"]}, ⭐ {p.get("rating", "N/A")})'
                    for p in matches[:5]
                )
                answer += (
                    "\n\nThese are demo listings. Add GROQ_API_KEY in Secrets "
                    "to enable the full conversational AI."
                )
            else:
                answer = (
                    "I can help with outfit ideas, budget products, ethnic wear, "
                    "western wear, accessories and beauty items. Try asking "
                    "'show products under ₹500' or add a Groq API key for "
                    "full conversational answers."
                )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
        with st.chat_message("assistant"):
            st.markdown(answer)

    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.rerun()

# -------------------- FOOTER --------------------

st.divider()
st.caption(
    "NOVA AI | Fashion & Beauty · Independent demo project · "
    "Sample catalogue · Not affiliated with Meesho"
)
