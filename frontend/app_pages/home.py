import base64
import datetime
import os
import requests
import streamlit as st
from app_pages import customize, track, support, profile, cart, dashboard, map_demo, stores, cakes_catalog, cake_detail, search, store_detail, login
from app_pages.data import CAKES, STORES


def home_page():
    """Landing/home content: cake gallery + flash sale countdown (store-aware)."""
    # Image files reside in frontend/images; build absolute paths robustly
    images_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'images'))
    # Hide the 'Custom Cake' from the home gallery list (button remains elsewhere)
    cake_data = [c for c in CAKES if c.get('id') != 'custom']

    # Begin translucent content wrapper
    st.markdown("<div class='content-translucent'>", unsafe_allow_html=True)

    for i in range(0, len(cake_data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(cake_data):
                cake = cake_data[i + j]
                filename = cake.get('image', '')
                name = cake.get('name', 'Cake')
                img_path = os.path.join(images_dir, filename)
                try:
                    with open(img_path, "rb") as file:
                        img_encoded = base64.b64encode(file.read()).decode()
                    with cols[j]:
                        st.markdown(f"""
                            <div class=\"cake-box\">
                                <img src=\"data:image/jpeg;base64,{img_encoded}\" class=\"cake-img\">
                                <div class=\"cake-title\">{name}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("View details", key=f"view_home_{cake.get('id','')}\_{i}_{j}"):
                            st.session_state.selected_cake_id = cake.get('id')
                            st.session_state.page = 'cake_detail'
                            st.rerun()
                except FileNotFoundError:
                    with cols[j]:
                        st.error(f"Image not found: {filename}")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='flash-sale'>", unsafe_allow_html=True)
    st.markdown("<h3>🎁 Flash Sale</h3>", unsafe_allow_html=True)
    end_time = datetime.datetime(2025, 7, 25, 23, 59, 59)
    remaining = end_time - datetime.datetime.now()
    d, s = remaining.days, remaining.seconds
    h = s // 3600
    m = (s % 3600) // 60
    s = s % 60
    st.markdown(f"<p style='margin:0 0 6px 0;'>⏳ Ends in: <code>{d}d {h}h {m}m {s}s</code></p>", unsafe_allow_html=True)
    st.markdown("<ul style='list-style:disc'>", unsafe_allow_html=True)
    st.markdown("<li>🎉 <strong>10% off</strong> Chocolate Cakes</li>", unsafe_allow_html=True)
    st.markdown("<li>🎂 Free delivery on <strong>₹500+</strong></li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div><hr style='opacity:0.4'>", unsafe_allow_html=True)
    st.markdown("<center><small style='opacity:0.7;'>© 2025 DelightAPI</small></center>", unsafe_allow_html=True)
    # Close translucent wrapper
    st.markdown("</div>", unsafe_allow_html=True)

def main_page():
    # Ensure a default page is set
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    # Force LIGHT theme globally
    st.session_state.ui_theme = 'light'
    # Default store selection
    if 'store_id' not in st.session_state:
        st.session_state.store_id = next(iter(STORES.keys())) if STORES else None
    light_vars = {
        'bg':'#ffffff','bg_alt':'#fafafa','surface':'#ffffff','surface_alt':'#f4f4f8','border':'#e3e3e8',
        'shadow':'0 2px 8px rgba(0,0,0,0.06)','text':'#1e1e25','text_soft':'#4a4a56','heading':'#1e1e25',
        'accent':'#ff3c6f','primary':'#000080','cake_title':'#6c3483'
    }
    chosen = light_vars
    root_overrides = "\n".join([f"--{k}:{v};" for k,v in chosen.items()])
    st.markdown(f"""
    <style>
    :root {{ --color-accent-grad-start:#ff3c6f; --color-accent-grad-end:#000080; --color-primary:#000080; {root_overrides} }}
    :root {{
        --bg-alt: var(--bg_alt);
        --surface-alt: var(--surface_alt);
        --text-soft: var(--text_soft);
        --cake-title: var(--cake_title);
    }}
    /* Preserve landing background image (only set color) */
    body,.stApp {{ background-color:var(--bg); color:var(--text)!important; }}
    .content-translucent {{
        background: rgba(255,255,255,0.60);
        -webkit-backdrop-filter: blur(6px) saturate(130%);
        backdrop-filter: blur(6px) saturate(130%);
        padding: 1.5rem 1.8rem 2.2rem;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.55);
        box-shadow: 0 8px 34px -10px rgba(0,0,0,0.35);
        margin-top: 8px;
    }}
    .nav-bar-wrapper {{ display:flex; align-items:center; gap:1.25rem; padding:10px 32px 14px; background:linear-gradient(90deg,var(--surface),var(--surface-alt)); border-bottom:1px solid var(--border); box-shadow:var(--shadow); flex-wrap:wrap; backdrop-filter:blur(6px); position: sticky; top: 0; z-index: 1000; }}
    .brand-title {{ font-size:30px; font-family:Georgia,serif; font-weight:700; background:linear-gradient(90deg,var(--accent),var(--primary)); -webkit-background-clip:text; color:transparent; margin-right:8px; }}
    .nav-buttons-row {{display:flex; gap:.65rem; flex-wrap:wrap;}}
    .nav-buttons-row .stButton>button {{background:transparent; color:var(--text_soft); border:1px solid var(--border); padding:.55rem 1.15rem; font-size:.87rem; font-weight:600; border-radius:9px; box-shadow:0 1px 4px -2px rgba(0,0,0,0.2); transition:.18s;}}
    .nav-buttons-row .stButton>button:hover {{transform:translateY(-2px); background:var(--surface); color:var(--text); border-color:var(--primary); box-shadow:var(--shadow);}}
    .theme-select label {{font-size:.6rem; text-transform:uppercase; letter-spacing:.08em; color:var(--text_soft); margin-bottom:2px;}}
    .cake-box {{border:1px solid var(--border); background:var(--surface); box-shadow:var(--shadow); padding:18px 18px 20px; border-radius:20px; transition:.18s;}}
    .cake-box:hover {{box-shadow:0 8px 24px -6px rgba(0,0,0,0.35); transform: translateY(-3px);}}
    .cake-img {{border-radius:14px; width:230px; height:230px; object-fit:cover; display:block; margin:0 auto 10px;}}
    .cake-title {{color:var(--cake_title); font-weight:600; font-size:1.05rem; text-align:center; letter-spacing:.5px;}}
    .store-banner {{
        padding: 8px 12px; margin: 0 0 10px; border: 1px solid var(--border);
        background: var(--surface-alt); border-radius: 10px; font-size: .9rem; color: var(--text);
    }}
    .cake-box.unavailable {{opacity:0.55; filter:grayscale(0.1);}} 
    .avail {{text-align:center; font-size:.78rem; margin-top:4px;}}
    .avail.ok {{color:#1a7f37;}}
    .avail.no {{color:#b23b3b;}}
    .flash-sale {{background:var(--surface_alt); border:1px solid var(--border); box-shadow:var(--shadow); border-radius:18px; padding:20px 26px 18px; margin-top:18px; color:var(--text);}}
    .flash-sale h3 {{margin:0 0 8px 0; font-size:1.25rem; background:linear-gradient(90deg,var(--accent),var(--primary)); -webkit-background-clip:text; color:transparent; font-weight:700; -webkit-text-stroke:0.6px rgba(0,0,0,0.18);}}
    .flash-sale ul {{padding-left:1.1rem; margin:0 0 6px;}}
    .flash-sale li {{margin-bottom:6px; font-size:0.95rem; color:var(--text);}}
    .flash-sale code {{background:rgba(0,0,0,0.08); color:var(--accent); padding:3px 9px; border-radius:8px; font-weight:600; box-shadow:inset 0 0 0 1px rgba(0,0,0,0.05);}}
    .stMarkdown code, code {{background:rgba(0,0,0,0.08); color:var(--accent); padding:2px 6px; border-radius:6px;}}
    /* Bottom nav */
    /* Floating bottom nav: centered, glassy, always visible */
    .bottom-nav {{
        position: fixed;
        bottom: 14px;
        left: 50%;
        transform: translateX(-50%);
        width: min(720px, 96vw);
        background: rgba(255,255,255,0.92);
        border: 1px solid var(--border);
        border-radius: 16px;
        box-shadow: 0 12px 28px -10px rgba(0,0,0,0.35);
        padding: 10px 14px 8px;
        z-index: 9999;
        backdrop-filter: saturate(140%) blur(10px);
    }}
    .bottom-nav .stButton>button {{ width:100%; border-radius:12px; padding:10px 8px; font-size:26px; line-height:1; }}
    /* Improve visibility of +/- small buttons */
    .stButton>button:has(span:contains('➖')), .stButton>button:has(span:contains('➕')) {{
        font-size: 18px !important;
        padding: 6px 0 !important;
    }}
    .bottom-nav .nav-cap {{ display:block; font-size:.72rem; color:var(--text_soft); margin-top:2px; text-align:center; }}
    .bottom-nav .nav-cap.active {{ color: var(--primary); font-weight: 700; }}
    .bottom-nav .indicator {{ height:3px; width:22px; border-radius:3px; background:transparent; margin:3px auto 0; }}
    .bottom-nav .indicator.active {{ background: var(--primary); }}
    .pill-badge {{ display:inline-block; background:#ff3c6f; color:#fff; font-weight:700; font-size:.70rem; line-height:1; border-radius:999px; padding:3px 6px; margin-left:6px; }}
    /* Keep content readable above bottom bar */
    .main .block-container {{ padding-bottom: 120px; }}
    @media (max-width: 1100px) {{
        .cake-img {{width:200px; height:200px;}}
    }}
    @media (max-width: 900px) {{
        .cake-img {{width:180px; height:180px;}}
    }}
    @media (max-width: 750px) {{
        .cake-img {{width:150px; height:150px;}}
    }}
    </style>
    <!-- Theme locked to light; removed dynamic theme script -->
    """, unsafe_allow_html=True)

    # Compute cart count once for badges
    API_BASE_URL = "http://127.0.0.1:8000/api"
    token = st.session_state.get('token', '')
    cart_count = 0
    try:
        if token:
            r = requests.get(f"{API_BASE_URL}/cart/", headers={"Authorization": f"Token {token}"})
            if r.status_code == 200:
                cart_count = len(r.json())
    except Exception:
        cart_count = 0

    # Top navigation + theme select
    nav_labels = [
        ("🏬 Stores", 'stores'), ("🍰 Cakes", 'cakes'), ("📊 Dashboard", 'dashboard'), ("🎨 Customize", 'customize'),
        ("📦 Track", 'track'), ("🛟 Support", 'support'), ("🗺️ Map", 'map_demo')
    ]
    nav_cols = st.columns([3,7,2])
    with nav_cols[0]:
        st.markdown('<div class="brand-title">🎂 DelightAPI</div>', unsafe_allow_html=True)
    with nav_cols[1]:
        st.markdown('<div class="nav-buttons-row">', unsafe_allow_html=True)
        btn_cols = st.columns(len(nav_labels))
        for (label, page_name), col in zip(nav_labels, btn_cols):
            with col:
                if st.button(label, key=f"nav_{page_name}"):
                    st.session_state.page = page_name
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with nav_cols[2]:
        rc = st.columns([1,1])
        with rc[0]:
            # bell icon for notifications (placeholder)
            if st.button("�", key="nav_right_bell"):
                st.info("No new notifications.")
        with rc[1]:
            # simple avatar button (first letter)
            initials = (st.session_state.get('username','U') or 'U')[0].upper()
            if st.button(f"{initials}", key="nav_right_avatar"):
                st.session_state.page = 'profile'
                st.rerun()

    # Floating chips removed in favor of top-right icons and bottom nav

    # --- Page Renderer based on st.session_state.page ---
    page = st.session_state.get('page', 'home')
    if page == 'home':
        home_page()
    elif page == 'dashboard':
        dashboard.main_page()
    elif page == 'customize':
        customize.main_page()
    elif page == 'track':
        track.main_page()
    elif page == 'support':
        support.main_page()
    elif page == 'cart':
        cart.main_page()
    elif page == 'profile':
        profile.main_page()
    elif page == 'map_demo':
        map_demo.map_demo_page()
    elif page == 'stores':
        stores.main_page()
    elif page == 'cakes':
        cakes_catalog.main_page()
    elif page == 'cake_detail':
        cake_detail.main_page()
    elif page == 'search':
        search.main_page()
    elif page == 'store_detail':
        store_detail.main_page()
    elif page == 'login':
        login.login_page()
    else:
        home_page()

    # Fixed bottom navigation (always visible)
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    bcols = st.columns(3)
    # Home
    with bcols[0]:
        if st.button("🏠", key="bottom_home"):
            st.session_state.page = 'home'
            st.rerun()
        is_active = page in ('home',)
        st.markdown(f'<span class="nav-cap{" active" if is_active else ""}">Home</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="indicator{" active" if is_active else ""}"></div>', unsafe_allow_html=True)
    # Search (tabbed search page)
    with bcols[1]:
        if st.button("🔎", key="bottom_search"):
            st.session_state.page = 'search'
            st.rerun()
        is_active = page in ('search','stores','cakes','cake_detail','store_detail')
        st.markdown(f'<span class="nav-cap{" active" if is_active else ""}">Search</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="indicator{" active" if is_active else ""}"></div>', unsafe_allow_html=True)
    # Cart
    with bcols[2]:
        if st.button("🛒", key="bottom_cart"):
            st.session_state.page = 'cart'
            st.rerun()
        is_active = page in ('cart',)
        if cart_count > 0:
            st.markdown(f'<span class="nav-cap{" active" if is_active else ""}">Cart <span class="pill-badge">{cart_count}</span></span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="nav-cap{" active" if is_active else ""}">Cart</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="indicator{" active" if is_active else ""}"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)