# frontend/app_pages/cake_detail.py
import os
import base64
import streamlit as st
import requests
from .data import CAKES, STORES
from .api_helpers import get_or_create_cake_id


def _get_cake(cake_id: str):
    for c in CAKES:
        if c.get('id') == cake_id:
            return c
    return None


def main_page():
    cake_id = st.session_state.get('selected_cake_id')
    cake = _get_cake(cake_id)
    if not cake:
        st.warning("No cake selected. Go back to Cakes.")
        if st.button("Back to Cakes"):
            st.session_state.page = 'cakes'
            st.rerun()
        return

    st.header(cake['name'])

    # image
    images_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'images'))
    img_path = os.path.join(images_dir, cake.get('image', ''))
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        st.image(f"data:image/jpeg;base64,{encoded}", caption=cake['name'])

    st.write(cake.get('description', 'A delightful cake.'))
    st.caption(f"Price: ₹{int(cake.get('price',0))}")

    # store selection (restricted to available stores for the cake)
    store_ids = cake.get('stores', [])
    store_names = [STORES[sid] for sid in store_ids if sid in STORES]
    if not store_names:
        st.error("This cake is currently unavailable in all stores")
        return
    chosen = st.selectbox("Choose a store", options=store_names, key=f"detail_store_{cake['id']}")
    chosen_sid = store_ids[store_names.index(chosen)]

    # quantity +/-
    qty_key = f"qty_{cake['id']}"
    if qty_key not in st.session_state:
        st.session_state[qty_key] = 1
    cols = st.columns([1,1,2])
    with cols[0]:
        if st.button("➖", key=f"minus_{cake['id']}"):
            st.session_state[qty_key] = max(1, st.session_state[qty_key] - 1)
    with cols[1]:
        if st.button("➕", key=f"plus_{cake['id']}"):
            st.session_state[qty_key] = st.session_state[qty_key] + 1
    with cols[2]:
        st.write(f"Quantity: {st.session_state[qty_key]}")

    # add to cart
    if st.button("Add to Cart", key=f"add_cart_{cake['id']}"):
        API_BASE_URL = "http://127.0.0.1:8000/api"
        headers = {"Authorization": f"Token {st.session_state.get('token', '')}"}
        resolved_id = get_or_create_cake_id(cake['name'], cake.get('price', 0), size="1 kg")
        payload = {"cake": resolved_id or cake['id'], "quantity": st.session_state[qty_key], "customization": f"store:{chosen_sid}"}
        try:
            resp = requests.post(f"{API_BASE_URL}/cart/", headers=headers, json=payload)
            if resp.status_code in (200, 201):
                st.success("Added to cart")
                go_cols = st.columns(2)
                with go_cols[0]:
                    if st.button("Go to Cart", key=f"go_cart_{cake['id']}"):
                        st.session_state.page = 'cart'
                        st.rerun()
                with go_cols[1]:
                    if st.button("Back to Cakes", key=f"back_cakes_{cake['id']}"):
                        st.session_state.page = 'cakes'
                        st.rerun()
            else:
                st.error("Failed to add to cart. Please login and try again.")
        except Exception as e:
            st.error(f"Error adding to cart: {e}")
