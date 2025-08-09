#!/usr/bin/env python3
"""
Demonstration script for the AI Code-to-Documentation Generator.
This script shows various ways to use the tool.
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and print the output."""
    print(f"\n🚀 Running: {command}")
    print("=" * 60)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running command: {e}")

def main():
    """Run the demonstration."""
    print("🤖 AI Code-to-Documentation Generator Demo")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: Please run this script from the project root directory.")
        return
    
    print("\n📋 Available commands:")
    print("1. Basic usage - generate docs for a file")
    print("2. Functions only - skip classes")
    print("3. Classes only - skip functions")
    print("4. Save output to file")
    print("5. Batch processing")
    print("6. Version info")
    
    # Demo 1: Basic usage
    print("\n" + "="*60)
    print("📝 Demo 1: Basic usage")
    run_command("python main.py docgen examples/sample.py")
    
    # Demo 2: Functions only
    print("\n" + "="*60)
    print("📝 Demo 2: Functions only")
    run_command("python main.py docgen examples/sample.py --functions-only")
    
    # Demo 3: Classes only
    print("\n" + "="*60)
    print("📝 Demo 3: Classes only")
    run_command("python main.py docgen examples/sample.py --classes-only")
    
    # Demo 4: Save to file
    print("\n" + "="*60)
    print("📝 Demo 4: Save output to file")
    run_command("python main.py docgen examples/sample.py --output demo_output.txt")
    
    # Demo 5: Version
    print("\n" + "="*60)
    print("📝 Demo 5: Version info")
    run_command("python main.py version")
    
    print("\n" + "="*60)
    print("🎉 Demo completed!")
    print("\n💡 To use with real AI models:")
    print("1. Get an API key from HuggingFace or OpenAI")
    print("2. Set environment variable: export DEEPSEEK_API_KEY='your_key'")
    print("3. Run: python main.py docgen examples/sample.py --verbose")

if __name__ == "__main__":
    main() 