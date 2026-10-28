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
