#!/usr/bin/env python
import os
from typing import Dict, List
from dotenv import load_dotenv
from fastapi import FastAPI


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from langserve import add_routes
from langserve.schema import CustomUserType

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/auto",
    openai_api_key=api_key,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")


class Response(CustomUserType):
    content: str
    callback_events: List = []
    metadata: Dict = {}


def parseResponse(response: AIMessage) -> Response:
    """Sample function that expects a Response type which is a pydantic model"""
    return Response(
        content=response.content,
        callback_events=[],
        metadata={"model_used": "openrouter/auto"}
    )

# create server
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# create runnable
chain = prompt | model | RunnableLambda(parseResponse)

# create routes
add_routes(
    app,
    model,
    path="/openai",
)

add_routes(
    app,
    chain,
    path="/joke",
)

# run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)