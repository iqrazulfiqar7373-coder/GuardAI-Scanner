import os
import re

def scan_terraform_files():
    print("🚀 Starting GuardAI Cloud Security Scanner...\n")
    vulnerabilities_found = 0
    
    # Current folder mein .tf files dhoondo
    files = [f for f in os.listdir('.') if f.endswith('.tf')]
    
    if not files:
        print("❌ No Terraform (.tf) files found to scan.")
        return

    for file_name in files:
        print(file_name, "🔍 Scanning...")
        with open(file_name, 'r') as f:
            content = f.read()
            
            # Check 1: Open Ports (0.0.0.0/0)
            if '0.0.0.0/0' in content:
                print("🚨 VULNERABILITY FOUND: Open Security Group Port (0.0.0.0/0) detected!")
                print("💡 Fix: Restrict CIDR blocks to internal corporate IPs only.\n")
                vulnerabilities_found += 1
                
            # Check 2: Public S3 Bucket
            if 'public-read' in content or 'public-read-write' in content:
                print("🚨 VULNERABILITY FOUND: Public S3 Bucket ACL detected!")
                print("💡 Fix: Change ACL to 'private' to secure sensitive data.\n")
                vulnerabilities_found += 1

    print(f"✅ Scan Complete. Total Vulnerabilities Detected: {vulnerabilities_found}")

if __name__ == "__main__":
    scan_terraform_files()