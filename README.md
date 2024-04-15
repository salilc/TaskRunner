Problem Statement:
This repository deals with a workflow runner that can accept the specification of a workflow in the form of a DAG 
represented in JSON where letters are assigned to the vertices and numbers are assigned to the edges. The corresponding code prints each vertex(letters) 
it visits where each edge ei going out of a vertex waits ti seconds before traveling to the connected vertex where ti is the number that is tied to edge ei.

Design:
There are 2 key aspects while taking into consideration the design of the problem.
1. Graph traversal - I have made use of graph traversal using recursive DFS(Depth first search) to identify all the vertices and the corresponding edges in the graph.
2. Identify the next available vertex to print without blocking the main thread. - Use async and await from Python's asyncio module to schedule tasks that can run concurrently.


Since this exercise deals with printing vertices while traversing a graph, I have made use of Python's asyncio module which can run a number of tasks concurrently thereby not blocking any 
I/O operations.
This design is useful incase, the server is waiting for a request and it can execute other tasks while waiting for execution. Thus, we can traverse the edges of the graph (ei) if the request 
is waiting (ti) seconds before printing the corresponding vertex.

Other Design considerations & challenges - 
This problem can be solved by running a multi-threaded application as well. However, multi threading comes with its own caveats. There are requests which are CPU bound which need heavy calculations 
and thus need blocking of specific tasks. 
Also, they can trigger a race condition as well. So, asyncio is a safer choice in this case (although the answer may vary depending on the overall scope of the project as well as the business implications.)

Implementation:
1. The entry point of the program is the main function which initializes the TaskRunner class by passing the json input. There is a proper input validation in place which can handle bad/corrupt/malformed
   JSON before the program can execute.
3. Next, a check is implemented to see if there is a cycle in the input DAG. This takes care of the case, where we cannot print all the vertices in the graph if a cycle exists.
4. Once we are sure the input json is correct and there is no cycle in the graph, we can kick off the asynchronous tasks by running the run_dag_recursive_async coroutine.
5. We check for a start vertex to enter the graph.
6. Once the start vertex has been identified, the traverse_graph coroutine is initiated.
7. This coroutine is responsible for printing the vertex and traversing the next edge of the graph, thereby creating individual tasks that wait for ti seconds for every edge(vertex) it visits concurrently.


Assumption:
There is an assumption made that the vertices to be printed need not be in order of the traversal path i.e. for the input graph
{
        "A": {"start": true, "edges": {"B": 5, "C": 2}},
        "B": {"edges": {"D": 3}},
        "C": {"edges": {"E": 4}},
        "D": {"edges": {}},
        "E": {"edges": {}}
}

The correct output should be A,C,B,E,D
Explanation:
We start by printing vertex A. Once, we print A we can traverse to the edges B & C. Now, we have to wait 5 seconds before printing B but only 2 seconds before we print C. So, we print C. Now, a total of t0+2 seconds has been passed,
assuming t0 is the time took to print A. Next, we print B and not E, because the time elapsed to print B is (t0+2)+3 seconds and for E is (to+2)+4 seconds. We follow the same logic, to print edge D which is (t0+2+3+3) seconds.

Tests:
The file **test_dag_async** tests different scenarios -
1. Test validity of input JSON
2. Test if a cycle exists in the graph
3. Test if there is no start vertex in the graph
4. Test if the given example prints the correct output
5. Test if a modified example prints the correct output
6. Test if another modified example prints the correct output

Conclusion: This exercise tests a unique feature of Python of dealing with asychronous tasks without blocking the main thread. Tasks are executed concurrently, thereby optimizing the performance of the application as well as making it scalable
and in a better shape than a multi-threaded application.

Steps to run - 
1. Pull/fork this repository into your local machine.
2. Run **main.py** on any editor or just by running python3 main.py in your working directory. Feel free to change the input of the JSON as it is purposely made to be edited as per the reviewer's choice.
3. To run tests, simply run **test_dag_async** as a pytest or run it in on any editor.

Dependencies/libraries to install - None.
   

