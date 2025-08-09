#!/usr/bin/env python3
"""
Web interface for the AI Code-to-Documentation Generator.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
import json
from pathlib import Path
from parser import extract_functions, extract_classes, analyze_code_complexity
from generator import generate_docstring, generate_class_docstring, create_generator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure templates directory exists
templates_dir = Path(__file__).parent / 'templates'
templates_dir.mkdir(exist_ok=True)

@app.route('/')
def index():
    """Main page with the code input form."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze uploaded code and return structure information."""
    try:
        code = request.json.get('code', '')
        if not code.strip():
            return jsonify({'error': 'No code provided'}), 400
        
        # Extract functions and classes
        functions = extract_functions(code)
        classes = extract_classes(code)
        complexity = analyze_code_complexity(code)
        
        return jsonify({
            'functions': functions,
            'classes': classes,
            'complexity': complexity,
            'total_items': len(functions) + len(classes)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_docs():
    """Generate documentation for the provided code."""
    try:
        data = request.json
        code = data.get('code', '')
        selected_items = data.get('selected_items', [])
        provider = data.get('provider', 'mock')
        api_key = data.get('api_key', '')
        
        if not code.strip():
            return jsonify({'error': 'No code provided'}), 400
        
        results = []
        
        # Extract functions and classes
        functions = extract_functions(code)
        classes = extract_classes(code)
        
        # Process selected items
        for item_id in selected_items:
            item_type, item_name = item_id.split(':', 1)
            
            if item_type == 'function':
                for func in functions:
                    if func['name'] == item_name:
                        docstring = generate_docstring(func['body'], provider=provider, api_key=api_key)
                        results.append({
                            'id': item_id,
                            'type': 'function',
                            'name': item_name,
                            'docstring': docstring,
                            'original_code': func['body']
                        })
                        break
            elif item_type == 'class':
                for cls in classes:
                    if cls['name'] == item_name:
                        docstring = generate_class_docstring(cls['body'], provider=provider, api_key=api_key)
                        results.append({
                            'id': item_id,
                            'type': 'class',
                            'name': item_name,
                            'docstring': docstring,
                            'original_code': cls['body']
                        })
                        break
        
        return jsonify({
            'results': results,
            'total_generated': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_docs():
    """Download generated documentation as a file."""
    try:
        data = request.json
        code = data.get('code', '')
        results = data.get('results', [])
        filename = data.get('filename', 'documented_code.py')
        
        if not code or not results:
            return jsonify({'error': 'No code or results provided'}), 400
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.write('\n\n# Generated Documentation\n')
            f.write('=' * 50 + '\n')
            
            for result in results:
                f.write(f'\n{result["type"].title()}: {result["name"]}\n')
                f.write('-' * 30 + '\n')
                f.write(result['docstring'])
                f.write('\n')
            
            temp_path = f.name
        
        return send_file(temp_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/examples')
def examples():
    """Show example code snippets."""
    examples_data = {
        'fibonacci': {
            'name': 'Fibonacci Function',
            'code': '''def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)''',
            'description': 'A recursive function to calculate Fibonacci numbers.'
        },
        'calculator': {
            'name': 'Calculator Class',
            'code': '''class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self) -> list:
        return self.history.copy()''',
            'description': 'A simple calculator class with operation history.'
        },
        'data_processor': {
            'name': 'Data Processor',
            'code': '''def process_data(data: list, filter_key: str = None, sort_by: str = None) -> list:
    result = data.copy()
    
    if filter_key:
        result = [item for item in result if filter_key in item]
    
    if sort_by:
        result.sort(key=lambda x: x.get(sort_by, 0))
    
    return result''',
            'description': 'A data processing function with filtering and sorting.'
        }
    }
    return render_template('examples.html', examples=examples_data)

@app.route('/api/examples')
def get_examples():
    """Get example code snippets as JSON."""
    examples_data = {
        'fibonacci': {
            'name': 'Fibonacci Function',
            'code': '''def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)''',
            'description': 'A recursive function to calculate Fibonacci numbers.'
        },
        'calculator': {
            'name': 'Calculator Class',
            'code': '''class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self) -> list:
        return self.history.copy()''',
            'description': 'A simple calculator class with operation history.'
        },
        'data_processor': {
            'name': 'Data Processor',
            'code': '''def process_data(data: list, filter_key: str = None, sort_by: str = None) -> list:
    result = data.copy()
    
    if filter_key:
        result = [item for item in result if filter_key in item]
    
    if sort_by:
        result.sort(key=lambda x: x.get(sort_by, 0))
    
    return result''',
            'description': 'A data processing function with filtering and sorting.'
        }
    }
    return jsonify(examples_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 