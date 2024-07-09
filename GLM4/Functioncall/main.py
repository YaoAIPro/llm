<<<<<<< HEAD
from openai import OpenAI
import os
import json
import requests
# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'http://192.168.3.15:10580'
os.environ['HTTPS_PROXY'] = 'https://192.168.3.15:10580'

# GLM4的api接口，这里换上你的url
base_url = "http://172.16.255.110:8000/v1/"
client = OpenAI(api_key="EMPTY", base_url=base_url)

# 天气信息来源于YY天气http://www.yytianqi.com/home
def get_current_weather(city: str):
    f = open("cityid.json", "r", encoding="utf-8")
    fr = json.loads(f.read())
    f.close()

    # 换上你的api_key
    key = "you api_key"
    url = f"http://api.yytianqi.com/observe?city={fr[city.lower()]}&key={key}"
    res = requests.get(url)
    data = res.json()["data"]
    if res.status_code == 200:
        return f"""lastUpdate:{data["lastUpdate"]} | weather:{data["tq"]} | temperature:{data["qw"]} | 
                wind power:{data["fl"]} | wind direction:{data["fx"]} | humidity:{data["sd"]}"""
    else:
        return None


def custom_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the weather information of a city, automatically inferring the temperature unit from the user's location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city, e.g. Guangzhou",
                        },
                    },
                    "required": ["city"],
                },
            }
        },
    ]
    return tools


def assistant_messages(messages,response,function):
    messages.append({
        "role": "assistant",
            "content": None,
            "function_call": None,
            "tool_calls": [
                {
                    "id": response.choices[0].message.tool_calls[0].id,
                    "function": {
                        "name": response.choices[0].message.tool_calls[0].function.name,
                        "arguments": response.choices[0].message.tool_calls[0].function.arguments
                    },
                    "type": "function"
                }
            ]
    })
    messages.append({
            "tool_call_id": response.choices[0].message.tool_calls[0].id,
            "role": "tool",
            "name": response.choices[0].message.tool_calls[0].function.name,
            "content": function(json.loads(response.choices[0].message.tool_calls[0].function.arguments).get("city")),
        })
    return messages

def chat(messages,tools,use_stream):
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        tools=tools,
        stream=use_stream,
        max_tokens=256,
        temperature=0.9,
        presence_penalty=1.2,
        top_p=0.1,
        tool_choice="auto"
    )
    if response:
        return response
    else:
        return None


if __name__ == '__main__':
    messages = [
        {
            "role": "user", "content": "我想知道广州的天气情况"
        },
    ]
    tools = custom_tools()
    response = chat(messages=messages,tools=tools,use_stream=False)
    print(response)
    messages = assistant_messages(messages,response,function=get_current_weather)

    response = chat(messages=messages,tools=tools,use_stream=False)
=======
from openai import OpenAI
import os
import json
import requests
# 设置代理环境变量
os.environ['HTTP_PROXY'] = 'http://192.168.3.15:10580'
os.environ['HTTPS_PROXY'] = 'https://192.168.3.15:10580'

# GLM4的api接口，这里换上你的url
base_url = "http://172.16.255.110:8000/v1/"
client = OpenAI(api_key="EMPTY", base_url=base_url)

# 天气信息来源于YY天气http://www.yytianqi.com/home
def get_current_weather(city: str):
    f = open("cityid.json", "r", encoding="utf-8")
    fr = json.loads(f.read())
    f.close()

    # 换上你的api_key
    key = "you api_key"
    url = f"http://api.yytianqi.com/observe?city={fr[city.lower()]}&key={key}"
    res = requests.get(url)
    data = res.json()["data"]
    if res.status_code == 200:
        return f"""lastUpdate:{data["lastUpdate"]} | weather:{data["tq"]} | temperature:{data["qw"]} | 
                wind power:{data["fl"]} | wind direction:{data["fx"]} | humidity:{data["sd"]}"""
    else:
        return None


def custom_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the weather information of a city, automatically inferring the temperature unit from the user's location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city, e.g. Guangzhou",
                        },
                    },
                    "required": ["city"],
                },
            }
        },
    ]
    return tools


def assistant_messages(messages,response,function):
    messages.append({
        "role": "assistant",
            "content": None,
            "function_call": None,
            "tool_calls": [
                {
                    "id": response.choices[0].message.tool_calls[0].id,
                    "function": {
                        "name": response.choices[0].message.tool_calls[0].function.name,
                        "arguments": response.choices[0].message.tool_calls[0].function.arguments
                    },
                    "type": "function"
                }
            ]
    })
    messages.append({
            "tool_call_id": response.choices[0].message.tool_calls[0].id,
            "role": "tool",
            "name": response.choices[0].message.tool_calls[0].function.name,
            "content": function(json.loads(response.choices[0].message.tool_calls[0].function.arguments).get("city")),
        })
    return messages

def chat(messages,tools,use_stream):
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        tools=tools,
        stream=use_stream,
        max_tokens=256,
        temperature=0.9,
        presence_penalty=1.2,
        top_p=0.1,
        tool_choice="auto"
    )
    if response:
        return response
    else:
        return None


if __name__ == '__main__':
    messages = [
        {
            "role": "user", "content": "我想知道广州的天气情况"
        },
    ]
    tools = custom_tools()
    response = chat(messages=messages,tools=tools,use_stream=False)
    print(response)
    messages = assistant_messages(messages,response,function=get_current_weather)

    response = chat(messages=messages,tools=tools,use_stream=False)
>>>>>>> d273e90 (Initial commit)
    print(response)