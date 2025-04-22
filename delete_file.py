import os
import logging

import logging as logging
# 服务端
from mcp.server import FastMCP
from mcp.server import Server
from mcp.types import SamplingMessage, TextContent

app = FastMCP('file_server')

@app.tool()
async def delete_file(file_path: str):
    # Cursor不支持SamplingMessage
    result = await app.get_context().session.create_message(
        messages=[
            SamplingMessage(
                role='user', content=TextContent(
                    type='text', text=f'是否要删除文件: {file_path} (Y)')
            )
        ],
        max_tokens=100
    )
    logging.basicConfig(level=logging.INFO)
    logging.info(str(result.content))
    try:
        # 删除文件
        os.remove(file_path)
        logging.info('文件删除成功')
        return f'文件删除成功:file_path'
    except FileNotFoundError:
        logging.error('文件不存在')
        return '文件不存在'
    except Exception as e:
        logging.error(f'删除文件失败：{e}')
        return f'删除文件失败：{e}'


if __name__ == '__main__':
    app.run(transport='stdio')