import streamlit as st
from src.translator import translate_message

st.set_page_config(page_title="Multilingual Support Hub", layout="wide")

st.title("Global Customer Support Real-Time Translation Engine")
st.caption("Powered by Hugging Face Models & Monitored via Langfuse Telemetry")

st.sidebar.header("Agent Workspace Settings")
agent_lang = st.sidebar.selectbox("Agent Language", ["eng_Latn", "spa_Latn", "fra_Latn", "deu_Latn"])
customer_lang = st.sidebar.selectbox("Customer Native Language", ["spa_Latn", "eng_Latn", "fra_Latn", "deu_Latn"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Incoming Customer View (Native)")
    customer_input = st.text_area(
        "Inbound Customer Ticket / Chat Input:", 
        "¡Hola! Mi paquete no ha llegado y necesito asistencia urgente con el reembolso."
    )

with col2:
    st.subheader("Agent Translation & Dispatch Space")
    
    if st.button("Translate Inbound Message"):
        with st.spinner("Translating via Hugging Face model..."):
            translated_inbound = translate_message(customer_input, source_lang=customer_lang, target_lang=agent_lang)
            st.success("Message Translated & Logged to Langfuse")
            st.markdown(f"> **Customer Message (Agent Language):** {translated_inbound}")

    agent_reply = st.text_area(
        "Draft Agent Reply (in Agent Language):", 
        "Hello! I am checking your tracking details right now to process your refund."
    )
    
    if st.button("Translate & Dispatch Reply to Customer"):
        with st.spinner("Translating outbound response..."):
            translated_outbound = translate_message(agent_reply, source_lang=agent_lang, target_lang=customer_lang)
            st.success("Dispatched to Customer & Logged to Langfuse")
            st.markdown(f"> **Outgoing (Customer Native Language):** {translated_outbound}")