import streamlit as st
from google import genai

# ---------- PAGE ----------
st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide"
)

# ---------- AI ---------- This sets:Application titlePage icon Wide layout
def get_client():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        return genai.Client(api_key=key) if key else None
    except Exception:
        return None

PRODUCTS = [
    {
        "id": 1,
        "name": "Floral Printed Kurta Set",
        "cat": "Women",
        "type": "Ethnic Wear",
        "price": 1499,
        "old": 2499,
        "rating": 4.5,
        "image": "https://images.pexels.com/photos/35504999/pexels-photo-35504999.jpeg"
    },

    {
        "id": 2,
        "name": "Pastel Oversized Shirt",
        "cat": "Women",
        "type": "Western Wear",
        "price": 899,
        "old": 1599,
        "rating": 4.3,
        "image": "https://images.pexels.com/photos/36899306/pexels-photo-36899306.jpeg"
    },

    {
        "id": 3,
        "name": "Classic Men's Casual Shirt",
        "cat": "Men",
        "type": "Western Wear",
        "price": 999,
        "old": 1799,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=700"
    },

    {
        "id": 4,
        "name": "Relaxed Fit Denim Jeans",
        "cat": "Men",
        "type": "Jeans",
        "price": 1299,
        "old": 2299,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=700"
    },

    {
        "id": 5,
        "name": "Hydrating Glow Serum",
        "cat": "Beauty",
        "type": "Skincare",
        "price": 799,
        "old": 1299,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700"
    },

    {
        "id": 6,
        "name": "Velvet Matte Lipstick",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 599,
        "old": 899,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=700"
    },

    {
        "id": 7,
        "name": "Minimal Gold Necklace",
        "cat": "Accessories",
        "type": "Jewellery",
        "price": 699,
        "old": 1199,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=700"
    },

    {
        "id": 8,
        "name": "Everyday Sneakers",
        "cat": "Footwear",
        "type": "Shoes",
        "price": 1299,
        "old": 2199,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700"
    },

    {
        "id": 9,
        "name": "Structured Women's Handbag",
        "cat": "Accessories",
        "type": "Bags",
        "price": 1199,
        "old": 1999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700"
    },

    {
        "id": 10,
        "name": "Soft Blush Makeup Palette",
        "cat": "Beauty",
        "type": "Makeup",
        "price": 899,
        "old": 1399,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=700"
    }
]
# Product Name Category Type Price Original Price Rating Image

# ---------- STATE ----------
if "cart" not in st.session_state: st.session_state.cart = []
if "wish" not in st.session_state: st.session_state.wish = []
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role":"assistant",
        "content":"Hi! I'm **NOVA AI** ✨\n\nI can help with outfits, makeup, skincare, accessories and budget shopping."
    }]

# ---------- STYLE ---------- This controls: NOVA AI logo Hero section Colors Fonts Product cards Buttons Chat area Footer
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#f7f7f8;color:#222}
#MainMenu,header,footer{visibility:hidden}
.block-container{max-width:1250px;padding:1.2rem 1rem 3rem}

.top{background:white;padding:20px 25px;border-radius:18px;
box-shadow:0 4px 20px #0000000c;margin-bottom:20px}
.logo{font:700 36px 'Playfair Display';color:#222}
.logo span{color:#d63384}
.sub{color:#666}

.hero{padding:38px;border-radius:24px;margin-bottom:25px;
background:linear-gradient(120deg,#fff0f6,#f5efff,#fff8ef)}
.pill{display:inline-block;background:#171717;color:white;padding:7px 14px;
border-radius:30px;font-size:12px;font-weight:600}
.hero h1{font:700 44px/1.1 'Playfair Display';color:#222;margin:18px 0 10px}
.hero p{color:#555;font-size:17px}

.title{font:700 28px 'Playfair Display';color:#222;margin:25px 0 15px}
.ai{background:linear-gradient(135deg,#fff0f7,#f7efff);
padding:22px;border:1px solid #efd9e7;border-radius:20px}
.card{background:#fff;border:1px solid #eee;border-radius:15px;overflow:hidden}
.card img{width:100%;height:210px;object-fit:cover}
.body{padding:13px}
.name{font-weight:600;color:#222}
.type{font-size:12px;color:#777}
.price{font-size:18px;font-weight:700;color:#222;margin-top:7px}
.old{text-decoration:line-through;color:#999;font-size:12px;margin-left:5px}
.rate{color:#087f5b;font-size:12px;margin-top:5px}

.stButton>button{border-radius:9px;color:#222!important;background:white;
border:1px solid #ddd;font-weight:600}
.stButton>button:hover{border-color:#d63384;color:#d63384!important}
/* Make every important text visible */
.stApp,.stApp p,.stApp span,.stApp label,.stApp div{color:#222}
.top,.top *{color:#222!important}
.logo,.logo *{color:#222!important}
.logo span{color:#d63384!important}
.hero,.hero *{color:#222!important}
.hero .pill,.hero .pill *{color:#fff!important}
.title,.title *{color:#222!important}
.ai,.ai *{color:#222!important}
.card,.card *{color:#222}
.type,.old{color:#777!important}
.rate{color:#087f5b!important}
.stButton>button,.stButton>button *{color:#222!important}
.stRadio label,.stRadio label *{color:#222!important}
[data-testid="stChatMessage"], [data-testid="stChatMessage"] *{color:#222!important}
[data-testid="stChatInput"] textarea{color:#fff!important;background:#272932!important;caret-color:#fff!important}
[data-testid="stChatInput"] textarea::placeholder{color:#d5d5d5!important;opacity:1!important}
[data-testid="stChatInput"]{color:#fff!important}
</style>
""", unsafe_allow_html=True)

# ---------- HELPERS ----------
def product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

def catalog_text():
    return "\n".join(
        f"{p['name']} | {p['cat']} | ₹{p['price']} | {p['type']}"
        for p in PRODUCTS
    )

def ask_nova(question):
    client = get_client()
    if client:
        prompt = f"""You are NOVA AI, a friendly Indian fashion and beauty shopping assistant.
Answer briefly and naturally. Use ₹ for prices. Recommend only products in this catalog.
Do not invent products. For unclear requests, ask one short question.
Catalog:
{catalog_text()}

Customer: {question}"""
        try:
            r = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if r and r.text:
                return r.text
        except Exception:
            pass

    q = question.lower()
    if "wedding" in q or "party" in q:
        return "✨ For a wedding look: **Floral Printed Kurta Set ₹1,499**, **Minimal Gold Necklace ₹699** and **Soft Blush Makeup Palette ₹899**."
    if "makeup" in q:
        return "💄 Try the **Soft Blush Makeup Palette ₹899** with **Velvet Matte Lipstick ₹599** for a simple soft-glam look."
    if "skin" in q:
        return "🧴 The **Hydrating Glow Serum ₹799** is a catalog option. For specific skin concerns, consider professional advice."
    if "men" in q:
        return "👔 Try the **Classic Men's Casual Shirt ₹999** with **Relaxed Fit Denim Jeans ₹1,299** and **Everyday Sneakers ₹1,299**."
    if "under" in q or "budget" in q:
        return "💰 Tell me your budget and occasion, for example: **wedding outfit under ₹3000**."
    return "✨ I can help with fashion, makeup, skincare, accessories, footwear and budget shopping. What are you looking for?"

# ---------- HEADER ----------
st.markdown("""
<div class="top">
  <div class="logo">NOVA<span>AI</span></div>
  <div class="sub">Fashion • Beauty • Lifestyle • AI Styling</div>
</div>
<div class="hero">
  <span class="pill">NOVA AI STYLE STUDIO</span>
  <h1>Your style.<br>Your beauty.<br>Your NOVA. ✨</h1>
  <p>Your personal assistant for fashion, beauty and shopping.</p>
</div>
""", unsafe_allow_html=True)

# ---------- QUICK CHAT ----------
st.markdown('<div class="title">What can NOVA help with?</div>', unsafe_allow_html=True)
quick = ["👗 Wedding outfit","💄 Makeup","🧴 Skincare","👔 Men's fashion","👜 Accessories","💰 Budget"]
cols = st.columns(6)

for i, text in enumerate(quick):
    with cols[i]:
        if st.button(text, key=f"q{i}", use_container_width=True):
            q = text.split(" ",1)[1]
            st.session_state.messages.append({"role":"user","content":q})
            st.session_state.messages.append({"role":"assistant","content":ask_nova(q)})
            st.rerun()

# ---------- CHAT ----------
st.markdown("""
<div class="ai">
<div class="title" style="margin:0">✨ Ask NOVA</div>
<p style="color:#666">Get quick recommendations for your next look.</p>
</div>
""", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Ask NOVA... e.g. Suggest a wedding outfit under ₹3000")

if question:
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("NOVA is styling your look..."):
            answer = ask_nova(question)
        st.markdown(answer)
    st.session_state.messages.append({"role":"assistant","content":answer})

# ---------- PRODUCTS ----------
st.markdown('<div class="title">✨ Explore Products</div>', unsafe_allow_html=True)

categories = ["All","Women","Men","Beauty","Accessories","Footwear"]
cat = st.radio("Category", categories, horizontal=True, label_visibility="collapsed")
items = PRODUCTS if cat == "All" else [p for p in PRODUCTS if p["cat"] == cat]

for start in range(0, len(items), 4):
    cols = st.columns(4)
    for col, p in zip(cols, items[start:start+4]):
        with col:
            off = round((p["old"]-p["price"])*100/p["old"])
            st.markdown(f"""
            <div class="card">
              <img src="{p['image']}">
              <div class="body">
                <div class="name">{p['name']}</div>
                <div class="type">{p['type']}</div>
                <div class="price">₹{p['price']}
                  <span class="old">₹{p['old']}</span>
                  <span style="color:#087f5b;font-size:12px">{off}% OFF</span>
                </div>
                <div class="rate">★ {p['rating']} • Popular choice</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            c1,c2 = st.columns(2)
            with c1:
                if st.button("🛍 Add", key=f"add{p['id']}", use_container_width=True):
                    if p["id"] not in st.session_state.cart:
                        st.session_state.cart.append(p["id"])
                    st.toast("Added to cart")
            with c2:
                heart = "❤️" if p["id"] in st.session_state.wish else "♡"
                if st.button(heart, key=f"wish{p['id']}", use_container_width=True):
                    if p["id"] in st.session_state.wish:
                        st.session_state.wish.remove(p["id"])
                    else:
                        st.session_state.wish.append(p["id"])
                    st.rerun()

# ---------- CART ----------
st.markdown('<div class="title">🛍 Shopping Space</div>', unsafe_allow_html=True)
a,b = st.columns(2)

with a:
    st.subheader("Your Cart")
    cart = [product(i) for i in st.session_state.cart]
    if cart:
        for p in cart: st.write(f"**{p['name']}** — ₹{p['price']}")
        st.write(f"**Total: ₹{sum(p['price'] for p in cart):,}**")
    else:
        st.info("Your cart is empty.")

with b:
    st.subheader("❤️ Wishlist")
    wish = [product(i) for i in st.session_state.wish]
    if wish:
        for p in wish: st.write(f"**{p['name']}** — ₹{p['price']}")
    else:
        st.info("Your wishlist is empty.")

# ---------- FOOTER ----------
st.markdown("""
<div style="margin-top:45px;background:#171717;color:white;padding:28px;
border-radius:18px;text-align:center">
  <div style="font:700 28px 'Playfair Display'">NOVA<span style="color:#ff72ad">AI</span></div>
  <div style="color:#bbb;margin-top:5px">Fashion • Beauty • Lifestyle • AI Styling</div>
</div>
""", unsafe_allow_html=True)
