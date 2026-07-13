import os
from dotenv import load_dotenv
import anthropic

# Load environment variables securely
load_dotenv()

def ai_review_terraform(tf_content: str, static_findings: list) -> str:
    """
    Sends Terraform content and static analysis logs to Claude for a
    comprehensive secondary security review.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        # Public-friendly expert info instead of crashing or throwing hard errors
        return "AI_INFO: Claude AI review skipped. To enable Layer 2 deep context, please add your ANTHROPIC_API_KEY to a .env file."

    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Format baseline findings cleanly without dynamic inline char syntax to avoid ID errors
        formatted_static = "None"
        if static_findings:
            formatted_static = "\n".join(static_findings)

        prompt = (
            "You are an expert cloud security architect reviewing IaC templates.\n"
            "Analyze this Terraform code and the associated static analysis findings.\n"
            "Identify advanced logical flaws, context-dependent risks, or IAM misconfigurations "
            "that rule-based scanners might miss.\n\n"
            f"=== Static Analysis Findings ===\n{formatted_static}\n\n"
            f"=== Terraform Code ===\n{tf_content}\n\n"
            "Respond ONLY in this strict pipe-delimited format for each issue found (one per line):\n"
            "RESOURCE_NAME | RISK_LEVEL | ARCHITECTURAL_FIX_RECOMMENDATION\n"
            "If no additional vulnerabilities are found beyond static findings, reply with 'NO_ADDITIONAL_ISSUES'."
        )

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

    except Exception as e:
        return f"AI_ERROR: Failed to execute Claude review layer. Details: {str(e)}"