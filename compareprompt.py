import asyncio
import streamlit as st
import os
import json
import re
import pandas as pd
from dotenv import load_dotenv

from fastmcp import Client
# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_ollama import ChatOllama


# load_dotenv()
# HF_TOKEN = os.getenv("HF_TOKEN")

async def run_comparison():
    # connect to FastMCP server
    async with Client("compareserver.py") as client:

        # call MCP tools
        nike_data = await client.call_tool(
            "get_brand_data",
            {"brand_name": "nike"}
        )

        puma_data = await client.call_tool(
            "get_brand_data",
            {"brand_name": "puma"}
        )

        # build context
        context = f"Nike Data: {nike_data}\nPuma Data: {puma_data}"

        # structured prompt
        final_prompt = f"""
Based on this real-time data:
{context}

Create a comparison table.

Return ONLY valid JSON list with fields:
brand, product, price, rating

Limit to maximum 10 rows.
Example:
[
  {{"brand":"Nike","product":"...","price":100,"rating":4.5}}
]
"""

        print("--- Context Provided to AI ---")
        print(final_prompt)

        # LLM setup
        llm = ChatOllama(model="llama3.2:1b")

        response = llm.invoke(final_prompt)

        # print("\n--- AI RESPONSE ---")
        # print(response.content)

        # extract JSON safely
        try:
            json_text = re.search(r"\[.*\]", response.content, re.S).group()
            data = json.loads(json_text)
        except Exception:
            data = json.loads(response.content)

        # convert to dataframe
        df = pd.DataFrame(data)

        print("\n--- DATAFRAME ---")
        print(df)

        return df


if __name__ == "__main__":
    asyncio.run(run_comparison())
