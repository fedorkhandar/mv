# # """
# # # define Actors (nodes) types
# # 1. docker container
# # 2. whole microservice
# # 3. microservice component
# # 4. database

# # # define Messages (nodes) types
# # 1. http request
# # 2. http response
# # 3. database query
# # 4. database response
# # 5. NATS message
# # """

# from dataclasses import dataclass
# from typing import List, Union
# from graphviz import Source, Digraph

# @dataclass
# class BaseActor:
#     name: str
#     title: str = None
#     comment: str = None

#     border_color: str = "#000000"
#     background_color: str = "#FFFFFF"
#     font_color: str = "#000000"
#     shape: str = "egg"
#     style: str = "filled"
#     fontname: str = "Arial"
#     fontsize: int = 10

#     def to_node(self):
#         return f"{self.name} [label=\"{self.title}\", comment=\"{self.comment}\", color=\"{self.border_color}\", fillcolor=\"{self.background_color}\", fontcolor=\"{self.font_color}\", shape=\"{self.shape}\", style=\"{self.style}\", fontname=\"{self.fontname}\", fontsize={self.fontsize}]"

# @dataclass
# class MicroserviceComponent(BaseActor):
#     title: str = None
#     shape: str = "circle"

# @dataclass
# class Microservice(BaseActor):
#     title: str = "Microservice"
#     shape: str = "box"
#     components: list = None

# @dataclass
# class Database(BaseActor):
#     title: str = "Database"
#     database_name: str = None # MySQL, PostgreSQL, MongoDB, etc.
#     database_type: str = None # SQL, NoSQL, Graph, etc.
#     shape: str = "cylinder"

# @dataclass
# class DockerContainer(BaseActor):
#     title: str = "Docker Container"
#     shape: str = "box3d"
#     microservices: List[Union[Microservice, Database]] = None
   
# @dataclass
# class BaseMessage:
#     name: str
#     title: str = None


#     color: str = "#000000"
#     font_color: str = "#000000"
#     fontname: str = "Arial"
#     fontsize: int = 10
#     shape: str = "box"

# @dataclass
# class HttpRequest(BaseMessage):
#     title: str = "HTTP Request"
#     shape: str = "box"
#     color: str = "#0000FF"
#     font_color: str = "#FFFFFF"

# @dataclass
# class HttpResponse(BaseMessage):
#     title: str = "HTTP Response"
#     shape: str = "box"
#     color: str = "#00FF00"
#     font_color: str = "#FFFFFF"

# @dataclass
# class DatabaseQuery(BaseMessage):
#     title: str = "Database Query"
#     shape: str = "box"
#     color: str = "#FF0000"
#     font_color: str = "#FFFFFF"

# @dataclass
# class DatabaseResponse(BaseMessage):
#     title: str = "Database Response"
#     shape: str = "box"
#     color: str = "#FF00FF"
#     font_color: str = "#FFFFFF"

# @dataclass
# class NATSMessage(BaseMessage):
#     title: str = "NATS Message"
#     shape: str = "box"
#     color: str = "#FFFF00"
#     font_color: str = "#000000"


# class MSDiagram:
#     name: str = "MS Diagram"
#     actors: List[Union[Microservice, MicroserviceComponent, Database, DockerContainer]] = None
#     messages: List[Union[HttpRequest, HttpResponse, DatabaseQuery, DatabaseResponse, NATSMessage]] = None
#     edges: List[tuple] = None
#     filename: str = None

#     def __init__(self, name: str = None, actors: List[Union[Microservice, MicroserviceComponent, Database, DockerContainer]] = None, messages: List[Union[HttpRequest, HttpResponse, DatabaseQuery, DatabaseResponse, NATSMessage]] = None):
#         self.name = name
#         self.actors = actors
#         self.messages = messages

#     def __str__(self):
#         return f"MSDiagram(name={self.name}, actors={self.actors}, messages={self.messages})"
    
#     def __repr__(self):
#         return f"MSDiagram(name={self.name}, actors={self.actors}, messages={self.messages})"
    
#     def add_actor(self, actor: Union[Microservice, MicroserviceComponent, Database, DockerContainer]):
#         self.actors.append(actor)

#     def add_message(self, message: Union[HttpRequest, HttpResponse, DatabaseQuery, DatabaseResponse, NATSMessage]):
#         self.messages.append(message)

#     def draw(self):
#         self.filename = self.name.lower().replace(' ', '_') + '.gv'
#         g = Digraph('G', filename=self.filename)

#         # for actor in self.actors:
#         #     g.node(actor.name, actor.title, comment=actor.comment, color=actor.border_color, fillcolor=actor.background_color, fontcolor=actor.font_color, shape=actor.shape, style=actor.style, fontname=actor.fontname, fontsize=str(actor.fontsize))

#         g.attr(compound='true')
#         g.node_attr.update(style='filled', color='white')
#         g.edge_attr.update(color='blue', style='dashed')
#         g.attr(rankdir='LR')

#         with g.subgraph(name='cluster_0') as c:
#             c.attr(style='filled', color='lightgrey')
#             c.node_attr.update(style='filled', color='white')
#             c.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
#             c.attr(label='process #1')
#             with c.subgraph(name='cluster_11') as c1:
#                 c1.attr(color='green')
#                 c1.node_attr['style'] = 'filled'
#                 c1.edges([('c0', 'c1'), ('c1', 'c2'), ('c2', 'c3')])
#                 c1.attr(label='sub process #1')

#         with g.subgraph(name='cluster_1') as c:
#             c.attr(color='blue')
#             c.node_attr['style'] = 'filled'
#             c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
#             c.attr(label='process #2')
#             c.attr(style='filled', color='lightgrey')
#             c.node_attr.update(style='filled', color='white')

#         g.edge('start', 'a0')
#         g.edge('start', 'b0')
#         g.edge('a1', 'b3')
#         g.edge('b2', 'a3')
#         g.edge('a3', 'a0')
#         g.edge('a3', 'end')
#         g.edge('b3', 'end')

#         g.node('start', shape='Mdiamond')
#         g.node('end', shape='Msquare')

#         g.save()
#         s = Source.from_file(self.filename, format='png')
#         s.view()


# ms = MSDiagram(name="MS Diagram", actors=[], messages=[])

# # ms.add_actor(Microservice(name="ms1", title="Microservice 1", components=[]))
# # ms.add_actor(Microservice(name="ms2", title="Microservice 2", components=[]))
# # db_docker = DockerContainer(name="db_docker", microservices=[])
# # db = Database(name="db", database_name="PostgreSQL", database_type="SQL")
# # db_docker.microservices.append(db)

# # ms.add_actor(db_docker)
# ms.draw()


# # # print(db_docker)
# # # print(db_docker.microservices[0])



# # g = Digraph('G', filename='cluster.gv')

# # with g.subgraph(name='cluster_0') as c:
# #     c.attr(style='filled', color='lightgrey')
# #     c.node_attr.update(style='filled', color='white')
# #     c.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
# #     c.attr(label='process #1')

# # g.save()
# # s = Source.from_file('cluster.gv', format='png')
# # s.view()

    

# # # s = Source(g, filename="cluster.gv", format="png")
# # # s.view()

from graphviz import Source

with open("nodes.gv", "r") as fin:
    temp = fin.read()
# temp = """
# digraph G{
# edge [dir=forward]
# node [shape=plaintext]

# 0 [label="0 (None)"]
# 0 -> 5 [label="root"]
# 1 [label="1 (Hello)"]
# 2 [label="2 (how)"]
# 2 -> 1 [label="advmod"]
# 3 [label="3 (are)"]
# 4 [label="4 (you)"]
# 5 [label="5 (doing)"]
# 5 -> 3 [label="aux"]
# 5 -> 2 [label="advmod"]
# 5 -> 4 [label="nsubj"]
# }
# """
s = Source(temp, filename="test.gv", format="png")
s.view()