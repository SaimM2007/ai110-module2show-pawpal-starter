"""
PawPal+ Tests
tests/test_pawpal.py
"""

from datetime import datetime
from pawpal_system import Task, Pet


def make_task(**kwargs):
    defaults = dict(
        title="Test task",
        task_type="feed",
        scheduled_time=datetime(2025, 1, 1, 8, 0),
        priority=2,
    )
    return Task(**{**defaults, **kwargs})


# ---------------------------------------------------------------------------
# Test 1: Task Completion
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = make_task(title="Feed Biscuit")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


# ---------------------------------------------------------------------------
# Test 2: Task Addition
# ---------------------------------------------------------------------------

def test_add_task_increases_count():
    pet = Pet(name="Biscuit", species="Dog", breed="Labrador", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(make_task(title="Morning walk"))
    assert len(pet.tasks) == 1
    pet.add_task(make_task(title="Evening walk"))
    assert len(pet.tasks) == 2