import streamlit as st
import json
from searchtool import functions, functions_map
from time import sleep
from openai import NotFoundError
import openai as client


def makeAssistant():
    return client.beta.assistants.create(
        name="Investor Assistant",
        instructions="You help users do research on publicly traded companies and you help users decide if they should buy the stock or not.",
        model="gpt-4-1106-preview",
        tools=functions,
    )


@st.cache_data
def getAssistantId(apiKey):
    return makeAssistant().id


def makeThread(keyword):
    print(f"Make Thread Now {keyword}")

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": keyword,
            }
        ]
    )

    return thread


def excuteRun(threadId, apiKey):
    try:
        return client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=getAssistantId(apiKey),
        )
    except NotFoundError:
        st.cache_data.clear()
        return client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=getAssistantId(apiKey),
        )


def get_run(run_id, thread_id):
    return client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id,
    )


def get_messages(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    messages = list(messages)
    messages.reverse()
    for message in messages:
        print(f"{message.role}: {message.content[0].text.value}")


def get_tool_outputs(run_id, thread_id):
    run = get_run(run_id, thread_id)
    while run.status != "requires_action":
        run = get_run(run_id, thread_id)
        sleep(5)

    outputs = []
    for action in run.required_action.submit_tool_outputs.tool_calls:
        action_id = action.id
        function = action.function
        print(f"Calling function: {function.name} with arg {function.arguments}")
        outputs.append(
            {
                "output": functions_map[function.name](json.loads(function.arguments)),
                "tool_call_id": action_id,
            }
        )
    return outputs


def submitToolOutputs(run_id, thread_id):
    outputs = get_tool_outputs(run_id, thread_id)
    client.beta.threads.runs.submit_tool_outputs(
        run_id=run_id,
        thread_id=thread_id,
        tool_outputs=outputs,
    )

    return outputs
