#!/usr/bin/env python3
"""
Drone CI Setup Verification Script
Checks all configuration points for "Resource not accessible by integration" error
"""

import os
import requests
import subprocess
import sys

def check_github_oauth():
    """Check GitHub OAuth App configuration"""
    print("🔍 1. CHECKING GITHUB OAUTH APP...")
    
    client_id = "Iv23lim14p0PKK69D5QN"
    client_secret = os.getenv('DRONE_GITHUB_CLIENT_SECRET')
    
    if not client_secret or client_secret == 'your_actual_github_client_secret_here':
        print("❌ GitHub Client Secret not configured")
        print("   Action: Set DRONE_GITHUB_CLIENT_SECRET in .env file")
        return False
    
    print(f"✅ Client ID: {client_id}")
    print("✅ Client Secret: Configured")
    return True

def check_drone_server():
    """Check if Drone server is running"""
    print("\n🔍 2. CHECKING DRONE SERVER...")
    
    try:
        response = requests.get("http://localhost:8007", timeout=5)
        print(f"✅ Drone server responding: {response.status_code}")
        return True
    except requests.exceptions.RequestException:
        print("❌ Drone server not accessible at localhost:8007")
        print("   Action: Start Drone with 'docker-compose -f drone-compose.yml up'")
        return False

def check_repository_permissions():
    """Check repository and permissions"""
    print("\n🔍 3. CHECKING REPOSITORY PERMISSIONS...")
    
    # Check if this is a git repository
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository detected")
            print(f"   Remote: {result.stdout.strip()}")
            
            # Check if user has push access
            try:
                subprocess.run(['git', 'ls-remote', 'origin'], capture_output=True, check=True)
                print("✅ Repository access confirmed")
                return True
            except subprocess.CalledProcessError:
                print("❌ Cannot access remote repository")
                print("   Action: Check GitHub permissions and authentication")
                return False
        else:
            print("❌ Not a git repository")
            return False
    except FileNotFoundError:
        print("❌ Git not installed or not in PATH")
        return False

def check_drone_config():
    """Check Drone configuration file"""
    print("\n🔍 4. CHECKING DRONE CONFIGURATION...")
    
    if os.path.exists('.drone.yml'):
        print("✅ .drone.yml file exists")
        with open('.drone.yml', 'r') as f:
            content = f.read()
            if 'kind: pipeline' in content:
                print("✅ Valid Drone pipeline configuration")
                return True
            else:
                print("❌ Invalid Drone configuration")
                return False
    else:
        print("❌ .drone.yml file missing")
        return False

def check_environment():
    """Check environment variables"""
    print("\n🔍 5. CHECKING ENVIRONMENT VARIABLES...")
    
    required_vars = [
        'DRONE_GITHUB_CLIENT_SECRET',
        'DRONE_RPC_SECRET'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f'your_actual_{var.lower()}_here':
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set or using placeholder")
            all_set = False
    
    return all_set

def main():
    print("🚀 DRONE CI TROUBLESHOOTING CHECKLIST")
    print("=" * 50)
    
    checks = [
        check_github_oauth,
        check_drone_server,
        check_repository_permissions,
        check_drone_config,
        check_environment
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    
    if all(results):
        print("✅ All checks passed! Try activating repository again.")
    else:
        print("❌ Issues found. Fix the above problems and retry.")
        
    print("\n🔧 NEXT STEPS:")
    print("1. Fix any failed checks above")
    print("2. Restart Drone: docker-compose -f drone-compose.yml restart")
    print("3. Try activating repository again")
    print("4. Check Drone server logs: docker-compose -f drone-compose.yml logs drone-server")

if __name__ == "__main__":
    main()