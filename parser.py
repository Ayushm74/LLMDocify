"""
Code Parser Module
Extracts functions and classes from Python source code using AST.
"""

import ast
from typing import List, Dict, Any, Optional


def extract_functions(source_code: str) -> List[Dict[str, Any]]:
    """
    Extract all function definitions from Python source code.
    
    Args:
        source_code (str): The Python source code to parse
        
    Returns:
        List[Dict[str, Any]]: List of function information dictionaries
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get function arguments
            args = []
            for arg in node.args.args:
                args.append(arg.arg)
            
            # Get default values
            defaults = []
            if node.args.defaults:
                for default in node.args.defaults:
                    if isinstance(default, ast.Constant):
                        defaults.append(repr(default.value))
                    else:
                        defaults.append(ast.unparse(default))
            
            # Get keyword-only arguments
            kwonly_args = []
            if hasattr(node.args, 'kwonly'):
                for arg in node.args.kwonly:
                    kwonly_args.append(arg.arg)
            
            # Get function body source
            try:
                body_source = ast.get_source_segment(source_code, node)
            except (ValueError, TypeError):
                # Fallback to unparse if get_source_segment fails
                body_source = ast.unparse(node)
            
            function_info = {
                "name": node.name,
                "args": args,
                "defaults": defaults,
                "kwonly_args": kwonly_args,
                "docstring": ast.get_docstring(node),
                "body": body_source,
                "lineno": node.lineno,
                "end_lineno": getattr(node, 'end_lineno', None),
                "has_return": _has_return_statement(node),
                "is_async": isinstance(node, ast.AsyncFunctionDef)
            }
            
            functions.append(function_info)
    
    return functions


def extract_classes(source_code: str) -> List[Dict[str, Any]]:
    """
    Extract all class definitions from Python source code.
    
    Args:
        source_code (str): The Python source code to parse
        
    Returns:
        List[Dict[str, Any]]: List of class information dictionaries
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Get base classes
            bases = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                else:
                    bases.append(ast.unparse(base))
            
            # Get class methods
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({
                        "name": item.name,
                        "is_async": isinstance(item, ast.AsyncFunctionDef),
                        "docstring": ast.get_docstring(item)
                    })
            
            # Get class body source
            try:
                body_source = ast.get_source_segment(source_code, node)
            except (ValueError, TypeError):
                # Fallback to unparse if get_source_segment fails
                body_source = ast.unparse(node)
            
            class_info = {
                "name": node.name,
                "bases": bases,
                "methods": methods,
                "docstring": ast.get_docstring(node),
                "body": body_source,
                "lineno": node.lineno,
                "end_lineno": getattr(node, 'end_lineno', None),
                "method_count": len(methods)
            }
            
            classes.append(class_info)
    
    return classes


def extract_imports(source_code: str) -> List[Dict[str, Any]]:
    """
    Extract all import statements from Python source code.
    
    Args:
        source_code (str): The Python source code to parse
        
    Returns:
        List[Dict[str, Any]]: List of import information dictionaries
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "type": "import",
                    "module": alias.name,
                    "asname": alias.asname,
                    "lineno": node.lineno
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append({
                    "type": "from_import",
                    "module": module,
                    "name": alias.name,
                    "asname": alias.asname,
                    "lineno": node.lineno
                })
    
    return imports


def get_function_signature(function_info: Dict[str, Any]) -> str:
    """
    Generate a function signature string from function information.
    
    Args:
        function_info (Dict[str, Any]): Function information dictionary
        
    Returns:
        str: Formatted function signature
    """
    name = function_info["name"]
    args = function_info["args"]
    defaults = function_info["defaults"]
    kwonly_args = function_info["kwonly_args"]
    
    # Build argument string
    arg_parts = []
    
    # Regular arguments
    for i, arg in enumerate(args):
        if i >= len(args) - len(defaults):
            default_idx = i - (len(args) - len(defaults))
            arg_parts.append(f"{arg}={defaults[default_idx]}")
        else:
            arg_parts.append(arg)
    
    # Keyword-only arguments
    if kwonly_args:
        arg_parts.append("*")
        for arg in kwonly_args:
            arg_parts.append(arg)
    
    signature = f"{name}({', '.join(arg_parts)})"
    
    if function_info["is_async"]:
        signature = f"async {signature}"
    
    return signature


def _has_return_statement(node: ast.FunctionDef) -> bool:
    """
    Check if a function has a return statement.
    
    Args:
        node (ast.FunctionDef): The function node to check
        
    Returns:
        bool: True if the function has a return statement
    """
    for child in ast.walk(node):
        if isinstance(child, ast.Return):
            return True
    return False


def analyze_code_complexity(source_code: str) -> Dict[str, Any]:
    """
    Analyze code complexity metrics.
    
    Args:
        source_code (str): The Python source code to analyze
        
    Returns:
        Dict[str, Any]: Complexity metrics
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}")
    
    metrics = {
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "lines": len(source_code.splitlines()),
        "characters": len(source_code)
    }
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            metrics["functions"] += 1
        elif isinstance(node, ast.ClassDef):
            metrics["classes"] += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            metrics["imports"] += 1
    
    return metrics 