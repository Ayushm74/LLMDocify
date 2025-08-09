#!/usr/bin/env python3
"""
Test script using HuggingFace API endpoint for DeepSeek models.
"""

import os
import sys
import requests

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import extract_functions, extract_classes
from generator import generate_docstring, generate_class_docstring

# Set the API key
API_KEY = "sk-or-v1-xxa346c41f33547a3af56549b761ca2fe8f06df74a54c63ff8345b4207xxxxxx"

def test_huggingface_api():
    """Test the HuggingFace API endpoint."""
    print("🧪 Testing HuggingFace API endpoint...")
    
    url = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-coder-6.7b-instruct"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": "Write a Python docstring for this function: def hello(name): return f'Hello {name}'",
        "parameters": {
            "temperature": 0.3,
            "max_new_tokens": 200
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print("Response:", result)
            return True
        else:
            print(f"❌ API call failed: {response.status_code}")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_direct_api():
    """Test direct API call to DeepSeek."""
    print("\n🧪 Testing direct DeepSeek API...")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Write a Python docstring for: def hello(name): return f'Hello {name}'"}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print("Response:", result)
            return True
        else:
            print(f"❌ API call failed: {response.status_code}")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run the API tests."""
    print("🚀 Testing different API endpoints...\n")
    
    tests = [
        test_huggingface_api,
        test_direct_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print(f"\n📊 API Test Results: {passed}/{total} tests passed")
    
    if passed > 0:
        print("🎉 At least one API endpoint is working!")
    else:
        print("❌ All API endpoints failed. Please check the API key and endpoints.")
    
    return passed > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 