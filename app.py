import streamlit as st
from docx import Document
from datetime import date
import os

st.set_page_config(page_title="Janaza Attest Generator", layout="centered")
st.title("🧾 Attest Rituele Verzorging")

st.markdown("Vul onderstaande gegevens in:")

with st.form("attest_form"):
    moskee = st.selectbox("Selecteer moskee", [
        "El Mohsinien ICCEM", "El Fath En Nassr"
    ])
    naam = st.text_input("Naam")
    voornaam = st.text_input("Voornaam")
    datum = st.date_input("Datum", value=date.today())
    bestandsnaam = st.text_input("Bestandsnaam (.docx)", value="attest_rituele_verzorging")
    submitted = st.form_submit_button("✅ Genereer attest")

if submitted:
    template_file = "template_mohsinien.docx" if moskee == "El Mohsinien ICCEM" else "template_fath_en_nassr.docx"

    if not os.path.exists(template_file):
        st.error(f"❗ Templatebestand '{template_file}' ontbreekt.")
    else:
        doc = Document(template_file)
        vervangingen = {
            "<<NAAM>>": naam,
            "<<VOORNAAM>>": voornaam,
            "<<DATUM>>": datum.strftime("%d/%m/%Y")
        }

        for para in doc.paragraphs:
            for run in para.runs:
                for key, val in vervangingen.items():
                    if key in run.text:
                        run.text = run.text.replace(key, val)

        output_docx = f"{bestandsnaam}.docx"
        doc.save(output_docx)

        with open(output_docx, "rb") as f:
            st.success("✅ Attest succesvol gegenereerd!")
            st.download_button("📥 Download .docx", f, file_name=output_docx, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")