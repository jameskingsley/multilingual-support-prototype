import streamlit as st
from src.translator import translate_message

st.set_page_config(page_title="Multilingual Support Hub", layout="wide")

st.title("Global Customer Support Real-Time Translation Engine")
st.caption("Powered by Hugging Face Models & Monitored via Langfuse Telemetry")

# Supported Languages mapping with NLLB language codes
LANGUAGES = {
    "English": "eng_Latn",
    "Spanish": "spa_Latn",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Nigerian Pidgin": "pcm_Latn"
}

st.sidebar.header("Agent Workspace Settings")
agent_lang_name = st.sidebar.selectbox("Agent Native Language", list(LANGUAGES.keys()), index=0)
customer_lang_name = st.sidebar.selectbox("Customer Native Language", list(LANGUAGES.keys()), index=1)

agent_lang = LANGUAGES[agent_lang_name]
customer_lang = LANGUAGES[customer_lang_name]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Incoming Customer View ({customer_lang_name})")
    customer_input = st.text_area(
        "Inbound Customer Ticket / Chat Input:", 
        "Abeg my package never reach me o, I need help urgently for refund!"
    )

with col2:
    st.subheader(f"Agent Workspace ({agent_lang_name})")
    
    if st.button("Translate Inbound Message"):
        with st.spinner("Translating via Hugging Face model..."):
            translated_inbound = translate_message(customer_input, source_lang=customer_lang, target_lang=agent_lang)
            st.success("Message Translated & Logged to Langfuse")
            st.markdown(f"> **Customer Message:** {translated_inbound}")

    agent_reply = st.text_area(
        "Draft Agent Reply:", 
        "Hello! I am checking your tracking details right now to process your refund."
    )
    
    if st.button("Translate & Dispatch Reply to Customer"):
        with st.spinner("Translating outbound response..."):
            translated_outbound = translate_message(agent_reply, source_lang=agent_lang, target_lang=customer_lang)
            st.success("Dispatched to Customer & Logged to Langfuse")
            st.markdown(f"> **Outgoing (Customer Native):** {translated_outbound}")