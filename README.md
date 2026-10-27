# Multimodal Construction Intelligence Platform
### Skill Wallet Capstone Project 1 • Platform ID: `6ac4c98d1dcde6d7857c1642`
**Category:** Generative AI | Real Estate Decision Support  
**Target Environment:** Python 3.9+, Streamlit Community Cloud (Zero external database dependencies)

---

## 🏗️ Executive Summary
The **Multimodal Construction Intelligence Platform** is an enterprise-grade AI decision-support system designed for civil contractors, structural forensic consultants, real estate developers, and environmental health and safety (EHS) site directors.

The platform bridges real-time multimodal vision inspection with Indian construction standards (**IS 456:2000, IS 1893, IS 13920, IS 7861**) and international safety protocols (**OSHA 29 CFR 1926, ACI 224R-01**).

---

## 🎯 Kanban Epics Coverage Matrix

| Epic | Module / Focus | Implementation Status | Key Deliverables |
| :--- | :--- | :---: | :--- |
| **Epic 1** | Requirements & Environment | **Completed (100%)** | Python 3.12+, zero-DB deployment, Streamlit Cloud ready |
| **Epic 2** | PPE Safety Vision & Crack Diagnostics | **Completed (100%)** | Multimodal audits, OSHA/IS 456 compliance, crack classification & repairs |
| **Epic 3** | Project Planning & Valuation | **Completed (100%)** | CapEx tracking, WIP valuation in INR (Lakhs/Crores), BOM forecasting |
| **Epic 4** | Multimodal AI & JSON Contracts | **Completed (100%)** | Strict structured JSON schema validation, graceful demonstration fallback |
| **Epic 5** | Site Chatbot & Weather Advisory | **Completed (100%)** | Dynamic microclimate alerts (crane limits, curing), multi-turn resident engineer bot |
| **Epic 6** | Interface, Testing & Deployment | **Completed (100%)** | Responsive high-contrast UI, 1-click synthetic presets, complete test suite |

---

## 🚀 Key Modules & Capabilities

### 1. 🛡️ Tab 1 - Site Safety & PPE Audit (Epic 2)
- **Multimodal Visual Inspection:** Detects hard hats, high-vis vests, steel-toe footwear, and full-body safety harnesses at height.
- **Regulatory Framework:** Evaluates contraventions under **OSHA 1926.100, 1926.201, 1926.502** and **IS 2925, IS 15809, IS 3521**.
- **Structured JSON Contracts:**
  - `safety_score` (0-100 composite safety index)
  - `overall_status` (*Compliant*, *Minor Infractions*, *Critical Violations*, *Work Stop Required*)
  - PPE equipment status with compliant vs non-compliant worker counts.
  - Granular site hazards list with severity (*Critical, High, Medium, Low*), standard clauses, and immediate corrective remedies.
- **Export:** Instant one-click downloadable JSON audit report.

### 2. 🔍 Tab 2 - Crack Diagnostics & Structural Integrity (Epic 2)
- **Defect Classification:** Diagnoses Structural Shear (45°), Foundation Settlement, Hairline Shrinkage, Thermal Expansion, and Spalling with rebar corrosion.
- **Forensic Quantifications:** Estimated crack width ($mm$), through-section depth categorization, and IS 456 Cl 35.3.2 permissible crack limit benchmark ($0.3\text{ mm}$ for mild/moderate exposure).
- **Engineering Repair Protocol:** Step-by-step remediation specifications including low-viscosity epoxy resin injection (0.2-0.4 MPa), structural CFRP composite wrapping, and polyurethane sealing.
- **Urgency Windows:** *Immediate (Within 24 Hours)*, *High Priority (Within 7 Days)*, *Medium Priority*, and *Routine Monitoring*.

### 3. 🏢 Tab 3 - Planning & Real Estate Valuation (Epic 3)
- **Parametric Cost Engine:** Configurable by structure type (Residential RCC, Commercial Grade A, Industrial PEB, Luxury Plotted, Affordable Housing), location tier (Tier 1/2/3 Indian metropolitan hubs), and specification grades.
- **Financial Projections in INR:** Total project budget, CapEx incurred to date, remaining cash outflow, and current Work-In-Progress (WIP) asset valuation in **₹ Lakhs** and **₹ Crores**.
- **Bill of Materials (BOM) Forecaster:** Structural steel (Fe500D) MT, cement bags & MT, Ready Mix Concrete (RMC) volume ($m^3$), coarse aggregate, and river sand quantities.
- **Pollinations AI 3D Rendering Studio:** Automated synthesis of photorealistic 3D architectural elevations and perspectives directly from project parameters.

### 4. 🌦️ Tab 4 - Daily Site Assistant & Weather-Aware Advisory (Epic 5)
- **Microclimate Alert Matrix:** Dynamic directives for High Wind (>45 km/h), Heavy Monsoon (>30 mm/h), Extreme Heat (>40°C), and Cold Waves.
- **Critical Protocols:** Tower crane operation suspension limits (OSHA 1926.1431), electrical GFCI hazard mitigation, excavation de-watering, and hot weather concreting (IS 7861 Part 1).
- **Interactive Resident Engineer Chatbot:** Multi-turn AI assistant fluent in Indian civil codes and NBC 2016, equipped with quick-answer chips and chat reset.

---

## 🛠️ Technology Stack
- **Frontend & App Framework:** Streamlit 1.35+
- **Multimodal AI Engine:** Google GenAI SDK (`gemini-2.5-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`) with automated Demonstration Mode fallback
- **Data Visualization:** Plotly Graph Objects & Altair
- **Computer Vision & Imaging:** Pillow (PIL)
- **Architectural Synthesis:** Pollinations / Flux Generative Architecture API
- **Data Contracts:** Python Pydantic & JSON Schemas

---

## ⚡ Quickstart Guide

### 1. Clone & Set Up Environment
```bash
git clone <repository-url>
cd multimodal-construction-intelligence
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Application
```bash
streamlit run app.py
```

### 3. Configuration & API Key
- Enter your **Google Gemini API Key** in the sidebar to enable live multimodal inference.
- If no key is provided, the platform automatically runs in **High-Fidelity Demonstration Mode** using built-in engineering presets and synthetic test scenes.

---

## 📁 Repository Structure
```
multimodal-construction-intelligence/
├── app.py                          # Main Streamlit application entrypoint
├── requirements.txt                # Production dependency list for Streamlit Cloud
├── README.md                       # Platform documentation and architecture
├── assets/
│   └── sample_images.py            # Synthetic 1-click test image generators (Safety & Cracks)
└── modules/
    ├── gemini_client.py            # Gemini GenAI wrapper with fallback engine
    ├── safety_audit.py             # OSHA 1926 & IS 456 multimodal PPE audit module
    ├── crack_diagnostics.py        # Forensic concrete crack classification & repair module
    ├── valuation_engine.py         # Cost estimation, CapEx, INR valuation & Pollinations 3D studio
    └── site_assistant.py           # Weather-aware safety advisory & resident engineer chatbot
```

---

## 📜 Statutory Standards Reference
- **IS 456:2000**: Plain and Reinforced Concrete — Code of Practice
- **IS 2925:1984**: Specification for Industrial Safety Helmets
- **IS 15809:2017**: High Visibility Warning Clothes
- **IS 3521:1999**: Industrial Safety Belts and Harnesses
- **IS 7861 (Parts 1 & 2)**: Code of Practice for Extreme Weather Concreting
- **OSHA 29 CFR 1926**: Safety and Health Regulations for Construction
- **ACI 224R-01**: Control of Cracking in Concrete Structures
