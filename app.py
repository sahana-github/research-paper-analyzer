import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import streamlit as st
from workflows.research_workflow import ResearchPaperWorkflow
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Research Paper Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🔬 Research Paper Analyzer</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align: center; font-size: 1.2rem; color: #666;">Multi-Agent AI System for Automated Research Analysis</p>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    max_papers = st.slider(
        "Maximum Papers to Analyze",
        min_value=5,
        max_value=50,
        value=10,
        step=5,
        help="More papers = longer processing time"
    )
    
    st.markdown("---")
    
    st.header("🤖 Agent Pipeline")
    st.markdown("""
    **1. 🔍 Discovery Agent**  
    Searches ArXiv, Scholar, Web
    
    **2. 📥 Scraping Agent**  
    Downloads & extracts PDFs
    
    **3. 🔬 Analysis Agent**  
    Extracts hypotheses & code
    
    **4. 📝 Report Agent**  
    Compiles final report
    """)
    
    st.markdown("---")
    
    st.header("📊 Tools Used")
    st.markdown("""
    - ArXiv Search API
    - Google Scholar Scraper
    - DuckDuckGo Search
    - PDF Text Extractor
    - Code Analyzer
    - Hypothesis Extractor
    - LLM Analysis (Groq)
    """)
    
    st.markdown("---")
    
    st.info("💡 **Tip:** Start with 5-10 papers for faster results")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_input(
        "🔎 Enter Research Query",
        placeholder="e.g., deep learning medical imaging, natural language processing, quantum computing",
        help="Be specific for better results"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)

# Examples
with st.expander("💡 Example Queries"):
    st.markdown("""
    - `deep learning medical imaging`
    - `natural language processing transformers`
    - `reinforcement learning robotics`
    - `computer vision object detection`
    - `machine learning healthcare diagnosis`
    - `neural networks optimization`
    """)

# Main execution
if run_button and query:
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Metrics
    metrics_cols = st.columns(4)
    metric_papers_found = metrics_cols[0].empty()
    metric_papers_scraped = metrics_cols[1].empty()
    metric_papers_analyzed = metrics_cols[2].empty()
    metric_hypotheses = metrics_cols[3].empty()
    
    try:
        # Initialize workflow
        workflow = ResearchPaperWorkflow()
        
        # Create placeholder for intermediate results
        results_container = st.container()
        
        with results_container:
            # Step 1: Discovery
            status_text.markdown("### 🔍 Step 1/4: Discovering Papers...")
            progress_bar.progress(10)
            
            discovery_placeholder = st.empty()
            with discovery_placeholder.container():
                st.info("🔍 Searching ArXiv, Google Scholar, and Web sources...")
            
            # Step 2: Setup for scraping
            status_text.markdown("### 📥 Step 2/4: Preparing to Scrape Papers...")
            progress_bar.progress(30)
            
            # Run workflow
            with st.spinner("🤖 Multi-Agent System Processing..."):
                result = workflow.run(query=query, max_papers=max_papers)
            
            # Update metrics
            papers_found = len(result['discovery_results'].get('arxiv_papers', []))
            papers_scraped = len(result['scraped_papers'])
            papers_analyzed = len(result['analyses'])
            total_hypotheses = sum(len(a.get('hypotheses', [])) for a in result['analyses'])
            
            metric_papers_found.metric("📄 Papers Found", papers_found)
            metric_papers_scraped.metric("📥 Papers Scraped", papers_scraped)
            metric_papers_analyzed.metric("🔬 Papers Analyzed", papers_analyzed)
            metric_hypotheses.metric("💡 Hypotheses", total_hypotheses)
            
            # Clear intermediate messages
            discovery_placeholder.empty()
            
            # Update progress
            progress_bar.progress(100)
            status_text.markdown("### ✅ Analysis Complete!")
            
            st.success(f"🎉 Successfully analyzed {papers_analyzed} research papers!")
            
            # Display report
            if result['final_report']:
                report = result['final_report']
                
                st.markdown("---")
                st.markdown(f"## 📋 {report['title']}")
                st.caption(f"Generated: {report['generated_date']}")
                
                # Executive Summary
                with st.expander("📊 Executive Summary", expanded=True):
                    st.markdown(report.get('executive_summary', 'No summary available'))
                
                # Key Findings
                if report.get('key_findings'):
                    with st.expander("🔍 Key Findings", expanded=True):
                        for i, finding in enumerate(report['key_findings'], 1):
                            st.markdown(f"**{i}.** {finding}")
                
                # Hypotheses
                if report.get('hypotheses_summary'):
                    with st.expander(f"🔬 Research Hypotheses ({len(report['hypotheses_summary'])} found)"):
                        for hyp in report['hypotheses_summary']:
                            st.markdown(f"**Paper:** {hyp['paper']}")
                            st.markdown(f"**Hypothesis:** {hyp['hypothesis']}")
                            st.markdown(f"**Evidence:** {hyp['evidence']}")
                            st.markdown("---")
                
                # Code Analysis
                if report.get('code_analysis'):
                    code_data = report['code_analysis']
                    with st.expander("💻 Code Analysis"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Code Blocks", code_data.get('total_code_blocks', 0))
                        col2.metric("Total Lines", code_data.get('total_lines', 0))
                        col3.metric("Languages", len(code_data.get('languages_used', {})))
                        
                        if code_data.get('languages_used'):
                            st.markdown("**Languages Distribution:**")
                            for lang, count in code_data['languages_used'].items():
                                st.markdown(f"- **{lang}**: {count} blocks")
                
                # Conclusions
                with st.expander("📊 Conclusions"):
                    st.markdown(report.get('conclusions', 'No conclusions available'))
                
                # Recommendations
                if report.get('recommendations'):
                    with st.expander("✅ Recommendations"):
                        for i, rec in enumerate(report['recommendations'], 1):
                            st.markdown(f"**{i}.** {rec}")
                
                # Paper Details
                if report.get('paper_details'):
                    with st.expander(f"📚 Analyzed Papers ({len(report['paper_details'])})"):
                        for paper in report['paper_details']:
                            st.markdown(f"### {paper['title']}")
                            col1, col2 = st.columns(2)
                            col1.write(f"**Hypotheses:** {paper['hypotheses_count']}")
                            col2.write(f"**Code Blocks:** {paper['code_blocks']}")
                            st.write(f"**Key Finding:** {paper['key_findings']}")
                            st.markdown("---")
                
                # Download buttons
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download as JSON
                    json_str = json.dumps(report, indent=2)
                    st.download_button(
                        label="📥 Download Report (JSON)",
                        data=json_str,
                        file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Save as markdown
                    if st.button("💾 Save as Markdown"):
                        from agents.report_agent import ReportAgent
                        agent = ReportAgent()
                        filename = f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        agent.save_report_markdown(report, filename)
                        st.success(f"✅ Report saved as {filename}")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)

elif run_button and not query:
    st.warning("⚠️ Please enter a research query")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">Built with LangGraph • Groq LLM • ArXiv API • Multi-Agent AI</p>',
    unsafe_allow_html=True
)