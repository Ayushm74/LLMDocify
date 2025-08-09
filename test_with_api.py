#!/usr/bin/env python3
"""
Test script using the DeepSeek API key to generate documentation.
"""

import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import extract_functions, extract_classes
from generator import DeepSeekGenerator, generate_docstring, generate_class_docstring

# Set the API key
DEEPSEEK_API_KEY = "sk-or-v1-xxa346c41f33547a3af56549b761ca2fe8f06df74a54c63ff8345b4207xxxxxx"

def test_with_api():
    """Test the AI generation with the provided API key."""
    print("🧪 Testing AI generation with DeepSeek API...")
    
    try:
        # Create generator with the API key
        generator = DeepSeekGenerator(api_key=DEEPSEEK_API_KEY)
        print("✅ DeepSeek generator created successfully")
        
        # Test with a simple function
        test_function = """
def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
"""
        
        print("\n📝 Testing function docstring generation...")
        docstring = generate_docstring(test_function, generator)
        print("Generated docstring:")
        print(docstring)
        
        # Test with a class
        test_class = """
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        return a + b
"""
        
        print("\n📝 Testing class docstring generation...")
        class_docstring = generate_class_docstring(test_class, generator)
        print("Generated class docstring:")
        print(class_docstring)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing with API: {str(e)}")
        return False

def test_sample_file():
    """Test with the sample file."""
    print("\n📁 Testing with sample file...")
    
    try:
        with open("examples/sample.py", "r", encoding="utf-8") as f:
            source_code = f.read()
        
        functions = extract_functions(source_code)
        classes = extract_classes(source_code)
        
        print(f"Found {len(functions)} functions and {len(classes)} classes")
        
        # Test with the first function
        if functions:
            generator = DeepSeekGenerator(api_key=DEEPSEEK_API_KEY)
            first_func = functions[0]
            print(f"\n📝 Generating docstring for function: {first_func['name']}")
            
            docstring = generate_docstring(first_func['body'], generator)
            print("Generated docstring:")
            print(docstring)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing sample file: {str(e)}")
        return False

def main():
    """Run the API tests."""
    print("🚀 Starting API tests with DeepSeek...\n")
    
    tests = [
        test_with_api,
        test_sample_file
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
    
    if passed == total:
        print("🎉 All API tests passed! The AI generation is working correctly.")
        print("\n💡 You can now use the tool with:")
        print("   python main.py docgen examples/sample.py --verbose")
    else:
        print("❌ Some API tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 