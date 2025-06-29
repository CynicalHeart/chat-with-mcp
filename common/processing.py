# 工具列表
from openai import OpenAI

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


if __name__ == "__main__":
    # 调用deepseek，进行意图实验测试
    client = OpenAI(
        api_key="",
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一个AI助手，请简单明了的回答用户的问题，不要有任何解释。",
            },
            {
                "role": "user",
                "content": "当前北京时间是多少？明天此地点的天气如何？",
            },
        ],
        max_tokens=1024,
        temperature=0.5,
        stream=True,
        tools=tool_list,
    )

    tools_param = {}
    for chunk in response:
        delta = chunk.choices[0].delta
        print(f"增量内容：{delta}")
        if hasattr(delta, "content") and delta.content:
            print(f"响应内容：{delta.content}", end="", flush=True)
        if hasattr(delta, "tool_calls") and delta.tool_calls:
            curr_tool = delta.tool_calls[0]
            param = tools_param.get(curr_tool.index, "")
            tools_param[curr_tool.index] = param + curr_tool.function.arguments
        print("\n")
    print("工具参数：", tools_param)
    # print(
    #     f"响应原因：{response.choices[0].finish_reason}, 响应内容{response.choices[0].message}"
    # )
