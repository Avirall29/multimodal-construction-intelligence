"""
Module: Planning & Real Estate Valuation (Epic 3)
Calculates project budgets, CapEx incurred, market asset valuation in INR (Lakhs/Crores),
quantifies steel/cement/aggregate requirements, and integrates Pollinations AI 3D rendering.
"""
from typing import Dict, Any, Tuple
import urllib.parse
import streamlit as st
import plotly.graph_objects as go

# Cost benchmarks per sq ft in INR (Baseline Tier 1)
STRUCTURE_BENCHMARKS = {
    "Residential High-Rise (RCC G+20)": {
        "base_cost_sqft": 2800,
        "market_rate_sqft": 7500,
        "steel_kg_sqft": 4.5,
        "cement_bags_sqft": 0.42,
        "rmc_cum_sqft": 0.038,
        "sand_cft_sqft": 1.9,
        "aggregate_cft_sqft": 2.2
    },
    "Commercial Office Complex (Grade A)": {
        "base_cost_sqft": 3600,
        "market_rate_sqft": 11500,
        "steel_kg_sqft": 5.2,
        "cement_bags_sqft": 0.46,
        "rmc_cum_sqft": 0.042,
        "sand_cft_sqft": 2.0,
        "aggregate_cft_sqft": 2.4
    },
    "Industrial Warehouse (Steel PEB)": {
        "base_cost_sqft": 1850,
        "market_rate_sqft": 4200,
        "steel_kg_sqft": 6.8,
        "cement_bags_sqft": 0.28,
        "rmc_cum_sqft": 0.024,
        "sand_cft_sqft": 1.4,
        "aggregate_cft_sqft": 1.8
    },
    "Luxury Villa / Plotted Development": {
        "base_cost_sqft": 3900,
        "market_rate_sqft": 13000,
        "steel_kg_sqft": 4.2,
        "cement_bags_sqft": 0.45,
        "rmc_cum_sqft": 0.036,
        "sand_cft_sqft": 2.1,
        "aggregate_cft_sqft": 2.5
    },
    "Affordable Housing (G+4 Mivan/Precast)": {
        "base_cost_sqft": 1950,
        "market_rate_sqft": 4800,
        "steel_kg_sqft": 3.6,
        "cement_bags_sqft": 0.38,
        "rmc_cum_sqft": 0.032,
        "sand_cft_sqft": 1.7,
        "aggregate_cft_sqft": 2.0
    }
}

TIER_MULTIPLIERS = {
    "Tier 1 (Mumbai, Bengaluru, Delhi-NCR, Hyderabad, Chennai, Pune)": {
        "cost_mult": 1.0,
        "valuation_mult": 1.0,
        "cities": "Mumbai, Bengaluru, Delhi-NCR, Hyderabad, Pune, Chennai"
    },
    "Tier 2 (Ahmedabad, Jaipur, Chandigarh, Kochi, Indore, Lucknow)": {
        "cost_mult": 0.82,
        "valuation_mult": 0.65,
        "cities": "Ahmedabad, Jaipur, Chandigarh, Kochi, Indore, Lucknow"
    },
    "Tier 3 (Regional Industrial Hubs & Developing Towns)": {
        "cost_mult": 0.68,
        "valuation_mult": 0.42,
        "cities": "Regional District Hubs"
    }
}

GRADE_MULTIPLIERS = {
    "Standard Grade (IS Standard Compliance)": 1.0,
    "Premium Grade (Imported Fittings & High Performance Glass)": 1.22,
    "Ultra-Luxury / LEED Platinum Grade": 1.48
}

def format_inr(amount: float) -> str:
    """Formats numeric INR into Crores or Lakhs with Indian currency symbol."""
    if amount >= 10_000_000:
        cr = amount / 10_000_000
        return f"₹ {cr:,.2f} Cr"
    elif amount >= 100_000:
        lakh = amount / 100_000
        return f"₹ {lakh:,.2f} Lakhs"
    else:
        return f"₹ {amount:,.0f}"

def calculate_project_metrics(
    structure_type: str,
    built_up_sqft: float,
    location_tier: str,
    grade: str,
    completion_pct: float
) -> Dict[str, Any]:
    """Calculates all budget, CapEx, valuation, and material requirement figures."""
    base_data = STRUCTURE_BENCHMARKS.get(structure_type, STRUCTURE_BENCHMARKS["Residential High-Rise (RCC G+20)"])
    tier_info = TIER_MULTIPLIERS.get(location_tier, TIER_MULTIPLIERS["Tier 1 (Mumbai, Bengaluru, Delhi-NCR, Hyderabad, Chennai, Pune)"])
    grade_mult = GRADE_MULTIPLIERS.get(grade, 1.0)

    # Unit construction cost per sqft
    unit_cost_sqft = base_data["base_cost_sqft"] * tier_info["cost_mult"] * grade_mult
    total_budget = unit_cost_sqft * built_up_sqft

    # Capital expenditure incurred to date
    capex_incurred = total_budget * (completion_pct / 100.0)
    remaining_outflow = total_budget - capex_incurred

    # Market asset valuation
    # Completed market value at 100%
    full_market_value = base_data["market_rate_sqft"] * tier_info["valuation_mult"] * grade_mult * built_up_sqft
    # Current WIP Valuation: CapEx incurred + partial embedded land appreciation
    # Work-in-progress valuation discounts future risk while recognizing invested capital
    progress_ratio = completion_pct / 100.0
    wip_valuation = capex_incurred + (full_market_value - total_budget) * (progress_ratio ** 1.3)
    if wip_valuation < capex_incurred:
        wip_valuation = capex_incurred

    # Material calculations
    steel_mt = (built_up_sqft * base_data["steel_kg_sqft"]) / 1000.0
    steel_cost = steel_mt * 65_000  # ₹65,000 per MT average Fe550D
    cement_bags = built_up_sqft * base_data["cement_bags_sqft"]
    cement_mt = (cement_bags * 50) / 1000.0
    cement_cost = cement_bags * 380  # ₹380 per 50kg bag
    rmc_volume_cum = built_up_sqft * base_data["rmc_cum_sqft"]
    sand_cft = built_up_sqft * base_data["sand_cft_sqft"]
    agg_cft = built_up_sqft * base_data["aggregate_cft_sqft"]

    # Budget Cost Breakdown
    breakdown = {
        "Civil & Structural Works (42%)": total_budget * 0.42,
        "Finishing & Architectural (26%)": total_budget * 0.26,
        "MEP, HVAC & Fire Safety (18%)": total_budget * 0.18,
        "Regulatory Approvals & Fees (8%)": total_budget * 0.08,
        "Contingency Reserve (6%)": total_budget * 0.06
    }

    return {
        "unit_cost_sqft": unit_cost_sqft,
        "total_budget": total_budget,
        "capex_incurred": capex_incurred,
        "remaining_outflow": remaining_outflow,
        "wip_valuation": wip_valuation,
        "full_market_value": full_market_value,
        "completion_pct": completion_pct,
        "steel_mt": steel_mt,
        "steel_cost": steel_cost,
        "cement_bags": cement_bags,
        "cement_mt": cement_mt,
        "cement_cost": cement_cost,
        "rmc_volume_cum": rmc_volume_cum,
        "sand_cft": sand_cft,
        "agg_cft": agg_cft,
        "cost_breakdown": breakdown
    }

def generate_pollinations_prompt(
    structure_type: str,
    arch_style: str,
    elevation_view: str,
    lighting_time: str
) -> Tuple[str, str]:
    """Builds an architectural rendering prompt and corresponding Pollinations AI URL."""
    base_subject = structure_type.split("(")[0].strip()
    clean_prompt = (
        f"Award-winning 8k architectural photograph of a modern {base_subject}, "
        f"style of {arch_style}, {elevation_view}, dramatic {lighting_time}, "
        f"photorealistic construction textures, reinforced concrete slabs, floor-to-ceiling curtain wall glass, "
        f"landscaped urban terrace, ultra-detailed architectural rendering, octane render, architectural digest feature"
    )
    encoded = urllib.parse.quote(clean_prompt)
    pollinations_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&model=flux&nologo=true&seed=42"
    return clean_prompt, pollinations_url

def render_valuation_ui():
    """Renders the complete interactive Planning & Real Estate Valuation module."""
    st.markdown("### 🏢 Project Planning, CapEx & Real Estate Valuation")
    st.caption("Epic 3: Decision-Support for Capital Allocation, Material Forecasting & Indian Real Estate Valuation")

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        structure_type = st.selectbox(
            "Structure Archetype",
            list(STRUCTURE_BENCHMARKS.keys()),
            index=0
        )
        built_up_sqft = st.number_input(
            "Total Built-up Area (Sq. Ft.)",
            min_value=1_000,
            max_value=2_000_000,
            value=85_000,
            step=5_000
        )
        grade = st.selectbox(
            "Specification Grade",
            list(GRADE_MULTIPLIERS.keys()),
            index=0
        )

    with col_in2:
        location_tier = st.selectbox(
            "Location Tier (Indian Real Estate)",
            list(TIER_MULTIPLIERS.keys()),
            index=0
        )
        completion_pct = st.slider(
            "Physical Completion Milestone (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=5
        )
        # Determine milestone phase name
        if completion_pct <= 20:
            milestone_phase = "Substructure & Deep Foundation"
        elif completion_pct <= 55:
            milestone_phase = "RCC Superstructure & Core Framing"
        elif completion_pct <= 75:
            milestone_phase = "Brickwork, Masonry & MEP Conduiting"
        elif completion_pct <= 90:
            milestone_phase = "Internal Finishing & Glass Glazing"
        else:
            milestone_phase = "Snagging, Testing & Handover Commissioning"
        st.markdown(f"**Current Milestone:** `{milestone_phase}`")

    # Perform calculations
    metrics = calculate_project_metrics(
        structure_type=structure_type,
        built_up_sqft=built_up_sqft,
        location_tier=location_tier,
        grade=grade,
        completion_pct=completion_pct
    )

    st.markdown("---")

    # Financial Metric Cards
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Total Project Budget</div>
                <div style="font-size: 26px; font-weight: 800; color: #38BDF8; margin: 4px 0;">{format_inr(metrics['total_budget'])}</div>
                <div style="font-size: 11px; color: #94A3B8;">₹ {metrics['unit_cost_sqft']:,.0f} / sq.ft</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with f2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">CapEx Incurred to Date</div>
                <div style="font-size: 26px; font-weight: 800; color: #F59E0B; margin: 4px 0;">{format_inr(metrics['capex_incurred'])}</div>
                <div style="font-size: 11px; color: #94A3B8;">{completion_pct}% of budget utilized</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with f3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Current Asset Valuation</div>
                <div style="font-size: 26px; font-weight: 800; color: #10B981; margin: 4px 0;">{format_inr(metrics['wip_valuation'])}</div>
                <div style="font-size: 11px; color: #10B981;">WIP Indian Market Value</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with f4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 12px; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Remaining Outflow</div>
                <div style="font-size: 26px; font-weight: 800; color: #EC4899; margin: 4px 0;">{format_inr(metrics['remaining_outflow'])}</div>
                <div style="font-size: 11px; color: #94A3B8;">Forecasted to Completion</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Progress Bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(completion_pct / 100.0, text=f"Milestone Progress: {completion_pct}% — {milestone_phase}")

    st.markdown("---")

    # Two columns: Material Quantities and Cost Breakdown Chart
    col_mat, col_chart = st.columns([1, 1.2])

    with col_mat:
        st.subheader("📦 Bill of Materials (BOM) Requirements")
        st.caption("Standard consumption ratios under Indian Standards (IS 456 / SP 23 / CPWD)")

        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #334155; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #F1F5F9;">🏗️ Structural Steel (Fe500D)</span>
                    <span style="color: #38BDF8; font-weight: 800; font-size: 16px;">{metrics['steel_mt']:,.1f} MT</span>
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">Estimated Material Outlay: <b>{format_inr(metrics['steel_cost'])}</b> (@ ₹65k/MT)</div>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #334155; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #F1F5F9;">🧱 OPC/PPC Cement</span>
                    <span style="color: #38BDF8; font-weight: 800; font-size: 16px;">{metrics['cement_bags']:,.0f} Bags ({metrics['cement_mt']:,.1f} MT)</span>
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">Estimated Material Outlay: <b>{format_inr(metrics['cement_cost'])}</b> (@ ₹380/bag)</div>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #334155; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #F1F5F9;">🚛 Ready Mix Concrete (RMC)</span>
                    <span style="color: #38BDF8; font-weight: 800; font-size: 16px;">{metrics['rmc_volume_cum']:,.1f} m³</span>
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">Coarse Aggregate: <b>{metrics['agg_cft']:,.0f} cft</b> | Sand: <b>{metrics['sand_cft']:,.0f} cft</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_chart:
        st.subheader("📊 Capital Budget Allocation")
        # Plotly Donut Chart
        labels = list(metrics["cost_breakdown"].keys())
        values = list(metrics["cost_breakdown"].values())

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.48,
            marker=dict(colors=["#0284C7", "#0D9488", "#F59E0B", "#8B5CF6", "#EF4444"]),
            textinfo="label+percent",
            hoverinfo="label+value+percent"
        )])
        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Conceptual 3D Architectural Rendering via Pollinations AI
    st.subheader("🎨 Conceptual 3D Architectural Rendering Studio")
    st.caption("Epic 3 / Epic 4: Real-time synthesis of photorealistic structural visualization via Pollinations AI engine")

    r1, r2, r3 = st.columns(3)
    with r1:
        arch_style = st.selectbox(
            "Architectural Design Language",
            [
                "Biophilic Green Eco-Architecture with Hanging Vertical Gardens",
                "Ultra-Modern Minimalist Glass & Steel Curtain-Wall",
                "Sculptural Parametric RCC & Fair-Faced Concrete",
                "Neo-Classical Heritage Contemporary Hybrid",
                "Industrial High-Tech Modular Steel Framing"
            ],
            index=0
        )
    with r2:
        elevation_view = st.selectbox(
            "Perspective / Elevation",
            [
                "Street-Level Pedestrian Eye View (Hero Angle)",
                "Aerial 45° Drone View revealing Podium & Landscape",
                "Dramatic Low-Angle Upward Architectural Perspective",
                "Isometric 3D Cutaway Architectural Model"
            ],
            index=0
        )
    with r3:
        lighting_time = st.selectbox(
            "Atmospheric Lighting",
            [
                "Golden Hour Sunset with warm facade illumination and interior glow",
                "Crisp Blue-Sky Morning Sun with sharp geometrical shadows",
                "Dusk Twilight with LED architectural accent lighting",
                "Overcast Diffused Studio Lighting highlighting concrete texture"
            ],
            index=0
        )

    render_prompt, pollinations_url = generate_pollinations_prompt(
        structure_type=structure_type,
        arch_style=arch_style,
        elevation_view=elevation_view,
        lighting_time=lighting_time
    )

    with st.expander("🛠️ Inspect Generated Synthesis Prompt", expanded=False):
        st.code(render_prompt, language="text")

    if st.button("🚀 Synthesize 3D Architectural Visualization", type="primary"):
        with st.spinner("Synthesizing conceptual 3D render from architectural parameters..."):
            st.image(
                pollinations_url,
                caption=f"Conceptual 3D Render: {structure_type} | {arch_style}",
                use_container_width=True
            )
            st.markdown(
                f"[🔗 Open Full-Resolution 4K Render in New Tab]({pollinations_url})"
            )
    else:
        # Show immediate preview button or direct render
        st.image(
            pollinations_url,
            caption=f"Conceptual 3D Visualization: {structure_type} ({arch_style})",
            use_container_width=True
        )
        st.caption("Click 'Synthesize 3D Architectural Visualization' above to refresh with new design parameters.")
