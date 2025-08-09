#!/usr/bin/env python3
"""
AI Code-to-Documentation Generator
A CLI tool that generates high-quality docstrings for Python functions using AI.
"""

import typer
import os
import sys
from pathlib import Path
from typing import Optional, List
from parser import extract_functions, extract_classes
from generator import generate_docstring, generate_class_docstring

app = typer.Typer(
    name="codex-docgen",
    help="AI-powered code documentation generator",
    add_completion=False
)

def validate_file(file_path: str) -> bool:
    """Validate that the file exists and is a Python file."""
    if not os.path.exists(file_path):
        typer.echo(f"❌ Error: File '{file_path}' does not exist.", err=True)
        return False
    
    if not file_path.endswith('.py'):
        typer.echo(f"❌ Error: File '{file_path}' is not a Python file.", err=True)
        return False
    
    return True

@app.command()
def docgen(
    file: str = typer.Argument(..., help="Path to the Python file to process"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path (optional)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    functions_only: bool = typer.Option(False, "--functions-only", help="Process only functions, skip classes"),
    classes_only: bool = typer.Option(False, "--classes-only", help="Process only classes, skip functions")
):
    """
    Generate docstrings for all functions and classes in a Python file.
    
    Examples:
        python main.py docgen examples/sample.py
        python main.py docgen myfile.py --output documented_myfile.py
        python main.py docgen myfile.py --functions-only --verbose
    """
    if not validate_file(file):
        raise typer.Exit(1)
    
    try:
        with open(file, "r", encoding="utf-8") as f:
            source_code = f.read()
        
        if verbose:
            typer.echo(f"📁 Processing file: {file}")
            typer.echo(f"📊 File size: {len(source_code)} characters")
        
        results = []
        
        # Process functions
        if not classes_only:
            functions = extract_functions(source_code)
            if verbose:
                typer.echo(f"🔍 Found {len(functions)} functions")
            
            for func in functions:
                if verbose:
                    typer.echo(f"  📝 Processing function: {func['name']}")
                
                try:
                    docstring = generate_docstring(func['body'])
                    results.append({
                        'type': 'function',
                        'name': func['name'],
                        'original': func['body'],
                        'docstring': docstring
                    })
                    typer.echo(f"✅ Generated docstring for function: {func['name']}")
                except Exception as e:
                    typer.echo(f"❌ Error generating docstring for {func['name']}: {str(e)}", err=True)
        
        # Process classes
        if not functions_only:
            classes = extract_classes(source_code)
            if verbose:
                typer.echo(f"🔍 Found {len(classes)} classes")
            
            for cls in classes:
                if verbose:
                    typer.echo(f"  📝 Processing class: {cls['name']}")
                
                try:
                    docstring = generate_class_docstring(cls['body'])
                    results.append({
                        'type': 'class',
                        'name': cls['name'],
                        'original': cls['body'],
                        'docstring': docstring
                    })
                    typer.echo(f"✅ Generated docstring for class: {cls['name']}")
                except Exception as e:
                    typer.echo(f"❌ Error generating docstring for {cls['name']}: {str(e)}", err=True)
        
        # Display results
        if not results:
            typer.echo("ℹ️  No functions or classes found to document.")
            return
        
        typer.echo(f"\n📋 Generated {len(results)} docstrings:")
        for result in results:
            typer.echo(f"\n{'='*50}")
            typer.echo(f"{result['type'].title()}: {result['name']}")
            typer.echo(f"{'='*50}")
            typer.echo(result['docstring'])
        
        # Save to output file if specified
        if output:
            try:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(source_code)
                    f.write("\n\n# Generated Documentation\n")
                    f.write("=" * 50 + "\n")
                    for result in results:
                        f.write(f"\n{result['type'].title()}: {result['name']}\n")
                        f.write("-" * 30 + "\n")
                        f.write(result['docstring'])
                        f.write("\n")
                typer.echo(f"\n💾 Results saved to: {output}")
            except Exception as e:
                typer.echo(f"❌ Error saving to {output}: {str(e)}", err=True)
        
    except Exception as e:
        typer.echo(f"❌ Error processing file: {str(e)}", err=True)
        raise typer.Exit(1)

@app.command()
def batch(
    directory: str = typer.Argument(..., help="Directory containing Python files to process"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Process subdirectories recursively"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """
    Process all Python files in a directory.
    
    Examples:
        python main.py batch ./src
        python main.py batch ./src --recursive --verbose
    """
    if not os.path.exists(directory):
        typer.echo(f"❌ Error: Directory '{directory}' does not exist.", err=True)
        raise typer.Exit(1)
    
    if not os.path.isdir(directory):
        typer.echo(f"❌ Error: '{directory}' is not a directory.", err=True)
        raise typer.Exit(1)
    
    # Find all Python files
    pattern = "**/*.py" if recursive else "*.py"
    python_files = list(Path(directory).glob(pattern))
    
    if not python_files:
        typer.echo(f"ℹ️  No Python files found in {directory}")
        return
    
    if verbose:
        typer.echo(f"📁 Found {len(python_files)} Python files to process")
    
    for file_path in python_files:
        if verbose:
            typer.echo(f"\n🔄 Processing: {file_path}")
        
        try:
            # Call the docgen function for each file
            docgen(str(file_path), None, verbose, False, False)
        except Exception as e:
            typer.echo(f"❌ Error processing {file_path}: {str(e)}", err=True)

@app.command()
def version():
    """Show the version of the tool."""
    typer.echo("codex-docgen v1.0.0")
    typer.echo("AI-powered code documentation generator")

if __name__ == "__main__":
    app() 