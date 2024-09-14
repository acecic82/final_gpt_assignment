import openai as client
from assistant import makeThread, excuteRun, submitToolOutputs
from openai import AuthenticationError
import streamlit as st


@st.cache_data(show_spinner="Searching Data....")
def getOutput(keyword, _runId, _threadId):
    return submitToolOutputs(_runId, _threadId)


with st.sidebar:
    apiKey = st.text_input("Please set an open ai api key")
    client.api_key = apiKey

    st.write(
        """
        
        Github : https://github.com/acecic82/final_gpt_assignment 

        streamlit : https://finalgptassignment-2x5hgzottjvacfozdyrygs.streamlit.app/

        """
    )

if apiKey:

    keyword = st.text_input(
        "Write down a keyword",
        placeholder="Research for keyword",
    )

    if keyword:
        try:
            thread = makeThread(keyword)

            run = excuteRun(thread.id, apiKey)

            outputs = getOutput(keyword, run.id, thread.id)

            for output in outputs:
                st.write(output["output"])
        except AuthenticationError:
            st.write("Check your API KEY")

else:
    st.markdown(
        """
            # Final Assignment
                    
            Ask questions about the content of a website.
                    
            Start by writing the URL of the website on the sidebar.
        """
    )
