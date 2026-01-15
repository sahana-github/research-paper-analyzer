from langchain.tools import tool
from tools.analysis.hypothesis_extractor import extract_hypotheses
from tools.analysis.code_analyzer import extract_code_references
from tools.analysis.evaluation_analyzer import evaluate_paper


@tool
def analyze_paper(text_path: str):
    """
    Analyze research paper and return agent-wise narrated output
    """

    narration = []

    # Hypothesis Agent
    narration.append({
        "agent": "Hypothesis Analysis Agent",
        "message": "Hello, I am the Hypothesis Analysis Agent. I analyze the paper text to extract core research claims.",
    })

    hypotheses = extract_hypotheses(text_path)

    narration.append({
        "agent": "Hypothesis Analysis Agent",
        "output": hypotheses,
        "handoff": "Passing extracted hypotheses to Code Analysis Agent."
    })

    # Code Agent
    narration.append({
        "agent": "Code Analysis Agent",
        "message": "Hello, I am the Code Analysis Agent. I check if the authors have shared implementation or GitHub links.",
    })

    code_refs = extract_code_references(text_path)

    narration.append({
        "agent": "Code Analysis Agent",
        "output": code_refs,
        "handoff": "Passing code information to Evaluation Agent."
    })

    # Evaluation Agent
    narration.append({
        "agent": "Evaluation Agent",
        "message": "Hello, I am the Evaluation Agent. I evaluate research quality based on clarity, experiments, and limitations.",
    })

    evaluation = evaluate_paper(text_path, hypotheses, code_refs)

    narration.append({
        "agent": "Evaluation Agent",
        "output": evaluation
    })

    return narration
