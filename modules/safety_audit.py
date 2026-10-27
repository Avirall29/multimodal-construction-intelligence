"""
Module: Site Safety & PPE Audit (Epic 2)
Analyzes worker PPE compliance and site hazards under OSHA 1926 and IS 456 standards.
Outputs structured JSON contracts and renders interactive metric cards, status pills, and tables.
"""
from typing import Dict, Any, Tuple
import json
import streamlit as st
from modules.gemini_client import GeminiClientWrapper

SAFETY_AUDIT_PROMPT = """
You are an expert Chief Construction Safety Officer certified in OSHA CFR 1926 regulations 
and Indian Standard IS 456 / IS 2925 / IS 15809 / IS 3521 compliance.

Analyze the uploaded construction site image thoroughly. You MUST return ONLY valid JSON matching this exact schema:

{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<'Compliant' | 'Minor Infractions' | 'Critical Violations' | 'Work Stop Required'>",
  "total_workers_detected": <integer>,
  "ppe_compliance_rate_pct": <integer from 0 to 100>,
  "executive_summary": "<Concise 2-sentence executive summary of site safety conditions>",
  "ppe_detection": [
    {
      "equipment": "Hard Hats / Safety Helmets",
      "required_standard": "OSHA 1926.100 / IS 2925:1984",
      "detected_compliant": <integer>,
      "detected_non_compliant": <integer>,
      "compliance_status": "<'Compliant' | 'Partial Violation' | 'Critical Non-Compliance'>",
      "observations": "<Observations on chin-straps, ANSI rating, or unhelmeted personnel>"
    },
    {
      "equipment": "High-Visibility Retro-reflective Vests",
      "required_standard": "OSHA 1926.201 / IS 15809:2017 Class 2/3",
      "detected_compliant": <integer>,
      "detected_non_compliant": <integer>,
      "compliance_status": "<'Compliant' | 'Partial Violation' | 'Critical Non-Compliance'>",
      "observations": "<Observations on vest visibility, fluorescent material>"
    },
    {
      "equipment": "Steel-Toe Puncture-Resistant Boots",
      "required_standard": "OSHA 1926.96 / IS 15298:2019",
      "detected_compliant": <integer>,
      "detected_non_compliant": <integer>,
      "compliance_status": "<'Compliant' | 'Partial Violation' | 'Critical Non-Compliance'>",
      "observations": "<Observations on footwear suitability>"
    },
    {
      "equipment": "Fall Arrest Harnesses & Lanyards",
      "required_standard": "OSHA 1926.502 / IS 3521:1999 (Work at Height >1.8m)",
      "detected_compliant": <integer>,
      "detected_non_compliant": <integer>,
      "compliance_status": "<'Compliant' | 'Partial Violation' | 'Critical Non-Compliance' | 'Not Applicable'>",
      "observations": "<Observations on 100% tie-off, anchorage points, double lanyards>"
    }
  ],
  "identified_site_hazards": [
    {
      "hazard_title": "<Name of hazard, e.g. Unguarded Floor Edge / Protruding Impalement Rebar>",
      "location_target": "<Area in image, e.g. Scaffold Bay 2, Edge Beam>",
      "severity": "<'Critical' | 'High' | 'Medium' | 'Low'>",
      "osha_is_reference": "<e.g. OSHA 1926.501(b)(1) / IS 456 Cl 35>",
      "risk_description": "<Brief description of danger>",
      "corrective_remedy": "<Mandatory engineering/administrative corrective action>"
    }
  ],
  "urgent_actions": [
    "<Action item 1>",
    "<Action item 2>"
  ]
}
"""

def get_demo_safety_data() -> Dict[str, Any]:
    """Returns high-fidelity demonstration audit data reflecting OSHA/IS 456 standards."""
    return {
        "safety_score": 58,
        "overall_status": "Critical Violations",
        "total_workers_detected": 4,
        "ppe_compliance_rate_pct": 52,
        "executive_summary": "Active site inspection detected severe fall protection violations at elevated scaffolding (elevation > 3.2m) and exposed un-capped rebar pins creating impalement hazards under OSHA 1926.701(b). Ground personnel exhibit partial PPE compliance.",
        "ppe_detection": [
            {
                "equipment": "Hard Hats / Safety Helmets",
                "required_standard": "OSHA 1926.100 / IS 2925:1984 (Type 1 Class E)",
                "detected_compliant": 3,
                "detected_non_compliant": 1,
                "compliance_status": "Partial Violation",
                "observations": "One elevated worker working directly below hoist line observed without protective hard hat."
            },
            {
                "equipment": "High-Visibility Retro-reflective Vests",
                "required_standard": "OSHA 1926.201 / IS 15809:2017 Class 2",
                "detected_compliant": 2,
                "detected_non_compliant": 2,
                "compliance_status": "Partial Violation",
                "observations": "Two workers wearing plain dark cotton clothing with zero retro-reflective trim near heavy vehicular zone."
            },
            {
                "equipment": "Steel-Toe Puncture-Resistant Boots",
                "required_standard": "OSHA 1926.96 / IS 15298:2019",
                "detected_compliant": 3,
                "detected_non_compliant": 1,
                "compliance_status": "Compliant",
                "observations": "Steel-toe footwear observed on ground crew; elevated personnel footwear requires physical verification."
            },
            {
                "equipment": "Fall Arrest Harnesses & Lanyards",
                "required_standard": "OSHA 1926.502 / IS 3521:1999 (Work at Height >1.8m)",
                "detected_compliant": 0,
                "detected_non_compliant": 1,
                "compliance_status": "Critical Non-Compliance",
                "observations": "CRITICAL: Scaffolding worker positioned at 3.5m height without full-body harness, shock-absorbing lanyard, or lifeline anchorage."
            }
        ],
        "identified_site_hazards": [
            {
                "hazard_title": "Fall from Height Hazard without Fall Arrest",
                "location_target": "Scaffold Tier 2 (East Elevation)",
                "severity": "Critical",
                "osha_is_reference": "OSHA 1926.501(b)(1) / IS 3521",
                "risk_description": "Worker exposed to 3.5m free-fall potential without personal fall arrest system (PFAS) or toe-boards.",
                "corrective_remedy": "Issue immediate Stop-Work Order on Bay 2; equip worker with dual-lanyard harness anchored to certified 22.2 kN anchor point."
            },
            {
                "hazard_title": "Exposed Protruding Rebar (Impalement Risk)",
                "location_target": "Slab Foundation Perimeter Grid B4",
                "severity": "High",
                "osha_is_reference": "OSHA 1926.701(b) / IS 456 Cl 35.1",
                "risk_description": "Un-capped starter reinforcement rebar dowels protruding 600mm vertically within worker travel pathway.",
                "corrective_remedy": "Install OSHA-compliant steel-reinforced mushroom impalement caps or wooden trough protection over rebar ends."
            },
            {
                "hazard_title": "Scaffolding Missing Mid-Rails & Toe-Boards",
                "location_target": "Main Access Tubular Scaffold",
                "severity": "High",
                "osha_is_reference": "OSHA 1926.451(g)(1) / IS 4014 (Part 2)",
                "risk_description": "Missing guardrails allow tool drop hazards onto ground personnel and slip-and-fall hazards.",
                "corrective_remedy": "Install standard top rails at 42 inches, mid-rails at 21 inches, and 4-inch toe-boards across all working platforms."
            },
            {
                "hazard_title": "Housekeeping & Trip Hazards",
                "location_target": "Ground Level Material Staging Pathway",
                "severity": "Medium",
                "osha_is_reference": "OSHA 1926.25(a) / NBC 2016 Part 7",
                "risk_description": "Loose binding wire coils and timber formwork cutoffs obstructing designated safe walkways.",
                "corrective_remedy": "Perform end-of-shift 5S housekeeping; clear walkways and segregate rebar scraps into disposal skip."
            }
        ],
        "urgent_actions": [
            "1. Immediately halt all work on Scaffolding Tier 2 until full-body harness tie-off is secured.",
            "2. Cap all exposed vertical rebar along Grid B4 with certified orange impalement caps.",
            "3. Issue fluorescent Class 2 safety vests to workers in material unloading zones before resuming shifts."
        ]
    }

def run_safety_audit(
    client: GeminiClientWrapper,
    image_bytes: bytes,
    mime_type: str = "image/png"
) -> Tuple[Dict[str, Any], bool, str]:
    """Runs multimodal audit on the image or provides demo fallback."""
    demo_fallback = get_demo_safety_data()
    return client.generate_multimodal(
        prompt=SAFETY_AUDIT_PROMPT,
        image_bytes=image_bytes,
        mime_type=mime_type,
        fallback_json=demo_fallback
    )

def render_safety_audit_ui(audit_data: Dict[str, Any], is_live: bool, status_msg: str):
    """Renders the complete visual interface for the safety audit."""
    if is_live:
        st.success("🟢 Live Multimodal Safety Audit completed via Google Gemini.")
    else:
        st.info("ℹ️ Running in Multimodal Demonstration Mode (Standard OSHA 1926 & IS 456 Model).")
    
    if status_msg and "Error" in status_msg:
        st.warning(status_msg)

    score = audit_data.get("safety_score", 70)
    overall_status = audit_data.get("overall_status", "Minor Infractions")
    workers_count = audit_data.get("total_workers_detected", 0)
    compliance_rate = audit_data.get("ppe_compliance_rate_pct", 75)

    # Status Pill Color Logic
    status_colors = {
        "Compliant": "#2E7D32",
        "Minor Infractions": "#F57C00",
        "Critical Violations": "#D32F2F",
        "Work Stop Required": "#7F0000"
    }
    pill_color = status_colors.get(overall_status, "#0D47A1")

    # Score Color
    score_color = "#2E7D32" if score >= 85 else ("#F57C00" if score >= 60 else "#D32F2F")

    # Metric Cards Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 13px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Safety Score</div>
                <div style="font-size: 38px; font-weight: 800; color: {score_color}; margin: 4px 0;">{score}<span style="font-size: 18px; color: #94A3B8;">/100</span></div>
                <div style="font-size: 11px; color: #94A3B8;">IS 456 & OSHA Index</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 13px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Overall Status</div>
                <div style="display: inline-block; background: {pill_color}; color: #FFFFFF; font-weight: 700; font-size: 15px; padding: 6px 14px; border-radius: 20px; margin: 10px 0;">
                    {overall_status}
                </div>
                <div style="font-size: 11px; color: #94A3B8;">Action Threshold Status</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 13px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Workers Identified</div>
                <div style="font-size: 38px; font-weight: 800; color: #38BDF8; margin: 4px 0;">{workers_count}</div>
                <div style="font-size: 11px; color: #94A3B8;">Active in frame</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 13px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">PPE Compliance Rate</div>
                <div style="font-size: 38px; font-weight: 800; color: {score_color}; margin: 4px 0;">{compliance_rate}%</div>
                <div style="font-size: 11px; color: #94A3B8;">Mandatory 4-gear audit</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Executive Summary
    summary = audit_data.get("executive_summary", "")
    if summary:
        st.markdown(f"**Site Officer Brief:** {summary}")

    st.markdown("---")

    # PPE Detection Checklist & Identified Site Hazards
    col_left, col_right = st.columns([1.1, 1.3])

    with col_left:
        st.subheader("🛡️ PPE Compliance Matrix")
        ppe_items = audit_data.get("ppe_detection", [])
        for ppe in ppe_items:
            eq = ppe.get("equipment", "Safety Gear")
            std = ppe.get("required_standard", "")
            stat = ppe.get("compliance_status", "Compliant")
            obs = ppe.get("observations", "")
            comp_cnt = ppe.get("detected_compliant", 0)
            non_cnt = ppe.get("detected_non_compliant", 0)

            badge_color = "#2E7D32" if "Compliant" in stat and "Non" not in stat and "Partial" not in stat else ("#F57C00" if "Partial" in stat else "#D32F2F")
            icon = "✅" if "Compliant" in stat and "Non" not in stat and "Partial" not in stat else ("⚠️" if "Partial" in stat else "❌")

            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-left: 4px solid {badge_color}; border-radius: 6px; padding: 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #F1F5F9; font-size: 14px;">{icon} {eq}</span>
                        <span style="background: {badge_color}; color: #FFFFFF; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 12px;">{stat}</span>
                    </div>
                    <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Standard: <code>{std}</code></div>
                    <div style="font-size: 12px; color: #E2E8F0; margin-top: 6px;">{obs}</div>
                    <div style="font-size: 11px; color: #38BDF8; margin-top: 4px;">Compliant: <b>{comp_cnt}</b> | Non-compliant: <b>{non_cnt}</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_right:
        st.subheader("⚠️ Identified Site Hazards & Remedies")
        hazards = audit_data.get("identified_site_hazards", [])
        sev_colors = {
            "Critical": "#D32F2F",
            "High": "#E65100",
            "Medium": "#F57C00",
            "Low": "#2E7D32"
        }

        for idx, h in enumerate(hazards, 1):
            htitle = h.get("hazard_title", f"Hazard #{idx}")
            loc = h.get("location_target", "Site general")
            sev = h.get("severity", "Medium")
            ref = h.get("osha_is_reference", "")
            risk = h.get("risk_description", "")
            remedy = h.get("corrective_remedy", "")
            col = sev_colors.get(sev, "#E65100")

            with st.expander(f"{sev.upper()}: {htitle} ({loc})", expanded=(sev in ["Critical", "High"])):
                st.markdown(f"**Severity Rating:** <span style='background: {col}; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 600;'>{sev}</span>", unsafe_allow_html=True)
                st.markdown(f"**Regulatory Clause:** `{ref}`")
                st.markdown(f"**Risk Profile:** {risk}")
                st.markdown(f"**Mandatory Corrective Remedy:**")
                st.info(remedy)

    # Downloadable JSON Report
    st.markdown("---")
    d_col1, d_col2 = st.columns([3, 1])
    with d_col1:
        st.caption("Standardized JSON audit record adheres to OSHA Inspection Standard 1926 & IS 456 Section 35 Safety Protocols.")
    with d_col2:
        json_str = json.dumps(audit_data, indent=2)
        st.download_button(
            label="📥 Download JSON Audit Report",
            data=json_str,
            file_name="site_safety_ppe_audit_report.json",
            mime="application/json",
            use_container_width=True
        )
