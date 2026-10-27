"""
Comprehensive Unit & Integration Test Suite for Multimodal Construction Intelligence Platform
Tests all modules, math models, JSON schemas, and sample image generators.
"""
import sys
import os

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.gemini_client import GeminiClientWrapper
from modules.safety_audit import get_demo_safety_data, run_safety_audit
from modules.crack_diagnostics import get_demo_crack_data, run_crack_diagnostics
from modules.valuation_engine import calculate_project_metrics, format_inr, generate_pollinations_prompt
from modules.site_assistant import get_engineering_fallback, WEATHER_PROTOCOLS
from assets.sample_images import generate_sample_safety_image, generate_sample_crack_image

def test_sample_image_generators():
    safety_png = generate_sample_safety_image()
    assert isinstance(safety_png, bytes)
    assert len(safety_png) > 1000

    crack_png = generate_sample_crack_image()
    assert isinstance(crack_png, bytes)
    assert len(crack_png) > 1000

def test_gemini_client_fallback_mode():
    client = GeminiClientWrapper(api_key="")
    assert client.is_live is False

    safety_png = generate_sample_safety_image()
    audit_res, is_live, msg = run_safety_audit(client, safety_png)
    assert is_live is False
    assert "safety_score" in audit_res
    assert audit_res["safety_score"] >= 0 and audit_res["safety_score"] <= 100
    assert "ppe_detection" in audit_res
    assert len(audit_res["ppe_detection"]) > 0
    assert "identified_site_hazards" in audit_res
    assert len(audit_res["identified_site_hazards"]) > 0

    crack_png = generate_sample_crack_image()
    diag_res, is_live_crack, msg_crack = run_crack_diagnostics(client, crack_png)
    assert is_live_crack is False
    assert "defect_type" in diag_res
    assert "estimated_crack_width_mm" in diag_res
    assert "recommended_engineering_repairs" in diag_res
    assert len(diag_res["recommended_engineering_repairs"]) > 0

def test_valuation_engine_calculations():
    metrics = calculate_project_metrics(
        structure_type="Residential High-Rise (RCC G+20)",
        built_up_sqft=100_000,
        location_tier="Tier 1 (Mumbai, Bengaluru, Delhi-NCR, Hyderabad, Chennai, Pune)",
        grade="Standard Grade (IS Standard Compliance)",
        completion_pct=50
    )

    assert metrics["total_budget"] > 0
    assert metrics["capex_incurred"] == metrics["total_budget"] * 0.5
    assert metrics["remaining_outflow"] == metrics["total_budget"] * 0.5
    assert metrics["wip_valuation"] >= metrics["capex_incurred"]
    assert metrics["steel_mt"] > 0
    assert metrics["cement_bags"] > 0
    assert metrics["rmc_volume_cum"] > 0
    assert len(metrics["cost_breakdown"]) == 5

    # Test INR formatting
    assert "Cr" in format_inr(25_000_000)
    assert "Lakhs" in format_inr(500_000)

    # Test Pollinations prompt generation
    prompt, url = generate_pollinations_prompt(
        structure_type="Commercial Office Complex (Grade A)",
        arch_style="Biophilic Green Eco-Architecture",
        elevation_view="Hero Eye View",
        lighting_time="Golden Hour"
    )
    assert "image.pollinations.ai" in url
    assert "Biophilic" in prompt

def test_weather_and_chat_assistant():
    for cond_name, info in WEATHER_PROTOCOLS.items():
        assert "severity" in info
        assert "crane_status" in info
        assert "crane_protocol" in info
        assert "concreting_protocol" in info

    cover_ans = get_engineering_fallback("Explain cover requirements under IS 456")
    assert "IS 456" in cover_ans
    assert "Table 16" in cover_ans

    crane_ans = get_engineering_fallback("What are wind limits for crane operations?")
    assert "km/h" in crane_ans

if __name__ == "__main__":
    test_sample_image_generators()
    test_gemini_client_fallback_mode()
    test_valuation_engine_calculations()
    test_weather_and_chat_assistant()
    print("All unit tests passed successfully!")
