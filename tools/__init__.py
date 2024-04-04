class BaseTool:
    def __init__(self):
        self.name = '基本工具'
        self.description = '基本工具'
        self.variable_description = []
    def json(self):
        variable_list,type_list,description_list=zip(*self.variable_description)
        properties={}
        for i in range(len(variable_list)):
            properties[variable_list[i]]={
                'type':type_list[i],
                'description':description_list[i]
            }
        tool_json={
            'type':'function',
            'function':{
                'name':self.name,
                'description':self.description,
                'parameters':{
                    'type':'object',
                    'properties':properties
                },
                'required':variable_list
            }
        }
        return tool_json
    def value(self,arguments:dict):
        return {'description':'基本工具'}
