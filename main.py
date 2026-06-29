#!/usr/bin/env python
import os
from typing import Dict, List
from dotenv import load_dotenv
from fastapi import FastAPI

# లేటెస్ట్ LangChain Core మోడ్యూల్స్
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from langserve import add_routes
from pydantic import BaseModel, Field  # Pydantic v2 కి అనుగుణంగా మార్చాము

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/auto",
    openai_api_key=api_key,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# Pydantic v2 కి పక్కాగా సపోర్ట్ చేసేలా మార్చిన రెస్పాన్స్ క్లాస్
class JokeResponse(BaseModel):
    content: str
    callback_events: List = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)

def parseResponse(response: AIMessage) -> JokeResponse:
    """Sample function that expects a Response type which is a pydantic model"""
    return JokeResponse(
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
    # Render లో మరియు లోకల్ లో ఎర్రర్ రాకుండా ఉండటానికి host="0.0.0.0" పెట్టాలి
    uvicorn.run(app, host="0.0.0.0", port=8000)