import os
from dotenv import load_dotenv
from langfuse import Langfuse
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

load_dotenv()

# Initialize Langfuse telemetry tracking
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

MODEL_ID = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=os.getenv("HF_TOKEN"))
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, token=os.getenv("HF_TOKEN"))

def translate_message(text: str, source_lang: str, target_lang: str) -> str:
    """Translates incoming/outgoing customer messages and logs metrics to Langfuse."""
    trace = langfuse.trace(
        name="customer_support_translation",
        metadata={
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    )
    
    try:
        inputs = tokenizer(text, return_tensors="pt")
        target_lang_id = tokenizer.lang_code_to_id.get(target_lang)
        
        translated_tokens = model.generate(
            **inputs, 
            forced_bos_token_id=target_lang_id
        )
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        
        trace.generation(
            name="nllb_translation_step",
            model=MODEL_ID,
            input=text,
            output=translated_text,
            metadata={"token_count": len(translated_tokens[0])}
        )
        
        return translated_text
    except Exception as e:
        trace.update(output=str(e), level="ERROR")
        raise e