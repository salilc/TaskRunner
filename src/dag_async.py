import asyncio
import logging

log = logging.getLogger(__name__) 


async def run_dag_recursive_async(task_runner_obj):
    data = task_runner_obj.data
    start_vertex = task_runner_obj.get_start_vertex()

    await traverse_graph(data, start_vertex)

async def traverse_graph(data, vertex):
    print(vertex)
    if vertex in data:
        edges = data[vertex].get("edges", {})

        try:
            # create tasks for all edges simultaneously
            tasks = [delay_task(data, edge_vertex, time) for edge_vertex, time in edges.items()]
            log.info(f"creating tasks for all edges...")
            
            # gather all tasks to run concurrently
            await asyncio.gather(*tasks)
        
        except Exception as e:
            log.error(f"Error traversing graph - {e}")
    
async def delay_task(data, vertex, time):
    # traverse the next edge concurrently after time (ti) seconds  
    await asyncio.sleep(time)
    await traverse_graph(data, vertex)
