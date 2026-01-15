from agents.langchain_agent import create_agent

agent = create_agent()

result = agent.run(
    "Search arXiv for large language models, download the paper, analyze it and summarize"
)

print(result)
