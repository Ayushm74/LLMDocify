# 🌐 AI Code-to-Documentation Generator - Web Interface

A beautiful, modern web interface for the AI Code-to-Documentation Generator that makes it easy to generate professional documentation for your Python code.

## ✨ Features

- 🎨 **Modern UI**: Beautiful, responsive design with gradient backgrounds and glassmorphism effects
- 📝 **Real-time Analysis**: Instantly analyze your code and see functions/classes
- 🎯 **Selective Generation**: Choose which functions/classes to document
- 🔄 **Multiple AI Providers**: Support for DeepSeek, OpenAI, and mock mode
- 📥 **Download Results**: Download generated documentation as Python files
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- 🚀 **Easy to Use**: No installation required, just run and open in browser

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Server
```bash
python run_web.py
```

### 3. Open Your Browser
Navigate to: **http://localhost:5000**

## 🎯 How to Use

### Step 1: Input Your Code
- Paste your Python code into the text area
- Or click one of the example buttons (Fibonacci, Calculator, Data Processor)

### Step 2: Choose AI Provider
- **Mock (Demo)**: Try the tool without an API key
- **DeepSeek**: Use DeepSeek AI models (requires API key)
- **OpenAI**: Use OpenAI GPT models (requires API key)

### Step 3: Analyze Code
- Click "Analyze Code" to see all functions and classes
- The tool will automatically detect and list all code elements

### Step 4: Select Items
- Check the boxes for functions/classes you want to document
- Use "Select All" or "Deselect All" for bulk operations

### Step 5: Generate Documentation
- Click "Generate Documentation" to create docstrings
- View the results in the generated documentation section
- Download the results as a Python file

## 🎨 Interface Features

### Code Input
- Syntax-highlighted code editor
- Dark theme for better readability
- Auto-resizing text area

### Analysis Results
- Visual progress indicators
- Function and class categorization
- Argument and method count display

### Generated Documentation
- Syntax-highlighted docstrings
- Organized by function/class type
- Easy copy/paste functionality

### Download Options
- Custom filename support
- Complete code with documentation
- Ready-to-use Python files

## 🔧 Configuration

### Environment Variables
```bash
# For DeepSeek
export DEEPSEEK_API_KEY="your_api_key_here"

# For OpenAI
export OPENAI_API_KEY="your_api_key_here"
```

### API Key Setup
1. Get an API key from [DeepSeek Platform](https://platform.deepseek.com/) or [OpenAI](https://platform.openai.com/api-keys)
2. Enter the key in the web interface (stored locally only)
3. Select your preferred provider

## 📁 Project Structure

```
web-interface/
├── app.py                 # Flask web application
├── run_web.py            # Startup script
├── templates/
│   ├── index.html        # Main interface
│   └── examples.html     # Examples page
├── parser.py             # Code parsing logic
├── generator.py          # AI generation logic
└── requirements.txt      # Dependencies
```

## 🎯 Example Usage

### 1. Basic Function Documentation
```python
def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
```

**Generated Docstring:**
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

### 2. Class Documentation
```python
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
```

**Generated Docstring:**
```python
class Calculator:
    """A simple calculator class for basic arithmetic operations.
    
    This class provides methods for addition, subtraction, multiplication,
    and division with operation history tracking.
    
    Attributes:
        history (List[str]): List of performed operations as strings.
        
    Methods:
        add(a, b): Add two numbers and record the operation.
        subtract(a, b): Subtract b from a and record the operation.
        multiply(a, b): Multiply two numbers and record the operation.
        divide(a, b): Divide a by b and record the operation.
        get_history(): Get a copy of the operation history.
        clear_history(): Clear the operation history.
    """
```

## 🔧 Development

### Running in Development Mode
```bash
# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the application
python app.py
```

### Customizing the Interface
- Edit `templates/index.html` for main interface changes
- Modify `templates/examples.html` for examples page
- Update `app.py` for backend logic changes

### Adding New Features
1. Add new routes in `app.py`
2. Create corresponding templates
3. Update JavaScript in templates for frontend functionality

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check if Flask is installed
pip install flask>=2.3.0

# Check if all files exist
ls app.py parser.py generator.py templates/
```

**API key issues:**
- Ensure your API key is valid and has proper permissions
- Check the provider selection (DeepSeek vs OpenAI)
- Try mock mode first to test functionality

**Code analysis fails:**
- Ensure your Python code is syntactically correct
- Check for proper indentation
- Verify function/class definitions are complete

### Error Messages

- **"No code provided"**: Enter some Python code in the text area
- **"Invalid provider"**: Select a valid AI provider (Mock, DeepSeek, or OpenAI)
- **"API request failed"**: Check your API key and internet connection

## 🚀 Deployment

### Local Development
```bash
python run_web.py
```

### Production Deployment
```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t code-doc-generator .
docker run -p 5000:5000 code-doc-generator
```

### Environment Variables
```bash
# Production settings
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY=your-secret-key-here
```

## 📊 Performance

### Optimization Tips
- Use mock mode for testing (no API calls)
- Limit code size for faster analysis
- Use selective generation for large codebases
- Enable caching for repeated requests

### Resource Usage
- **Memory**: ~50MB for basic usage
- **CPU**: Minimal for code analysis
- **Network**: API calls to AI providers

## 🤝 Contributing

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Reporting Issues
- Include error messages
- Describe steps to reproduce
- Specify your environment (OS, Python version, etc.)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components
- [Font Awesome](https://fontawesome.com/) for the icons
- [Prism.js](https://prismjs.com/) for syntax highlighting

---

**🎉 Happy coding! Transform your Python code into beautiful documentation with the power of AI!** 