#!/usr/bin/env python3
"""
天气查询 MCP 服务器
使用 fastmcp 库实现
"""

import os
from typing import Optional, Dict, Any
import httpx
from fastmcp import FastMCP

# 创建 FastMCP 应用
mcp = FastMCP("Weather Service")

# 天气 API 配置
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"

@mcp.tool()
async def get_current_weather(
    city: str,
    country: Optional[str] = None,
    units: str = "metric"
) -> Dict[str, Any]:
    """
    获取指定城市的当前天气信息
    
    Args:
        city: 城市名称 (例如: "北京", "上海", "New York")
        country: 国家代码 (可选，例如: "CN", "US") 
        units: 温度单位 ("metric"=摄氏度, "imperial"=华氏度)
    
    Returns:
        当前天气信息
    """
    if not WEATHER_API_KEY:
        return {"错误": "请设置环境变量 WEATHER_API_KEY"}
    
    try:
        # 构建查询参数
        location = city
        if country:
            location = f"{city},{country}"
        
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": units,
            "lang": "zh_cn"  # 中文描述
        }
        
        # 发送 API 请求
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{WEATHER_BASE_URL}/weather", params=params)
            response.raise_for_status()
            
        data = response.json()
        
        # 格式化天气信息
        weather_info = {
            "城市": data["name"],
            "国家": data["sys"]["country"],
            "天气状况": data["weather"][0]["description"],
            "当前温度": f"{data['main']['temp']}°{'C' if units == 'metric' else 'F'}",
            "体感温度": f"{data['main']['feels_like']}°{'C' if units == 'metric' else 'F'}",
            "最低温度": f"{data['main']['temp_min']}°{'C' if units == 'metric' else 'F'}",
            "最高温度": f"{data['main']['temp_max']}°{'C' if units == 'metric' else 'F'}",
            "湿度": f"{data['main']['humidity']}%",
            "气压": f"{data['main']['pressure']} hPa",
            "风速": f"{data['wind']['speed']} {'m/s' if units == 'metric' else 'mph'}",
            "云量": f"{data['clouds']['all']}%"
        }
        
        return weather_info
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"错误": f"未找到城市: {city}"}
        elif e.response.status_code == 401:
            return {"错误": "API密钥无效，请检查 WEATHER_API_KEY 环境变量"}
        else:
            return {"错误": f"API请求失败: {e.response.status_code}"}
    except Exception as e:
        return {"错误": f"获取天气信息失败: {str(e)}"}

def main():
    """运行 MCP 服务器"""
    mcp.run(transport="http")

if __name__ == "__main__":
    main()
