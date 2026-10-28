import os
import io
import time
import uuid
import requests
import streamlit as st
from PIL import Image, ImageOps, ImageDraw
from supabase import create_client
from groq import Groq
import streamlit.components.v1 as components

# Optional: install mediapipe to enable approximate face-shape estimation.
try:
    import mediapipe as mp
    FACE_ANALYSIS_AVAILABLE = True
except Exception:
    FACE_ANALYSIS_AVAILABLE = False

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="🛍️",
    layout="wide",
)

# ==================== SECRETS ====================

def secret(name, default=""):
    try:
        value = st.secrets.get(name, default)
        if value:
            return value
    except Exception:
        pass
    return os.getenv(name, default)

SUPABASE_URL = secret("SUPABASE_URL")
SUPABASE_KEY = secret("SUPABASE_KEY")
GROQ_API_KEY = secret("GROQ_API_KEY")
GROQ_MODEL = secret("GROQ_MODEL", "llama-3.3-70b-versatile")
VTON_API_KEY = secret("VTON_API_KEY")

VTON_URL = "https://api.tryonlabs.ai/api/v1/vton/generate/"
VTON_DOWNLOAD_URL = "https://api.tryonlabs.ai/api/v1/vton/download/"
VIDEO_URL = "https://api.tryonlabs.ai/api/v1/video/generate/"
VIDEO_STATUS_URL = "https://api.tryonlabs.ai/api/v1/video/status/"
VIDEO_DOWNLOAD_URL = "https://api.tryonlabs.ai/api/v1/video/download/"

# ==================== PRODUCT CATALOGUE ====================
# Sample catalogue. Replace these URLs with genuine photos of each
# exact product before commercial use. Sample prices are not live prices.

PRODUCTS = [
    {"id":"NOVA001","name":"Floral Printed Kurta Set","category":"Women Ethnic","price":499,"mrp":999,"rating":4.2,"color":"Cream & Orange","sizes":"S, M, L, XL","image_url":"https://fashor.com/cdn/shop/files/27266_13.jpg?v=1749480577","description":"Floral printed kurta with matching trousers and dupatta"},
    {"id":"NOVA002","name":"Festive Saree","category":"Women Ethnic","price":799,"mrp":1599,"rating":4.4,"color":"Wine","sizes":"Free Size","image_url":"https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=85","description":"Festive traditional wear"},
    {"id":"NOVA003","name":"Casual Everyday Top","category":"Women Western","price":249,"mrp":599,"rating":4.1,"color":"White","sizes":"XS, S, M, L, XL","image_url":"https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=700&q=85","description":"College and office wear"},
    {"id":"NOVA004","name":"Floral Summer Dress","category":"Women Western","price":499,"mrp":999,"rating":4.3,"color":"Blue","sizes":"S, M, L, XL","image_url":"https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=700&q=85","description":"Daytime summer outfit"},
    {"id":"NOVA005","name":"Men's Casual Shirt","category":"Men Fashion","price":449,"mrp":899,"rating":4.0,"color":"Blue","sizes":"M, L, XL, XXL","image_url":"https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=700&q=85","description":"Classic casual shirt"},
    {"id":"NOVA006","name":"Basic Cotton T-shirt","category":"Men Fashion","price":229,"mrp":499,"rating":4.1,"color":"Black","sizes":"S, M, L, XL, XXL","image_url":"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=700&q=85","description":"Everyday cotton basic"},
    {"id":"NOVA007","name":"Shoulder Handbag","category":"Bags & Accessories","price":549,"mrp":1199,"rating":4.3,"color":"Tan","sizes":"One Size","image_url":"https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=700&q=85","description":"Compact everyday handbag"},
    {"id":"NOVA008","name":"Statement Earrings","category":"Jewellery","price":179,"mrp":399,"rating":4.0,"color":"Gold","sizes":"One Size","image_url":"https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=700&q=85","description":"Statement jewellery"},
    {"id":"NOVA009","name":"Skincare Essentials","category":"Beauty","price":349,"mrp":699,"rating":4.1,"color":"Mixed","sizes":"Set","image_url":"https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=700&q=85","description":"Demo skincare bundle"},
    {"id":"NOVA010","name":"Makeup Essentials Kit","category":"Beauty","price":399,"mrp":899,"rating":4.0,"color":"Mixed","sizes":"Kit","image_url":"https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=700&q=85","description":"Makeup and beauty collection"},
    {"id":"NOVA011","name":"Women's Flats","category":"Footwear","price":299,"mrp":699,"rating":4.1,"color":"Beige","sizes":"36-41","image_url":"https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=700&q=85","description":"Everyday casual footwear"},
    {"id":"NOVA012","name":"Cushion Cover Set","category":"Home & Living","price":199,"mrp":499,"rating":4.0,"color":"Multicolor","sizes":"Set of 2","image_url":"https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=700&q=85","description":"Home decor refresh"},
    {"id":"NOVA013","name":"Minimal Sneakers","category":"Footwear","price":599,"mrp":1299,"rating":4.3,"color":"White","sizes":"36-44","image_url":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=700&q=85","description":"Sporty casual sneakers"},
    {"id":"NOVA014","name":"Gold Tone Necklace","category":"Jewellery","price":299,"mrp":699,"rating":4.2,"color":"Gold","sizes":"One Size","image_url":"https://images.unsplash.com/photo-1611652022419-a9419f74343d?auto=format&fit=crop&w=700&q=85","description":"Traditional accessory"},
    {"id":"NOVA015","name":"Travel Backpack","category":"Bags & Accessories","price":499,"mrp":999,"rating":4.2,"color":"Black","sizes":"One Size","image_url":"https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=700&q=85","description":"College and travel bag"},
    {"id":"NOVA016","name":"Tinted Lip Balm","category":"Beauty","price":149,"mrp":299,"rating":4.1,"color":"Rose","sizes":"4 g","image_url":"https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=700&q=85","description":"Check ingredients and expiry"},
    {"id":"NOVA017","name":"Men's Ethnic Kurta","category":"Men Fashion","price":499,"mrp":999,"rating":4.3,"color":"Cream","sizes":"M, L, XL, XXL","image_url":"https://images.unsplash.com/photo-1617137968427-85924c800a22?auto=format&fit=crop&w=700&q=85","description":"Traditional occasion wear"},
    {"id":"NOVA018","name":"Printed Cotton Saree","category":"Women Ethnic","price":599,"mrp":1199,"rating":4.0,"color":"Green","sizes":"Free Size","image_url":"https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=700&q=85","description":"Printed ethnic drape"},
    {"id":"NOVA019","name":"Casual Summer Outfit","category":"Women Western","price":449,"mrp":899,"rating":4.2,"color":"Multicolor","sizes":"S, M, L, XL","image_url":"https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=700&q=85","description":"Casual seasonal fashion"},
    {"id":"NOVA020","name":"Reusable Water Bottle","category":"Home & Living","price":249,"mrp":499,"rating":4.2,"color":"Pink","sizes":"750 ml","image_url":"https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=700&q=85","description":"Reusable daily bottle"},
]

# ==================== SUPABASE ====================

@st.cache_resource
def get_db():
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

def get_products():
    db = get_db()
    if db:
        try:
            result = db.table("products").select("*").eq("active", True).execute()
            if result.data:
                return result.data
        except Exception as exc:
            st.warning(f"Supabase catalogue unavailable; using demo products. {exc}")
    return PRODUCTS

if "sid" not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "wishlist" not in st.session_state:
    st.session_state.wishlist = set()
if "chat" not in st.session_state:
    st.session_state.chat = []
if "tryon_image" not in st.session_state:
    st.session_state.tryon_image = None

products = get_products()
product_map = {p["id"]: p for p in products}
categories = ["All"] + sorted({p.get("category", "Other") for p in products})

def save_item(table, product_id, quantity=None, remove=False):
    db = get_db()
    if not db:
        return True
    try:
        query = db.table(table)
        if remove:
            query.delete().eq("session_id", st.session_state.sid).eq(
                "product_id", product_id
            ).execute()
        else:
            row = {"session_id": st.session_state.sid, "product_id": product_id}
            if quantity is not None:
                row["quantity"] = quantity
            query.upsert(row).execute()
        return True
    except Exception as exc:
        st.error(f"Database save failed: {exc}")
        return False

# ==================== DESIGN ====================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#fffafd}
.block-container{padding-top:1rem;max-width:1500px}
.nova-banner{background:linear-gradient(110deg,#70164d,#b62574,#ef9dc4);
color:white;padding:24px;border-radius:18px;margin-bottom:18px}
.logo{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:700}
.tagline{font-size:1rem}
.promo{background:#fff0f6;border:1px solid #f5c5da;padding:12px 16px;
border-radius:12px;color:#79234f;margin:12px 0 18px}
.price{font-size:1.15rem;font-weight:750;color:#211822}
.old{color:#938895;text-decoration:line-through;font-size:.85rem}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nova-banner">
 <div class="logo">NOVA AI</div>
 <b>FASHION & BEAUTY</b>
 <div class="tagline">Discover your style · Affordable finds · AI-powered shopping</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛍️ Shop NOVA")
    page = st.radio(
        "Menu",
        ["Shop", "AI Style Studio", "NOVA Chatbot", "My Cart", "Wishlist", "Project Info"]
    )
    st.divider()
    search = st.text_input("Search", placeholder="Kurti, saree, makeup...")
    category = st.selectbox("Category", categories)
    max_price = st.slider("Maximum price ₹", 100, 5000, 2000, 50)
    rating_min = st.selectbox("Minimum rating", ["Any", "3.5", "4.0", "4.5"])

def filtered():
    result = products.copy()
    q = search.lower().strip()
    if q:
        result = [p for p in result if q in (
            str(p.get("name","")) + " " + str(p.get("category","")) + " "
            + str(p.get("description","")) + " " + str(p.get("color",""))
        ).lower()]
    if category != "All":
        result = [p for p in result if p.get("category") == category]
    result = [p for p in result if float(p.get("price", 0)) <= max_price]
    if rating_min != "Any":
        result = [p for p in result if float(p.get("rating",0)) >= float(rating_min)]
    return result

def product_card(p):
    pid = p["id"]
    price = float(p.get("price",0))
    mrp = float(p.get("mrp",price))
    discount = round(100 * (1 - price/mrp)) if mrp else 0
    with st.container(border=True):
        st.image(p["image_url"], use_container_width=True)
        st.markdown(f"**{p['name']}**")
        st.markdown(
            f'<span class="price">₹{price:.0f}</span> '
            f'<span class="old">₹{mrp:.0f}</span> '
            f'<span style="color:green">{discount}% off</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"⭐ {p.get('rating','N/A')} · {p.get('category','')}")
        st.caption(p.get("description",""))
        a,b = st.columns(2)
        with a:
            if st.button("♡ Wishlist", key=f"w_{pid}", use_container_width=True):
                adding = pid not in st.session_state.wishlist
                if save_item("wishlist_items", pid, remove=not adding):
                    if adding:
                        st.session_state.wishlist.add(pid)
                    else:
                        st.session_state.wishlist.discard(pid)
                    st.rerun()
        with b:
            if st.button("Add to cart", key=f"c_{pid}", type="primary",
                         use_container_width=True):
                qty = st.session_state.cart.get(pid,0)+1
                if save_item("cart_items",pid,quantity=qty):
                    st.session_state.cart[pid] = qty
                    st.toast("Added to NOVA cart")
                    st.rerun()

# ==================== SHOP ====================

if page == "Shop":
    st.markdown(
        '<div class="promo">✨ <b>NOVA Style Days</b> — Fashion, beauty, accessories and more.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Shop by category")
    catcols = st.columns(min(6, max(1, len(categories)-1)))
    for col, cat in zip(catcols, categories[1:]):
        with col:
            st.markdown(
                f"<div style='background:#fff0f6;border-radius:12px;padding:12px;text-align:center'>{cat}</div>",
                unsafe_allow_html=True,
            )
    items = filtered()
    st.markdown(f"### ✨ Products for you ({len(items)})")
    for start in range(0,len(items),4):
        cols = st.columns(4,gap="medium")
        for col,p in zip(cols,items[start:start+4]):
            with col:
                product_card(p)
    if not items:
        st.info("No products found. Change the filters.")

# ==================== CART ====================

elif page == "My Cart":
    st.markdown("## 🛒 My Cart")
    cart = [(product_map[pid],qty) for pid,qty in st.session_state.cart.items()
            if pid in product_map and qty > 0]
    if not cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for p,qty in cart:
            a,b,c = st.columns([1,3,1])
            with a:
                st.image(p["image_url"],width=85)
            with b:
                st.write(f"**{p['name']}**")
                st.write(f"₹{p['price']} × {qty}")
            with c:
                new_qty = st.number_input(
                    "Quantity",0,20,qty,key=f"qty_{p['id']}"
                )
                if new_qty != qty:
                    if save_item("cart_items",p["id"],quantity=new_qty,remove=new_qty==0):
                        if new_qty == 0:
                            st.session_state.cart.pop(p["id"],None)
                        else:
                            st.session_state.cart[p["id"]] = new_qty
                        st.rerun()
            total += float(p["price"])*qty
        st.divider()
        st.subheader(f"Subtotal: ₹{total:.0f}")
        st.caption("Demo only: payments and real orders are not enabled.")

# ==================== WISHLIST ====================

elif page == "Wishlist":
    st.markdown("## ♡ My Wishlist")
    items = [p for p in products if p["id"] in st.session_state.wishlist]
    if not items:
        st.info("Your wishlist is empty.")
    for start in range(0,len(items),4):
        cols = st.columns(4)
        for col,p in zip(cols,items[start:start+4]):
            with col:
                product_card(p)

# ==================== FACE-SHAPE ESTIMATE ====================

def estimate_face_shape(image_bytes):
    """Rough landmark-based shape estimate; not a beauty score or identity analysis."""
    if not FACE_ANALYSIS_AVAILABLE:
        return None, "Install mediapipe to enable optional face-shape estimation."
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        with mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5,
        ) as mesh:
            result = mesh.process(__import__("numpy").array(image))
        if not result.multi_face_landmarks:
            return None, "No clear face landmarks detected. Try a front-facing, well-lit photo."
        lm = result.multi_face_landmarks[0].landmark
        # Relative horizontal distances: forehead, cheek area, jaw and face height.
        forehead = abs(lm[103].x - lm[332].x)
        cheeks = abs(lm[234].x - lm[454].x)
        jaw = abs(lm[172].x - lm[397].x)
        height = abs(lm[10].y - lm[152].y)
        if min(forehead, cheeks, jaw, height) <= 0:
            return None, "Unable to estimate face proportions from this photo."
        ratio = height / cheeks
        if ratio > 1.45 and forehead > jaw * 1.12:
            shape = "Oval / long"
        elif ratio < 1.22 and abs(forehead-jaw)/max(forehead,jaw) < 0.18:
            shape = "Round / soft"
        elif jaw > forehead * 1.12:
            shape = "Square / strong jaw"
        elif forehead > jaw * 1.15:
            shape = "Heart / wider forehead"
        else:
            shape = "Balanced / oval-like"
        return shape, (
            "This is an approximate geometry-based suggestion. Hair, angle, "
            "lighting and landmark errors can change the result."
        )
    except Exception as exc:
        return None, f"Face-shape estimation unavailable: {exc}"

# ==================== STYLE STUDIO + TRY-ON ====================
 
# ==================== STYLE STUDIO + TRY-ON ====================

if page == "AI Style Studio":
    st.markdown("## ✨ NOVA AI Virtual Try-On Studio")
    st.write(
        "Preview how an outfit may look using an open-source AI model. "
        "This version does not use TryOn AI credits."
    )

    st.info(
        "For best results, prepare a clear person photo and a separate "
        "photo of the garment you want to try."
    )

    with st.expander("📸 Photo preparation tips", expanded=True):
        st.markdown("""
        - Use a clear, front-facing, well-lit photo.
        - Prefer an upper-body or full-body photo over an ID photo.
        - Use a garment image where the clothing is clearly visible.
        - Upload only photos you have permission to use.
        """)

    st.markdown("### 👗 AI Try-On")

    st.caption(
        "The hosted model performs the image generation. "
        "NOVA AI does not send requests to the paid TryOn AI API."
    )

    st.link_button(
        "Open IDM-VTON directly ↗",
        "https://huggingface.co/spaces/yisol/IDM-VTON",
        use_container_width=True,
    )

    st.markdown("#### Try it inside NOVA AI")

    components.iframe(
        "https://yisol-idm-vton.hf.space",
        height=900,
        scrolling=True,
    )

    st.caption(
        "If the embedded demo is blank, loading, or unavailable, "
        "open IDM-VTON directly using the button above."
    )

    st.warning(
        "The hosted demo may have queues, usage limits, or downtime. "
        "AI-generated images are previews and cannot guarantee exact "
        "clothing fit, size, colour, or fabric."
    )

# ==================== CHATBOT ====================

                      
                

# ==================== CHATBOT ====================

elif page == "NOVA Chatbot":
    st.markdown("## 🤖 Chat with NOVA AI")
    st.caption("Ask for outfit ideas, budget products or beauty catalogue suggestions.")
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("Ask NOVA AI...")
    if prompt:
        st.session_state.chat.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        context = "\n".join(
            f'{p["name"]}: ₹{p["price"]}, category {p["category"]}, '
            f'rating {p.get("rating","N/A")}, image {p["image_url"]}'
            for p in products
        )
        answer = None
        if GROQ_API_KEY:
            try:
                client = Groq(api_key=GROQ_API_KEY)
                messages = [{
                    "role":"system",
                    "content":(
                        "You are NOVA AI, a helpful Indian fashion and beauty assistant. "
                        "Use INR, recommend catalogue items only when naming store products, "
                        "and don't claim prices or stock are live. Never claim face analysis "
                        "or size/fit is 100% accurate. Catalogue:\n"+context
                    )
                }]
                messages += st.session_state.chat[-12:]
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    temperature=0.4,
                    max_tokens=700,
                )
                answer = completion.choices[0].message.content
            except Exception as exc:
                st.warning(f"AI service unavailable; using catalogue fallback. {exc}")
        if not answer:
            query = prompt.lower()
            matches = [p for p in products if any(
                word in (p["name"]+" "+p["category"]+" "+p["description"]).lower()
                for word in query.split() if len(word)>2
            )]
            if "under" in query or "cheap" in query or "budget" in query:
                matches = sorted(
                    [p for p in products if float(p["price"]) <= 500],
                    key=lambda p:float(p["price"])
                )[:5]
            answer = (
                "Here are some catalogue matches:\n\n" +
                "\n".join(
                    f'- **{p["name"]}** — ₹{p["price"]} · {p["category"]}'
                    for p in matches[:5]
                ) if matches else
                "Try asking about kurtis, sarees, western wear, jewellery, beauty or products under ₹500."
            )
        st.session_state.chat.append({"role":"assistant","content":answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
    if st.button("Clear chat"):
        st.session_state.chat = []
        st.rerun()

# ==================== PROJECT INFO ====================

elif page == "Project Info":
    st.markdown("## NOVA AI project information")
    st.write("Meesho-inspired independent shopping demo with AI styling.")
    st.markdown("""
- Product images are example URLs; verify they depict the exact listed product.
- Supabase stores products when the table is configured. The code uses a session ID for cart and wishlist; add real user authentication before production.
- Groq powers the conversational chatbot when its API key is configured.
- Try-on and video generation require an active TryOn AI API token and may consume credits.
- Face-shape output is approximate, not medical analysis or identity recognition.
- AI images cannot guarantee real-world sizing, fabric, colour or fit.
- Payment, shipping and production order management are not implemented.
""")
    st.markdown("[Meesho website](https://www.meesho.com/) · [TryOn AI documentation](https://docs.tryonlabs.ai/)")
    
st.divider()
st.caption("NOVA AI | Fashion & Beauty · Independent demo · Not affiliated with Meesho")
