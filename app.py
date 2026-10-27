"""
Multimodal Construction Intelligence Platform (Skill Wallet Capstone Project 1)
Platform ID: 6ac4c98d1dcde6d7857c1642
Turnkey Production-Ready Streamlit Application in Python
"""
import streamlit as st
from PIL import Image
import io
import os

from modules.gemini_client import GeminiClientWrapper
from modules.safety_audit import run_safety_audit, render_safety_audit_ui
from modules.crack_diagnostics import run_crack_diagnostics, render_crack_diagnostics_ui
from modules.valuation_engine import render_valuation_ui
from modules.site_assistant import render_site_assistant_ui
from assets.sample_images import generate_sample_safety_image, generate_sample_crack_image

# 1. Page Configuration
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Styling for Production Theme
st.markdown("""
<style>
    /* Main App Layout */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    
    /* Header Gradient & Badges */
    .platform-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .platform-title {
        font-size: 28px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .platform-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-top: 6px;
    }
    .meta-tag {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-right: 8px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        color: #94A3B8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 700;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("### 🏗️ Platform Navigation")
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-bottom: 16px;">
            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">Platform Identifier</div>
            <div style="font-size: 12px; font-weight: 700; color: #38BDF8; font-family: monospace;">6ac4c98d1dcde6d7857c1642</div>
            <div style="font-size: 11px; color: #E2E8F0; margin-top: 4px;">Skill Wallet Capstone Project 1</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 🔑 Gemini API Key Configuration")
    user_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="AIzaSy...",
        help="Optional: Enter your Google Gemini API key. If omitted, the platform seamlessly runs in high-fidelity Demonstration Mode."
    )

    model_choice = st.selectbox(
        "Multimodal LLM Model",
        ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )

    # Instantiate Gemini Client Wrapper
    gemini_client = GeminiClientWrapper(api_key=user_api_key, model_name=model_choice)

    # API Status Badge
    if gemini_client.is_live:
        st.markdown(
            f"""
            <div style="background: rgba(46, 125, 50, 0.2); border: 1px solid #2E7D32; border-radius: 6px; padding: 8px 12px; margin-bottom: 16px;">
                <span style="color: #4ADE80; font-weight: 700; font-size: 13px;">🟢 Live Gemini Mode Active</span>
                <div style="font-size: 11px; color: #CBD5E1; margin-top: 2px;">Model: <code>{model_choice}</code></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background: rgba(2, 132, 199, 0.15); border: 1px solid #0284C7; border-radius: 6px; padding: 8px 12px; margin-bottom: 16px;">
                <span style="color: #38BDF8; font-weight: 700; font-size: 13px;">ℹ️ Demonstration Mode Active</span>
                <div style="font-size: 11px; color: #CBD5E1; margin-top: 2px;">Zero API key required. Rich engineering presets loaded.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("#### 📐 Statutory Standards & Codes")
    st.markdown("""
    - **OSHA 29 CFR 1926**: Safety and Health Regulations for Construction
    - **IS 456:2000**: Code of Practice for Plain and Reinforced Concrete
    - **IS 1893:2016**: Earthquake Resistant Design of Structures
    - **IS 13920:2016**: Ductile Design and Detailing of RCC
    - **IS 7861 (Part 1 & 2)**: Hot and Cold Weather Concreting
    - **ACI 224R-01**: Control of Cracking in Concrete Structures
    - **NBC 2016**: National Building Code of India
    """)

    st.markdown("---")
    st.markdown("#### 📋 Kanban Epics Coverage")
    st.markdown("""
    - `[x]` **Epic 1**: Environment & Requirements
    - `[x]` **Epic 2**: PPE Safety Vision & Crack Diagnostics
    - `[x]` **Epic 3**: Project Planning & Valuation in INR
    - `[x]` **Epic 4**: Multimodal AI & JSON Data Contracts
    - `[x]` **Epic 5**: Site Chatbot & Weather Advisory
    - `[x]` **Epic 6**: Interface, Testing & Cloud Deployment
    """)

    st.caption("v1.0.0 • Streamlit Community Cloud Ready • Zero External DB")

# 4. Main Page Header
st.markdown(
    """
    <div class="platform-header">
        <div style="margin-bottom: 8px;">
            <span class="meta-tag">GENERATIVE AI</span>
            <span class="meta-tag">REAL ESTATE DECISION SUPPORT</span>
            <span class="meta-tag">CIVIL & STRUCTURAL ENGINEERING</span>
        </div>
        <h1 class="platform-title">Multimodal Construction Intelligence Platform</h1>
        <p class="platform-subtitle">
            Enterprise decision-support system analyzing site photos for OSHA/IS 456 PPE safety compliance, 
            classifying concrete defects with structural severity scores, estimating project CapEx and real estate 
            valuation in INR, and delivering microclimate-aware daily protocols.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Core Application Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Tab 1 - Site Safety & PPE Audit",
    "🔍 Tab 2 - Crack Diagnostics & Integrity",
    "🏢 Tab 3 - Planning & Valuation (INR)",
    "🌦️ Tab 4 - Daily Site Assistant & Weather"
])

# -------------------------------------------------------------
# TAB 1: Site Safety & PPE Audit
# -------------------------------------------------------------
with tab1:
    st.markdown("### 🛡️ Site Safety & PPE Compliance Audit")
    st.caption("Epic 2: Multimodal vision inspection for PPE adherence under OSHA 1926 and IS 456 standards")

    col_up1, col_up2 = st.columns([1, 1.2])

    with col_up1:
        st.markdown("#### 1. Upload or Select Site Image")
        uploaded_safety_file = st.file_uploader(
            "Upload Construction Site Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="safety_uploader"
        )
        use_sample_safety = st.button("📸 Load Sample Site Photo (High-Rise Scaffolding Hazard)")

        active_safety_bytes = None
        active_mime = "image/png"

        if uploaded_safety_file is not None:
            active_safety_bytes = uploaded_safety_file.getvalue()
            active_mime = uploaded_safety_file.type
            st.image(active_safety_bytes, caption="Uploaded Construction Site Photo", use_container_width=True)
        elif use_sample_safety or "sample_safety_loaded" in st.session_state:
            st.session_state["sample_safety_loaded"] = True
            active_safety_bytes = generate_sample_safety_image()
            active_mime = "image/png"
            st.image(active_safety_bytes, caption="Preset: Scaffolding Worker without Harness & Exposed Rebar Hazard", use_container_width=True)
        else:
            st.info("👆 Upload a construction site photo above or click **'Load Sample Site Photo'** to test immediately.")

    with col_up2:
        st.markdown("#### 2. Audit Execution & Analysis")
        if active_safety_bytes:
            if st.button("⚡ Run Multimodal Safety & PPE Audit", type="primary", use_container_width=True):
                with st.spinner("Analyzing site hazards, PPE compliance, and OSHA/IS 456 regulations..."):
                    audit_res, is_live_call, status_note = run_safety_audit(
                        client=gemini_client,
                        image_bytes=active_safety_bytes,
                        mime_type=active_mime
                    )
                    st.session_state["safety_audit_result"] = audit_res
                    st.session_state["safety_is_live"] = is_live_call
                    st.session_state["safety_status_note"] = status_note

        if "safety_audit_result" in st.session_state:
            render_safety_audit_ui(
                audit_data=st.session_state["safety_audit_result"],
                is_live=st.session_state.get("safety_is_live", False),
                status_msg=st.session_state.get("safety_status_note", "")
            )

# -------------------------------------------------------------
# TAB 2: Crack Diagnostics & Structural Integrity
# -------------------------------------------------------------
with tab2:
    st.markdown("### 🔍 Concrete Crack Diagnostics & Structural Integrity")
    st.caption("Epic 2: Forensic defect classification, width estimation (mm), and engineering repair specs under IS 456 & ACI 224R")

    col_c1, col_c2 = st.columns([1, 1.2])

    with col_c1:
        st.markdown("#### 1. Upload or Select Defect Image")
        uploaded_crack_file = st.file_uploader(
            "Upload Concrete / Wall Surface Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader"
        )
        use_sample_crack = st.button("🧱 Load Sample Concrete Defect Photo (45° Shear Crack)")

        active_crack_bytes = None
        active_crack_mime = "image/png"

        if uploaded_crack_file is not None:
            active_crack_bytes = uploaded_crack_file.getvalue()
            active_crack_mime = uploaded_crack_file.type
            st.image(active_crack_bytes, caption="Uploaded Concrete Defect Specimen", use_container_width=True)
        elif use_sample_crack or "sample_crack_loaded" in st.session_state:
            st.session_state["sample_crack_loaded"] = True
            active_crack_bytes = generate_sample_crack_image()
            active_crack_mime = "image/png"
            st.image(active_crack_bytes, caption="Preset: 45° Diagonal Shear Crack + Spalling in RCC Column", use_container_width=True)
        else:
            st.info("👆 Upload a concrete defect image above or click **'Load Sample Concrete Defect Photo'**.")

    with col_c2:
        st.markdown("#### 2. Diagnostic Execution & Remediations")
        if active_crack_bytes:
            if st.button("⚡ Analyze Concrete Defect & Structural Integrity", type="primary", use_container_width=True):
                with st.spinner("Classifying crack kinematics, measuring estimated width, and formulating repair specifications..."):
                    diag_res, is_live_crack, status_crack_note = run_crack_diagnostics(
                        client=gemini_client,
                        image_bytes=active_crack_bytes,
                        mime_type=active_crack_mime
                    )
                    st.session_state["crack_diag_result"] = diag_res
                    st.session_state["crack_is_live"] = is_live_crack
                    st.session_state["crack_status_note"] = status_crack_note

        if "crack_diag_result" in st.session_state:
            render_crack_diagnostics_ui(
                diag_data=st.session_state["crack_diag_result"],
                is_live=st.session_state.get("crack_is_live", False),
                status_msg=st.session_state.get("crack_status_note", "")
            )

# -------------------------------------------------------------
# TAB 3: Planning & Real Estate Valuation
# -------------------------------------------------------------
with tab3:
    render_valuation_ui()

# -------------------------------------------------------------
# TAB 4: Daily Site Assistant & Weather-Aware Advisory
# -------------------------------------------------------------
with tab4:
    render_site_assistant_ui(client=gemini_client)
