import asyncio
import httpx
from dataclasses import dataclass
from contextlib import asynccontextmanager
from mcp.server import FastMCP
from mcp.server.fastmcp import Context
from openai import OpenAI
import urllib.parse

@dataclass
# 初始化一个生命周期上下文对象
class AppContext:
    # 里面有一个字段用于存储请求历史
    histories: dict

@asynccontextmanager
async def app_lifespan(server):
    # 在 MCP 初始化时执行
    histories = {}
    try:
        # 每次通信会把这个上下文通过参数传入工具
        yield AppContext(histories=histories)
    finally:
        # 当 MCP 服务关闭时执行
        print(histories)

# # 初始化 FastMCP 服务器
app = FastMCP('web-search',
              # 设置生命周期监听函数
              lifespan=app_lifespan
              )


@app.tool()
async def web_search(ctx: Context, query: str) -> str:
    """
       搜索互联网内容

       Args:
           query: 要搜索内容

       Returns:
           搜索结果的总结
    """
    # 如果之前问过同样的问题，就直接返回缓存
    histories = ctx.request_context.lifespan_context.histories
    if query in histories:
        return histories[query]


    client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个生活助手，可以帮你查询互联网上的信息"},
            {"role": "user", "content": query},
        ],
        stream=False
    )
    # 打印结果

    original_string = response.choices[0].message.content
    print(original_string)
    # 将查询值和返回值存入到 histories 中
    ctx.request_context.lifespan_context.histories[query] = original_string
    # gbk_string = original_string.encode("gbk", errors="replace")
    # params = urllib.parse.quote(gbk_string.decode("gbk"))
    return original_string


# async def main():
#     print(await web_search("今天上海天气怎么样"))


if __name__ == "__main__":
    app.run(transport='stdio')
    # asyncio.run(main())
