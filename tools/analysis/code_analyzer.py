import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import re
from typing import List, Dict
from pydantic import BaseModel


class CodeBlock(BaseModel):
    """Extracted code block"""
    language: str
    code: str
    line_count: int
    location: str


def extract_code_blocks(text: str) -> List[CodeBlock]:
    """
    Extract code blocks from paper text
    
    Args:
        text: Full paper text
        
    Returns:
        List of CodeBlock objects
    """
    print("💻 Extracting code blocks...")
    
    blocks = []
    
    # Pattern 1: Markdown code blocks
    markdown_pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(markdown_pattern, text, re.DOTALL)
    
    for lang, code in matches:
        if len(code.strip()) > 20:
            blocks.append(CodeBlock(
                language=lang or "python",
                code=code.strip(),
                line_count=len(code.strip().split('\n')),
                location="markdown"
            ))
    
    # Pattern 2: Python-style indented code
    python_pattern = r'\n((?:    |\t)[^\n]+(?:\n(?:    |\t)[^\n]+)*)'
    py_matches = re.findall(python_pattern, text)
    
    for code in py_matches:
        if len(code.strip()) > 50 and ('def ' in code or 'class ' in code):
            blocks.append(CodeBlock(
                language="python",
                code=code.strip(),
                line_count=len(code.strip().split('\n')),
                location="indented"
            ))
    
    print(f"✅ Found {len(blocks)} code blocks")
    return blocks


def analyze_code_complexity(code: str) -> Dict[str, int]:
    """
    Analyze code complexity metrics
    
    Args:
        code: Code string
        
    Returns:
        Dictionary of metrics
    """
    metrics = {
        'lines': len(code.split('\n')),
        'functions': len(re.findall(r'\bdef\s+\w+', code)),
        'classes': len(re.findall(r'\bclass\s+\w+', code)),
        'imports': len(re.findall(r'\bimport\s+\w+', code)),
        'loops': len(re.findall(r'\b(for|while)\s+', code)),
        'conditionals': len(re.findall(r'\b(if|elif)\s+', code))
    }
    
    return metrics


if __name__ == "__main__":
    sample_text = """
    Here's our implementation:
```python
    def train_model(X, y):
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)
        return model
    
    class DataProcessor:
        def __init__(self):
            self.scaler = StandardScaler()
```
    """
    
    blocks = extract_code_blocks(sample_text)
    
    for i, block in enumerate(blocks, 1):
        print(f"\n--- Code Block {i} ---")
        print(f"Language: {block.language}")
        print(f"Lines: {block.line_count}")
        print(f"Code:\n{block.code[:200]}...")
        
        metrics = analyze_code_complexity(block.code)
        print(f"Metrics: {metrics}")