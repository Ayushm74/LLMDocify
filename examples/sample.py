"""
Sample Python file for testing the AI documentation generator.
This file contains various functions and classes to demonstrate the tool's capabilities.
"""

import os
import json
from typing import List, Dict, Optional, Union
from datetime import datetime


def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


def process_data(data: List[Dict], filter_key: str = None, sort_by: str = None) -> List[Dict]:
    result = data.copy()
    
    if filter_key:
        result = [item for item in result if filter_key in item]
    
    if sort_by:
        result.sort(key=lambda x: x.get(sort_by, 0))
    
    return result


def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


async def fetch_api_data(url: str, headers: Optional[Dict] = None) -> Dict:
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


class DataProcessor:
    def __init__(self, config: Dict):
        self.config = config
        self.cache = {}
    
    def process_item(self, item: Dict) -> Dict:
        processed = item.copy()
        processed['processed_at'] = datetime.now().isoformat()
        return processed
    
    def batch_process(self, items: List[Dict]) -> List[Dict]:
        return [self.process_item(item) for item in items]


class FileManager:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.ensure_directory()
    
    def ensure_directory(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def save_data(self, filename: str, data: Union[Dict, List]) -> bool:
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self, filename: str) -> Optional[Union[Dict, List]]:
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None


class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def get_history(self) -> List[str]:
        return self.history.copy()
    
    def clear_history(self):
        self.history.clear()


def main():
    # Example usage
    calc = Calculator()
    print(calc.add(5, 3))
    print(calc.multiply(4, 7))
    print("History:", calc.get_history())


if __name__ == "__main__":
    main() 