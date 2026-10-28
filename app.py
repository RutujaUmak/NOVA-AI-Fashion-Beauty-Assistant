
# ---------- Navigation ----------
page = st.sidebar.radio(
    "NOVA MENU",
    ["Home & Shop", "AI Style Chat", "Virtual Try-On", "Wishlist", "My Cart", "Admin: Add Product"],
    index=0,
)
st.sidebar.markdown("---")
st.sidebar.metric("Items in cart", cart_total_count)
if not cloud_catalog:
    st.sidebar.caption("Demo catalog mode")
else:
    st.sidebar.caption("Cloud catalog connected")

# ---------- Home / Shop ----------
if page == "Home & Shop":
    st.subheader("Find your next favourite look")
    search = st.text_input("🔎 Search products", placeholder="Try: black dress, kurti, party wear...")
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    categories = sorted({str(p.get("category", "Other")) for p in products})
    colors = sorted({str(p.get("color", "Other")) for p in products})
    with filter_col1:
        chosen_category = st.selectbox("Category", ["All"] + categories)
    with filter_col2:
        chosen_color = st.selectbox("Color", ["All"] + colors)
    with filter_col3:
        max_price = st.slider(
            "Maximum price",
            min_value=0,
            max_value=max(2000, int(max([float(p.get("price") or 0) for p in products] + [2000]))),
            value=max(2000, int(max([float(p.get("price") or 0) for p in products] + [2000]))),
            step=100,
        )
    sort_by = st.selectbox("Sort by", ["Recommended", "Price: low to high", "Price: high to low", "Name A–Z"])

    filtered = []
    for p in products:
        if not product_matches_query(p, search):
            continue
        if chosen_category != "All" and p.get("category") != chosen_category:
            continue
        if chosen_color != "All" and p.get("color") != chosen_color:
            continue
        try:
            price = float(p.get("price", 0))
        except (ValueError, TypeError):
            price = 0
        if price > max_price:
            continue
        filtered.append(p)

    if sort_by == "Price: low to high":
        filtered.sort(key=lambda p: float(p.get("price") or 0))
    elif sort_by == "Price: high to low":
        filtered.sort(key=lambda p: float(p.get("price") or 0), reverse=True)
    elif sort_by == "Name A–Z":
        filtered.sort(key=lambda p: str(p.get("name", "")).lower())

    st.caption(f"{len(filtered)} product(s) found")
    if not filtered:
        st.info("No products match these filters. Try another search or price range.")
    else:
        columns = st.columns(4)
        for i, p in enumerate(filtered):
            with columns[i % 4]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                url = product_image_url(p)
                if url:
                    st.image(url, use_container_width=True)
                else:
                    st.info("Product image not available")
                st.markdown(f"**{p.get('name', 'Unnamed product')}**")
                st.markdown(f"### {money(p.get('price'))}")
                old_price = p.get("original_price")
                if old_price:
                    st.caption(f"MRP {money(old_price)}")
                st.caption(f"{p.get('category', 'Fashion')} · {p.get('color', 'Various')}")
                st.caption(str(p.get("description", ""))[:100])
                sizes = p.get("sizes") or ["Free Size"]
                if isinstance(sizes, str):
                    try:
                        sizes = json.loads(sizes)
                    except json.JSONDecodeError:
                        sizes = [s.strip() for s in sizes.split(",") if s.strip()]
                if not isinstance(sizes, list) or not sizes:
                    sizes = ["Free Size"]
                size = st.selectbox("Size", sizes, key=f"size_{p.get('id')}")
                if st.button("Add to cart", key=f"add_{p.get('id')}", use_container_width=True):
                    add_to_cart(str(p.get("id")), str(size))
                    st.toast(f"Added {p.get('name')} to cart")
                wish_id = str(p.get("id"))
                wish_label = "♥ Saved" if wish_id in st.session_state.wishlist else "♡ Wishlist"
                if st.button(wish_label, key=f"wish_{p.get('id')}", use_container_width=True):
                    if wish_id in st.session_state.wishlist:
                        st.session_state.wishlist.remove(wish_id)
                    else:
                        st.session_state.wishlist.append(wish_id)
                    st.rerun()
                if st.button("Ask AI about this", key=f"ask_{p.get('id')}", use_container_width=True):
                    st.session_state["chat_prefill"] = (
                        f"Help me style the product '{p.get('name')}' priced at {money(p.get('price'))}. "
                        f"Category: {p.get('category')}. Color: {p.get('color')}. "
                        "Suggest an occasion and matching items."
                    )
                    st.info("Open AI Style Chat from the sidebar to ask about this product.")
                st.markdown('</div>', unsafe_allow_html=True)

# ---------- AI Style Chat ----------
elif page == "AI Style Chat":
    st.subheader("💬 Chat with NOVA, your AI shopping stylist")
    st.write("Ask for outfits by occasion, color, category, or budget. The chatbot receives the current product catalog so it can recommend items that actually exist in this store.")
    if not GROQ_API_KEY:
        st.warning("AI chat is not connected yet. Add GROQ_API_KEY in Streamlit Secrets. The store and catalog can still be used.")
        st.markdown("Get an API key from the [Groq Console](https://console.groq.com/). API access and free-tier limits depend on the provider's current terms.")
    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prefill = st.session_state.pop("chat_prefill", "")
    prompt = st.chat_input("Example: Find a party dress under ₹1000")
    if not prompt and prefill:
        st.info("Suggested prompt ready. Copy it into the chat box: " + prefill)
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not GROQ_API_KEY:
            answer = "AI chat needs a Groq API key. Add GROQ_API_KEY to Streamlit Secrets, then retry. You can still use the product search and filters."
        else:
            catalog_context = [
                {
                    "id": str(p.get("id")),
                    "name": p.get("name"),
                    "category": p.get("category"),
                    "price_inr": p.get("price"),
                    "color": p.get("color"),
                    "sizes": p.get("sizes"),
                    "description": p.get("description"),
                    "stock": p.get("stock"),
                }
                for p in products[:100]
            ]
            system_prompt = (
                "You are NOVA, a helpful Indian fashion ecommerce shopping assistant. "
                "Recommend only products present in the supplied catalog; never invent products, prices, stock, sizes, discounts, or delivery promises. "
                "If no product matches the requested budget or criteria, say so honestly and suggest relaxing a filter. "
                "Use INR. Ask one short clarifying question when necessary. Give practical styling tips. "
                "Do not infer sensitive traits from a user's photo. "
                "Catalog JSON: " + json.dumps(catalog_context, ensure_ascii=False)
            )
            try:
                client = Groq(api_key=GROQ_API_KEY)
                recent = st.session_state.chat_history[-10:]
                completion = client.chat.completions.create(
                    model=GROQ_MODEL,
