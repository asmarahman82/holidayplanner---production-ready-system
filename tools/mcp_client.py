# tools/mcp_client.py
import logging

class MCPClient:
    """
    Minimal in-memory MCP context. Use this to pass contexts/messages between agents.
    For Module 2 this keeps things simple and traceable.
    """
    def __init__(self):
        self.store = {}

    def send(self, sender: str, receiver: str, payload: dict):
        logging.info(f"MCP: {sender} -> {receiver}")
        self.store[receiver] = payload

    def fetch(self, receiver: str):
        return self.store.get(receiver, {})
