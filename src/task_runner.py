import json
import logging 

log = logging.getLogger(__name__) 


class TaskRunner:
    def __init__(self, json_data) -> None:
        self.data = self.validate_json_input(json_data)
        
    def validate_json_input(self, json_data):
        try:
            return json.loads(json_data) 

        except json.decoder.JSONDecodeError:
            print("Invalid JSON input")
            log.error(f"Error validating input JSON data")
            
    def has_cycle(self):
        visited = set()

        def dfs(vertex):
            visited.add(vertex)
            if vertex in self.data:
                edges = self.data[vertex].get("edges", {}) 
                for next_vertex in edges:
                    if next_vertex in visited:
                        return True
                    if dfs(next_vertex):
                        return True
                return False
            
        for vertex in self.data:
            if vertex not in visited:
                if dfs(vertex):
                    return True

        return False

    def get_start_vertex(self):
        start_vertex = None

        # find start vertex
        for vertex, value in self.data.items():
            if value.get("start"):
                start_vertex = vertex
                log.info(f"Fetched start vertex ... {start_vertex}")
                # breaking since we just need the start node and ignore anything after
                break

        if not start_vertex:
            print("No start vertex found in the JSON input")
            log.error("No start vertex found in the JSON input")
        
        return start_vertex
    