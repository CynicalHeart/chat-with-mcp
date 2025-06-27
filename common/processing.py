# 工具列表
tool_list = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取指定时区的时间，返回时间戳",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区名称，例如：Asia/Shanghai、America/New_York、Europe/London",
                        "enum": [
                            "Asia/Shanghai",
                            "America/New_York",
                            "Europe/London",
                            "UTC",
                        ],
                    },
                    "format": {
                        "type": "string",
                        "description": "时间格式，默认为ISO格式",
                        "enum": ["ISO", "YYYY-MM-DD HH:MM:SS", "timestamp"],
                        "default": "ISO",
                    },
                },
                "required": ["timezone"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定坐标点的天气信息信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "纬度坐标，范围-90到90",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "经度坐标，范围-180到180",
                    },
                    "units": {
                        "type": "string",
                        "description": "温度单位",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "celsius",
                    },
                    "language": {
                        "type": "string",
                        "description": "返回语言",
                        "enum": ["zh-CN", "en-US"],
                        "default": "zh-CN",
                    },
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
]
