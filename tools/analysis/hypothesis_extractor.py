import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from typing import List
from pydantic import BaseModel
from utils.llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate


class Hypothesis(BaseModel):
    """Research hypothesis"""
    statement: str
    supporting_evidence: str
    methodology: str
    results: str


def extract_hypotheses(abstract: str, full_text: str = "") -> List[Hypothesis]:
    """
    Extract research hypotheses using LLM
    
    Args:
        abstract: Paper abstract
        full_text: Full paper text (optional, first 3000 chars used)
        
    Returns:
        List of Hypothesis objects
    """
    print("🔬 Extracting hypotheses...")
    
    llm = get_llm(temperature=0.2)
    
    content = f"ABSTRACT:\n{abstract}\n\nCONTENT:\n{full_text[:3000]}"
    
    prompt = ChatPromptTemplate.from_template(
        """Analyze this research paper and extract the main hypotheses.

{content}

For each hypothesis, identify:
1. The hypothesis statement (what they claim)
2. Supporting evidence mentioned
3. Methodology used to test it
4. Key results/findings

Format each as:
HYPOTHESIS: [clear statement]
EVIDENCE: [supporting data]
METHODOLOGY: [how tested]
RESULTS: [key findings]
---

Extract 2-3 main hypotheses."""
    )
    
    try:
        response = llm.invoke(prompt.format(content=content))
        
        hypotheses = []
        sections = response.content.split('---')
        
        for section in sections:
            if 'HYPOTHESIS:' in section:
                lines = section.strip().split('\n')
                hyp_data = {}
                
                for line in lines:
                    if 'HYPOTHESIS:' in line:
                        hyp_data['statement'] = line.split('HYPOTHESIS:')[1].strip()
                    elif 'EVIDENCE:' in line:
                        hyp_data['supporting_evidence'] = line.split('EVIDENCE:')[1].strip()
                    elif 'METHODOLOGY:' in line:
                        hyp_data['methodology'] = line.split('METHODOLOGY:')[1].strip()
                    elif 'RESULTS:' in line:
                        hyp_data['results'] = line.split('RESULTS:')[1].strip()
                
                if 'statement' in hyp_data:
                    hypotheses.append(Hypothesis(
                        statement=hyp_data.get('statement', ''),
                        supporting_evidence=hyp_data.get('supporting_evidence', 'Not specified'),
                        methodology=hyp_data.get('methodology', 'Not specified'),
                        results=hyp_data.get('results', 'Not specified')
                    ))
        
        print(f"✅ Extracted {len(hypotheses)} hypotheses")
        return hypotheses
        
    except Exception as e:
        print(f"⚠️ Extraction error: {e}")
        return []


if __name__ == "__main__":
    sample_abstract = """
    We hypothesize that deep learning models can improve diagnostic accuracy 
    in medical imaging by 30% compared to traditional methods. We tested this 
    using a dataset of 10,000 X-ray images with CNN architecture. Results 
    showed 92% accuracy vs 70% for traditional methods.
    """
    
    hypotheses = extract_hypotheses(sample_abstract)
    
    for i, hyp in enumerate(hypotheses, 1):
        print(f"\n--- Hypothesis {i} ---")
        print(f"Statement: {hyp.statement}")
        print(f"Evidence: {hyp.supporting_evidence}")
        print(f"Method: {hyp.methodology}")
        print(f"Results: {hyp.results}")