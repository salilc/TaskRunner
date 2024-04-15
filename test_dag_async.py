import pytest

from src.task_runner import TaskRunner
from src.dag_async import run_dag_recursive_async


def test_task_runner_incorrect_json(capsys):
    json_data = """
    {
        "A": {"start": true, "edges': {"B": 5, "C": 7}},
        "B": {"edges": {}},
        "C": {"edges": {}}
    }
    """
    
    TaskRunner(json_data)
    expected_output = "Invalid JSON input\n"
    captured_output = capsys.readouterr()
    assert expected_output == captured_output.out
    
@pytest.mark.asyncio
async def test_task_runner_given_data(capsys):
    json_data = """
    {
        "A": {"start": true, "edges": {"B": 5, "C": 7}},
        "B": {"edges": {}},
        "C": {"edges": {}}
    }
    """
    
    test_task_runner_obj = TaskRunner(json_data)
    await run_dag_recursive_async(test_task_runner_obj)
    expected_output = "A\nB\nC\n"
    captured_output = capsys.readouterr()
    assert expected_output == captured_output.out


@pytest.mark.asyncio
async def test_task_runner_extra_data_1(capsys):
    json_data = """
    {
        "A": {"start": true, "edges": {"B": 5, "C": 2}},
        "B": {"edges": {"D": 3}},
        "C": {"edges": {"E": 4}},
        "D": {"edges": {}},
        "E": {"edges": {}}
    }
    """
    
    test_task_runner_obj = TaskRunner(json_data)
    await run_dag_recursive_async(test_task_runner_obj)
    expected_output = "A\nC\nB\nE\nD\n"
    captured_output = capsys.readouterr()
    assert expected_output == captured_output.out

    
@pytest.mark.asyncio
async def test_task_runner_extra_data_2(capsys):
    json_data = """
    {
        "X": {"start": true, "edges": {"Y": 1, "Z": 2}},
        "Y": {"edges": {}},
        "Z": {"edges": {"A": 3, "B": 4}}
    }
    """
    test_task_runner_obj = TaskRunner(json_data)
    await run_dag_recursive_async(test_task_runner_obj)
    expected_output = "X\nY\nZ\nA\nB\n"
    captured_output = capsys.readouterr()
    assert expected_output == captured_output.out

@pytest.mark.asyncio
async def test_task_runner_no_start_vertex(capsys):
    json_data = """
    {
        "A": {"edges": {"B": 5, "C": 2}},
        "B": {"edges": {"D": 3}},
        "C": {"edges": {"E": 4}},
        "D": {"edges": {}},
        "E": {"edges": {}}
    }
    """
    test_task_runner_obj = TaskRunner(json_data)
    await run_dag_recursive_async(test_task_runner_obj)
    expected_output = "No start vertex found in the JSON input\nNone\n"
    captured_output = capsys.readouterr()
    assert expected_output == captured_output.out


def test_task_runner_has_cycle():
    json_data = """
    {
        "A": {"start": true, "edges": {"B": 5, "C": 2}},
        "B": {"edges": {"D": 3}},
        "C": {"edges": {"E": 4}},
        "D": {"edges": {"A": 5}},
        "E": {"edges": {}}
    }
    """
    test_task_runner_obj = TaskRunner(json_data)
    captured_output = test_task_runner_obj.has_cycle()
    assert captured_output == True

if __name__ == "__main__":
    pytest.main()
