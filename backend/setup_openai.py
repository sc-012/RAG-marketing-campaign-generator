#!/usr/bin/env python3
"""
OpenAI API Setup Script
This script helps you set up OpenAI API authentication for the DynamicRAGSystem.
"""

import os
import sys

def check_openai_key():
    """Check if OpenAI API key is already set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        print("OpenAI API key found in environment")
        return True
    return False

def set_openai_key():
    """Set OpenAI API key"""
    print("Setting up OpenAI API key...")
    
    # Check if already set
    if check_openai_key():
        return True
    
    # Manual key input
    api_key = input("Enter your OpenAI API key: ").strip()
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        print("Environment variable set for this session")
        print("To make it permanent, add this to your shell profile:")
        print(f"   export OPENAI_API_KEY='{api_key}'")
        return True
    else:
        print("No API key provided")
        return False

def main():
    """Main setup function"""
    print("OpenAI API Authentication Setup")
    print("=" * 50)
    
    # Step 1: Check if key is already set
    if check_openai_key():
        print("Setup complete! OpenAI API key is already configured.")
        return True
    
    # Step 2: Set up API key
    if not set_openai_key():
        print("Setup failed. Please provide a valid OpenAI API key.")
        return False
    
    print("\nSetup complete! You can now run the backend.")
    print("Make sure to get your API key from: https://platform.openai.com/api-keys")
    
    return True

if __name__ == "__main__":
    main()
