import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# Import your scanner functions
from scanner import run_static_analysis
from ai_review import ai_review_terraform

# Page config
st.set_page_config(page_title="GuardAI Scanner", page_icon="🛡️", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #00d4aa;
        text-align: center;
    }
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #00d4aa;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 2rem;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛡️ GuardAI Scanner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Terraform Security Vulnerability Scanner</div>', unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **GuardAI Scanner** uses a dual-layer approach:
    
    1. **Static Analysis** — Rule-based pattern matching
    2. **AI Deep Analysis** — Claude LLM contextual review
    
    🔒 Your code is processed securely.
    """)
    st.divider()
    st.caption("Made with ❤️ by Iqra Zulfiqar")

# Main input
st.subheader("📄 Paste Your Terraform Configuration")
tf_content = st.text_area(
    "Terraform (.tf) code:",
    height=300,
    placeholder="""resource "aws_security_group" "example" {
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}""",
    help="Paste your Terraform HCL code here to scan for security issues."
)

# Scan button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    scan_clicked = st.button("🔍 RUN SECURITY SCAN", use_container_width=True)

# Results section
if scan_clicked:
    if not tf_content.strip():
        st.warning("⚠️ Please paste some Terraform code first!")
    else:
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Layer 1: Static Analysis
        status_text.text("📋 Running Layer 1: Static Analysis...")
        progress_bar.progress(25)
        
        static_issues = run_static_analysis(tf_content)
        
        # Display Layer 1 Results
        st.divider()
        st.subheader("🛡️ Layer 1 — Static Security Assertions")
        
        if static_issues:
            for issue in static_issues:
                st.error(f"🔴 {issue}")
        else:
            st.success("✅ No baseline anomalies caught.")
        
        # Layer 2: AI Analysis
        status_text.text("🤖 Running Layer 2: AI Deep Contextual Analysis...")
        progress_bar.progress(60)
        
        ai_raw_output = ai_review_terraform(tf_content, static_issues)
        
        progress_bar.progress(100)
        status_text.empty()
        
        # Display Layer 2 Results
        st.subheader("🧠 Layer 2 — AI Deep Security Context")
        
        if "AI_ERROR" in ai_raw_output:
            st.warning(f"⚠️ {ai_raw_output}")
        elif "NO_ADDITIONAL_ISSUES" in ai_raw_output:
            st.success("✅ No additional sophisticated vulnerability vectors observed.")
        else:
            ai_issues = [line.strip() for line in ai_raw_output.strip().split('\n') if line.strip()]
            for issue in ai_issues:
                st.warning(f"🟡 {issue}")
        
        # Final Report
        st.divider()
        st.subheader("📊 Scan Summary")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Static Issues", len(static_issues))
        with col_b:
            ai_count = 0 if "AI_ERROR" in ai_raw_output or "NO_ADDITIONAL_ISSUES" in ai_raw_output else len([l for l in ai_raw_output.strip().split('\n') if l.strip()])
            st.metric("AI Findings", ai_count)
        
        # Download report
        import json
        report = {
            "scan_type": "GuardAI Security Audit",
            "static_issues": static_issues,
            "ai_output": ai_raw_output
        }
        st.download_button(
            label="📥 Download JSON Report",
            data=json.dumps(report, indent=4),
            file_name="security_audit_manifest.json",
            mime="application/json"
        )