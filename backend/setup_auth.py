#!/usr/bin/env python3
"""
Hugging Face Authentication Setup Script
This script helps you set up authentication for the Mistral model.
"""

import os
import subprocess
import sys

def check_huggingface_cli():
    """Check if huggingface-cli is installed"""
    try:
        result = subprocess.run(['huggingface-cli', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Hugging Face CLI is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Hugging Face CLI not found. Installing...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'huggingface_hub'], 
                      check=True)
        print(" Hugging Face CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Hugging Face CLI")
        return False

def setup_authentication():
    """Set up Hugging Face authentication"""
    print("🔐 Setting up Hugging Face Authentication for Mistral Model")
    print("=" * 60)
    
    # Check if already logged in
    try:
        result = subprocess.run(['huggingface-cli', 'whoami'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f" Already logged in as: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("\n📋 Follow these steps to get your Hugging Face token:")
    print("1. Go to https://huggingface.co/ and create an account")
    print("2. Visit https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1")
    print("3. Click 'Request Access' and wait for approval")
    print("4. Go to https://huggingface.co/settings/tokens")
    print("5. Create a new token with 'Read' access")
    print("\n" + "=" * 60)
    
    # Try to login via CLI
    print("\n🔑 Please enter your Hugging Face token:")
    try:
        subprocess.run(['huggingface-cli', 'login'], check=True)
        print(" Authentication successful!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Authentication failed. Please try again.")
        return False
    except KeyboardInterrupt:
        print("\n❌ Authentication cancelled.")
        return False

def set_environment_variable():
    """Set HUGGINGFACE_TOKEN environment variable"""
    print("\n🌍 Setting up environment variable...")
    
    # Get token from huggingface-cli
    try:
        result = subprocess.run(['huggingface-cli', 'whoami'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(" Token found in Hugging Face CLI")
            return True
    except FileNotFoundError:
        pass
    
    # Manual token input
    token = input("Enter your Hugging Face token: ").strip()
    if token:
        os.environ['HUGGINGFACE_TOKEN'] = token
        print(" Environment variable set for this session")
        print("💡 To make it permanent, add this to your shell profile:")
        print(f"   export HUGGINGFACE_TOKEN='{token}'")
        return True
    else:
        print("❌ No token provided")
        return False

def main():
    """Main setup function"""
    print("🚀 Hugging Face Authentication Setup")
    print("=" * 60)
    
    # Step 1: Check/install huggingface-cli
    if not check_huggingface_cli():
        print("❌ Cannot proceed without Hugging Face CLI")
        return False
    
    # Step 2: Set up authentication
    if not setup_authentication():
        print("❌ Authentication setup failed")
        return False
    
    # Step 3: Set environment variable
    if not set_environment_variable():
        print("❌ Environment variable setup failed")
        return False
    
    print("\n🎉 Setup complete! You can now run the backend.")
    print("💡 Make sure to request access to the Mistral model at:")
    print("   https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1")
    
    return True

if __name__ == "__main__":
    main()
