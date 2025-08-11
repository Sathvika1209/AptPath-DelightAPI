import streamlit as st
from typing import List, Dict


def _bot_reply(user_text: str) -> str:
    """Very small rule-based bot for common queries."""
    t = (user_text or '').lower()
    if any(k in t for k in ['order', 'track', 'tracking']):
        return "You can track your order from Track page or Dashboard. If it’s out for delivery, you’ll also see ETA."
    if any(k in t for k in ['refund', 'cancel', 'cancellation']):
        return "Orders can be cancelled while status is Pending or Confirmed from Dashboard > your order. Refunds reflect in 5-7 business days."
    if any(k in t for k in ['address', 'change address', 'edit address']):
        return "Go to Profile > Addresses to add or edit delivery addresses before checkout."
    if any(k in t for k in ['login', 'password', 'reset']):
        return "Use the Login screen’s Reset Password option. If needed, contact support@delightapi.com."
    if any(k in t for k in ['custom', 'design', 'photo']):
        return "Use the Customize page to place custom cake orders at supporting stores."
    return "Thanks! I’ve noted your question. Our team will reply soon at support@delightapi.com."


def main_page():
    st.title("🛟 Help & Support")
    st.markdown("---")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Live Chatbot")
        if 'support_chat' not in st.session_state:
            st.session_state.support_chat: List[Dict] = []
        chat = st.session_state.support_chat

        for entry in chat:
            role = entry.get('role')
            text = entry.get('text', '')
            if role == 'user':
                st.chat_message("user").markdown(text)
            else:
                st.chat_message("assistant").markdown(text)

        prompt = st.chat_input("Type your question…")
        if prompt:
            chat.append({'role': 'user', 'text': prompt})
            reply = _bot_reply(prompt)
            chat.append({'role': 'assistant', 'text': reply})
            st.session_state.support_chat = chat
            st.rerun()

    with c2:
        st.subheader("Contact")
        st.write("📧 **Email:** support@delightapi.com")
        st.write("📱 **Phone:** +91-9876543210")
        with st.expander("Send us a message"):
            message = st.text_area("Your message here…")
            if st.button("Send Message"):
                st.success("Your message has been sent to our support team.")

    st.markdown("---")
    st.subheader("FAQs")
    faqs = [
        ("How do I track my order?", "Go to the Track page or Dashboard and select your order to view status and ETA."),
        ("Can I cancel my order?", "Yes, while the status is Pending or Confirmed—open the order in Dashboard and tap Cancel."),
        ("How do I change my delivery address?", "Use Profile > Addresses to add/edit an address. Choose it at checkout."),
        ("Do you support custom cakes?", "Yes! Use the Customize page. Some stores show a ✅ Custom Cakes badge."),
        ("I forgot my password.", "Open Login and use Reset Password. If you’re stuck, mail support@delightapi.com."),
    ]
    for q, a in faqs:
        with st.expander(q):
            st.write(a)
