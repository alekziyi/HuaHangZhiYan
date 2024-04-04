import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher
class Neo4j:
    def __init__(self,url,username,password,name):
        self.graph = Graph(url, user=username, password=password, name=name)
        self.matcher = NodeMatcher(self.graph)

    def create_node(self, label, name):
        node = Node(label, name=name)
        self.graph.create(node)
        return f"节点{name}已创建"
    def create_edge(self, head, tail, relation):
        try:
            head_node = self.matcher.match( name=head).first()
        except:
            return f"节点{head}未找到"
        try:
            tail_node = self.matcher.match( name=tail).first()
        except:
            return f"节点{tail}未找到"
        try:
            self.graph.create(Relationship(head_node, relation, tail_node))
        except:
            return '发生未知错误，请检查节点是否存在'
        return f"边{relation}已创建"

    def query(self,query):
        return self.graph.run(query)


