
import os
import io
import requests
import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageDraw

# --------------------------------------------------
# NOVA AI | Fashion & Beauty
# --------------------------------------------------

st.set_page_config(
    page_title="NOVA AI | Fashion & Beauty",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Read credentials safely. The app still runs without them.
def get_secret(name, default=""):
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return os.getenv(name, default)


VTON_API_URL = get_secret("VTON_API_URL")
VTON_API_KEY = get_secret("VTON_API_KEY")

# --------------------------------------------------
# Aesthetic styling
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #100f19 0%, #201529 55%, #321b30 100%);
    color: #f9f3f8;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #17131f;
    border-right: 1px solid #463348;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f8d8e8 !important;
}
p, label, span {
    color: #f4eaf2;
}
div.stButton > button {
    background: linear-gradient(90deg, #d85c9b, #9b72dc);
    color: white;
    border: 0;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: all .2s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px #d85c9b40;
    border: 0;
}
.nova-hero {
    padding: 32px;
    border-radius: 24px;
    background: linear-gradient(120deg, #35213e, #542b4a, #302347);
    border: 1px solid #86547b;
    margin-bottom: 22px;
}
.nova-subtitle {
    color: #e9c7df;
    font-size: 16px;
}
.nova-card {
    padding: 20px;
    background: #211a2a;
    border: 1px solid #49364e;
    border-radius: 18px;
    margin-bottom: 12px;
}
.nova-tag {
    display: inline-block;
    background: #493047;
    padding: 5px 10px;
    border-radius: 20px;
    color: #ffd7ed;
    font-size: 12px;
    margin: 3px;
}
hr { border-color: #49364e; }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def open_image(upload):
    """Safely open and normalize an uploaded image."""
    if upload is None:
        return None

    try:
        image = Image.open(io.BytesIO(upload.getvalue()))
        image = ImageOps.exif_transpose(image).convert("RGB")

        # Limit image dimensions to keep requests manageable.
        image.thumbnail((1200, 1200))
        return image
    except Exception:
        return None


def image_bytes(image, fmt="JPEG"):
    """Convert PIL image into uploadable bytes."""
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format=fmt, quality=90)
    return buffer.getvalue()


def dominant_color(image):
    """Find a representative image color without facial recognition."""
    if image is None:
        return None

    small = image.resize((80, 80))
    pixels = np.asarray(small).reshape(-1, 3).astype(np.float32)

    # Ignore near-white and very dark pixels when possible.
    brightness = pixels.mean(axis=1)
    selected = pixels[(brightness > 25) & (brightness < 245)]

    if len(selected) == 0:
        selected = pixels

    rgb = np.median(selected, axis=0).astype(int)
    return tuple(int(v) for v in rgb)


def color_name(rgb):
    """Approximate color family for simple style suggestions."""
    if rgb is None:
        return "unknown"

    r, g, b = rgb
    maximum = max(r, g, b)
    minimum = min(r, g, b)

    if maximum < 65:
        return "black or deep neutral"
    if minimum > 205:
        return "white or ivory"
    if maximum - minimum < 25:
        return "neutral grey"
    if r > g * 1.25 and r > b * 1.15:
        return "red, rose or warm pink"
    if r > 150 and g > 100 and b < 115:
        return "warm peach, beige or brown"
    if g > r * 1.15 and g > b * 1.1:
        return "green"
    if b > r * 1.15 and b > g * 1.05:
        return "blue or violet"
    if r > 150 and b > 130 and g < 150:
        return "pink or purple"

    return "mixed or neutral tones"


def recommend_style(preferred_style, occasion, preferred_colors):
    """Explain recommendations using explicit user preferences."""
    recommendations = {
        "Minimal": [
            "Try clean silhouettes and solid colors.",
            "Consider a simple kurta set, shirt dress or tailored outfit.",
        ],
        "Elegant": [
            "Consider a flowing silhouette with refined detailing.",
            "Try a coordinated outfit with subtle accessories.",
        ],
        "Casual": [
            "Try comfortable cuts and easy-to-style separates.",
            "Consider jeans with a top, a relaxed dress or a casual co-ord.",
        ],
        "Traditional": [
            "Explore sarees, anarkali suits, lehengas or kurta sets.",
            "Choose detailing and fabrics appropriate to your occasion.",
        ],
        "Streetwear": [
            "Try relaxed fits, layering and statement sneakers.",
            "Consider an oversized shirt, cargo trousers or a co-ord.",
        ],
    }

    items = recommendations.get(
        preferred_style,
        recommendations["Elegant"]
    )

    return items + [
        f"Occasion: {occasion}.",
        f"Preferred colors: {', '.join(preferred_colors)}.",
    ]


def run_virtual_tryon(person_image, garment_image, category):
    """
    Calls a user-configured virtual try-on API.

    IMPORTANT:
    VTON_API_URL must point to an API you control or a service
    whose documented request/response format matches this example.

    Expected request:
      multipart fields: person, garment, category
      optional header: Authorization: Bearer <API key>

    Expected response:
      either raw image bytes or JSON containing an image_url field.
    """
    if not VTON_API_URL:
        return None, (
            "Virtual try-on is not connected yet. Configure VTON_API_URL "
            "with a compatible virtual try-on API before using this feature."
        )

    headers = {}
    if VTON_API_KEY:
        headers["Authorization"] = f"Bearer {VTON_API_KEY}"

    files = {
        "person": (
            "person.jpg",
            image_bytes(person_image),
            "image/jpeg",
        ),
        "garment": (
            "garment.jpg",
            image_bytes(garment_image),
            "image/jpeg",
        ),
    }

    try:
        response = requests.post(
            VTON_API_URL,
            headers=headers,
            files=files,
            data={"category": category},
            timeout=180,
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "image/" in content_type:
            result = Image.open(
                io.BytesIO(response.content)
            ).convert("RGB")
            return result, None

        data = response.json()
        image_url = data.get("image_url")

        if not image_url:
            return None, (
                "The API responded, but no image_url was returned. "
                "Update the response parser to match your provider's API."
            )

        # Only download images from HTTPS URLs.
        if not image_url.startswith("https://"):
            return None, "The API returned an unsupported image URL."

        image_response = requests.get(
            image_url, timeout=60
        )
        image_response.raise_for_status()

        result = Image.open(
            io.BytesIO(image_response.content)
        ).convert("RGB")
        return result, None

    except requests.Timeout:
        return None, "The virtual try-on request timed out. Please retry."
    except requests.RequestException:
        return None, (
            "The virtual try-on service could not be reached. "
            "Check its endpoint, credentials and service status."
        )
    except (ValueError, OSError, KeyError):
        return None, (
            "The service returned an unsupported image response. "
            "Check the provider's API documentation."
        )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
<div class="nova-hero">
    <span class="nova-tag">AI PERSONAL STYLIST</span>
    <h1 style="font-size:42px; margin-bottom:4px;">
        ✨ NOVA AI
    </h1>
    <p class="nova-subtitle">
        Discover your style. Explore your look.
        Find outfits for your next moment.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ✨ NOVA STUDIO")
    page = st.radio(
        "Explore",
        [
            "Home",
            "Virtual Try-On",
            "AI Style Advisor",
            "My Wardrobe",
        ],
    )

    st.divider()
    st.caption("Your photo stays in this app session unless "
               "you submit it to a configured external API.")


# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "Home":
    st.subheader("Your personal fashion space")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="nova-card">
            <h3>👗 Virtual Try-On</h3>
            <p>Upload your photo and a garment image.
            Connect a compatible AI service to generate
            a virtual outfit preview.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore Virtual Try-On", key="home_tryon"):
            st.session_state["selected_page"] = "Virtual Try-On"
            st.info("Select Virtual Try-On in the sidebar.")

    with right:
        st.markdown("""
        <div class="nova-card">
            <h3>💖 AI Style Advisor</h3>
            <p>Get outfit ideas using your occasion,
            preferred colors and personal style choices.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore Style Advisor", key="home_style"):
            st.info("Select AI Style Advisor in the sidebar.")

    st.subheader("How NOVA AI works")

    c1, c2, c3 = st.columns(3)
    c1.metric("01", "Upload")
    c2.metric("02", "Personalize")
    c3.metric("03", "Explore")

    st.caption(
        "Style suggestions are informational, not guarantees "
        "of fit, appearance or color suitability."
    )


# --------------------------------------------------
# VIRTUAL TRY-ON
# --------------------------------------------------

elif page == "Virtual Try-On":
    st.subheader("👗 AI Virtual Try-On")
    st.write(
        "Upload a clear, well-lit photo and a picture of the "
        "garment you want to try."
    )

    person_source = st.radio(
        "Choose your photo source",
        ["Upload photo", "Take a photo"],
        horizontal=True,
    )

    person_upload = None

    if person_source == "Upload photo":
        person_upload = st.file_uploader(
            "Upload your selfie or full-body photo",
            type=["jpg", "jpeg", "png"],
            key="person_upload",
        )
    else:
        person_upload = st.camera_input(
            "Take a photo",
            key="person_camera",
        )

    garment_upload = st.file_uploader(
        "Upload the selected dress or garment image",
        type=["jpg", "jpeg", "png"],
        key="garment_upload",
    )

    category = st.selectbox(
        "Garment category",
        [
            "upper_body",
            "lower_body",
            "dresses",
        ],
        format_func=lambda x: {
            "upper_body": "Top / Shirt",
            "lower_body": "Trousers / Skirt",
            "dresses": "Dress / Full outfit",
        }[x],
    )

    person_image = open_image(person_upload)
    garment_image = open_image(garment_upload)

    if person_image:
        st.image(
            person_image,
            caption="Your uploaded photo",
            width=280,
        )

    if garment_image:
        st.image(
            garment_image,
            caption="Selected garment",
            width=280,
        )

    st.info(
        "For best results, use a clear photo and a garment image "
        "with minimal background clutter. Actual results depend "
        "on the connected try-on model."
    )

    if st.button(
        "✨ Generate Virtual Try-On",
        type="primary",
        key="generate_tryon",
    ):
        if person_image is None or garment_image is None:
            st.warning(
                "Please upload both your photo and a garment image."
            )
        else:
            with st.spinner("Generating your outfit preview..."):
                result, error = run_virtual_tryon(
                    person_image,
                    garment_image,
                    category,
                )

            if result is not None:
                st.success("Your virtual try-on result is ready!")
                st.image(
                    result,
                    caption="AI-generated virtual try-on preview",
                    use_container_width=True,
                )

                st.download_button(
                    "Download result",
                    data=image_bytes(result),
                    file_name="nova_virtual_tryon.jpg",
                    mime="image/jpeg",
                )
            else:
                st.warning(error)

    st.caption(
        "A true 360° video is not generated by this version. "
        "That feature requires a model or service that produces "
        "multiple consistent views or a 3D avatar."
    )


# --------------------------------------------------
# AI STYLE ADVISOR
# --------------------------------------------------

elif page == "AI Style Advisor":
    st.subheader("💖 Your AI Style Advisor")
    st.write(
        "Tell NOVA what you like to receive personalized "
        "outfit ideas."
    )

    col1, col2 = st.columns(2)

    with col1:
        style = st.selectbox(
            "Your preferred style",
            [
                "Elegant",
                "Minimal",
                "Casual",
                "Traditional",
                "Streetwear",
            ],
        )

        occasion = st.selectbox(
            "Choose an occasion",
            [
                "Everyday",
                "College",
                "Office",
                "Party",
                "Wedding",
                "Interview",
                "Travel",
            ],
        )

    with col2:
        colors = st.multiselect(
            "Colors you enjoy wearing",
            [
                "Black",
                "White",
                "Pink",
                "Blue",
                "Red",
                "Purple",
                "Green",
                "Beige",
                "Pastels",
                "Earth tones",
            ],
            default=["Black", "Blue"],
        )

        budget = st.selectbox(
            "Budget per outfit",
            [
                "Under ₹1,000",
                "₹1,000–₹2,500",
                "₹2,500–₹5,000",
                "Above ₹5,000",
            ],
        )

    st.markdown("### Optional photo-based color analysis")

    photo_upload = st.file_uploader(
        "Upload a photo if you want a rough color overview",
        type=["jpg", "jpeg", "png"],
        key="style_photo",
    )

    style_photo = open_image(photo_upload)

    if style_photo:
        st.image(
            style_photo,
            caption="Photo used for approximate color analysis",
            width=250,
        )

    if st.button("Generate My Style Guide", type="primary"):
        if not colors:
            st.warning("Please choose at least one preferred color.")
        else:
            suggestions = recommend_style(
                style,
                occasion,
                colors,
            )

            st.markdown("### ✨ Your style guide")

            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")

            st.markdown("### 🎨 Color inspiration")

            if style_photo:
                rgb = dominant_color(style_photo)
                name = color_name(rgb)

                st.markdown(
                    f"Your photo has a prominent color family "
                    f"that appears closest to **{name}**."
                )

                swatch = Image.new("RGB", (420, 100), rgb)
                st.image(
                    swatch,
                    caption=f"Approximate sampled color: RGB {rgb}",
                    width=320,
                )

                st.caption(
                    "This is a rough image-color estimate, not "
                    "skin-tone, face-shape or personality analysis. "
                    "Lighting and background can affect the result."
                )

            st.markdown("### 🛍️ Suggested outfit directions")

            outfit_ideas = {
                "Everyday": "Comfortable separates with sneakers.",
                "College": "A relaxed co-ord or jeans with a top.",
                "Office": "Tailored trousers with a clean shirt.",
                "Party": "A statement dress or coordinated evening look.",
                "Wedding": "A saree, lehenga or occasion-appropriate suit.",
                "Interview": "A neat, well-fitted formal outfit.",
                "Travel": "Comfortable layers and versatile basics.",
            }

            st.markdown(
                f"<div class='nova-card'>"
                f"<h3>{style} · {occasion}</h3>"
                f"<p>{outfit_ideas.get(occasion, 'Explore versatile outfits.')}</p>"
                f"<p>Budget: {budget}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )


# --------------------------------------------------
# MY WARDROBE / PRODUCT GALLERY
# --------------------------------------------------

elif page == "My Wardrobe":
    st.subheader("🛍️ My Wardrobe")
    st.write(
        "Build your own catalog by uploading real product images. "
        "This avoids showing an unrelated stock image as a product."
    )

    catalog_uploads = st.file_uploader(
        "Upload garment/product photos",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="wardrobe_uploads",
    )

    if catalog_uploads:
        cols = st.columns(3)

        for index, upload in enumerate(catalog_uploads):
            image = open_image(upload)

            if image is None:
                continue

            with cols[index % 3]:
                st.image(
                    image,
                    caption=upload.name,
                    use_container_width=True,
                )

                rgb = dominant_color(image)
                st.caption(
                    f"Approximate color: {color_name(rgb)}"
                )

                st.download_button(
                    "Download image",
                    data=image_bytes(image),
                    file_name=f"nova_product_{index + 1}.jpg",
                    mime="image/jpeg",
                    key=f"download_{index}",
                )
    else:
        st.info(
            "No products uploaded yet. Upload product photos to "
            "create your own visual catalog."
        )

    st.caption(
        "This gallery uses the images you provide. It does not "
        "automatically verify product names, prices, brands or stock."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<p style='text-align:center;color:#c9a8c6;'>"
    "✨ NOVA AI · Fashion meets intelligent personalization"
    "</p>",
    unsafe_allow_html=True,
)
