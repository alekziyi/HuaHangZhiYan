
def tools2json(tools):
    tools_json = []
    for tool in tools:
        tools_json.append(tool.json())
    return tools_json

class Agent:
    def __init__(self,client,tools,prompt="你是一个AI",model='glm-4'):
        self.model=model
        self.client = client
        self.tools = {}
        self.prompt =prompt
        self.tools_json=tools2json(tools)
        self.messages=[]
        self.messages.append({'role': 'system', 'content': prompt})
        self.messages.append({'role': 'system', 'content': '请务必在回答问题前完成所有必要的工具调用，因为你只有一次回答的机会'})

        for tool in tools:
            self.tools[tool.name]=tool
    def use_tools(self,tool_calls):
        for tool_call in tool_calls:
            result=self.tools[tool_call.function.name].value(eval(tool_call.function.arguments))
            self.messages.append({
                'role':'tool',
                'content':str(result),
                'tool_call_id':tool_call.id
            })
    def run(self,message):
        self.messages.append(message)
        while True:
            response = self.client.chat.completions.create(
                model=self.model,  # 填写需要调用的模型名称
                messages=self.messages,
                tools=self.tools_json,
                tool_choice="auto",
                #temperature=0.5
            )
            print(response.choices[0].message)
            self.messages.append(response.choices[0].message.model_dump())
            if response.choices[0].message.tool_calls:
                self.use_tools(response.choices[0].message.tool_calls)
            else:
                break

        self.messages=[]
        return response.choices[0].message.content

