import streamlit as st
import json
import pyperclip
from vcf_parser import VCFParse

from vcf_parser import VCFParse
# import streamlit as st
from llm_parser import LLMParser
import json, datetime

import debug

llmparse = LLMParser
parser = VCFParse

vcfparse = VCFParse

##
debug_status = True
##

st.set_page_config(page_title="PharmaGuard", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

.stApp {
    background: linear-gradient(135deg, #0d1117 0%, #0f1923 50%, #0d1a2b 100%);
}

/* Title block */
.title-block {
    padding: 2rem 0 1.5rem 0;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.5rem;
}
.main-title {
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #58a6ff, #79c0ff, #a5d6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.sub-title {
    font-size: 1rem;
    color: #8b949e;
    margin-top: 0.4rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-weight: 600;
}

/* Section labels */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 0.4rem;
}

/* Check badges row */
.checks-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
}
.check-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 2rem;
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    color: #e6edf3;
    transition: border-color 0.2s;
}
.check-badge.pass { border-color: #238636; color: #3fb950; }
.check-badge.warn { border-color: #9e6a03; color: #d29922; }
.check-badge.fail { border-color: #da3633; color: #f85149; }
.check-badge .dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }

/* JSON card */
.json-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    position: relative;
}
.json-card-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 0.5rem;
}

/* Info panel */
.info-panel {
    border-radius: 10px;
    padding: 1.4rem;
    height: 100%;
    min-height: 320px;
    border: 1px solid rgba(255,255,255,0.08);
}
.info-panel h3 {
    margin-top: 0;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.info-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    font-size: 0.85rem;
}
.info-item:last-child { border-bottom: none; }
.info-key { color: rgba(255,255,255,0.6); }
.info-val { font-weight: 600; font-family: 'JetBrains Mono', monospace; }

/* Divider */
.divider { border-top: 1px solid #21262d; margin: 1.2rem 0; }

/* Override streamlit elements */
.stSelectbox > div, .stMultiSelect > div {
    background: #161b22 !important;
    border-color: #30363d !important;
}
.stFileUploader {
    background: #161b22;
    border: 1px dashed #30363d;
    border-radius: 8px;
    padding: 0.5rem;
}
button[kind="secondary"] {
    background: #21262d !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)
panel_color = "#0f2a1e"

# header of page
st.markdown("""
<div class="title-block">
  <h2 class="main-title">PharmaGuard</h2>
  <p class="sub-title">Pharmacogenomic Risk Prediction System</p>
</div>
""", unsafe_allow_html=True)

col_upload, col_drugs = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown('<p class="section-label">Upload VCF File</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="",
        type=["vcf", "csv", "txt", "json", "tsv"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✓ {uploaded_file.name}  ({uploaded_file.size:,} bytes)")

with col_drugs:
    st.markdown('<p class="section-label">Choose Drugs</p>', unsafe_allow_html=True)
    drug_options = ["CODEINE", "WARFARIN", "CLOPIDOGREL", "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"]
    selected_drugs = st.multiselect(
        label="",
        options=drug_options,
        default=[],
        placeholder="Choose one or more drugs…",
        label_visibility="collapsed"
    )
    if selected_drugs:
        badges = "".join([
            f'<span style="display:inline-block;background:#1f2d3d;border:1px solid #58a6ff33;'
            f'border-radius:4px;padding:2px 10px;margin:3px;font-size:0.78rem;'
            f'font-family:JetBrains Mono,monospace;color:#79c0ff;">{d}</span>'
            for d in selected_drugs
        ])
        st.markdown(badges, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
<style>
/* Full-width run button */
div[data-testid="stButton"] > button.run-btn {
    width: 100%;
}
.run-btn-wrap {
    width: 100%;
}
/* Style the primary button */
div[data-testid="stButton"] button[kind="primary"] {
    width: 100%;
    background: linear-gradient(90deg, #1a56db 0%, #0e3fa1 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    color: #ffffff !important;
    text-transform: uppercase !important;
    cursor: pointer;
    transition: opacity 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 0 20px rgba(88,166,255,0.18) !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    opacity: 0.88 !important;
    box-shadow: 0 0 32px rgba(88,166,255,0.35) !important;
}
div[data-testid="stButton"] button[kind="primary"]:active {
    opacity: 0.75 !important;
}
</style>
""", unsafe_allow_html=True)

run_analysis = st.button(
    "-- Parse and Generate Report --",
    type="primary",
    use_container_width=True,
    key="run_analysis_btn"
)

if run_analysis:
    st.session_state["analysis_run"] = True
output_1 = {
            "label": "Report",
            "data": {"PharmaGuard":"PHARMACOGENOMIC RISK PREDICTION SYSTEM"}
}

sample_jsons = [
    output_1
]

status_succ = status_ext = status_size = status_header =status_selected= "warn"

risk_level = "-"
patient_id= 11

if st.session_state.get("analysis_run"):
    # print(selected_drugs)
    
    file_path = str(uploaded_file.name)
    validate_out = vcfparse.validate(file_path=file_path)

    if(selected_drugs):
        if validate_out['vcf_parsing_success'] == True: status_succ ="pass"
        else: status_succ = "fail"

        if validate_out['extension'] == ".vcf": status_ext ="pass"
        else: status_ext = "fail"

        if int(validate_out['file_size']) < 5: status_size ="pass"
        else: status_size = "fail"

        if validate_out['header'] == True: status_header ="pass"
        else: status_header = "fail"
        status_selected = "pass"

        output_1 = {}

        if(debug_status==True):
            sample_jsons = []
            output_1 = {"label":"Report for CODEINE","data":debug.single}
            op2 = {"label":"Report for WARFARIN", "data":debug.m}
            risk_level = debug.single[0]['risk_assessment']['risk_label']
            sample_jsons.append(output_1)
            sample_jsons.append(op2)
        else: 
            sample_jsons = []
            for drug in selected_drugs:
                parsed = parser.parse(file_path)
                gene_match = parser.gene_match(parser.parse(file_path))
                llm_output = LLMParser.llm(parser.parse(file_path),parser.gene_match(parser.parse(file_path)), drug)
                # llm_output.replace('json','')
                # print(llm_output)
                j = json.loads(llm_output)
                d = j['pharmacogenomic_profile']
                d['detected_variants'] = [ gene_match ]
                output = { "patient_id": f"PATIENT {patient_id}",
                    "drug": drug,
                    "timestamp": str(datetime.datetime.now()).replace("-", "").replace(".","").replace(" ", ""),
                    "risk_assessment": j['risk_assessment'],
                    "pharmacogenomic_profile": d,
                    "clinical_recommendation": j['clinical_recommendation'],
                    "llm_generated_explanation": j['llm_generated_explanation'],
                    "quality_metrics": VCFParse.validate(file_path)
                }
                risk_level =  j['risk_assessment']['risk_label']
                ou = {"label": f"Report for {drug}", "data": output}
                sample_jsons.append(ou)
                
        if risk_level == "Safe": panel_color = "#34bc56"
        elif risk_level == "Adjust Dosage": panel_color = "#f69f76"
        elif risk_level == "Toxic": panel_color = "#dd4444"
        else: panel_color = "#f69f76"

    else: 
        status_succ = status_ext = status_size = status_header = "warn"
        status_selected = "fail"

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">Checks</p>', unsafe_allow_html=True)

checks = [
    ("VCF Parse Success", status_succ),
    ("File Extension (.vcf)", status_ext),
    ("File Size (under 2 MB)", status_size),
    ("Header Check", status_header),
    ("Drug Selection", status_selected),
    # ("TPMT Status", "pass"),
    # ("DPYD Screening", "fail"),
    # ("SLCO1B1 Check", "pass"),
    # ("Gene Coverage QC", "pass"),
    # ("Allele Phasing", "warn"),
    # ("VCF Format Valid", "pass"),
]

icons = {"pass": "✓", "warn": "⚠", "fail": "✗"}

badge_html = '<div class="checks-row">'
for label, status in checks:
    badge_html += f'<span class="check-badge {status}"><span class="dot"></span>{icons[status]} {label}</span>'
badge_html += '</div>'
st.markdown(badge_html, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col_json, col_info = st.columns([1.1, 0.9], gap="large")

# sample_jsons = [
#     {
#         "label": "Gene-Drug Interactions",
#         "data": {
#             "patient_id": "PGX-2024-001",
#             "drug": "WARFARIN",
#             "gene": "CYP2C9",
#             "diplotype": "*1/*3",
#             "phenotype": "Intermediate Metabolizer",
#             "recommendation": "Reduce dose by 25–40%",
#             "evidence_level": "1A"
#         }
#     },
#     {
#         "label": "DPYD Variant Report",
#         "data": {
#             "gene": "DPYD",
#             "drug": "FLUOROURACIL",
#             "variant": "c.1905+1G>A",
#             "rsid": "rs3918290",
#             "activity_score": 0.5,
#             "phenotype": "Intermediate Metabolizer",
#             "recommendation": "50% dose reduction or alternative therapy",
#             "toxicity_risk": "HIGH"
#         }
#     },
#     {
#         "label": "Full PGx Summary",
#         "data": {
#             "report_version": "2.1.0",
#             "analysis_date": "2025-02-19",
#             "genes_analyzed": 12,
#             "actionable_findings": 3,
#             "drugs_screened": ["WARFARIN", "CLOPIDOGREL", "SIMVASTATIN"],
#             "overall_risk": "MODERATE",
#             "clinical_review_required": True
#         }
#     }
# ]

with col_json:
    st.markdown('<p class="section-label">JSON Outputs</p>', unsafe_allow_html=True)
    for item in sample_jsons:
        json_str = json.dumps(item["data"], indent=2)
        st.markdown(f'<div class="json-card-label">{item["label"]}</div>', unsafe_allow_html=True)
        st.code(json_str, language="json")
        dl_col, cp_col, _ = st.columns([1, 1, 2])
        with dl_col:
            st.download_button(
                label="⬇ Download",
                data=json_str,
                file_name=f'{item["label"].lower().replace(" ", "_")}.json',
                mime="application/json",
                key=f"dl_{item['label']}"
            )
        with cp_col:
            if st.button("⧉ Copy", key=f"cp_{item['label']}"):
                st.session_state[f"copied_{item['label']}"] = True
            if st.session_state.get(f"copied_{item['label']}"):
                st.caption("✓ Copied!")

with col_info:
    st.markdown('<p class="section-label">Essential Summary Panel</p>', unsafe_allow_html=True)

    # Color picker for the panel
    # panel_color = "#0f2a1e"

    # # Derive text color based on brightness
    # hex_c = panel_color.lstrip("#")
    # r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
    # brightness = (r * 299 + g * 587 + b * 114) / 1000
    text_color = "#ffffff"
    accent_color = "#460A64"

    info_items = [
        ("Patient ID", patient_id),
        # ("Genes Analyzed", "12"),
        # ("Actionable Findings", output_1["data"][0]['risk_assessment']['risk_label']),
        ("Overall Risk", risk_level),
        ("Drugs Flagged", ", ".join(selected_drugs) if selected_drugs else "None"),
        ("Report Status", "Pending Review" if not uploaded_file else "Ready"),
        ("Evidence Level", "CPIC 1A / 2A"),
        ("Analysis Engine", "PGxCore"),
    ]

    rows_html = "".join([
        f'<div class="info-item">'
        f'<span class="info-key" style="color:rgba({"255,255,255"},0.55);">{k}</span>'
        f'<span class="info-val" style="color:{text_color};">{v}</span>'
        f'</div>'
        for k, v in info_items
    ])

    st.markdown(f"""
    <div class="info-panel" style="background:{panel_color}; border-color:rgba({'255,255,255'},0.12);">
      <h3 style="color:{text_color}; border-bottom:1px solid rgba({'255,255,255'},0.15); padding-bottom:0.6rem; margin-bottom:0.6rem;">
        Clinical Summary
      </h3>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)