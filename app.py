                        raise ValueError("Provider response did not include a supported HTTPS image_url.")
                    img_resp = requests.get(result_url, timeout=60)
                    img_resp.raise_for_status()
                    result = Image.open(io.BytesIO(img_resp.content)).convert("RGB")
                st.success("AI-generated result received from the configured provider.")
                st.image(result, caption="AI virtual try-on result", use_container_width=True)
                out = io.BytesIO()
                result.save(out, format="JPEG", quality=92)
                st.download_button("Download result", out.getvalue(), "nova_virtual_tryon.jpg", "image/jpeg")
            except Exception:
                st.error("Virtual try-on failed. Check that the provider's endpoint, request fields, authentication and response format match this integration. No fake result was shown.")
    st.caption("This starter assumes an API accepting multipart fields named 'person' and 'garment', and returning image bytes or JSON with an HTTPS 'image_url'. Adapt the integration to your chosen provider's official documentation. A 360° video needs a separate multi-view/3D-capable service.")

# ---------- Wishlist ----------
elif page == "Wishlist":
    st.subheader("♡ Your Wishlist")
    wished = [product_by_id[x] for x in st.session_state.wishlist if x in product_by_id]
    if not wished:
        st.info("Your wishlist is empty. Save a product from the shop to see it here.")
    else:
        for p in wished:
            left, right = st.columns([1, 3])
            with left:
                if product_image_url(p):
                    st.image(product_image_url(p), use_container_width=True)
            with right:
                st.markdown(f"**{p.get('name')}**")
                st.write(money(p.get("price")))
                if st.button("Remove from wishlist", key=f"remove_wish_{p.get('id')}"):
                    st.session_state.wishlist.remove(str(p.get("id")))
                    st.rerun()

# ---------- Cart ----------
elif page == "My Cart":
    st.subheader("🛒 Your Shopping Cart")
    lines = get_cart_lines()
    if not lines:
        st.info("Your cart is empty. Explore the shop and add a product.")
    else:
        total = 0.0
        for key, p, item in lines:
            c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
            with c1:
                if product_image_url(p):
                    st.image(product_image_url(p), use_container_width=True)
            with c2:
                st.markdown(f"**{p.get('name')}**")
                st.caption(f"Size: {item['size']}")
                st.write(f"{money(p.get('price'))} × {item['quantity']}")
            with c3:
                new_qty = st.number_input("Qty", min_value=1, max_value=20, value=int(item["quantity"]), key=f"qty_{key}")
                if int(new_qty) != int(item["quantity"]):
                    st.session_state.cart[key]["quantity"] = int(new_qty)
                    st.rerun()
            with c4:
                if st.button("Remove", key=f"remove_cart_{key}"):
                    del st.session_state.cart[key]
                    st.rerun()
            total += float(p.get("price") or 0) * int(item["quantity"])
        st.divider()
        st.markdown(f"## Total: {money(total)}")
        st.caption("Shipping, taxes, payment and order persistence are not configured in this demo.")
        st.warning("Demo checkout only — no payment will be collected.")
        if st.button("Place demo order", type="primary"):
            st.success("Demo order summary created. This does not create a paid order or reserve inventory.")
            st.json({
                "items": [
                    {"product": p.get("name"), "size": item["size"], "quantity": item["quantity"], "unit_price": p.get("price")}
                    for _, p, item in lines
                ],
                "total_inr": total,
                "status": "DEMO_ONLY",
            })

# ---------- Admin add product ----------
elif page == "Admin: Add Product":
    st.subheader("⚙️ Add a product to the cloud catalog")
    st.warning("Starter admin screen only. Before a public launch, add real authentication and server-side role checks. Do not rely on hiding this page as security.")
    if db is None:
        st.error("Configure SUPABASE_URL and SUPABASE_KEY to add products to the cloud database.")
    else:
        with st.form("add_product_form"):
            name = st.text_input("Product name")
            category = st.selectbox("Category", ["Kurtis", "Dresses", "Tops", "Sarees", "Co-ord Sets", "Accessories", "Beauty"])
            price = st.number_input("Price (INR)", min_value=1.0, value=499.0, step=50.0)
            original_price = st.number_input("Original price (INR)", min_value=0.0, value=799.0, step=50.0)
            color = st.text_input("Color", "Pink")
            sizes_text = st.text_input("Sizes, comma separated", "S,M,L,XL")
            image_url = st.text_input("Public product image HTTPS URL")
            description = st.text_area("Description")
            stock = st.number_input("Stock", min_value=0, value=10, step=1)
            submitted = st.form_submit_button("Save product")
        if submitted:
            if not name.strip() or not image_url.startswith("https://"):
                st.error("Enter a product name and an HTTPS image URL.")
            else:
                record = {
                    "name": name.strip(),
                    "category": category,
                    "price": float(price),
                    "original_price": float(original_price),
                    "color": color.strip(),
                    "sizes": [s.strip() for s in sizes_text.split(",") if s.strip()],
                    "image_url": image_url.strip(),
                    "description": description.strip(),
                    "stock": int(stock),
                    "active": True,
                }
                try:
                    db.table("products").insert(record).execute()
                    st.success("Product saved to Supabase. Refresh the app to load the updated catalog.")
                    st.cache_data.clear()
                except Exception:
                    st.error("Could not save product. Check the products table schema and Supabase permissions.")

st.divider()
st.caption("NOVA AI · Shopping demo. Verify product rights, inventory, prices, database security, user authentication, payment processing and privacy before production use.")
