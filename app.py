import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Session state init — only runs once per session
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Challenge 4: Professional UI — emoji icons for each task type
TYPE_EMOJI = {
    "walk":        "🦮",
    "feed":        "🍽️",
    "medication":  "💊",
    "appointment": "🏥",
}

# Challenge 3: Priority-based color coding — 🔴 high urgency down to ⚪ low
PRIORITY_BADGE = {
    1: "🔴 P1",
    2: "🟠 P2",
    3: "🟡 P3",
    4: "🟢 P4",
    5: "⚪ P5",
}

st.divider()

# ---------------------------------------------------------------------------
# Owner Setup
# ---------------------------------------------------------------------------

st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    owner_email = st.text_input("Owner email", value="jordan@example.com")

if st.button("Save owner"):
    st.session_state.owner.name  = owner_name
    st.session_state.owner.email = owner_email
    st.success(f"Owner set to {owner_name}.")

st.divider()

# ---------------------------------------------------------------------------
# Add a Pet
# ---------------------------------------------------------------------------

st.subheader("Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="Unknown")
with col4:
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, breed=breed, age=int(pet_age))
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} added!")

if st.session_state.owner.pets:
    st.write("Your pets:")
    st.table([
        {"Name": p.name, "Species": p.species, "Breed": p.breed, "Age": p.age}
        for p in st.session_state.owner.pets
    ])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Add a Task
# ---------------------------------------------------------------------------

st.subheader("Schedule a Task")

if not st.session_state.owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_options = {p.name: p for p in st.session_state.owner.pets}
    selected_pet_name = st.selectbox("Select pet", list(pet_options.keys()))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_type = st.selectbox("Type", ["walk", "feed", "medication", "appointment"])
    with col3:
        task_priority = st.selectbox("Priority (1=high)", [1, 2, 3, 4, 5])
    with col4:
        task_hour = st.number_input("Hour (24h)", min_value=0, max_value=23, value=8)

    is_recurring = st.checkbox("Recurring daily?")

    if st.button("Add task"):
        today = datetime.now().replace(second=0, microsecond=0)
        new_task = Task(
            title=task_title,
            task_type=task_type,
            scheduled_time=today.replace(hour=int(task_hour), minute=0),
            priority=task_priority,
            is_recurring=is_recurring,
            recurrence_interval_days=1 if is_recurring else 0,
        )
        pet_options[selected_pet_name].add_task(new_task)
        st.success(f"{TYPE_EMOJI.get(task_type, '')} Task '{task_title}' added to {selected_pet_name}!")

st.divider()

# ---------------------------------------------------------------------------
# Generate Schedule
# ---------------------------------------------------------------------------

st.subheader("Today's Schedule")

sort_mode = st.radio(
    "Sort by",
    ["Priority (urgent first)", "Time (chronological)"],
    horizontal=True,
)

if st.button("Generate schedule"):
    if not st.session_state.owner.pets:
        st.warning("Add a pet and some tasks first.")
    else:
        scheduler    = Scheduler(pets=st.session_state.owner.pets)
        todays_tasks = scheduler.get_tasks_for_today()
        conflicts    = scheduler.detect_conflicts(todays_tasks)

        if sort_mode == "Priority (urgent first)":
            sorted_tasks = scheduler.sort_by_priority(todays_tasks)
        else:
            sorted_tasks = scheduler.sort_by_time(todays_tasks)

        if not sorted_tasks:
            st.info("No tasks scheduled for today.")
        else:
            pet_lookup = {p.pet_id: p.name for p in st.session_state.owner.pets}
            rows = []
            for t in sorted_tasks:
                rows.append({
                    "Time"     : t.scheduled_time.strftime("%I:%M %p"),
                    "Priority" : PRIORITY_BADGE.get(t.priority, f"P{t.priority}"),
                    "Pet"      : pet_lookup.get(t.pet_id, "Unknown"),
                    "Task"     : t.title,
                    "Type"     : f"{TYPE_EMOJI.get(t.task_type, '')} {t.task_type}",
                    "Recurring": "✓" if t.is_recurring else "",
                })
            st.table(rows)
            st.success(f"{len(sorted_tasks)} task(s) scheduled for today.")

        if conflicts:
            st.error(f"⚠️ {len(conflicts)} scheduling conflict(s) detected:")
            pet_lookup = {p.pet_id: p.name for p in st.session_state.owner.pets}
            for t1, t2 in conflicts:
                p1 = pet_lookup.get(t1.pet_id, "Unknown")
                p2 = pet_lookup.get(t2.pet_id, "Unknown")
                time_str = t1.scheduled_time.strftime("%I:%M %p")
                st.warning(
                    f"{TYPE_EMOJI.get(t1.task_type, '')} '{t1.title}' ({p1}) and "
                    f"{TYPE_EMOJI.get(t2.task_type, '')} '{t2.title}' ({p2}) "
                    f"are both scheduled around {time_str}. Consider rescheduling one."
                )
        else:
            st.success("No scheduling conflicts.")