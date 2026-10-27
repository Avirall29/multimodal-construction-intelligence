"""
Module: Crack Diagnostics & Structural Integrity (Epic 2)
Analyzes concrete/masonry defects, classifies crack types under IS 456:2000 and ACI 224R,
estimates crack widths, assesses root causes, and generates actionable structural repair specs.
"""
from typing import Dict, Any, Tuple
import json
import streamlit as st
from modules.gemini_client import GeminiClientWrapper

CRACK_DIAGNOSTICS_PROMPT = """
You are a Principal Forensic Structural Engineer specialized in concrete diagnostics,
failure analysis, and structural remediation under IS 456:2000, IS 13920, and ACI 224R-01.

Analyze the uploaded image of the concrete/wall surface. You MUST return ONLY valid JSON matching this exact schema:

{
  "defect_type": "<'Structural Shear' | 'Settlement' | 'Hairline' | 'Thermal Expansion' | 'Spalling & Delamination'>",
  "subtype_description": "<Specific technical subtype, e.g. 45° Diagonal Beam-Column Shear or Plastic Shrinkage Fissures>",
  "estimated_crack_width_mm": <number in mm, e.g. 2.4>,
  "crack_depth_assessment": "<'Surface Plaster (<5mm)' | 'Cover Concrete Depth (15-40mm)' | 'Full Depth Through-Section'>",
  "structural_severity": "<'Critical' | 'High' | 'Medium' | 'Low'>",
  "urgency_level": "<'Immediate (Within 24 Hours)' | 'High Priority (Within 7 Days)' | 'Medium Priority (Within 30 Days)' | 'Routine Monitoring Only'>",
  "is456_compliance_status": "<'Exceeds Permissible Limit (0.3mm)' | 'Compliant with IS 456 Section 35.3.2' | 'Critical Structural Impairment'>",
  "root_causes": [
    "<Primary root cause, e.g. Inadequate shear stirrups or differential foundation settlement>",
    "<Secondary contributing factor, e.g. Concrete shrinkage / thermal gradients>"
  ],
  "recommended_engineering_repairs": [
    {
      "step_number": 1,
      "method": "<e.g. Low-Viscosity Epoxy Resin Injection / CFRP Composite Wrap / Micro-Concrete Jacketing>",
      "specification": "<Engineering specification, e.g. Inject epoxy under 0.2-0.4 MPa through surface ports at 150mm c/c>",
      "materials_required": "<e.g. Sikadur 52 / Nitokit LV / Sikawrap CFRP>"
    },
    {
      "step_number": 2,
      "method": "<Subsequent step, e.g. Carbonation Passivation & Polymer Mortar Fairing>",
      "specification": "<Detailed spec>",
      "materials_required": "<e.g. Zinc-rich rebar primer + SikaTop 122>"
    }
  ],
  "structural_health_risk": "<1-paragraph technical assessment of ongoing load safety>",
  "monitoring_protocol": "<Tell-tale crack monitor installation interval and periodic gauge reading plan>"
}
"""

def get_demo_crack_data() -> Dict[str, Any]:
    """Returns high-fidelity demonstration diagnostic report for structural shear cracking."""
    return {
        "defect_type": "Structural Shear",
        "subtype_description": "45° Diagonal Diagonal Tension Shear Crack with Localized Concrete Spalling",
        "estimated_crack_width_mm": 2.8,
        "crack_depth_assessment": "Full Depth Through-Section (>50mm)",
        "structural_severity": "Critical",
        "urgency_level": "Immediate (Within 24 Hours)",
        "is456_compliance_status": "Critical Structural Impairment (Permissible max is 0.3mm per IS 456 Cl 35.3.2)",
        "root_causes": [
            "Inadequate shear reinforcement (transverse stirrup spacing exceeding d/2 under IS 456 Cl 26.5.1.6).",
            "Superimposed live load exceeding design shear capacity during upper floor slab casting.",
            "Moisture ingress triggering corrosion of internal stirrup steel and subsequent volumetric expansion."
        ],
        "recommended_engineering_repairs": [
            {
                "step_number": 1,
                "method": "Immediate Propping & Dead Load Shoring",
                "specification": "Erect telescopic heavy-duty steel props within a 1.5m radius to relieve diagonal shear tension immediately before repair.",
                "materials_required": "IS 2750 Heavy Duty Adjustable Steel Acrow Props (Rated 35 kN)"
            },
            {
                "step_number": 2,
                "method": "V-Groove Routing & Surface Port Installation",
                "specification": "Chisel a 15mm x 15mm V-groove along the entire crack profile. Clean with compressed air; install brass/plastic injection nipples at 200mm centers.",
                "materials_required": "Non-sag epoxy thixotropic adhesive (Sikadur-31 / Nitomortar FC)"
            },
            {
                "step_number": 3,
                "method": "High-Pressure Low-Viscosity Epoxy Injection",
                "specification": "Pump solvent-free low-viscosity epoxy resin from lowest port upward until clean resin exudes from adjacent ports under 0.35 MPa pressure.",
                "materials_required": "Low-viscosity structural epoxy resin (Sikadur-52 / Nitokit LV)"
            },
            {
                "step_number": 4,
                "method": "External CFRP Shear Strengthening Wrap",
                "specification": "Bond bi-directional Carbon Fiber Reinforced Polymer (CFRP) fabric jackets at 90° to beam axis to reinstate depleted shear capacity.",
                "materials_required": "SikaWrap-300C (300 g/m² woven carbon fiber) saturated with Sikadur-330 primer"
            }
        ],
        "structural_health_risk": "Crack width of 2.8 mm significantly exceeds the IS 456 permissible limit of 0.3 mm (moderate exposure) and exhibits active diagonal tension shear kinematics. Failure to stabilize could trigger sudden brittle shear failure under seismic or dead load peak.",
        "monitoring_protocol": "Install Avongard 2-axis calibrated acrylic tell-tale displacement gauges across crack terminus; log micrometric movements twice daily."
    }

def run_crack_diagnostics(
    client: GeminiClientWrapper,
    image_bytes: bytes,
    mime_type: str = "image/png"
) -> Tuple[Dict[str, Any], bool, str]:
    """Runs multimodal diagnostic analysis on the concrete/wall surface image."""
    demo_fallback = get_demo_crack_data()
    return client.generate_multimodal(
        prompt=CRACK_DIAGNOSTICS_PROMPT,
        image_bytes=image_bytes,
        mime_type=mime_type,
        fallback_json=demo_fallback
    )

def render_crack_diagnostics_ui(diag_data: Dict[str, Any], is_live: bool, status_msg: str):
    """Renders the complete visual interface for structural crack diagnostics."""
    if is_live:
        st.success("🟢 Live Forensic Structural Diagnostics completed via Google Gemini.")
    else:
        st.info("ℹ️ Running in Multimodal Demonstration Mode (IS 456:2000 & ACI 224R Structural Engine).")

    if status_msg and "Error" in status_msg:
        st.warning(status_msg)

    defect_type = diag_data.get("defect_type", "Structural Shear")
    subtype = diag_data.get("subtype_description", "")
    width_mm = diag_data.get("estimated_crack_width_mm", 2.5)
    severity = diag_data.get("structural_severity", "High")
    urgency = diag_data.get("urgency_level", "Immediate (Within 24 Hours)")
    compliance = diag_data.get("is456_compliance_status", "Exceeds Permissible Limit")

    # Severity Colors
    sev_colors = {
        "Critical": "#D32F2F",
        "High": "#E65100",
        "Medium": "#F57C00",
        "Low": "#2E7D32"
    }
    sev_color = sev_colors.get(severity, "#E65100")

    # Urgency Banner
    is_urgent = "Immediate" in urgency or severity in ["Critical", "High"]
    banner_bg = "rgba(211, 47, 47, 0.15)" if is_urgent else "rgba(46, 125, 50, 0.15)"
    banner_border = "#D32F2F" if is_urgent else "#2E7D32"

    st.markdown(
        f"""
        <div style="background: {banner_bg}; border: 1px solid {banner_border}; border-left: 6px solid {banner_border}; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 800; color: #FFFFFF; font-size: 16px;">🚨 ACTION DIRECTIVE: {urgency}</span>
                <span style="background: {sev_color}; color: #FFFFFF; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 4px;">{severity.upper()} SEVERITY</span>
            </div>
            <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px;">
                <b>IS 456 Cl 35.3.2 Status:</b> {compliance} | <b>Depth Category:</b> {diag_data.get('crack_depth_assessment', 'Full Depth')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metric Cards Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Defect Classification</div>
                <div style="font-size: 20px; font-weight: 800; color: #38BDF8; margin: 8px 0; min-height: 48px; display: flex; align-items: center; justify-content: center;">{defect_type}</div>
                <div style="font-size: 11px; color: #94A3B8;">ACI 224R-01 Class</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Crack Width (Est.)</div>
                <div style="font-size: 32px; font-weight: 800; color: {sev_color}; margin: 4px 0;">{width_mm} <span style="font-size: 16px; color: #94A3B8;">mm</span></div>
                <div style="font-size: 11px; color: #F57C00;">IS 456 Limit: 0.3mm</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Structural Severity</div>
                <div style="font-size: 24px; font-weight: 800; color: {sev_color}; margin: 6px 0;">{severity}</div>
                <div style="font-size: 11px; color: #94A3B8;">Forensic Risk Grade</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Repair Window</div>
                <div style="font-size: 17px; font-weight: 700; color: #FBBF24; margin: 8px 0; min-height: 48px; display: flex; align-items: center; justify-content: center;">{urgency}</div>
                <div style="font-size: 11px; color: #94A3B8;">Intervention Schedule</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if subtype:
        st.markdown(f"**Forensic Classification:** *{subtype}*")

    st.markdown("---")

    col_causes, col_repairs = st.columns([1, 1.3])

    with col_causes:
        st.subheader("🔍 Root Cause Analysis")
        causes = diag_data.get("root_causes", [])
        for idx, cause in enumerate(causes, 1):
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-left: 3px solid #38BDF8; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                    <span style="color: #38BDF8; font-weight: 700;">#{idx}</span> <span style="color: #F1F5F9; font-size: 13px;">{cause}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("#### 📐 Structural Health Risk Assessment")
        risk_text = diag_data.get("structural_health_risk", "")
        if risk_text:
            st.warning(risk_text)

        monitor = diag_data.get("monitoring_protocol", "")
        if monitor:
            st.info(f"**Monitoring Protocol:** {monitor}")

    with col_repairs:
        st.subheader("🛠️ Recommended Engineering Repairs")
        repairs = diag_data.get("recommended_engineering_repairs", [])
        for rep in repairs:
            step = rep.get("step_number", 1)
            method = rep.get("method", "Remediation Step")
            spec = rep.get("specification", "")
            mat = rep.get("materials_required", "")

            with st.expander(f"Step {step}: {method}", expanded=True):
                st.markdown(f"**Engineering Specification:**\n{spec}")
                st.markdown(f"**Approved Materials & Codes:** `{mat}`")

    # Downloadable Diagnostic Report
    st.markdown("---")
    d1, d2 = st.columns([3, 1])
    with d1:
        st.caption("Forensic crack diagnostic conforms to IS 456:2000 Section 35 & ACI 224R Control of Cracking in Concrete Structures.")
    with d2:
        report_json = json.dumps(diag_data, indent=2)
        st.download_button(
            label="📥 Download Diagnostic Report",
            data=report_json,
            file_name="structural_crack_diagnostic_report.json",
            mime="application/json",
            use_container_width=True
        )
