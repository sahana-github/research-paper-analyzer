# 🔬 Research Paper Analyzer

Advanced multi-agent AI system that automatically discovers, analyzes, and compiles comprehensive reports from research papers.

## 🚀 Live Demo

[Try it here!](https://sahana-research-paper-analyzer.streamlit.app/)

## ✨ Features

- **Multi-Source Discovery**: ArXiv, Google Scholar, DuckDuckGo
- **Automated PDF Extraction**: Download and extract text from 50+ papers
- **Hypothesis Extraction**: AI-powered research hypothesis identification
- **Code Analysis**: Extract and analyze code snippets from papers
- **Comprehensive Reports**: Auto-generated research summaries with insights
- **7 Specialized Tools**: Search, scraping, analysis, visualization
- **4 AI Agents**: Discovery, Scraping, Analysis, Report compilation

## 🏗️ Architecture
```
User Query → Discovery Agent → Scraping Agent → Analysis Agent → Report Agent
                ↓                    ↓                 ↓              ↓
           (7 Tools)           (PDF Extract)    (Code/Hypothesis)  (Compile)
```

### **The 4 Agents:**

1. **🔍 Paper Discovery Agent** - Searches multiple sources
2. **📥 Scraping Agent** - Downloads and extracts PDFs
3. **🔬 Analysis Agent** - Extracts hypotheses, code, findings
4. **📝 Report Agent** - Compiles comprehensive reports

### **The 7 Tools:**

1. **ArXiv Search** - Academic paper search
2. **Google Scholar Scraper** - Supplementary research
3. **DuckDuckGo Search** - Web results
4. **PDF Extractor** - Extract text from PDFs
5. **Web Scraper** - BeautifulSoup scraping
6. **Code Analyzer** - Extract and analyze code
7. **Hypothesis Extractor** - AI-powered hypothesis identification

## 🛠️ Tech Stack

- **LangGraph** - Multi-agent orchestration
- **LangChain** - Agent framework
- **Groq** - Fast LLM inference (Llama 3.3 70B)
- **ArXiv API** - Research paper access
- **PDFPlumber** - PDF text extraction
- **BeautifulSoup** - Web scraping
- **Streamlit** - Web interface
- **Pydantic** - Data validation

## 🏃 Run Locally

### Prerequisites
- Python 3.10+
- Groq API key ([Get free key](https://console.groq.com/))

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/research-paper-analyzer.git
cd research-paper-analyzer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile

# Run app
streamlit run app.py
```

## 💡 Example Queries

- `deep learning medical imaging`
- `natural language processing transformers`
- `reinforcement learning robotics`
- `computer vision object detection`
- `quantum computing algorithms`

## 📊 Performance

- Processes 10-50 papers in 5-15 minutes
- Extracts 100+ hypotheses from papers
- Analyzes code blocks across papers
- Generates comprehensive 10+ page reports

## 🎯 Use Cases

- Literature reviews
- Research trend analysis
- Technology landscape mapping
- Competitive research analysis
- Academic research assistance

## 📄 License

MIT License

## 👨‍💻 Author

**Sahana**
- GitHub: [@sahana-github](https://github.com/sahana-github)
- LinkedIn: [sahana-durgekar](https://www.linkedin.com/in/sahana-durgekar/)


---

⭐ Star this repo if you find it helpful!
