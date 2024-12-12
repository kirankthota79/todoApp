
from uuid import uuid4
import requests
from ..api import *

ENDPOINT = "https://yr62m2k2xhppsjf5nlaspqymd40amlau.lambda-url.us-east-1.on.aws/"

def test_can_create_and_get_task():
    user_id = f"user_{uuid4().hex}"
    random_task_content = f"task content: {uuid4().hex}"
    create_response = create_task(user_id, random_task_content)
    assert create_response.status_code == 200 
    
    task_id = create_response.json()["task"][task_id]
    get_response = get_task(task_id)
    assert get_response.status_code == 200
    
    task = get_response.json()
    assert task["user_id"] == user_id
    assert task["content"] == random_task_content
    
# def test_can_list_tasks():
#     """ Creating new user for this test """
#     user_id = f"user_{uuid4().hex}"
    
#     """ Creating 3 tasks for this user """
#     for i in range(3):
#         create_task(user_id, f"task_{i}")
    
#     """Listing the tasks for this user """
#     response = list_tasks(user_id)
#     tasks = response.json()["tasks"]
#     assert len(tasks) ==3
    
# def test_can_update_task():
#     """ Creating new user for this test """
#     user_id = f"user_{uuid4().hex}"
#     create_response = create_task(user_id, "task content")
#     task_id = create_response.json()["task"]["task_id"]
    
#     """ Updating the task with new content """
#     new_task_content = f"updated task content: {uuid4().hex}"
#     payload = {
#         "content" : new_task_content,
#         "task_id" : task_id,
#         "is_done" : True,
#     }
    
#     update_task_response = update_task(payload)
#     assert update_task_response.status_code == 200
    
# def test_can_delete_task():
#     """ Creating new user for this test """
#     user_id = f"user_{uuid4().hex}"
#     create_response = create_task(user_id, "task1")
#     task_id = create_response.json()["task"]["task_id"]
    
#     """ Delete the task """
#     delete_task(task_id)
    
#     """ We shouldn't be able to retrive the task anymore. """
#     get_task_response = get_task(task_id)
#     assert get_task_response.status_code == 404


def list_tasks(user_id: str) -> dict:
    return requests.get(f"{ENDPOINT}/list-tasks/{user_id}")

def create_task(user_id:str, content:str) ->dict:
    payload = {
        "user_id": user_id,
        "content": content
    }
    return requests.put(f"{ENDPOINT}/create_task", json=payload)

def get_task(task_id:str) -> dict:
    return requests.get(f"{ENDPOINT}/get-task/{task_id}")

# def delete_task(task_id: str) -> dict:
#     return requests.delete(f"{ENDPOINT}/delete-task/{task_id}")

# def update_task(payload:dict) -> dict:
#     return requests.put(f"{ENDPOINT}/update-task", json=payload)
