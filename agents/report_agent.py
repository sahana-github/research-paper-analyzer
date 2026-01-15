import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Dict
from datetime import datetime
from utils.llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate
import json


class ReportAgent:
    """Agent that compiles comprehensive research reports"""
    
    def __init__(self):
        self.name = "Report Compiler Agent"
        self.llm = get_llm(temperature=0.5)
    
    def compile_report(
        self,
        query: str,
        discovery_results: Dict,
        analyses: List[Dict]
    ) -> Dict:
        """
        Compile final research report
        
        Args:
            query: Original research query
            discovery_results: Results from discovery agent
            analyses: Results from analysis agent
            
        Returns:
            Complete report dictionary
        """
        print("\n" + "="*60)
        print(f"📝 {self.name} ACTIVATED")
        print("="*60)
        print(f"Compiling report for: {query}\n")
        
        report = {
            'title': f"Research Analysis: {query}",
            'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'query': query,
            'executive_summary': "",
            'papers_analyzed': len(analyses),
            'total_papers_found': len(discovery_results.get('arxiv_papers', [])),
            'key_findings': [],
            'hypotheses_summary': [],
            'code_analysis': {},
            'methodology_overview': "",
            'conclusions': "",
            'recommendations': [],
            'paper_details': []
        }
        
        # Generate executive summary
        print("📋 Generating executive summary...")
        report['executive_summary'] = self._generate_executive_summary(query, analyses)
        
        # Aggregate key findings
        print("🔍 Aggregating key findings...")
        report['key_findings'] = self._aggregate_findings(analyses)
        
        # Summarize hypotheses
        print("🔬 Summarizing hypotheses...")
        report['hypotheses_summary'] = self._summarize_hypotheses(analyses)
        
        # Analyze code across papers
        print("💻 Analyzing code patterns...")
        report['code_analysis'] = self._analyze_code_patterns(analyses)
        
        # Generate conclusions
        print("📊 Generating conclusions...")
        report['conclusions'] = self._generate_conclusions(query, analyses)
        
        # Generate recommendations
        print("✅ Generating recommendations...")
        report['recommendations'] = self._generate_recommendations(query, analyses)
        
        # Add paper details
        report['paper_details'] = [
            {
                'title': a['title'],
                'hypotheses_count': len(a.get('hypotheses', [])),
                'code_blocks': len(a.get('code_blocks', [])),
                'key_findings': a.get('key_findings', '')[:200]
            }
            for a in analyses
        ]
        
        print("\n" + "="*60)
        print(f"✅ REPORT COMPLETE")
        print(f"   Papers analyzed: {report['papers_analyzed']}")
        print(f"   Total findings: {len(report['key_findings'])}")
        print(f"   Total hypotheses: {len(report['hypotheses_summary'])}")
        print("="*60 + "\n")
        
        return report
    
    def _generate_executive_summary(self, query: str, analyses: List[Dict]) -> str:
        """Generate executive summary"""
        
        # Gather key info
        total_hypotheses = sum(len(a.get('hypotheses', [])) for a in analyses)
        total_code = sum(len(a.get('code_blocks', [])) for a in analyses)
        
        context = f"""
        Query: {query}
        Papers analyzed: {len(analyses)}
        Total hypotheses identified: {total_hypotheses}
        Total code blocks found: {total_code}
        
        Sample findings from papers:
        {chr(10).join([a.get('key_findings', '')[:200] for a in analyses[:3]])}
        """
        
        prompt = ChatPromptTemplate.from_template(
            """Create an executive summary (3-4 paragraphs) for this research analysis:

{context}

Executive Summary:"""
        )
        
        try:
            response = self.llm.invoke(prompt.format(context=context))
            return response.content
        except:
            return f"Analysis of {len(analyses)} research papers on {query}."
    
    def _aggregate_findings(self, analyses: List[Dict]) -> List[str]:
        """Aggregate key findings from all papers"""
        
        findings = []
        for analysis in analyses:
            if analysis.get('key_findings'):
                findings.append(f"[{analysis['title'][:50]}...] {analysis['key_findings'][:200]}")
        
        return findings[:10]  # Top 10
    
    def _summarize_hypotheses(self, analyses: List[Dict]) -> List[Dict]:
        """Summarize all hypotheses"""
        
        all_hypotheses = []
        for analysis in analyses:
            for hyp in analysis.get('hypotheses', []):
                all_hypotheses.append({
                    'paper': analysis['title'][:50],
                    'hypothesis': hyp.statement,
                    'evidence': hyp.supporting_evidence[:100]
                })
        
        return all_hypotheses[:15]  # Top 15
    
    def _analyze_code_patterns(self, analyses: List[Dict]) -> Dict:
        """Analyze code patterns across papers"""
        
        total_code = sum(len(a.get('code_blocks', [])) for a in analyses)
        total_lines = sum(
            sum(block.line_count for block in a.get('code_blocks', []))
            for a in analyses
        )
        
        languages = {}
        for analysis in analyses:
            for block in analysis.get('code_blocks', []):
                lang = block.language
                languages[lang] = languages.get(lang, 0) + 1
        
        return {
            'total_code_blocks': total_code,
            'total_lines': total_lines,
            'languages_used': languages,
            'average_lines_per_block': total_lines / total_code if total_code > 0 else 0
        }
    
    def _generate_conclusions(self, query: str, analyses: List[Dict]) -> str:
        """Generate conclusions"""
        
        findings_summary = "\n".join([
            f"- {a.get('key_findings', '')[:150]}"
            for a in analyses[:5]
        ])
        
        prompt = ChatPromptTemplate.from_template(
            """Based on this research analysis, provide 3-4 key conclusions:

Query: {query}

Key findings from papers:
{findings}

Conclusions:"""
        )
        
        try:
            response = self.llm.invoke(prompt.format(query=query, findings=findings_summary))
            return response.content
        except:
            return f"Analysis suggests significant research activity in {query}."
    
    def _generate_recommendations(self, query: str, analyses: List[Dict]) -> List[str]:
        """Generate recommendations"""
        
        prompt = ChatPromptTemplate.from_template(
            """Based on this research analysis, provide 3-5 actionable recommendations for future research:

Query: {query}
Papers analyzed: {count}

Recommendations:"""
        )
        
        try:
            response = self.llm.invoke(prompt.format(query=query, count=len(analyses)))
            recs = [line.strip() for line in response.content.split('\n') if line.strip()]
            return recs[:5]
        except:
            return ["Continue monitoring research in this area"]
    
    def save_report_markdown(self, report: Dict, filename: str = "research_report.md"):
        """Save report as markdown file"""
        
        md_content = f"""# {report['title']}

**Generated:** {report['generated_date']}  
**Query:** {report['query']}  
**Papers Analyzed:** {report['papers_analyzed']} / {report['total_papers_found']} found

---

## Executive Summary

{report['executive_summary']}

---

## Key Findings

{chr(10).join([f"{i+1}. {finding}" for i, finding in enumerate(report['key_findings'])])}

---

## Research Hypotheses

{chr(10).join([f"**{h['paper']}**\n- {h['hypothesis']}\n- Evidence: {h['evidence']}\n" for h in report['hypotheses_summary']])}

---

## Code Analysis

- **Total Code Blocks:** {report['code_analysis'].get('total_code_blocks', 0)}
- **Total Lines of Code:** {report['code_analysis'].get('total_lines', 0)}
- **Languages Used:** {', '.join([f"{k} ({v})" for k, v in report['code_analysis'].get('languages_used', {}).items()])}

---

## Conclusions

{report['conclusions']}

---

## Recommendations

{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(report['recommendations'])])}

---

## Paper Details

{chr(10).join([f"### {p['title']}\n- Hypotheses: {p['hypotheses_count']}\n- Code Blocks: {p['code_blocks']}\n- Key Finding: {p['key_findings']}\n" for p in report['paper_details']])}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"💾 Report saved to: {filename}")


if __name__ == "__main__":
    # Test with sample data
    sample_analyses = [
        {
            'title': "Deep Learning in Healthcare",
            'hypotheses': [{'statement': 'AI improves diagnosis', 'supporting_evidence': 'Test data', 'methodology': 'CNN', 'results': '95% accuracy'}],
            'code_blocks': [{'language': 'python', 'code': 'model.fit()', 'line_count': 5}],
            'key_findings': "Deep learning shows 95% accuracy in medical imaging"
        }
    ]
    
    agent = ReportAgent()
    report = agent.compile_report(
        query="AI in healthcare",
        discovery_results={'arxiv_papers': [1, 2, 3]},
        analyses=sample_analyses
    )
    
    print(f"\n📊 Report Preview:")
    print(f"Title: {report['title']}")
    print(f"Executive Summary: {report['executive_summary'][:200]}...")
    
    agent.save_report_markdown(report, "test_report.md")