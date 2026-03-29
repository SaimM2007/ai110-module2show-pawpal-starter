
"""
PawPal+ System — Core Logic Layer
pawpal_system.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    task_type: str           # "feed" | "walk" | "medication" | "appointment"
    scheduled_time: datetime
    priority: int            # 1 (highest) to 5 (lowest)
    is_recurring: bool = False
    recurrence_interval_days: int = 0
    is_completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass  # TODO

    def reschedule(self, new_time: datetime) -> None:
        """Move the task to a new time."""
        pass  # TODO

    def generate_next_occurrence(self) -> Optional[Task]:
        """Return a new Task shifted by recurrence_interval_days, or None if not recurring."""
        pass  # TODO


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        pass  # TODO

    def remove_task(self, task_id: str) -> None:
        """Remove a task by its ID."""
        pass  # TODO

    def get_upcoming_tasks(self) -> list[Task]:
        """Return incomplete tasks sorted by scheduled_time."""
        pass  # TODO


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

@dataclass
class Owner:
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)
    owner_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        pass  # TODO

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet by its ID."""
        pass  # TODO

    def get_all_tasks(self) -> list[Task]:
        """Gather every task across all owned pets."""
        pass  # TODO


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, pets: list[Pet]):
        self.pets = pets

    def get_tasks_for_today(self) -> list[Task]:
        """Return all incomplete tasks scheduled for today across all pets."""
        pass  # TODO

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks: lowest priority number = highest urgency."""
        pass  # TODO

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Find pairs of tasks with overlapping scheduled times (within 15 min)."""
        pass  # TODO

    def add_recurring_tasks(self, pet: Pet) -> None:
        """Scan a pet's tasks and generate the next occurrence for any recurring ones."""
        pass  # TODO