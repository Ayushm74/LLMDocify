"""
AI Documentation Generator Module
Connects to LLM APIs to generate high-quality docstrings for Python code.
"""

import requests
import json
import os
from typing import Dict, Any, Optional
import time

try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    _openai_available = False


class LLMGenerator:
    """Base class for LLM-based documentation generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set DEEPSEEK_API_KEY or HUGGINGFACE_API_KEY environment variable or pass api_key parameter.")
    
    def generate(self, prompt: str) -> str:
        """Generate text using the LLM."""
        raise NotImplementedError("Subclasses must implement generate method")


class MockGenerator(LLMGenerator):
    """Mock generator for demonstration purposes."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Don't require API key for mock generator
        self.api_key = api_key or "mock-key"
    
    def generate(self, prompt: str) -> str:
        # ... your mock implementation unchanged ...
        pass  # Keep your existing mock generate code here


class DeepSeekGenerator(LLMGenerator):
    """DeepSeek model implementation for documentation generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat"):
        super().__init__(api_key)
        self.model = model
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def generate(self, prompt: str, max_retries: int = 3) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional Python developer who writes excellent docstrings."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 100
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                elif response.status_code == 503 and attempt < max_retries - 1:
                    time.sleep(10)
                else:
                    response.raise_for_status()
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise Exception(f"API request failed: {str(e)}")
        return ""


class OpenAIGenerator(LLMGenerator):
    """OpenAI model implementation for documentation generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key)
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional Python developer who writes excellent docstrings."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API request failed: {str(e)}")


class OpenRouterGenerator(LLMGenerator):
    """OpenRouter (DeepSeek via OpenAI client) provider with optional proxy support."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek/deepseek-r1:free", proxies: Optional[Dict[str, str]] = None):
        if not _openai_available:
            raise ImportError("openai package is required for OpenRouter integration. Run 'pip install openai'.")
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or \
                       "sk-or-v1-xxe8963f3d8b8af23b5a9d756596425a6fef23aacade3eea3f235c769bxxxxxx"
        self.model = model
        
        # Proxy support: environment variables or passed proxies dict
        self._proxies = proxies or {}
        # Note: openai.OpenAI client does not support proxies param directly.
        # Instead, set environment vars HTTP_PROXY/HTTPS_PROXY before launching Python process.
        if self._proxies:
            # Set environment variables dynamically for proxies if passed
            if "http" in self._proxies:
                os.environ["HTTP_PROXY"] = self._proxies["http"]
            if "https" in self._proxies:
                os.environ["HTTPS_PROXY"] = self._proxies["https"]
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

    def generate(self, prompt: str, max_retries: int = 3) -> str:
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    extra_headers={
                        "HTTP-Referer": "https://yourdomain.com",  # Optional
                        "X-Title": "MyAIApp",                      # Optional
                    }
                )
                return completion.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return f"# Error generating docstring via OpenRouter: {str(e)}\n# Please add documentation manually."


# Rest of your existing functions remain unchanged
# ...


        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    if attempt < max_retries - 1:
                        time.sleep(10)
                        continue
                    else:
                        raise Exception("Model is not ready after multiple attempts")
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise Exception(f"API request failed: {str(e)}")
        
        return ""


class OpenAIGenerator(LLMGenerator):
    """OpenAI model implementation for documentation generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key)
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str) -> str:
        """
        Generate documentation using OpenAI model.
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            str: Generated documentation text
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional Python developer who writes excellent docstrings."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API request failed: {str(e)}")


class OpenRouterGenerator(LLMGenerator):
    """OpenRouter (DeepSeek via OpenAI client) provider."""
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek/deepseek-r1:free"):
        if not _openai_available:
            raise ImportError("openai package is required for OpenRouter integration. Run 'pip install openai'.")
        # Hardcoded OpenRouter API key and base_url
        self.api_key = "sk-or-v1-xxe8963f3d8b8af23b5a9d756596425a6fef23aacade3eea3f235c769bxxxxxx"
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

    def generate(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                extra_headers={
                    "HTTP-Referer": "https://yourdomain.com",  # Optional
                    "X-Title": "MyAIApp",                      # Optional
                }
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"# Error generating docstring via OpenRouter: {str(e)}\n# Please add documentation manually."


def load_prompt_template(template_name: str) -> str:
    """
    Load a prompt template from the prompts directory.
    
    Args:
        template_name (str): Name of the template file
        
    Returns:
        str: The prompt template content
    """
    template_path = os.path.join("prompts", f"{template_name}.txt")
    
    if not os.path.exists(template_path):
        # Return default template if file doesn't exist
        return DEFAULT_FUNCTION_PROMPT
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load template {template_name}: {e}")
        return DEFAULT_FUNCTION_PROMPT


# Default prompt templates
DEFAULT_FUNCTION_PROMPT = """ "You are an expert Python developer and code reviewer.\n\n"
    "Your task is to analyze the following Python function or class and return a structured response containing:\n\n"
    "1. A complete, high-quality Python docstring following PEP-257 standards:\n"
    "   - Use triple double quotes (\"\"\").\n"
    "   - Start with a clear, concise summary of what the function/class does.\n"
    "   - Document all parameters (with types if obvious).\n"
    "   - Describe the return value (type and meaning).\n"
    "   - Mention raised exceptions if any.\n\n"
    "2. Time and space complexity of the function/method (in Big-O notation).\n\n"
    "3. Scope for improvement (if any):\n"
    "   - Suggest optimizations or cleaner implementation ideas.\n"
    "   - Highlight redundant logic or design flaws.\n\n"
    "4. Edge cases or limitations (if applicable).\n\n"
    "Here is the code snippet to analyze:\n\n"
    f"{code_snippet}\n\n"
    "Return only the analysis and docstring. Do NOT include the original code."""""

DEFAULT_CLASS_PROMPT = """ "You are an expert Python developer and code reviewer.\n\n"
    "Your task is to analyze the following Python function or class and return a structured response containing:\n\n"
    "1. A complete, high-quality Python docstring following PEP-257 standards:\n"
    "   - Use triple double quotes (\"\"\").\n"
    "   - Start with a clear, concise summary of what the function/class does.\n"
    "   - Document all parameters (with types if obvious).\n"
    "   - Describe the return value (type and meaning).\n"
    "   - Mention raised exceptions if any.\n\n"
    "2. Time and space complexity of the function/method (in Big-O notation).\n\n"
    "3. Scope for improvement (if any):\n"
    "   - Suggest optimizations or cleaner implementation ideas.\n"
    "   - Highlight redundant logic or design flaws.\n\n"
    "4. Edge cases or limitations (if applicable).\n\n"
    "Here is the code snippet to analyze:\n\n"
    f"{code_snippet}\n\n"
    "Return only the analysis and docstring. Do NOT include the original code."""


def generate_docstring(function_code: str, generator: Optional[LLMGenerator] = None, provider: Optional[str] = None, api_key: Optional[str] = None) -> str:
    """
    Generate a docstring for a Python function.
    
    Args:
        function_code (str): The function code to document
        generator (LLMGenerator, optional): The LLM generator to use
        
    Returns:
        str: Generated docstring
    """
    if generator is None:
        # Try to use provider if specified
        if provider == "openrouter":
            generator = OpenRouterGenerator(api_key)
        elif provider == "deepseek":
            generator = DeepSeekGenerator(api_key)
        elif provider == "openai":
            generator = OpenAIGenerator(api_key)
        else:
            # Fallback order: DeepSeek, OpenAI, Mock
            try:
                generator = DeepSeekGenerator()
            except ValueError:
                try:
                    generator = OpenAIGenerator()
                except ValueError:
                    generator = MockGenerator()
    
    prompt_template = load_prompt_template("function_prompt")
    prompt = prompt_template.replace("{function_code}", function_code)
    
    try:
        result = generator.generate(prompt)
        return result.strip()
    except Exception as e:
        return f"# Error generating docstring: {str(e)}\n# Please add documentation manually."


def generate_class_docstring(class_code: str, generator: Optional[LLMGenerator] = None, provider: Optional[str] = None, api_key: Optional[str] = None) -> str:
    """
    Generate a docstring for a Python class.
    
    Args:
        class_code (str): The class code to document
        generator (LLMGenerator, optional): The LLM generator to use
        
    Returns:
        str: Generated docstring
    """
    if generator is None:
        if provider == "openrouter":
            generator = OpenRouterGenerator(api_key)
        elif provider == "deepseek":
            generator = DeepSeekGenerator(api_key)
        elif provider == "openai":
            generator = OpenAIGenerator(api_key)
        else:
            try:
                generator = DeepSeekGenerator()
            except ValueError:
                try:
                    generator = OpenAIGenerator()
                except ValueError:
                    generator = MockGenerator()
    
    prompt_template = load_prompt_template("class_prompt")
    prompt = prompt_template.replace("{class_code}", class_code)
    
    try:
        result = generator.generate(prompt)
        return result.strip()
    except Exception as e:
        return f"# Error generating docstring: {str(e)}\n# Please add documentation manually."


def generate_readme_docstring(source_code: str, generator: Optional[LLMGenerator] = None) -> str:
    """
    Generate a README section based on source code.
    
    Args:
        source_code (str): The source code to analyze
        generator (LLMGenerator, optional): The LLM generator to use
        
    Returns:
        str: Generated README content
    """
    if generator is None:
        try:
            generator = DeepSeekGenerator()
        except ValueError:
            try:
                generator = OpenAIGenerator()
            except ValueError:
                generator = MockGenerator()
    
    prompt = f""" "You are an expert Python developer and code reviewer.\n\n"
    "Your task is to analyze the following Python function or class and return a structured response containing:\n\n"
    "1. A complete, high-quality Python docstring following PEP-257 standards:\n"
    "   - Use triple double quotes (\"\"\").\n"
    "   - Start with a clear, concise summary of what the function/class does.\n"
    "   - Document all parameters (with types if obvious).\n"
    "   - Describe the return value (type and meaning).\n"
    "   - Mention raised exceptions if any.\n\n"
    "2. Time and space complexity of the function/method (in Big-O notation).\n\n"
    "3. Scope for improvement (if any):\n"
    "   - Suggest optimizations or cleaner implementation ideas.\n"
    "   - Highlight redundant logic or design flaws.\n\n"
    "4. Edge cases or limitations (if applicable).\n\n"
    "Here is the code snippet to analyze:\n\n"
    f"{code_snippet}\n\n"
    "Return only the analysis and docstring. Do NOT include the original code."""
    
    try:
        result = generator.generate(prompt)
        return result.strip()
    except Exception as e:
        return f"# Error generating README: {str(e)}\n# Please write documentation manually."


def create_generator(provider: str = "deepseek", api_key: Optional[str] = None) -> LLMGenerator:
    """
    Create an LLM generator instance.
    
    Args:
        provider (str): The LLM provider to use ("deepseek", "openai", or "mock")
        api_key (str, optional): API key for the provider
        
    Returns:
        LLMGenerator: The generator instance
    """
    if provider.lower() == "deepseek":
        return DeepSeekGenerator(api_key)
    elif provider.lower() == "openai":
        return OpenAIGenerator(api_key)
    elif provider.lower() == "openrouter":
        return OpenRouterGenerator(api_key)
    elif provider.lower() == "mock":
        return MockGenerator(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}. Supported providers: deepseek, openai, openrouter, mock") 