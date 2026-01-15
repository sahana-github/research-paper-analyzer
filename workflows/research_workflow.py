import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from agents.discovery_agent import PaperDiscoveryAgent
from agents.scraping_agent import ScrapingAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent


class ResearchState(TypedDict):
    """State that flows through the workflow"""
    query: str
    max_papers: int
    discovery_results: Dict[str, Any]
    scraped_papers: List[Dict]
    analyses: List[Dict]
    final_report: Dict[str, Any]
    current_step: str
    progress: int


class ResearchPaperWorkflow:
    """Multi-agent workflow for research paper analysis"""
    
    def __init__(self):
        # Initialize all agents
        self.discovery_agent = PaperDiscoveryAgent()
        self.scraping_agent = ScrapingAgent()
        self.analysis_agent = AnalysisAgent()
        self.report_agent = ReportAgent()
        
        # Build workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        workflow = StateGraph(ResearchState)
        
        # Add nodes (each agent is a node)
        workflow.add_node("discover_papers", self.discover_papers_node)
        workflow.add_node("scrape_papers", self.scrape_papers_node)
        workflow.add_node("analyze_papers", self.analyze_papers_node)
        workflow.add_node("compile_report", self.compile_report_node)
        
        # Define the flow
        workflow.set_entry_point("discover_papers")
        workflow.add_edge("discover_papers", "scrape_papers")
        workflow.add_edge("scrape_papers", "analyze_papers")
        workflow.add_edge("analyze_papers", "compile_report")
        workflow.add_edge("compile_report", END)
        
        return workflow.compile()
    
    def discover_papers_node(self, state: ResearchState) -> ResearchState:
        """Node 1: Discover papers from multiple sources"""
        
        print("\n" + "🚀"*30)
        print("RESEARCH PAPER ANALYSIS WORKFLOW - STARTED")
        print("🚀"*30)
        
        results = self.discovery_agent.discover_papers(
            state["query"],
            max_papers=state["max_papers"]
        )
        
        state["discovery_results"] = results
        state["current_step"] = "discovery_complete"
        state["progress"] = 25
        
        return state
    
    def scrape_papers_node(self, state: ResearchState) -> ResearchState:
        """Node 2: Scrape and extract paper content"""
        
        arxiv_papers = state["discovery_results"].get("arxiv_papers", [])
        
        if not arxiv_papers:
            print("⚠️ No ArXiv papers found, skipping scraping...")
            state["scraped_papers"] = []
            state["current_step"] = "scraping_skipped"
            state["progress"] = 50
            return state
        
        # Limit to max papers for scraping
        max_to_scrape = min(len(arxiv_papers), state["max_papers"])
        
        scraped = self.scraping_agent.scrape_papers(
            arxiv_papers,
            max_papers=max_to_scrape
        )
        
        state["scraped_papers"] = scraped
        state["current_step"] = "scraping_complete"
        state["progress"] = 50
        
        return state
    
    def analyze_papers_node(self, state: ResearchState) -> ResearchState:
        """Node 3: Analyze paper content"""
        
        if not state["scraped_papers"]:
            print("⚠️ No papers to analyze, skipping analysis...")
            state["analyses"] = []
            state["current_step"] = "analysis_skipped"
            state["progress"] = 75
            return state
        
        analyses = self.analysis_agent.analyze_papers(state["scraped_papers"])
        
        state["analyses"] = analyses
        state["current_step"] = "analysis_complete"
        state["progress"] = 75
        
        return state
    
    def compile_report_node(self, state: ResearchState) -> ResearchState:
        """Node 4: Compile final report"""
        
        if not state["analyses"]:
            print("⚠️ No analyses available, creating basic report...")
            state["final_report"] = {
                'title': f"Research Analysis: {state['query']}",
                'executive_summary': "No papers were successfully analyzed.",
                'papers_analyzed': 0,
                'message': "Please try a different query or increase max_papers."
            }
        else:
            report = self.report_agent.compile_report(
                state["query"],
                state["discovery_results"],
                state["analyses"]
            )
            state["final_report"] = report
        
        state["current_step"] = "complete"
        state["progress"] = 100
        
        print("\n" + "✅"*30)
        print("RESEARCH WORKFLOW COMPLETE!")
        print("✅"*30 + "\n")
        
        return state
    
    def run(self, query: str, max_papers: int = 20) -> Dict[str, Any]:
        """
        Run the complete research workflow
        
        Args:
            query: Research query (e.g., "deep learning medical imaging")
            max_papers: Maximum papers to analyze
            
        Returns:
            Final state with complete report
        """
        
        # Initialize state
        initial_state = ResearchState(
            query=query,
            max_papers=max_papers,
            discovery_results={},
            scraped_papers=[],
            analyses=[],
            final_report={},
            current_step="started",
            progress=0
        )
        
        # Run workflow
        final_state = self.workflow.invoke(initial_state)
        
        return final_state


# Test the workflow
if __name__ == "__main__":
    workflow = ResearchPaperWorkflow()
    
    # Run with test query
    print("Testing Research Paper Workflow...")
    print("="*60)
    
    result = workflow.run(
        query="machine learning healthcare",
        max_papers=3  # Small number for testing
    )
    
    print("\n" + "="*60)
    print("FINAL RESULTS:")
    print("="*60)
    print(f"Query: {result['query']}")
    print(f"Papers Found: {len(result['discovery_results'].get('arxiv_papers', []))}")
    print(f"Papers Scraped: {len(result['scraped_papers'])}")
    print(f"Papers Analyzed: {len(result['analyses'])}")
    print(f"Report Generated: {bool(result['final_report'])}")
    print(f"Final Status: {result['current_step']}")
    
    if result['final_report']:
        print(f"\nReport Title: {result['final_report']['title']}")
        print(f"Executive Summary Preview:")
        print(result['final_report'].get('executive_summary', '')[:300] + "...")