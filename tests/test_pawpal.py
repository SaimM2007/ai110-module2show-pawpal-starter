"""
PawPal+ Test Suite
tests/test_pawpal.py
"""

from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(**kwargs):
    defaults = dict(
        title="Test task",
        task_type="feed",
        scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
        priority=2,
    )
    return Task(**{**defaults, **kwargs})

def make_pet(name="Biscuit"):
    return Pet(name=name, species="Dog", breed="Labrador", age=3)


# ---------------------------------------------------------------------------
# Original tests (from Phase 2)
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = make_task(title="Feed Biscuit")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_count():
    pet = make_pet()
    assert len(pet.tasks) == 0
    pet.add_task(make_task(title="Morning walk"))
    assert len(pet.tasks) == 1
    pet.add_task(make_task(title="Evening walk"))
    assert len(pet.tasks) == 2


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    pet = make_pet()
    # Add tasks out of order intentionally
    pet.add_task(make_task(title="Late task",  scheduled_time=datetime(2025, 1, 1, 14, 0)))
    pet.add_task(make_task(title="Early task", scheduled_time=datetime(2025, 1, 1, 7,  0)))
    pet.add_task(make_task(title="Mid task",   scheduled_time=datetime(2025, 1, 1, 10, 0)))

    scheduler = Scheduler(pets=[pet])
    sorted_tasks = scheduler.sort_by_time(pet.tasks)

    times = [t.scheduled_time for t in sorted_tasks]
    assert times == sorted(times)


def test_sort_by_priority_puts_p1_before_p2():
    pet = make_pet()
    pet.add_task(make_task(title="Low priority",  priority=3, scheduled_time=datetime(2025, 1, 1, 7, 0)))
    pet.add_task(make_task(title="High priority", priority=1, scheduled_time=datetime(2025, 1, 1, 14, 0)))

    scheduler = Scheduler(pets=[pet])
    sorted_tasks = scheduler.sort_by_priority(pet.tasks)

    assert sorted_tasks[0].title == "High priority"
    assert sorted_tasks[1].title == "Low priority"


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_recurring_task_generates_next_occurrence():
    next_task = make_task(
        is_recurring=True,
        recurrence_interval_days=1,
        scheduled_time=datetime(2025, 1, 1, 8, 0),
    ).generate_next_occurrence()

    assert next_task is not None
    assert next_task.scheduled_time == datetime(2025, 1, 2, 8, 0)


def test_non_recurring_task_returns_none():
    next_task = make_task(is_recurring=False).generate_next_occurrence()
    assert next_task is None


def test_mark_complete_auto_generates_next_occurrence():
    pet = make_pet()
    task = make_task(
        title="Feed Biscuit",
        is_recurring=True,
        recurrence_interval_days=1,
        scheduled_time=datetime(2025, 1, 1, 8, 0),
    )
    pet.add_task(task)

    scheduler = Scheduler(pets=[pet])
    task.mark_complete(pet=pet, scheduler=scheduler)

    titles = [t.title for t in pet.tasks]
    assert titles.count("Feed Biscuit") == 2
    next_task = pet.tasks[-1]
    assert next_task.scheduled_time == datetime(2025, 1, 2, 8, 0)
    assert next_task.is_completed is False


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_conflict_detected_for_same_time():
    pet = make_pet()
    pet.add_task(make_task(title="Task A", scheduled_time=datetime(2025, 1, 1, 8, 0)))
    pet.add_task(make_task(title="Task B", scheduled_time=datetime(2025, 1, 1, 8, 0)))

    scheduler = Scheduler(pets=[pet])
    conflicts = scheduler.detect_conflicts(pet.tasks)

    assert len(conflicts) == 1
    titles = {conflicts[0][0].title, conflicts[0][1].title}
    assert titles == {"Task A", "Task B"}


def test_no_conflict_for_tasks_far_apart():
    pet = make_pet()
    pet.add_task(make_task(title="Morning", scheduled_time=datetime(2025, 1, 1, 7,  0)))
    pet.add_task(make_task(title="Afternoon", scheduled_time=datetime(2025, 1, 1, 14, 0)))

    scheduler = Scheduler(pets=[pet])
    conflicts = scheduler.detect_conflicts(pet.tasks)

    assert len(conflicts) == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pet_with_no_tasks_returns_empty():
    pet = make_pet()
    scheduler = Scheduler(pets=[pet])
    assert scheduler.get_tasks_for_today() == []


def test_filter_complete_on_all_incomplete_returns_empty():
    pet = make_pet()
    pet.add_task(make_task(title="Walk"))
    scheduler = Scheduler(pets=[pet])
    assert scheduler.filter_tasks(status="complete") == []


def test_filter_by_pet_id_returns_only_that_pets_tasks():
    dog = make_pet("Biscuit")
    cat = make_pet("Mochi")
    dog.add_task(make_task(title="Dog task"))
    cat.add_task(make_task(title="Cat task"))

    scheduler = Scheduler(pets=[dog, cat])
    results = scheduler.filter_tasks(pet_id=dog.pet_id)

    assert len(results) == 1
    assert results[0].title == "Dog task"