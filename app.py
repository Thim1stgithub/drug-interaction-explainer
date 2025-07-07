import streamlit as st
import pandas as pd
from simplify_model import Simplifier
from umls_utils import get_service_ticket, get_umls_definition

# Setup
st.set_page_config(page_title="Drug Interaction Explainer", layout="centered")
st.title("💊 Drug Interaction Explainer")
st.markdown("This app explains drug interaction descriptions using a fine-tuned T5 model and optionally shows UMLS definitions.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/with_cuis_semantic_unique.csv", encoding="ISO-8859-1")

df = load_data()

# Create combined drug pair column
df["pair_str"] = df["Drug_1"] + " + " + df["Drug_2"]
pair_list = sorted(df["pair_str"].unique())

# Load model
with st.spinner("🔄 Loading T5 Simplifier Model..."):
    simplifier = Simplifier()

# UMLS Setup
api_key = st.secrets["UMLS_API_KEY"]
tgt = get_service_ticket(api_key)

# --- Select Drug Pair ---
st.subheader("🔍 Select Drug Pair")
selected_pair = st.selectbox("Choose a Drug Pair", pair_list)
drug1, drug2 = selected_pair.split(" + ")

# Filter row
selected_rows = df[(df["Drug_1"] == drug1) & (df["Drug_2"] == drug2)]
if selected_rows.empty:
    st.warning("⚠️ No interaction found for the selected pair.")
else:
    selected_row = selected_rows.iloc[0]
    interaction_text = selected_row["Interaction_Description"]
    cui1 = selected_row.get("cui_1", None)
    cui2 = selected_row.get("cui_2", None)

    # Original text
    st.markdown("**🧪 Original Interaction Description:**")
    st.info(interaction_text)

    # T5 Simplification
    with st.spinner("🔎 Simplifying..."):
        simplified_text = simplifier.simplify(interaction_text)
    st.markdown("**🤖 Simplified Explanation:**")
    st.success(simplified_text)

    # CUIs and Definitions
    st.subheader("📘 UMLS CUI Codes")
    #show_def = st.checkbox("Show UMLS Definitions", value=False)

    if cui1:
        st.markdown(f"🧬 **{drug1}** — CUI: `{cui1}`")
        #if show_def:
            #def1 = get_umls_definition(cui1, tgt)
            #st.info(def1 if def1 else "No definition found.")

    if cui2:
        st.markdown(f"🧬 **{drug2}** — CUI: `{cui2}`")
        #if show_def:
            #def2 = get_umls_definition(cui2, tgt)
            #st.info(def2 if def2 else "No definition found.")

# --- Custom Interaction Description ---
st.subheader("✍️ Try Your Own Interaction Text")
user_input = st.text_area("Paste any drug interaction description below:")

if st.button("Simplify It"):
    if user_input.strip():
        with st.spinner("🔎 Simplifying your input..."):
            user_result = simplifier.simplify(user_input)
        st.markdown("**🧠 Simplified Explanation:**")
        st.success(user_result)
    else:
        st.warning("⚠️ Please enter a valid description.")
