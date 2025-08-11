import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000/api"


def _headers():
    return {"Authorization": f"Token {st.session_state.get('token', '')}"}


def get_or_create_cake_id(name: str, price: float, size: str = "1 kg", flavor: str = "classic"):
    """Resolve a Cake PK by exact name from backend. If missing, do NOT auto-create here.
    Returns integer id or None if not found.
    """
    try:
        res = requests.get(f"{API_BASE_URL}/cakes/", headers=_headers())
        if res.status_code == 200:
            for c in res.json():
                if c.get('name') == name:
                    return c.get('id')
    except Exception as e:
        st.error(f"Error resolving cake: {e}")
        return None
    # Not found; advise seeding backend data
    st.error("Cake not found on backend. Please seed demo data: manage.py seed_demo")
    return None


def ensure_custom_cake_id(name: str, price: float, size: str, flavor: str):
    """Find or create a 'custom' cake variant on the backend.
    Tries to match by name+size+flavor; creates if missing.
    Returns PK or None on failure.
    """
    try:
        res = requests.get(f"{API_BASE_URL}/cakes/", headers=_headers())
        if res.status_code == 200:
            for c in res.json():
                if c.get('name') == name and c.get('size') == size and c.get('flavor','').lower() == flavor.lower():
                    return c.get('id')
        # Create
        payload = {"name": name, "flavor": flavor, "size": size, "price": price}
        cr = requests.post(f"{API_BASE_URL}/cakes/", headers=_headers(), json=payload)
        if cr.status_code in (200, 201):
            return cr.json().get('id')
        else:
            st.error(f"Could not create custom cake: {cr.status_code}")
            return None
    except Exception as e:
        st.error(f"Error creating custom cake: {e}")
        return None
