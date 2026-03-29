"""
PawPal+ System — Core Logic Layer
pawpal_system.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List
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
    pet_id: str = ""

    def mark_complete(self, pet: Optional[Pet] = None, scheduler: Optional[Scheduler] = None) -> None:
        """Mark this task as done and auto-generate next occurrence if recurring."""
        self.is_completed = True
        if self.is_recurring and pet is not None and scheduler is not None:
            scheduler.add_recurring_tasks(pet)

    def reschedule(self, new_time: datetime) -> None:
        """Move the task to a new time."""
        self.scheduled_time = new_time

    def generate_next_occurrence(self) -> Optional[Task]:
        """Return a new Task shifted by recurrence_interval_days using timedelta, or None if not recurring."""
        if not self.is_recurring or self.recurrence_interval_days <= 0:
            return None
        return Task(
            title=self.title,
            task_type=self.task_type,
            scheduled_time=self.scheduled_time + timedelta(days=self.recurrence_interval_days),
            priority=self.priority,
            is_recurring=self.is_recurring,
            recurrence_interval_days=self.recurrence_interval_days,
            pet_id=self.pet_id,
        )


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
    owner_id: str = ""

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet_id = self.pet_id
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by its ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_upcoming_tasks(self) -> list[Task]:
        """Return incomplete tasks sorted by scheduled_time."""
        return sorted(
            [t for t in self.tasks if not t.is_completed],
            key=lambda t: t.scheduled_time
        )


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
        pet.owner_id = self.owner_id
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet by its ID."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def get_all_tasks(self) -> list[Task]:
        """Gather every task across all owned pets."""
        return [task for pet in self.pets for task in pet.tasks]


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, pets: list[Pet]):
        self.pets = pets

    def get_tasks_for_today(self) -> list[Task]:
        """Return all incomplete tasks scheduled for today across all pets."""
        today = datetime.now().date()
        return [
            task
            for pet in self.pets
            for task in pet.tasks
            if not task.is_completed and task.scheduled_time.date() == today
        ]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically by scheduled_time."""
        return sorted(tasks, key=lambda t: t.scheduled_time)

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks: lowest priority number = highest urgency, time as tiebreaker."""
        return sorted(tasks, key=lambda t: (t.priority, t.scheduled_time))

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Find pairs of tasks with overlapping scheduled times (within 15 min)."""
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                diff = abs((tasks[i].scheduled_time - tasks[j].scheduled_time).total_seconds())
                if diff < 15 * 60:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def add_recurring_tasks(self, pet: Pet) -> None:
        """Scan a pet's tasks and generate the next occurrence for any recurring ones."""
        new_tasks = []
        for task in pet.tasks:
            if task.is_recurring and task.is_completed:
                next_time = task.scheduled_time + timedelta(days=task.recurrence_interval_days)
                already_exists = any(
                    t.title == task.title and t.scheduled_time.date() == next_time.date()
                    for t in pet.tasks
                )
                if not already_exists:
                    next_task = task.generate_next_occurrence()
                    if next_task:
                        new_tasks.append(next_task)
        for t in new_tasks:
            pet.add_task(t)

    def filter_tasks(
        self,
        pet_id: Optional[str] = None,
        status: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> list[Task]:
        """Filter tasks across all pets by pet, completion status, or type.
        status: 'complete' | 'incomplete'
        """
        results = [task for pet in self.pets for task in pet.tasks]
        if pet_id:
            results = [t for t in results if t.pet_id == pet_id]
        if status == "complete":
            results = [t for t in results if t.is_completed]
        elif status == "incomplete":
            results = [t for t in results if not t.is_completed]
        if task_type:
            results = [t for t in results if t.task_type == task_type]
        return results