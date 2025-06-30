# 工具列表
import asyncio
from openai import AsyncOpenAI
from itertools import groupby
from operator import attrgetter

# 示例工作列表
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


def deal_with_tool_call(tools_param: list) -> list[dict]:
    """
    处理流中所有的切片，组装最终报文
    :param tool_call: 流式切片集，包括可能多个工具调用信息
    :return: 工具调用的最终参数（需要存储到历史记录的信息）
    """
    tool_calls = []
    groups = group_by_index(tools_param)
    for group in groups:
        tool = {}
        function = {}
        args = []
        # 处理每个分组中的工具调用
        for item in group:
            if item.id:
                tool["id"] = item.id
            if item.function.name:
                function["name"] = item.function.name
            args.append(item.function.arguments)
        tool["type"] = "function"
        args = "".join(args)
        print(f"处理工具调用参数: {args}")
        if args:
            function["arguments"] = args
        tool["function"] = function
        tool_calls.append(tool)
    return tool_calls


def group_by_index(data):
    """
    按 index 字段对连续元素分组。
    仅当 data 中相同 index 值总是相邻出现时才正确。
    """
    grouped = []
    for _, group in groupby(data, key=attrgetter("index")):
        grouped.append(list(group))
    return grouped  # 二维


async def main():
    # 调用deepseek，进行意图实验测试
    client = AsyncOpenAI(
        api_key="",
        base_url="https://api.deepseek.com",
    )

    stream = await client.chat.completions.create(
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

    tools_param = []
    async for chunk in stream:
        delta = chunk.choices[0].delta
        print(f"增量内容：{delta}")
        if hasattr(delta, "content") and delta.content:
            print(f"响应内容：{delta.content}", end="", flush=True)
        if hasattr(delta, "tool_calls") and delta.tool_calls:
            tools_param.append(delta.tool_calls[0])
        print("\n")
    tool_calls = deal_with_tool_call(tools_param)
    print(f"最终工具调用参数: {tool_calls}")


if __name__ == "__main__":
    asyncio.run(main())
