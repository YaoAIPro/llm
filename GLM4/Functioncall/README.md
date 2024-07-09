
# LLM学习笔记

# GLM4-Functioncall
本仓库包含我使用大型模型GLM4.0进行函数调用的实践和实现。

## 1、天气查询

首先是天气查询接口，该接口来源于[YY天气](http://www.yytianqi.com/api.html)，是一个免费的天气查询接口，可查询到包括天气状况、温度、风力、风向以及湿度等信息。[cityid.json](https://github.com/yaohuang6/GLM4-Functioncall/blob/main/cityid.json)为该天气查询接口的城市id信息。

```python
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
```

## 2、自定义工具
tools是一个list，可以放置多个函数的tool，这里只放置了天气查询作为示例。需要注意的是，properties这个字段中的city，即是对应天气查询函数get_current_weather的输入参数，也与required字段中的city相对应。

```python
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
```

## 3、组合messages
assistant_messages函数中输入的message为我们第一次投入给GLM4的参数，response是模型第一次响应返回的结果，function为我们的天气查询函数get_current_weather
```python
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
```

## 4、两次响应返回的结果
### 第一次响应
```python
ChatCompletion(id='', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_1719904508088', function=Function(arguments='{"city": "Guangzhou"}', name='get_current_weather'), type='function')]))], created=1719904508, model='glm-4', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=13, prompt_tokens=175, total_tokens=188))

```
### 第二次响应
```python
ChatCompletion(id='', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='根据您的查询，我已经获取到了广州当前的天气信息。目前广州的天气状况是阴天，气温为30℃，风力为3-4级，风向为西南风，湿度为80%。这些数据是在2024年7月2日15点08分更新的。希望这个信息对您有所帮助！', role='assistant', function_call=None, tool_calls=None))], created=1719904510, model='glm-4', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=66, prompt_tokens=233, total_tokens=299))

```
>>>>>>> 19fd473 (first commit)
