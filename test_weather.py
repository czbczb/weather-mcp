"""测试天气 MCP 服务器"""

import asyncio
import os
from weather_mcp.server import get_current_weather

async def test_weather():
    # 测试北京天气
    result = await get_current_weather("北京", "CN")
    print("北京天气:", result)
    
    # 测试上海天气
    result = await get_current_weather("上海")
    print("上海天气:", result)

if __name__ == "__main__":
    asyncio.run(test_weather())
