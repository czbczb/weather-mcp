# weather-mcp

# 项目结构
weather-mcp/
├── .env                    # 环境变量文件 (不提交到git)
├── .gitignore             # Git忽略文件
├── README.md              # 项目说明文档
├── pyproject.toml         # 项目配置文件
├── test_weather.py        # 测试文件
└── src/
    └── weather_mcp/
        ├── __init__.py    # 包初始化文件
        └── server.py      # 主服务器代码

# 安装依赖
```bash
# 进入项目 
cd weather-mcp

# 安装依赖
uv sync
```

# 运行项目
```bash
# 方式 1: 直接运行模块
uv run python -m weather_mcp.server

# 方式 2: 运行文件
uv run python src/weather_mcp/server.py

# 方式 3: 如果设置了脚本，可以使用
uv run weather-mcp
```


