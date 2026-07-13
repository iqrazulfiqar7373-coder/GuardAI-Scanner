import os
import json
from ai_review import ai_review_terraform

def run_static_analysis(tf_content: str) -> list[str]:
    """Runs deterministic rule-based signature checks on the configuration text."""
    findings = []
    
    # Rule 1: Broad Ingress Rule
    if "0.0.0.0/0" in tf_content:
        findings.append("STATIC_ERR: Open firewall or security group allows unrestricted internet access (0.0.0.0/0).")
        
    # Rule 2: Unencrypted AWS S3 Bucket representation (generic pattern check)
    if "aws_s3_bucket" in tf_content and "server_side_encryption_configuration" not in tf_content:
        findings.append("STATIC_ERR: AWS S3 Bucket resource defined without explicit server-side encryption enabled.")
        
    return findings

def execute_dual_layer_audit(tf_file_path: str):
    """Orchestrates both baseline static scanning and contextual AI-driven reviews."""
    if not os.path.exists(tf_file_path):
        print(f"❌ Input file error: Target '{tf_file_path}' does not exist.")
        return

    print(f"🚀 Initializing GuardAI Scanner Pipeline against: '{tf_file_path}'")
    
    with open(tf_file_path, 'r') as f:
        tf_content = f.read()

    # 1. Trigger Static Rules
    print("📋 Processing Layer 1: Running Static Analysis Rules...")
    static_issues = run_static_analysis(tf_content)
    print(f"-> Layer 1 Complete. Static rule triggers: {len(static_issues)}")

    # 2. Trigger AI Refiner Layer
    print("🤖 Processing Layer 2: Launching LLM Contextual Analysis...")
    ai_raw_output = ai_review_terraform(tf_content, static_issues)
    print("-> Layer 2 Complete.")

    # 3. Consolidate and Parse into Structure
    ai_processed_issues = []
    if ai_raw_output and "NO_ADDITIONAL_ISSUES" not in ai_raw_output and "AI_ERROR" not in ai_raw_output:
        ai_processed_issues = [line.strip() for line in ai_raw_output.strip().split('\n') if line.strip()]

    # Display Consolidated Report to Console
    print("\n" + "="*70)
    print("                      GUARD AI SECURITY SCAN REPORT")
    print("="*70)
    print(f"Target Scope : {tf_file_path}")
    print(f"Status       : Complete")
    print("-"*70)
    
    print("\n[+] Layer 1 - Static Assertions:")
    if static_issues:
        for idx, issue in enumerate(static_issues, 1): print(f"  {idx}. {issue}")
    else:
        print("  No baseline anomalies caught.")

    print("\n[+] Layer 2 - AI Deep Security Context:")
    if "AI_ERROR" in ai_raw_output:
        print(f"  ⚠️ {ai_raw_output}")
    elif ai_processed_issues:
        for idx, issue in enumerate(ai_processed_issues, 1): print(f"  {idx}. {issue}")
    else:
        print("  No additional sophisticated vulnerability vectors observed.")
    print("="*70)

    # 4. Generate Final Artifact JSON (Proof for GitHub)
    final_report = {
        "target_file": tf_file_path,
        "metrics": {
            "static_vulnerabilities_count": len(static_issues),
            "ai_vulnerabilities_count": len(ai_processed_issues)
        },
        "findings": {
            "static_layer_output": static_issues,
            "ai_layer_output": ai_processed_issues if not "AI_ERROR" in ai_raw_output else [ai_raw_output]
        }
    }
    
    with open("security_audit_manifest.json", "w") as out_file:
        json.dump(final_report, out_file, indent=4)
    print("\n💾 Structured audit record exported successfully to 'security_audit_manifest.json'")

if __name__ == "__main__":
    # Standard baseline execution using a testing target file
    execute_dual_layer_audit("vulnerable.tf")