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


