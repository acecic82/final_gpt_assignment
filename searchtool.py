from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain.retrievers import WikipediaRetriever


def getInformationUsingWikipia(inputs):
    keyword = inputs["keyword"]
    # print(f"\n\n{keyword}\n\n")
    retriver = WikipediaRetriever(lang="ko")
    data_list = retriver.get_relevant_documents(keyword)
    output = "\n\n**************Using WikiPia*************\n\n"
    for data in data_list:
        output += f"{data.page_content}\n"

    return output


def getInformationUsingDuckDuckGo(inputs):
    keyword = inputs["keyword"]
    # print(f"\n\n{keyword}\n\n")
    output = "\n\n**************Using DDG*************\n\n"
    ddg = DuckDuckGoSearchAPIWrapper()
    output += ddg.run(f"Search for {keyword}")
    return output


functions_map = {
    "getInformationUsingWikipia": getInformationUsingWikipia,
    "getInformationUsingDuckDuckGo": getInformationUsingDuckDuckGo,
}


functions = [
    {
        "type": "function",
        "function": {
            "name": "getInformationUsingWikipia",
            "description": "Search information about keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The name of the target",
                    }
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "getInformationUsingDuckDuckGo",
            "description": "Search information about keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Ticker symbol of the target",
                    },
                },
                "required": ["keyword"],
            },
        },
    },
]
