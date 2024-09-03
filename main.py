from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vector-shift-lite.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NodeData(BaseModel):
    id: str
    nodeType: str

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, Any] 
    data: NodeData
    width: int
    height: int

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: str
    targetHandle: str
    type: str
    animated: bool
    markerEnd: Dict[str, Any] 

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def is_dag(edges):
    adj_list = {}
    nodes = set()

    for edge in edges:
        if edge.source not in adj_list:
            adj_list[edge.source] = []
        adj_list[edge.source].append(edge.target)
        
        
        nodes.add(edge.source)
        nodes.add(edge.target)
    visited = {node: False for node in nodes}
    rec_stack = {node: False for node in nodes}

    for node in nodes:
        if not visited[node]:
            if has_cycle(node, adj_list, visited, rec_stack):
                return False

    return True

def has_cycle(v, adj_list, visited, rec_stack):
    visited[v] = True
    rec_stack[v] = True

    for neighbor in adj_list.get(v, []):
        if not visited[neighbor]:
            if has_cycle(neighbor, adj_list, visited, rec_stack):
                return True
        elif rec_stack[neighbor]:
            return True

    rec_stack[v] = False
    return False

# API routes 
@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineData):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    is_dag_result = not is_dag(pipeline.edges)

    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": is_dag_result}
