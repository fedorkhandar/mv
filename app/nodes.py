from dataclasses import dataclass
from typing import List, Dict, Literal, Union, Optional, Any, Tuple, Set
from abc import ABC, abstractmethod
from uuid import uuid4

def to_fname(s: str)-> str:
    return s.replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_")

@dataclass
class MessageNode:
    name: str
    message: str
    protocol: Literal["HTTP", "NATS", "SQL", "gRPC"] = "HTTP"
    method: Optional[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "CONNECT"]] = None
    url: str = None
    status: Literal["200", "201", "202", "204", "400", "401", "403", "404", "500", "502", "503", "504"] | None = None
    subject: str = None
    comment: str = None

    border_color: str = "#000000"
    background_color: str = "#FFFFFF"
    font_color: str = "#000000"
    shape: str = "box"
    style: str = "filled"
    fontname: str = "Lucida Console"
    fontsize: int = 8

    def draw(self):
        msg = {
            "protocol": self.protocol,
            "message": self.message, 
            "method": self.method, 
            "url": self.url, 
            "status": self.status, 
            "subject": self.subject, 
            "comment": self.comment
        }
        msg = {k: v for k, v in msg.items() if v is not None}
        msg = ", ".join([f"{k}: '{v}'" for k, v in msg.items()])

        return f"    {self.name} [label = \"{msg}\" shape=\"{self.shape}\" style=\"{self.style}\" fontname=\"{self.fontname}\" fontsize={self.fontsize}]"
    # color=\"{self.border_color}\" fillcolor=\"{self.background_color}\" fontcolor=\"{self.font_color}\" shape=\"{self.shape}\" style=\"{self.style}\" fontname=\"{self.fontname}\" fontsize={self.fontsize}]"


@dataclass
class ActorNode:
    name: str
    label: str = None
    service_type: str = None
    comment: str = None

    border_color: str = "#000000"
    background_color: str = "#FFFFFF"
    font_color: str = "#000000"
    shape: str = "egg"
    style: str = "filled"
    fontname: str = "Arial"
    fontsize: int = 10

    def __post_init__(self):
        if self.label is None:
            self.label = self.name
        self.label = self.label.replace(' ','\\n')

    @abstractmethod
    def draw(self):
        pass

@dataclass
class Component(ActorNode):
    shape: str = "egg"

    def draw(self):
        
        return f"                {self.name} [label=\"{self.label}\" comment=\"{self.comment}\" color=\"{self.border_color}\" fillcolor=\"{self.background_color}\" fontcolor=\"{self.font_color}\" shape=\"{self.shape}\" style=\"{self.style}\" fontname=\"{self.fontname}\" fontsize={self.fontsize}]"

@dataclass
class Service(ActorNode):
    shape: str = "box"
    components: List[Component] = None
    fontname: str = "Courier"
    fontsize: int = 8
    background_color: str = "#FF00FF"
    style: str = "filled"

    def __post_init__(self):
        if self.components is None:
            self.components = []

    def draw(self):
        output = [
            f"        subgraph cluster_{self.name}{{",
            f"            label=\"{self.label}\"",
            f"            labelloc=\"t\"",
            f"            color=\"{self.background_color}\"",
            f"            fontcolor=\"{self.font_color}\"",
            f"            style={self.style}",
            f"            fontname=\"{self.fontname}\"",
            f"            fontsize={self.fontsize}"
        ]
        for c in self.components:
            output.append(c.draw())

        output.append("        }")
        return "\n".join(output)

@dataclass    
class DockerContainer(ActorNode):
    fontname: str = "Courier"
    fontsize: int = 8
    style: str = "dotted"
    services: List[Service] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []

    def draw(self):
        output = [
            f"    subgraph cluster_{self.name}{{",
            f"        label=\"{self.label}\"",
            f"        labelloc=\"t\"",
            f"        color=\"{self.border_color}\"",
            f"        fontcolor=\"{self.font_color}\"",
            f"        style=\"{self.style}\"",
            f"        fontname=\"{self.fontname}\"",
            f"        fontsize={self.fontsize}"
        ]

        for s in self.services:
            output.append(s.draw())

        output.append("    }")
        return "\n".join(output)
    
@dataclass
class RootNode(ActorNode):
    border: str = "#000000"
    background_color: str = "#FFFFFF"
    font_color: str = "#000000"
    margin: str = "2.5"

    shape: str = "box"
    containers: List[DockerContainer] = None
    messages: List[MessageNode] = None
    edges: List[tuple] = None

    def __post_init__(self):
        if self.containers is None:
            self.containers = []

    def draw(self):
        output = [
            f"digraph {self.name}{{",
            f"    graph[label=\"{self.label}\" labelloc=\"t\"]"
        ]

        if self.containers is not None:
            for c in self.containers:
                output.append(c.draw())

        if self.messages is not None:
            for m in self.messages:
                output.append(m.draw())

        if self.edges is not None:
            for e in self.edges:
                output.append(f"    {e[0]} -> {e[1]}")

        output.append("}")
        return "\n".join(output)
    

if __name__ == "__main__":
    root = RootNode(name = 'r', label="Biplan24")

    {
        ("d0","Manager Container"),
        ("d1","Manager Container"),
        ("d2","Manager Container"),
        ("d3","Manager Container"),
        ("d4","Manager Container"),
        
    }

    d0 = DockerContainer(name = "d0", label="Manager Container")
    
    s01 = Service(name="s01", label="Manager")
    c011 = Component(name="c011", label="REST API")
    c012 = Component(name="c012", label="NATS consumer module")
    c013 = Component(name="c013", label="NATS producer module")
    
    
    s02 = Service(name="s02", label="Manager Storage")





    d1 = DockerContainer(name = "d1", label="System Database Container")
    d2 = DockerContainer(name="d2", label="Outer Database Container")
    d3 = DockerContainer(name="d3", label="NATS Container")
    d4 = DockerContainer(name="d4", label="Downloader Container")
    d5 = DockerContainer(name="d5", label="Analytics Container")

    



    s1 = Service(name="s1", label="Inner Storage", background_color="#00FFFF")
    s2 = Service(name="s2", label="Outer Database", background_color="#00FF00")
    s3 = Service(name="s3", label="Message Broker")
    s4 = Service(name="s4", label="Clusterizator")
    s5 = Service(name="s5", label="Clusterizator Local Storage")
    s6 = Service(name="s6", label="Classificator")
    s7 = Service(name="s7", label="Classificator Local Storage")
    s8 = Service(name="s8", label="Downloader")

    s1.components.append(Component(name="c1", label="Inner PostgreSQL"))
    s2.components.append(Component(name="c2", label="Outer PostgreSQL"))
    s3.components.append(Component(name="c3", label="NATS"))
    s4.components.append(Component(name="c4", label="NATS consumer module"))
    s4.components.append(Component(name="c5", label="NATS producer module"))
    s4.components.append(Component(name="c6", label="computational module"))
    s4.components.append(Component(name="c7", label="storage module"))
    s6.components.append(Component(name="c8", label="NATS consumer module"))
    s6.components.append(Component(name="c9", label="NATS producer module"))
    s6.components.append(Component(name="c10", label="computational module"))
    s6.components.append(Component(name="c11", label="storage module"))
    s8.components.append(Component(name="c12", label="NATS consumer module"))
    s8.components.append(Component(name="c13", label="NATS producer module"))
    s8.components.append(Component(name="c14", label="downloading module"))
    s8.components.append(Component(name="c15", label="storage module"))

    d1.services.append(s1)
    d2.services.append(s2)
    d3.services.append(s3)
    d4.services.append(s8)
    d5.services.append(s4)
    d5.services.append(s6)
    d5.services.append(s5)
    d5.services.append(s7)

    root.containers.append(d1)
    root.containers.append(d2)
    root.containers.append(d3)
    root.containers.append(d4)
    root.containers.append(d5)



    messages = [
        MessageNode(name="m1", protocol="SQL", message="SELECT * FROM data WHERE id = 1"),
        MessageNode(name="m2", protocol="SQL", message="data1"),
    ]
    root.messages = messages

    root.edges = [
        ("c14", "m1"),
        ("m1", "c2"),
        ("c2", "m2"),
        ("m2", "c14")
    ]

    with open("nodes.gv", "w") as fout:
        print(root.draw(), file = fout)