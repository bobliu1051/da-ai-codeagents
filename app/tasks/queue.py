"""
Task queue - INCOMPLETE.

This is a placeholder for moving from sync to async task processing.
Don't use yet.
"""


class TaskQueue:
    def __init__(self):
        raise NotImplementedError("queue backend not configured")

    def enqueue(self, task_name, *args, **kwargs):
        raise NotImplementedError
