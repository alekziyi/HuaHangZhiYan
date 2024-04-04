from zhipuai import ZhipuAI
import json
from agent import *
from tools.weather import Weather

client = ZhipuAI(api_key="b1f1b929be39becee196708ac44e29b7.897v7ZIhyhwmjKpq") # 请填写您自己的APIKey
prompt="""
我是华航智言，是服务于北华航天工业学院全体师生的大语言模型的智能助手
"""

message = {
    'role':'user',
    'content':
"""
提瓦特大陆现在天气怎么样
"""
}
tools=[Weather()]
agent = Agent(client,tools,prompt)
print(agent.run(message))