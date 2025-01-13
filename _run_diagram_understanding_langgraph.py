import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from spreadsheet_intelligence.core.excel_autoshape_loader import ExcelAutoshapeLoader
# from prompt.jp_prompt import (
#     shape_analysis_user_message,
#     connector_analysis_user_message,
#     analysis_system_message,
#     chatbot_system_message,
#     chatbot_user_message,
# )
from prompt.en_prompt import (
    shape_analysis_user_message,
    connector_analysis_user_message,
    analysis_system_message,
    chatbot_system_message,
    chatbot_user_message,
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model_name = "gpt-4o"
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model=model_name)


class State(TypedDict):
    autoshape_data: str  # json形式のautoshapeの情報
    shape_data: str  # 解析したshapeの情報
    connector_data: str  # 解析したconnectorの情報
    ready_to_chatbot: bool  # chatbotを呼ぶかどうか
    user_question: str  # ユーザからの質問
    messages: Annotated[
        list, add_messages
    ]  # 今回は特に使わないが、メッセージを保存しておくために追加している

# Nodes
def fetch_diagram_data(state: State):
    """Excelファイルを読み込み、shapeやconnectorといったautoshapeの情報をJSON形式で返す"""
    loader = ExcelAutoshapeLoader("data/xlsx/flow_not_recurrent_group.xlsx")
    loader.load()
    diagram_json = loader.export()
    with open("data/json/diagram_json.json", "w") as f:
        f.write(diagram_json)
    return {"autoshape_data": diagram_json}


def shape_analysis(state: State):
    """取得したautoshape情報からshapeの情報を分析する"""
    messages = [
        SystemMessage(content=analysis_system_message),
        HumanMessage(
            content=shape_analysis_user_message.format(
                diagram_json=state["autoshape_data"]
            )
        ),
    ]
    response = llm.invoke(messages)
    return {
        "shape_data": response.content,
        "messages": state["messages"] + messages + [response],
    }


def connector_analysis(state: State):
    """取得したautoshape情報からconnectorの情報を分析する"""
    messages = [
        SystemMessage(content=analysis_system_message),
        HumanMessage(
            content=connector_analysis_user_message.format(
                diagram_json=state["autoshape_data"], shape_data=state["shape_data"]
            )
        ),
    ]
    response = llm.invoke(messages)
    return {
        "connector_data": response.content,
        "messages": state["messages"] + messages + [response],
        "ready_to_chatbot": True,
    }


def chatbot(state: State):
    """chatbotのメッセージを生成する"""
    messages = [
        SystemMessage(content=chatbot_system_message),
        HumanMessage(
            content=chatbot_user_message.format(
                user_question=state["user_question"],
                diagram_json=state["autoshape_data"],
                shape_data=state["shape_data"],
                connector_data=state["connector_data"],
            )
        ),
    ]
    response = llm.invoke(messages)
    return {"messages": state["messages"] + messages + [response], "user_question": ""}


if __name__ == "__main__":
    memory_saver = MemorySaver()
    graph_builder = StateGraph(State)
    # JSON形式のautoshape情報を取得してstateに反映
    graph_builder.add_node("fetch_diagram_data", fetch_diagram_data)
    # autoshape情報解析その1：shapeの情報を分析してstateに反映
    graph_builder.add_node("shape_analysis", shape_analysis)
    # autoshape情報解析その2：connectorの情報を分析してstateに反映
    graph_builder.add_node("connector_analysis", connector_analysis)
    # chatbotのメッセージを生成してstateに反映
    graph_builder.add_node("chatbot", chatbot)
    # ノードの接続
    graph_builder.add_edge(START, "fetch_diagram_data")
    graph_builder.add_edge("fetch_diagram_data", "shape_analysis")
    graph_builder.add_edge("shape_analysis", "connector_analysis")
    graph_builder.add_edge("connector_analysis", "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile(checkpointer=memory_saver)

    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

    config = {"configurable": {"thread_id": "1"}}
    # user_question = "赤いコネクタは何と何を繋いでいるか"
    user_question = "緑色のコネクタは何を繋いでいるか"
    state = State(
        autoshape_data="",
        shape_data="",
        connector_data="",
        messages=[],
        user_question=user_question,
        ready_to_chatbot=False,
    )

    with open("data/chat_log_en_simple_prompt.txt", "w") as f:
    # with open("data/chat_log_jp_simple_prompt.txt", "w") as f:
        for event in graph.stream(state, config, stream_mode="values"):
            # print(event)
            for message in event["messages"]:
                f.write("--------------------------------\n")
                f.write(f"Type: {type(message).__name__}\n")
                f.write(message.content)
                f.write("\n\n")
                print("--------------------------------")
                print(f"Type: {type(message).__name__}")
                print(message.content)
                print("\n\n\n\n")
        print("--------------------------------")
