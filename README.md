# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## 📸 Demo

<a href="/course_images/ai110/pawpal_demo_1.png" target="_blank"><img src='/course_images/ai110/pawpal_demo_1.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/pawpal_demo_2.png" target="_blank"><img src='/course_images/ai110/pawpal_demo_2.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- **Owner and pet management**: Register an owner and add multiple pets, each with their own task list.
- **Task scheduling**: Add care tasks with a type, priority level, scheduled time, and optional daily recurrence.
- **Sort by time**: View today's tasks in chronological order using `sort_by_time()`.
- **Sort by priority**: View tasks ranked by urgency (P1 = highest) with time as a tiebreaker via `sort_by_priority()`.
- **Conflict warnings**: The scheduler automatically flags any two tasks within 15 minutes of each other and tells you which pets are affected and when.
- **Daily recurrence**: Marking a recurring task complete auto-generates the next occurrence for the following day using `timedelta`.
- **Task filtering**: Filter tasks across all pets by pet, completion status, or task type using `filter_tasks()`.
- **Interactive UI**: A Streamlit interface lets you manage everything in the browser with sort controls and real-time conflict detection.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Run the tests

```bash
python -m pytest
```

### What the tests cover

The test suite has 12 tests across the following behaviors:

- **Task completion**: verifying `mark_complete()` correctly flips the status
- **Task addition**: confirming adding a task increases the pet's task count
- **Sorting correctness**: tasks added out of order are returned chronologically by `sort_by_time()` and by urgency via `sort_by_priority()`
- **Recurrence logic**: marking a daily recurring task complete auto-generates a new task for the following day
- **Conflict detection**: the scheduler correctly flags tasks at the same or overlapping times, and ignores tasks that are far apart
- **Edge cases**: pet with no tasks, filtering complete tasks when none exist, filtering by pet ID across multiple pets

### Confidence level

⭐⭐⭐⭐⭐ (5/5)

All core scheduling behaviors are covered including sorting, recurrence, conflict detection, filtering, and edge cases like empty pets and no completed tasks.

---

## Optional Extensions Completed

- **Challenge 3: Advanced Priority Scheduling and UI** — went beyond simple time sorting by implementing priority-based scheduling where P1 tasks always appear before lower priority ones. Added color-coded priority badges (🔴 P1, 🟠 P2, 🟡 P3, 🟢 P4, ⚪ P5) to the Streamlit schedule table so urgency is visible at a glance.
- **Challenge 4: Professional UI and Output Formatting** — added task type emojis (🦮 walk, 🍽️ feed, 💊 medication, 🏥 appointment) as color-coded status indicators throughout the UI, including the schedule table, the "Add task" success message, and the conflict warning messages. This significantly improves the readability and overall feel of the assistant.

## Smarter Scheduling

PawPal+ includes a set of algorithmic features that make task management more intelligent:

- **Sort by time**: Tasks can be ordered chronologically using `sort_by_time()`.
- **Sort by priority**: Tasks are ranked by urgency (1 = highest) with time as a tiebreaker via `sort_by_priority()`.
- **Filter tasks**: Filter across all pets by pet ID, completion status, or task type using `filter_tasks()`.
- **Conflict detection**: The scheduler flags any two tasks within 15 minutes of each other as a potential conflict using `detect_conflicts()`.
- **Recurring tasks**: Marking a recurring task complete automatically generates the next occurrence using `timedelta`.