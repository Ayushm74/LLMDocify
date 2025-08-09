#!/usr/bin/env python3
"""
Basic test script to verify the core functionality of the AI documentation generator.
This script tests the parsing functionality without requiring API keys.
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import extract_functions, extract_classes, analyze_code_complexity
from generator import DEFAULT_FUNCTION_PROMPT, DEFAULT_CLASS_PROMPT


def test_parser():
    """Test the code parser functionality."""
    print("🧪 Testing code parser...")
    
    # Test with a simple function
    test_code = """
def hello_world(name: str = "World") -> str:
    return f"Hello, {name}!"
"""
    
    functions = extract_functions(test_code)
    print(f"✅ Found {len(functions)} functions")
    
    if functions:
        func = functions[0]
        print(f"   Function name: {func['name']}")
        print(f"   Arguments: {func['args']}")
        print(f"   Has return: {func['has_return']}")
    
    # Test with a class
    test_class_code = """
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        return a + b
"""
    
    classes = extract_classes(test_class_code)
    print(f"✅ Found {len(classes)} classes")
    
    if classes:
        cls = classes[0]
        print(f"   Class name: {cls['name']}")
        print(f"   Methods: {len(cls['methods'])}")
        print(f"   Method names: {[m['name'] for m in cls['methods']]}")
    
    # Test complexity analysis
    complexity = analyze_code_complexity(test_code + test_class_code)
    print(f"✅ Complexity analysis: {complexity}")
    
    return True


def test_prompts():
    """Test the prompt templates."""
    print("\n🧪 Testing prompt templates...")
    
    # Test function prompt
    function_code = "def test_function(x: int) -> int:\n    return x * 2"
    prompt = DEFAULT_FUNCTION_PROMPT.replace("{function_code}", function_code)
    print(f"✅ Function prompt length: {len(prompt)} characters")
    
    # Test class prompt
    class_code = "class TestClass:\n    def __init__(self):\n        pass"
    class_prompt = DEFAULT_CLASS_PROMPT.replace("{class_code}", class_code)
    print(f"✅ Class prompt length: {len(class_prompt)} characters")
    
    return True


def test_sample_file():
    """Test parsing the sample file."""
    print("\n🧪 Testing sample file parsing...")
    
    try:
        with open("examples/sample.py", "r", encoding="utf-8") as f:
            source_code = f.read()
        
        functions = extract_functions(source_code)
        classes = extract_classes(source_code)
        complexity = analyze_code_complexity(source_code)
        
        print(f"✅ Sample file analysis:")
        print(f"   Functions: {len(functions)}")
        print(f"   Classes: {len(classes)}")
        print(f"   Lines: {complexity['lines']}")
        print(f"   Characters: {complexity['characters']}")
        
        # Show some function names
        if functions:
            func_names = [f['name'] for f in functions[:3]]
            print(f"   Sample functions: {func_names}")
        
        # Show some class names
        if classes:
            class_names = [c['name'] for c in classes[:3]]
            print(f"   Sample classes: {class_names}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Sample file not found")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting basic functionality tests...\n")
    
    tests = [
        test_parser,
        test_prompts,
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
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The core functionality is working correctly.")
        print("\n💡 To test with AI generation, you'll need to:")
        print("   1. Get an API key from HuggingFace or OpenAI")
        print("   2. Set the environment variable (HUGGINGFACE_API_KEY or OPENAI_API_KEY)")
        print("   3. Run: python main.py docgen examples/sample.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 