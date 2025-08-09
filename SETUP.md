# 🚀 Quick Setup Guide

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Basic Functionality
```bash
python test_basic.py
```

### 3. Run Demo (Mock Mode)
```bash
python demo.py
```

### 4. Test with Your API Key

#### Option A: DeepSeek API
1. Get an API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. Set the environment variable:
   ```bash
   # Windows
   set DEEPSEEK_API_KEY=your_api_key_here
   
   # Linux/Mac
   export DEEPSEEK_API_KEY=your_api_key_here
   ```
3. Test with your API key:
   ```bash
   python test_with_api.py
   ```

#### Option B: OpenAI API
1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set the environment variable:
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

### 5. Use the Tool

#### Basic Usage
```bash
python main.py docgen examples/sample.py --verbose
```

#### Advanced Options
```bash
# Functions only
python main.py docgen examples/sample.py --functions-only

# Classes only
python main.py docgen examples/sample.py --classes-only

# Save output to file
python main.py docgen examples/sample.py --output documented_file.py

# Batch process directory
python main.py batch ./src --recursive --verbose
```

## Troubleshooting

### API Key Issues
- **401 Unauthorized**: Check your API key format and validity
- **403 Forbidden**: Ensure your API key has the correct permissions
- **Rate Limit**: Wait a few seconds between requests

### Installation Issues
- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Python Version**: Ensure you're using Python 3.8+

### Mock Mode
If you don't have an API key, the tool will automatically use mock mode for demonstration purposes.

## Project Structure
```
codex-docgen/
├── main.py                 # CLI entry point
├── parser.py               # Code parsing logic
├── generator.py            # AI doc generation logic
├── prompts/                # AI prompt templates
├── examples/               # Sample code for testing
├── test_basic.py          # Basic functionality tests
├── test_with_api.py       # API integration tests
├── demo.py                # Demonstration script
└── README.md              # Complete documentation
```

## Features Implemented

✅ **Core Functionality**
- Python code parsing using AST
- Function and class extraction
- CLI interface with Typer
- Multiple output formats

✅ **AI Integration**
- DeepSeek API support
- OpenAI API support
- Mock generator for demos
- Retry mechanisms and error handling

✅ **Advanced Features**
- Batch processing
- Git integration (pre-commit hooks)
- Customizable prompts
- Verbose output options

✅ **Documentation**
- Comprehensive README
- Example code
- Setup guides
- API documentation

## Next Steps

1. **Get a Real API Key**: Sign up for DeepSeek or OpenAI
2. **Test with Your Code**: Try the tool on your own Python files
3. **Customize Prompts**: Edit files in `prompts/` directory
4. **Set up Git Hooks**: Run `pre-commit install` for automatic docs
5. **Extend Functionality**: Add support for other languages

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `python test_basic.py` to verify core functionality
3. Check your API key format and permissions
4. Review the README.md for detailed documentation

---

**Happy coding! 🎉** 