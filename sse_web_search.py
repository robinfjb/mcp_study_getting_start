# sse_web_search.py
import httpx

from mcp.server import FastMCP
from openai import OpenAI


app = FastMCP('web-search', port=9000)


@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """
    client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个生活助手，可以帮你查询互联网上的信息"},
            {"role": "user", "content": query},
        ],
        stream=False
    )

    original_string = response.choices[0].message.content
    print(original_string)
    return original_string



if __name__ == "__main__":
    app.run(transport='sse')