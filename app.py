import os
import json
import io
import re
from typing import Optional

import requests
import streamlit as st
from PIL import Image, ImageOps
from supabase import create_client, Client
from groq import Groq

# ============================================================
# NOVA AI | Fashion & Beauty Store
# Streamlit + Supabase (cloud database) + Groq (AI chat)
# ============================================================

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Secrets ----------
def secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
        return str(value) if value is not None else default
    except Exception:
        return os.getenv(name, default)

SUPABASE_URL = secret("SUPABASE_URL")
SUPABASE_KEY = secret("SUPABASE_KEY")  # Use a server-side secret; never expose service-role key to browsers.
GROQ_API_KEY = secret("GROQ_API_KEY")
GROQ_MODEL = secret("GROQ_MODEL", "llama-3.3-70b-versatile")
VTON_API_URL = secret("VTON_API_URL")
VTON_API_KEY = secret("VTON_API_KEY")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
.stApp { background: #fffafd; color: #302333; font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: #fff1f7; border-right: 1px solid #f2d6e4; }
h1,h2,h3 { font-family: 'Playfair Display', serif !important; color: #632d4d !important; }
div.stButton > button, div.stDownloadButton > button {
  background: linear-gradient(90deg,#d64f91,#9d62c9); color: white; border: 0;
  border-radius: 11px; font-weight: 700;
}
div.stButton > button:hover { filter: brightness(1.06); border: 0; }
.nova-hero { padding: 28px 30px; border-radius: 22px; color: #fff;
 background: linear-gradient(115deg,#4a2442,#9e467d,#d875a8); margin-bottom: 18px; }
.nova-hero h1 { color: #fff !important; margin: 4px 0; }
.nova-hero p { color: #fff4fa; margin-bottom: 0; }
.nova-pill { display:inline-block; background:#fae5f0; color:#81385e; padding:5px 10px;
 border-radius:20px; font-size:12px; margin:2px; }
.product-card { background:#fff; border:1px solid #f2dce7; padding:12px; border-radius:16px; }
.small-muted { color:#806b7b; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ---------- Database connection ----------
@st.cache_resource
def get_supabase() -> Optional[Client]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

db = get_supabase()

# ---------- Sample catalog (fallback/demo only) ----------
# Replace these examples with your own licensed product images and accurate stock/prices.
DEMO_PRODUCTS = [
    {"id":"demo-001","name":"Floral Everyday Kurti","category":"Kurtis","price":499.0,"original_price":799.0,"color":"Pink","sizes":["S","M","L","XL"],"description":"Lightweight everyday kurti with a floral print.","image_url":"https://images.unsplash.com/photo-1583391733956-6c78276477e3?auto=format&fit=crop&w=800&q=85","stock":20,"active":True},
    {"id":"demo-002","name":"Classic Black Dress","category":"Dresses","price":799.0,"original_price":1199.0,"color":"Black","sizes":["S","M","L"],"description":"A versatile black dress for evenings and parties.","image_url":"https://images.unsplash.com/photo-1539008835657-9e8e9680c956?auto=format&fit=crop&w=800&q=85","stock":12,"active":True},
    {"id":"demo-003","name":"Pastel Co-ord Set","category":"Co-ord Sets","price":899.0,"original_price":1399.0,"color":"Pastel","sizes":["S","M","L","XL"],"description":"Relaxed matching set for casual days and travel.","image_url":"https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=800&q=85","stock":8,"active":True},
    {"id":"demo-004","name":"Blue Casual Top","category":"Tops","price":399.0,"original_price":599.0,"color":"Blue","sizes":["XS","S","M","L"],"description":"Easy-to-style blue top for everyday wear.","image_url":"https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=800&q=85","stock":18,"active":True},
    {"id":"demo-005","name":"Elegant Occasion Saree","category":"Sarees","price":1499.0,"original_price":2199.0,"color":"Purple","sizes":["Free Size"],"description":"Occasion-ready saree styling inspiration.","image_url":"https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=85","stock":6,"active":True},
    {"id":"demo-006","name":"Minimal White Shirt","category":"Tops","price":549.0,"original_price":799.0,"color":"White","sizes":["S","M","L","XL"],"description":"A clean white shirt that pairs with many outfits.","image_url":"https://images.unsplash.com/photo-1598554747436-c9293d6a588f?auto=format&fit=crop&w=800&q=85","stock":14,"active":True},
    {"id":"demo-007","name":"Party Wear Midi Dress","category":"Dresses","price":999.0,"original_price":1599.0,"color":"Red","sizes":["S","M","L"],"description":"A statement midi dress for parties and celebrations.","image_url":"https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=85","stock":9,"active":True},
    {"id":"demo-008","name":"Everyday Cotton Kurta","category":"Kurtis","price":449.0,"original_price":699.0,"color":"Green","sizes":["S","M","L","XL","XXL"],"description":"Comfortable cotton kurta for everyday use.","image_url":"https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=85","stock":25,"active":True},
]

def fetch_products():
    """Fetch live catalog from Supabase; use clearly labelled demo data if DB is not configured."""
    if db is None:
        return [dict(p) for p in DEMO_PRODUCTS], False
    try:
        response = db.table("products").select("*").eq("active", True).order("id").execute()
        rows = response.data or []
        return rows, True
    except Exception:
