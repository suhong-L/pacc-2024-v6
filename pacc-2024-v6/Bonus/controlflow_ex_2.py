# uv pip install langchain-community, duckduckgo-search

import controlflow as cf
from langchain_community.tools import DuckDuckGoSearchRun


summarizer = cf.Agent(
    name="Headline Summarizer",
    description="An AI agent that fetches and summarizes current events",
    tools=[DuckDuckGoSearchRun()],
)

extractor = cf.Agent(
    name="Entity Extractor",
    description="An AI agent that does named entity recognition",
)


@cf.flow
def get_headlines():

    summarizer_task = cf.Task(
        "Retrieve and summarize today's two top business headlines",
        agents=[summarizer],
        result_type=list[str],
    )

    extractor_task = cf.Task(
        "Extract any fortune 500 companies mentioned in the headlines and whether the sentiment is positive, neutral, or negative",
        agents=[extractor],
        depends_on=[summarizer_task],
    )

    summarizer_task_output = summarizer_task.run()
    extractor_task_output = extractor_task.run()

    return summarizer_task_output, extractor_task_output


if __name__ == "__main__":
    headlines, entity_sentiment = get_headlines()
    print(headlines, entity_sentiment)
