import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Dict
from tools.analysis.code_analyzer import extract_code_blocks, analyze_code_complexity
from tools.analysis.hypothesis_extractor import extract_hypotheses
from utils.llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate


class AnalysisAgent:
    """Agent that analyzes paper content"""
    
    def __init__(self):
        self.name = "Analysis Agent"
        self.llm = get_llm(temperature=0.3)
    
    def analyze_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        Analyze multiple papers
        
        Args:
            papers: List of paper dictionaries with full_text
            
        Returns:
            List of analysis results
        """
        print("\n" + "="*60)
        print(f"🔬 {self.name} ACTIVATED")
        print("="*60)
        print(f"Analyzing {len(papers)} papers\n")
        
        analyses = []
        
        for i, paper in enumerate(papers, 1):
            print(f"\n[{i}/{len(papers)}] Analyzing: {paper['title'][:60]}...")
            
            analysis = self.analyze_single_paper(paper)
            analyses.append(analysis)
        
        print("\n" + "="*60)
        print(f"✅ ANALYSIS COMPLETE: {len(analyses)} papers analyzed")
        print("="*60 + "\n")
        
        return analyses
    
    def analyze_single_paper(self, paper: Dict) -> Dict:
        """Analyze a single paper"""
        
        result = {
            'title': paper['title'],
            'hypotheses': [],
            'code_blocks': [],
            'key_findings': "",
            'methodology': "",
            'statistics': {}
        }
        
        # Extract hypotheses
        print("   🔬 Extracting hypotheses...")
        result['hypotheses'] = extract_hypotheses(
            paper.get('abstract', ''),
            paper.get('full_text', '')[:5000]
        )
        
        # Extract code
        print("   💻 Extracting code blocks...")
        result['code_blocks'] = extract_code_blocks(paper.get('full_text', ''))
        
        # Analyze code complexity
        if result['code_blocks']:
            total_lines = sum(block.line_count for block in result['code_blocks'])
            result['statistics']['total_code_lines'] = total_lines
            result['statistics']['code_blocks_count'] = len(result['code_blocks'])
        
        # Extract key findings using LLM
        print("   📊 Extracting key findings...")
        result['key_findings'] = self._extract_key_findings(
            paper.get('abstract', ''),
            paper.get('full_text', '')[:3000]
        )
        
        # Extract methodology
        print("   🔧 Extracting methodology...")
        result['methodology'] = self._extract_methodology(
            paper.get('full_text', '')[:3000]
        )
        
        print(f"   ✅ Analysis complete!")
        
        return result
    
    def _extract_key_findings(self, abstract: str, text: str) -> str:
        """Extract key findings using LLM"""
        
        prompt = ChatPromptTemplate.from_template(
            """Summarize the key findings from this research paper in 3-4 bullet points.

Abstract: {abstract}

Content: {text}

Key Findings:"""
        )
        
        try:
            response = self.llm.invoke(prompt.format(abstract=abstract, text=text))
            return response.content
        except:
            return "Unable to extract key findings"
    
    def _extract_methodology(self, text: str) -> str:
        """Extract methodology using LLM"""
        
        prompt = ChatPromptTemplate.from_template(
            """Describe the research methodology used in this paper (2-3 sentences).

Content: {text}

Methodology:"""
        )
        
        try:
            response = self.llm.invoke(prompt.format(text=text))
            return response.content
        except:
            return "Unable to extract methodology"


if __name__ == "__main__":
    # Test with sample paper
    sample_paper = {
        'title': "Deep Learning for Medical Diagnosis",
        'abstract': "We propose a novel CNN architecture for X-ray diagnosis with 95% accuracy.",
        'full_text': """
        We hypothesize that deep learning can improve diagnosis.
```python
        def train_model(X, y):
            model = CNN(layers=10)
            model.fit(X, y)
            return model
```
        
        Our results show 95% accuracy on the test set.
        """
    }
    
    agent = AnalysisAgent()
    analysis = agent.analyze_single_paper(sample_paper)
    
    print(f"\n📊 Analysis Results:")
    print(f"Hypotheses found: {len(analysis['hypotheses'])}")
    print(f"Code blocks found: {len(analysis['code_blocks'])}")
    print(f"Key findings: {analysis['key_findings'][:200]}...")