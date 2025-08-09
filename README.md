# 🤖 AI Code-to-Documentation Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> **Transform your Python code into professional documentation using AI**

An intelligent command-line tool that automatically generates high-quality docstrings for Python functions and classes using state-of-the-art language models (DeepSeek, OpenAI). Perfect for developers who want to maintain clean, well-documented code without the manual effort.

## ✨ Features

- 🧠 **AI-Powered**: Uses DeepSeek V3 or OpenAI models for intelligent documentation generation
- 📝 **Comprehensive**: Generates docstrings for both functions and classes
- 🚀 **CLI Interface**: Easy-to-use command-line tool with rich options
- 🔄 **Git Integration**: Optional pre-commit hooks for automatic documentation
- 📊 **Batch Processing**: Process entire directories of Python files
- 🎯 **Smart Parsing**: Extracts function signatures, arguments, and return types
- 📋 **Multiple Formats**: Supports Google-style docstrings with type hints
- ⚡ **Fast & Efficient**: Optimized for speed with retry mechanisms

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- API key from [HuggingFace](https://huggingface.co/settings/tokens) or [OpenAI](https://platform.openai.com/api-keys)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/codex-docgen.git
   cd codex-docgen
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   # For DeepSeek (recommended)
   export DEEPSEEK_API_KEY="your_deepseek_api_key"
   
   # Or for OpenAI
   export OPENAI_API_KEY="your_openai_api_key"
   ```

4. **Test the installation**
   ```bash
   python main.py version
   ```

## 🚀 Usage

### Basic Usage

Generate documentation for a single file:
```bash
python main.py docgen examples/sample.py
```

### Advanced Options

```bash
# Generate with verbose output
python main.py docgen examples/sample.py --verbose

# Save results to a file
python main.py docgen examples/sample.py --output documented_sample.py

# Process only functions (skip classes)
python main.py docgen examples/sample.py --functions-only

# Process only classes (skip functions)
python main.py docgen examples/sample.py --classes-only

# Process all Python files in a directory
python main.py batch ./src --recursive --verbose
```

### Git Integration

Set up pre-commit hooks for automatic documentation:
```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Now every commit will automatically generate documentation
git add .
git commit -m "Add new feature"
```

## 📁 Project Structure

```
codex-docgen/
├── main.py                 # CLI entry point
├── parser.py               # Code parsing logic
├── generator.py            # AI doc generation logic
├── prompts/
│   ├── function_prompt.txt # Function docstring prompts
│   └── class_prompt.txt    # Class docstring prompts
├── examples/
│   └── sample.py          # Sample input code
├── .pre-commit-config.yaml # Git hook integration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

- `DEEPSEEK_API_KEY`: Your DeepSeek API key (for DeepSeek models)
- `OPENAI_API_KEY`: Your OpenAI API key (for GPT models)

### Custom Prompts

You can customize the AI prompts by editing the files in the `prompts/` directory:
- `prompts/function_prompt.txt`: Template for function docstrings
- `prompts/class_prompt.txt`: Template for class docstrings

## 📊 Example Output

### Input Function
```python
def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
```

### Generated Docstring
```python
def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed).
        
    Returns:
        int: The nth Fibonacci number.
        
    Examples:
        >>> calculate_fibonacci(0)
        0
        >>> calculate_fibonacci(1)
        1
        >>> calculate_fibonacci(10)
        55
    """
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
```

## 🎯 Supported Models

### DeepSeek (Recommended)
- **Model**: `deepseek-chat`
- **Pros**: Excellent code understanding, reliable API
- **Setup**: Get API key from [DeepSeek Platform](https://platform.deepseek.com/)

### OpenAI
- **Model**: `gpt-3.5-turbo` or `gpt-4`
- **Pros**: High quality, reliable
- **Setup**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## 🔄 API Reference

### CLI Commands

#### `docgen`
Generate documentation for a Python file.

```bash
python main.py docgen <file> [OPTIONS]
```

**Arguments:**
- `file`: Path to the Python file to process

**Options:**
- `--output, -o`: Output file path (optional)
- `--verbose, -v`: Enable verbose output
- `--functions-only`: Process only functions, skip classes
- `--classes-only`: Process only classes, skip functions

#### `batch`
Process all Python files in a directory.

```bash
python main.py batch <directory> [OPTIONS]
```

**Arguments:**
- `directory`: Directory containing Python files to process

**Options:**
- `--recursive, -r`: Process subdirectories recursively
- `--verbose, -v`: Enable verbose output

#### `version`
Show the version of the tool.

```bash
python main.py version
```

### Python API

```python
from parser import extract_functions, extract_classes
from generator import generate_docstring, generate_class_docstring

# Extract functions from source code
functions = extract_functions(source_code)

# Generate docstring for a function
docstring = generate_docstring(function_code)

# Extract classes from source code
classes = extract_classes(source_code)

# Generate docstring for a class
class_docstring = generate_class_docstring(class_code)
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [DeepSeek](https://www.deepseek.com/) for providing excellent code understanding models
- [OpenAI](https://openai.com/) for GPT models
- [HuggingFace](https://huggingface.co/) for model hosting and API
- [Typer](https://typer.tiangolo.com/) for the beautiful CLI framework

## 📈 Roadmap

- [ ] JavaScript/TypeScript support
- [ ] Java and C++ support
- [ ] IDE integration (VS Code extension)
- [ ] Local model support (Ollama integration)
- [ ] Documentation quality scoring
- [ ] Multi-language docstring generation
- [ ] Code explanation feature
- [ ] Automated testing integration

## 🐛 Known Issues

- Large files may hit API token limits
- Complex nested functions might not parse correctly
- Async functions with complex decorators may need manual review

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/codex-docgen/issues) page
2. Create a new issue with detailed information
3. Join our [Discord](https://discord.gg/your-server) for community support

---

**Made with ❤️ by the AI Code Documentation Team**

*Transform your code into beautiful documentation with the power of AI!* # LLMDocify
