import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="JK Enterprises", layout="wide")
st.title("JK Enterprises - Bank Reconcile (Option B)")

st.write("BEAWAR Excel + RGB PDF - True/False Check")

# --- True/False Logic ---
def check_true_false(bwr_total, bank_total, allowed_rs=1000, allowed_pct=2.0):
    diff = abs(bwr_total - bank_total)
    diff_pct = (diff / bwr_total * 100) if bwr_total else 0
    final = (diff <= allowed_rs) or (diff_pct <= allowed_pct)
    return diff, round(diff_pct,2), final

tab1, tab2 = st.tabs(["1. RGB PDF Upload", "2. Daily Check"])

with tab1:
    pdf = st.file_uploader("RGB Bank PDF upload karo", type=["pdf"])
    if pdf:
        import fitz
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        text_all = ""
        for page in doc:
            text_all += page.get_text() + "\n"
        
        # UPI IDs nikalna
        upi_pat = r'([a-zA-Z0-9.\-_]+@[a-z]+)'
        upis = re.findall(upi_pat, text_all)
        
        # Credit Sum nikalna - Aapki PDF me Credits word hai
        credit_match = re.search(r'Credits\s+([\d.]+)', text_all)
        total_credit = float(credit_match.group(1)) if credit_match else 0
        
        st.success(f"PDF Read Ho Gayi!")
        st.metric("Total Credit (Aapka Sawal)", f"₹ {total_credit}")
        st.metric("Total UPI Transactions", len(upis))
        st.dataframe(pd.DataFrame(upis, columns=["Payer UPI"]))

with tab2:
    st.subheader("True/False on Number Check with Sum Variation")
    bwr = st.number_input("BWR ka Total Sale (Aaj ka)", value=720000)
    bank = st.number_input("Bank ka Total Credit (RGB + AU)", value=723232.0)
    allowed_rs = st.number_input("Kitna Rs. ka fark allow hai?", value=1000)
    allowed_pct = st.number_input("Kitna % fark allow hai?", value=2.0)
    
    diff, pct, final = check_true_false(bwr, bank, allowed_rs, allowed_pct)
    st.write(f"Difference: ₹ {diff} ({pct}%)")
    if final:
        st.success("TRUE - Hisab OK hai ✅")
    else:
        st.error("FALSE - Fark zyada hai, check karo ❌")
