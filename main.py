"""
PawPal+ Demo Script
main.py — CLI testing ground
"""

from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

owner = Owner(name="Saim", email="saim@example.com")

dog = Pet(name="Biscuit", species="Dog", breed="Labrador", age=3)
cat = Pet(name="Mochi",   species="Cat", breed="Siamese",  age=5)

owner.add_pet(dog)
owner.add_pet(cat)

# ---------------------------------------------------------------------------
# Tasks — all scheduled for today
# ---------------------------------------------------------------------------

today = datetime.now().replace(second=0, microsecond=0)

dog.add_task(Task(
    title="Morning walk",
    task_type="walk",
    scheduled_time=today.replace(hour=7, minute=0),
    priority=2,
))

dog.add_task(Task(
    title="Feed Biscuit",
    task_type="feed",
    scheduled_time=today.replace(hour=8, minute=0),
    priority=1,
    is_recurring=True,
    recurrence_interval_days=1,
))

dog.add_task(Task(
    title="Heartworm medication",
    task_type="medication",
    scheduled_time=today.replace(hour=8, minute=10),  # conflicts with feeding
    priority=1,
))

cat.add_task(Task(
    title="Feed Mochi",
    task_type="feed",
    scheduled_time=today.replace(hour=8, minute=0),
    priority=1,
    is_recurring=True,
    recurrence_interval_days=1,
))

cat.add_task(Task(
    title="Vet appointment",
    task_type="appointment",
    scheduled_time=today.replace(hour=14, minute=30),
    priority=1,
))

# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

scheduler = Scheduler(pets=owner.pets)

todays_tasks  = scheduler.get_tasks_for_today()
sorted_tasks  = scheduler.sort_by_priority(todays_tasks)
conflicts     = scheduler.detect_conflicts(todays_tasks)

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

print("=" * 45)
print("         PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 45)

for task in sorted_tasks:
    pet_name = next(p.name for p in owner.pets if p.pet_id == task.pet_id)
    time_str = task.scheduled_time.strftime("%I:%M %p")
    status   = "✓" if task.is_completed else "○"
    recur    = " (recurring)" if task.is_recurring else ""
    print(f"  {status} [{time_str}] P{task.priority} | {pet_name}: {task.title}{recur}")

print()

if conflicts:
    print("⚠️  Conflicts detected:")
    for t1, t2 in conflicts:
        print(f"   {t1.title!r} and {t2.title!r} overlap within 15 min")
else:
    print("✓  No scheduling conflicts.")

print("=" * 45)