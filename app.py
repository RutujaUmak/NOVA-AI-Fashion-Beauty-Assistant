import os
import io
import time
import uuid
import requests
import streamlit as st
from PIL import Image
from supabase import create_client
from groq import Groq

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
    {"id":"NOVA001","name":"Floral Printed Kurti","category":"Women Ethnic","price":399,"mrp":899,"rating":4.2,"color":"Pink","sizes":"S, M, L, XL","image_url":"https://images.unsplash.com/photo-1583391733956-6c78276477e3?auto=format&fit=crop&w=700&q=85","description":"Everyday ethnic style"},
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

if page == "AI Style Studio":
    st.markdown("## 📸 NOVA AI Style Studio")
    st.write("Upload a photo and choose a garment for a virtual try-on.")
    st.warning(
        "Use a photo you have permission to process. AI previews can alter garment "
        "details and body proportions; they do not guarantee size, fit, fabric or colour."
    )
    photo = st.file_uploader("Upload a front-facing or full-length photo",
                             type=["jpg","jpeg","png"])
    clothing = [p for p in products if p.get("category") in
                ["Women Ethnic","Women Western","Men Fashion"]]
    if not clothing:
        clothing = products
    garment = st.selectbox(
        "Select a product",
        clothing,
        format_func=lambda p:f'{p["name"]} — ₹{p["price"]}',
    )
    occasion = st.selectbox(
        "Occasion",["Everyday","College","Office","Festive","Party","Travel"]
    )
    style = st.selectbox(
        "Style preference",["Comfortable","Traditional","Modern","Minimal","Bold colours"]
    )

    if photo:
        st.image(photo,caption="Photo preview",width=230)
        if st.button("Estimate face shape (optional)"):
            shape, note = estimate_face_shape(photo.getvalue())
            if shape:
                st.success(f"Approximate result: **{shape}**")
                suggestions = {
                    "Oval / long":"Try balanced necklines, layered looks and varied earring lengths.",
                    "Round / soft":"Try open necklines, structured layers or longer accessories if you like them.",
                    "Square / strong jaw":"Try soft draping, rounded necklines or curved accessories if preferred.",
                    "Heart / wider forehead":"Try balanced necklines and accessories that add visual balance.",
                    "Balanced / oval-like":"Experiment with different necklines, silhouettes and accessories.",
                }
                st.write(suggestions.get(shape,"Try the styles you feel comfortable wearing."))
            st.caption(note)
    if st.button("Generate AI virtual try-on",type="primary"):
    if st.button("Generate AI virtual try-on", type="primary"):
        if not photo:
            st.error("Upload a photo first.")
        elif not VTON_API_KEY:
            st.error("Add VTON_API_KEY to Streamlit Secrets.")
        else:
            try:
                garment_resp = requests.get(garment["image_url"],timeout=30)
                garment_resp.raise_for_status()
                # 1. Download the selected garment image.
                image_url = garment.get("image_url", "").strip()

                if not image_url.startswith("https://"):
                    st.error("The selected product has an invalid image URL.")
                    st.stop()

                garment_resp = requests.get(
                    image_url,
                    timeout=30,
                    headers={"User-Agent": "NOVA-AI/1.0"},
                )

                if garment_resp.status_code != 200:
                    st.error(
                        f"Product image unavailable "
                        f"(HTTP {garment_resp.status_code}). "
                        "Replace this product's image_url with a working "
                        "public HTTPS image URL."
                    )
                    st.stop()

                content_type = garment_resp.headers.get(
                    "Content-Type", ""
                ).split(";")[0].lower()

                if content_type not in ("image/jpeg", "image/png", "image/webp"):
                    st.error("The product URL did not return a supported image.")
                    st.stop()

                # Verify the downloaded image can be opened.
                from PIL import Image
                from io import BytesIO

                garment_bytes = garment_resp.content
                Image.open(BytesIO(garment_bytes)).verify()

                # 2. Prepare the selfie and garment as uploaded files.
                person_bytes = photo.getvalue()
                person_type = photo.type or "image/jpeg"

                files = {
                    "person_image":(photo.name,photo.getvalue(),photo.type),
                    "garment_image":("garment.jpg",garment_resp.content,"image/jpeg"),
                    "person_image": (
                        photo.name or "person.jpg",
                        person_bytes,
                        person_type,
                    ),
                    "garment_image": (
                        "garment.png" if content_type == "image/png"
                        else "garment.jpg",
                        garment_bytes,
                        content_type,
                    ),
                }

                # 3. Send the request to TryOn AI, not to Unsplash.
                response = requests.post(
                    VTON_URL,
                    headers={"Authorization":f"Bearer {VTON_API_KEY}"},
                    "https://api.tryonlabs.ai/api/v1/vton/generate/",
                    headers={
                        "Authorization": f"Bearer {VTON_API_KEY}"
                    },
                    files=files,
                    data={"resolution":"2k","generation_mode":"quality"},
                    data={
                        "resolution": "2k",
                        "generation_mode": "quality",
                    },
                    timeout=240,
                )
                response.raise_for_status()

                if not response.ok:
                    st.error(
                        f"TryOn AI returned HTTP {response.status_code}: "
                        f"{response.text[:1000]}"
                    )
                    st.stop()

                payload = response.json()
                experiment_id = payload.get("id") or payload.get("experiment_id")
                if not experiment_id and isinstance(payload.get("experiment"),dict):
                experiment_id = (
                    payload.get("id")
                    or payload.get("experiment_id")
                )

                if not experiment_id and isinstance(
                    payload.get("experiment"), dict
                ):
                    experiment_id = payload["experiment"].get("id")

                if not experiment_id:
                    st.error(f"API did not return an experiment ID: {str(payload)[:1000]}")
                else:
                    result = requests.get(
                        VTON_DOWNLOAD_URL,
                        headers={"Authorization":f"Bearer {VTON_API_KEY}"},
                        params={"experiment_id":experiment_id},
                        timeout=180,
                    st.error(
                        "The API response did not contain an experiment ID: "
                        + str(payload)[:1000]
                    )
                    result.raise_for_status()
                    if not result.headers.get("content-type","").startswith("image/"):
                        st.error("Try-on download did not return an image.")
                    else:
                        st.session_state.tryon_image = result.content
                        st.image(result.content,caption=f"AI preview: {garment['name']}")
                        st.success("Try-on image generated. Review it carefully; it is not a fit guarantee.")
                        st.caption(f"Occasion: {occasion} · Style: {style}")
                    st.stop()

                # 4. Download the generated try-on result.
                result = requests.get(
                    "https://api.tryonlabs.ai/api/v1/vton/download/",
                    headers={
                        "Authorization": f"Bearer {VTON_API_KEY}"
                    },
                    params={"experiment_id": experiment_id},
                    timeout=180,
                )
                result.raise_for_status()

                result_type = result.headers.get(
                    "Content-Type", ""
                ).split(";")[0].lower()

                if result_type not in (
                    "image/png", "image/jpeg", "image/webp"
                ):
                    st.error(
                        "The provider did not return an image. "
                        f"Response type: {result_type or 'unknown'}. "
                        f"Response: {result.text[:500]}"
                    )
                    st.stop()

                # 5. Display and allow downloading the result.
                result_image = Image.open(BytesIO(result.content))
                st.success("Virtual try-on generated!")
                st.image(
                    result_image,
                    caption=f"NOVA AI try-on preview — {garment['name']}",
                    use_container_width=True,
                )

                output = BytesIO()
                result_image.save(output, format="PNG")

                st.download_button(
                    "Download try-on image",
                    data=output.getvalue(),
                    file_name="nova_ai_tryon.png",
                    mime="image/png",
                )

            except requests.RequestException as exc:
                st.error(f"Network/API request failed: {exc}")
            except Exception as exc:
                st.error(f"Try-on API failed. Check your provider access and request format: {exc}")
                st.error(f"Virtual try-on failed: {exc}")

    # Video generation from the generated try-on image.
    st.divider()
    st.markdown("### 🎬 Generate a short fashion video")
    st.caption(
        "This calls the provider's video-generation API. Results may be a short "
        "fashion motion clip, not a true 360-degree 3D reconstruction."
    )
    if st.button("Generate video from latest try-on"):
        if not st.session_state.tryon_image:
            st.error("Generate a try-on image first.")
        elif not VTON_API_KEY:
            st.error("Add VTON_API_KEY to Streamlit Secrets.")
        else:
            try:
                video_prompt = (
                    "Create a short fashion product showcase video based on the "
                    "provided image. Keep the outfit and person's appearance as "
                    "consistent as possible. Slow camera orbit, studio lighting, "
                    "plain background. Do not claim exact garment fit."
                )
                video_response = requests.post(
                    VIDEO_URL,
                    headers={"Authorization":f"Bearer {VTON_API_KEY}"},
                    files={"image":("tryon.png",st.session_state.tryon_image,"image/png")},
                    data={
                        "prompt":video_prompt,
                        "duration":"8",
                        "resolution":"1080p",
                        "aspect_ratio":"9:16",
                    },
                    timeout=90,
                )
                video_response.raise_for_status()
                video_data = video_response.json()
                generation_id = video_data.get("generation_id") or video_data.get("id")
                if not generation_id:
                    st.error(f"Video API did not return a generation ID: {str(video_data)[:1000]}")
                else:
                    progress = st.progress(0)
                    status_box = st.empty()
                    completed = False
                    for attempt in range(24):
                        status_response = requests.get(
                            VIDEO_STATUS_URL,
                            headers={"Authorization":f"Bearer {VTON_API_KEY}"},
                            params={"generation_id":generation_id},
                            timeout=30,
                        )
                        status_response.raise_for_status()
                        status_data = status_response.json()
                        status = str(status_data.get("status","")).lower()
                        status_box.write(f"Video status: {status or 'processing'}")
                        progress.progress(min((attempt+1)/24,0.95))
                        if status in ["completed","complete","succeeded","success"]:
                            completed = True
                            break
                        if status in ["failed","error","cancelled"]:
                            st.error(f"Video generation failed: {status_data}")
                            break
                        time.sleep(5)
                    if completed:
                        video_result = requests.get(
                            VIDEO_DOWNLOAD_URL,
                            headers={"Authorization":f"Bearer {VTON_API_KEY}"},
                            params={"generation_id":generation_id},
                            timeout=180,
                        )
                        video_result.raise_for_status()
                        if video_result.headers.get("content-type","").startswith("video/") or video_result.content[:4] == b"\x00\x00\x00\x18":
                            st.video(video_result.content)
                            st.download_button(
                                "Download generated video",
                                data=video_result.content,
                                file_name="nova_ai_tryon_preview.mp4",
                                mime="video/mp4",
                            )
                            progress.progress(1.0)
                        else:
                            try:
                                result_json = video_result.json()
                                video_url = result_json.get("download_url") or result_json.get("video_url")
                                if video_url and video_url.startswith("https://"):
                                    st.video(video_url)
                                else:
                                    st.error(f"Video download response was not an MP4: {str(result_json)[:1000]}")
                            except Exception:
                                st.error("Video endpoint returned an unexpected format.")
                    elif not completed:
                        st.warning("Video is still processing or timed out. Try again later.")
            except Exception as exc:
                st.error(f"Video generation failed: {exc}")

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
