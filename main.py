import asyncio
import logging

from src.task_runner import TaskRunner
from src.dag_async import run_dag_recursive_async

log = logging.getLogger(__name__) 


if __name__ == "__main__":
    
    # JSON data
    json_data = """
    {
        "A": {"start": true, "edges": {"B": 5, "C": 7}},
        "B": {"edges": {}},
        "C": {"edges": {}}
    }
    """
    
    task_runner_obj = TaskRunner(json_data)
    if task_runner_obj.has_cycle():
        print("Cycle detected in DAG! Cannot run Task Runner!")
        log.error("Cycle detected in DAG! Cannot run Task Runner!")
    else:
        asyncio.run(run_dag_recursive_async(task_runner_obj))
        log.info("Task Runner successful for input DAG!")
