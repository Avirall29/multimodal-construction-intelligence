"""
Module: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Provides real-time dynamic weather safety alerts and an interactive multi-turn
construction engineering chatbot grounded in IS codes and OSHA standards.
"""
from typing import Dict, Any, List
import streamlit as st
from modules.gemini_client import GeminiClientWrapper

WEATHER_PROTOCOLS = {
    "High Wind (>45 km/h)": {
        "severity": "CRITICAL",
        "badge_color": "#D32F2F",
        "crane_status": "⛔ IMMEDIATELY SUSPEND ALL TOWER CRANE & HOIST OPERATIONS",
        "crane_protocol": "Under OSHA 1926.1431 and IS 456 scaffolding rules, all tower crane lifting, crawler cranes, and external passenger hoists must be weathervaned and secured when wind gusts exceed 38-45 km/h. Lower hook blocks to ground level and engage slew brakes in weathervane mode.",
        "scaffold_protocol": "Inspect all perimeter safety netting, tarpaulins, and temporary signages; remove or lash down loose timber sheets. High-rise perimeter facade work must cease.",
        "electrical_protocol": "De-energize temporary overhead powerlines susceptible to sway and conductor clashing.",
        "concreting_protocol": "Accelerated wind speeds increase plastic shrinkage cracking rate threefold. Apply chemical evaporation retarders immediately after screeding."
    },
    "Heavy Rain / Monsoon (>30 mm/h)": {
        "severity": "CRITICAL",
        "badge_color": "#D32F2F",
        "crane_status": "⚠️ RESTRICT CRANE LIFTS; MONITOR GROUND BEARING CAPACITY",
        "crane_protocol": "Check crane outrigger pads and crawler tracks for soil softening or subgrade wash-away. Ensure pad bearing pressures do not exceed safe soil capacity.",
        "scaffold_protocol": "Ensure sole plates beneath scaffold baseplates have not settled or washed out. Prohibit work on wet, slippery steel scaffold planks.",
        "electrical_protocol": "ELECTRICAL HAZARD MITIGATION: Mandatory daily test of all 30mA Ground Fault Circuit Interrupters (GFCI/ELCB). Elevate temporary distribution boards onto plastic pallets above flood grade. Inspect submersible pump cable seals.",
        "concreting_protocol": "HALT all exposed slab casting. If rain starts during pouring, immediately cover fresh concrete with polyethylene sheets and form cold construction joints per IS 456 Cl 13.4."
    },
    "Extreme Heat (>40°C / High UV)": {
        "severity": "HIGH",
        "badge_color": "#F57C00",
        "crane_status": "🟢 CRANES OPERATIONAL (MONITOR HYDRAULIC OIL TEMPERATURE)",
        "crane_protocol": "Monitor crane hydraulic fluid reservoirs for overheating. Cabin air conditioning must be functional for operator alertness.",
        "scaffold_protocol": "Bare metal scaffolding pipes can reach surface temperatures >65°C. Workers must wear heat-resistant leather gloves.",
        "electrical_protocol": "Derate temporary power cables by 15-20% to account for high ambient conductor temperatures.",
        "concreting_protocol": "IS 7861 (Part 1) HOT WEATHER CONCRETING PROTOCOL: Concrete delivery temperature must not exceed 30°C at placement. Use crushed ice in batching water, schedule major slab pours between 8 PM and 6 AM, apply wet hessian gunny bags continuously for minimum 14 days, and maintain ponding on slabs."
    },
    "Normal / Clear Sky (25°C - 32°C)": {
        "severity": "NORMAL",
        "badge_color": "#2E7D32",
        "crane_status": "🟢 FULL CRANE & HOIST OPERATIONS PERMITTED",
        "crane_protocol": "Standard pre-lift rigging inspection, load chart verification, and radio comms testing between rigger and operator.",
        "scaffold_protocol": "Standard 7-day statutory scaffolding inspection by Competent Scaffolding Inspector (Scafftag update).",
        "electrical_protocol": "Standard lock-out tag-out (LOTO) protocols and earth pit resistance checks (<5 ohms).",
        "concreting_protocol": "Standard IS 456 curing: Minimum 7 days continuous wet curing for OPC, 10 days for mineral admixtures (fly ash / slag / PPC)."
    },
    "Cold Wave / Dense Fog (<10°C / Fog)": {
        "severity": "MEDIUM",
        "badge_color": "#0284C7",
        "crane_status": "⚠️ LOW VISIBILITY RESTRICTIONS",
        "crane_protocol": "Suspend blind lifts if crane operator cannot clearly see banksman signals and hook position. Use aviation warning strobe lights on jibs.",
        "scaffold_protocol": "Dew and frost accumulation on walkway planks create slipping hazards. Spread dry sand or clean before morning shift.",
        "electrical_protocol": "Condensation inside outdoor junction boxes. Check enclosure IP65 seals and verify silica gel desiccants.",
        "concreting_protocol": "IS 7861 (Part 2) COLD WEATHER CONCRETING: Hydration retardation occurs below 10°C. Protect fresh concrete with insulating thermal blankets; do not strip formwork until cube test confirms 70% characteristic strength."
    }
}

SYSTEM_CHAT_INSTRUCTION = """
You are an expert Chief Resident Engineer and Project Director with 25+ years experience 
managing multi-million dollar high-rise, infrastructure, and industrial construction projects.
You are fluent in Indian Standards (IS 456:2000, IS 800:2007, IS 1893:2016, IS 13920:2016, IS 7861, SP 34),
National Building Code of India (NBC 2016), OSHA 1926, and CPWD specifications.

Answer user questions with technical rigor, citing specific clauses, concrete mix ratios, curing intervals,
reinforcement detailing rules, safety limits, and practical site execution protocols.
Keep explanations concise, well-structured with bullet points, and actionable for site engineers.
"""

EXPERT_KNOWLEDGE_BASE = {
    "cover": """**Nominal Concrete Cover Requirements (IS 456:2000 Table 16 & Cl 26.4):**
- **Footings / Rafts in contact with earth:** 50 mm (min.)
- **Columns (Main Longitudinal Reinforcement):** 40 mm (or diameter of main bar, whichever is greater. Can be reduced to 25 mm for columns ≤200 mm with bars ≤12 mm).
- **Beams:** 25 mm (or bar diameter).
- **Slabs / Plates:** 20 mm (or bar diameter, can be 15 mm for mild exposure).
- **Severe / Extreme Coastal Exposure (Marine Environment):** Add 15-20 mm extra sacrificial cover or use M40+ grade concrete with max w/c ratio 0.40.""",

    "crane": """**Tower Crane Wind Speed Limits & Safety Rules (OSHA 1926.1431 & IS 456):**
- **Operating Limit:** Most tower crane manufacturers (Liebherr, Potain) set the maximum operating wind limit at **38 to 45 km/h (20-24 knots)**.
- **Immediate Work Stop:** If wind gusts touch 45 km/h, all lifting operations must be suspended immediately.
- **Weathervaning Protocol:** Release slewing brake so the jib can freely rotate (weathervane) with the wind, reducing torsional stresses on the mast.
- **Hook Position:** Hoist block must be drawn up near the trolley and parked near the crane mast.""",

    "heat": """**Hot Weather Concreting Protocols (IS 7861 Part 1 & ACI 305R):**
1. **Concrete Placement Temperature:** Must not exceed 30°C (ideally <28°C). Use chilled water and partial flaked ice replacement during batching.
2. **Night Concreting:** Schedule heavy raft and slab pours between 8 PM and 6 AM to avoid solar radiation and peak ambient temperatures.
3. **Plastic Shrinkage Mitigation:** Erect temporary windbreaks, spray aliphatic alcohol evaporation retarders immediately after floating, and cover with moist hessian sheets within 30 minutes of initial set.
4. **Curing:** Continuous ponding / moist hessian wrapping for at least **14 days** (mandatory for blended PPC or fly ash mixes).""",

    "slump": """**Recommended Slump Values for Pumpable M30/M40 Concrete (IS 456 Cl 7.1 & IS 1199):**
- **Pumped Concrete (General Beams & Slabs):** 100 mm to 130 mm using polycarboxylate ether (PCE) superplasticizers.
- **Tremie Piles / Diaphragm Walls:** 150 mm to 180 mm (high flowability without segregation).
- **Heavily Reinforced Columns & Shear Walls:** 120 mm to 150 mm to ensure complete compaction without honeycombing around dense rebar cages."""
}

def get_engineering_fallback(user_query: str) -> str:
    """Provides high-quality domain responses when in offline demonstration mode."""
    q = user_query.lower()
    if "cover" in q or "is 456" in q and "coastal" in q:
        return EXPERT_KNOWLEDGE_BASE["cover"]
    elif "crane" in q or "wind" in q:
        return EXPERT_KNOWLEDGE_BASE["crane"]
    elif "heat" in q or "cure" in q or "curing" in q or "temperature" in q:
        return EXPERT_KNOWLEDGE_BASE["heat"]
    elif "slump" in q or "pump" in q or "mix" in q:
        return EXPERT_KNOWLEDGE_BASE["slump"]
    else:
        return (
            f"**Site Engineer Advisory Response:**\n\n"
            f"Regarding your query on *'{user_query}'*:\n\n"
            f"- **Statutory Standards:** Refer to **IS 456:2000 (Plain and Reinforced Concrete - Code of Practice)**, "
            f"**IS 1893:2016 (Criteria for Earthquake Resistant Design of Structures)**, and **OSHA 29 CFR 1926**.\n"
            f"- **Field Execution Rule:** Always ensure slump testing (IS 1199) and 150mm concrete cube compressive strength test sampling (IS 516) "
            f"at a frequency of 1 sample per 1-5 m³ for critical structural columns.\n"
            f"- **Quality Assurance:** Verify rebar spacing, clear cover blocks (minimum M40 grade mortar blocks, no PVC cover in fire-rated elements), "
            f"and strict 100% tie-off for scaffolding above 1.8m."
        )

def render_site_assistant_ui(client: GeminiClientWrapper):
    """Renders the weather-aware daily advisory and interactive multi-turn engineering chat."""
    st.markdown("### 🌦️ Weather-Aware Advisory & Daily Site Assistant")
    st.caption("Epic 5: Dynamic Microclimate Safety Protocols & Real-time Civil Engineering AI Chatbot")

    # Weather Condition Selector
    col_w1, col_w2 = st.columns([1.2, 2])
    with col_w1:
        selected_weather = st.selectbox(
            "Current Microclimate / Site Weather Condition",
            list(WEATHER_PROTOCOLS.keys()),
            index=0
        )
    
    w_info = WEATHER_PROTOCOLS[selected_weather]

    with col_w2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-left: 6px solid {w_info['badge_color']}; border-radius: 8px; padding: 12px 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 800; color: #FFFFFF; font-size: 15px;">CRANE & LIFTING DIRECTIVE</span>
                    <span style="background: {w_info['badge_color']}; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 11px;">{w_info['severity']}</span>
                </div>
                <div style="font-size: 13px; font-weight: 700; color: #F1F5F9; margin-top: 4px;">{w_info['crane_status']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Detailed Weather Protocols Accordion
    with st.expander(f"📋 View Full Emergency Protocols for {selected_weather}", expanded=True):
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(f"**🏗️ Heavy Lifting & Cranes:**\n{w_info['crane_protocol']}")
            st.markdown(f"**⚡ Electrical & Water Mitigation:**\n{w_info['electrical_protocol']}")
        with p2:
            st.markdown(f"**🪜 Scaffolding & Edge Protection:**\n{w_info['scaffold_protocol']}")
            st.markdown(f"**🧊 Concreting & Curing Protocol:**\n{w_info['concreting_protocol']}")

    st.markdown("---")

    # Interactive Multi-turn Chatbot
    st.subheader("💬 Resident Engineering Chatbot")
    st.caption("Interactive AI assistant grounded in IS 456, IS 800, IS 1893, OSHA 1926, and CPWD specifications.")

    # Initialize chat history in session_state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello Engineer! I am your Multimodal Construction Intelligence Assistant. How can I assist you with site safety, IS 456 concrete standards, crack remediation, or CapEx planning today?"
            }
        ]

    # Quick prompt chips
    st.markdown("**Suggested Quick Prompts:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_input = None
    with qc1:
        if st.button("🌊 IS 456 Coastal Cover", use_container_width=True):
            quick_input = "Explain IS 456 cover requirements for coastal exposure and marine environments"
    with qc2:
        if st.button("🏗️ Crane Wind Limits", use_container_width=True):
            quick_input = "What are the safe wind speed limits for tower crane operations under OSHA?"
    with qc3:
        if st.button("☀️ 42°C Concrete Curing", use_container_width=True):
            quick_input = "How should we cure slab concrete in 42°C extreme summer heat under IS 7861?"
    with qc4:
        if st.button("💧 M30 Pumpable Slump", use_container_width=True):
            quick_input = "What is the recommended slump and admixture for pumpable M30 concrete?"

    # Display chat messages
    for msg in st.session_state.chat_history:
        role = msg["role"]
        with st.chat_message(role):
            st.markdown(msg["content"])

    # Chat input or quick prompt trigger
    user_prompt = st.chat_input("Ask any civil engineering, safety, or valuation question...")
    effective_prompt = quick_input or user_prompt

    if effective_prompt:
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": effective_prompt})
        with st.chat_message("user"):
            st.markdown(effective_prompt)

        # Generate response
        fallback_reply = get_engineering_fallback(effective_prompt)
        context_instruction = (
            f"{SYSTEM_CHAT_INSTRUCTION}\n"
            f"Current Site Weather Condition: {selected_weather}\n"
            f"Active Alert: {w_info['crane_status']}"
        )

        with st.chat_message("assistant"):
            with st.spinner("Analyzing standards and formulating engineering response..."):
                reply_text, is_live = client.generate_chat_response(
                    messages=st.session_state.chat_history,
                    system_instruction=context_instruction,
                    fallback_reply=fallback_reply
                )
                st.markdown(reply_text)
                if is_live:
                    st.caption("⚡ Response generated via live Google Gemini API.")
                else:
                    st.caption("ℹ️ Response delivered via built-in Civil Engineering Expert Knowledge Base.")

        # Save assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": reply_text})

    # Clear Chat History Button
    if len(st.session_state.chat_history) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Reset Chat Conversation"):
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "Chat reset. How can I assist you with your construction site operations?"
                }
            ]
            st.rerun()
