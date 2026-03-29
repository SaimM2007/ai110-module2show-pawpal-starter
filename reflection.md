# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML had four classes (Task, Pet, Owner, and Scheduler) connected in a simple one-directional hierarchy.

- What classes did you include, and what responsibilities did you assign to each?

1. 'Task' is a dataclass that holds all the info about a single care action, things like the title, type (feed, walk, medication, appointment), scheduled time, priority level, whether it repeats, and whether it's been completed. It also has methods to mark itself done, reschedule, and generate the next occurrence if it's recurring.
2. 'Pet' is also a dataclass and owns a list of Tasks. It handles adding and removing tasks and can return a sorted list of what's coming up next.
3. 'Owner' is a dataclass that holds a list of Pets. Its main job is grouping pets under one person and being able to pull all tasks across every pet they own.
4. 'Scheduler' is a plain class because it's pure logic with no identity of its own. It takes in a list of Pets and handles the algorithmic work: filtering tasks for today, sorting by priority, detecting scheduling conflicts, and generating next occurrences for recurring tasks.

In the diagram, the relationships flow as: Owner owns Pets (one to many), Pet has Tasks (one to many), and Scheduler connects to both Pet and Task with dashed lines since it reads from them but doesn't own them.

**b. Design changes**

- Did your design change during implementation?

After reviewing the skeleton, I noticed two missing relationships that would cause problems later. So yes, I did change the design a bit during implementation.

- If yes, describe at least one change and why you made it.

First, Task had no reference back to which pet it belonged to. So if the Scheduler ever flattens all tasks into one list, there's no way to trace a task back to its pet without looping through everything. I added a pet_id field to Task to fix that.

Second, Pet had no reference back to its Owner. I added an owner_id field so that relationship is traceable in both directions when needed.

Neither of these changed the overall structure of the classes. They just filled in some gaps that the UML didn't make explicit.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers two main constraints: scheduled time and priority level. Priority was weighted above time, meaning a P1 task at 2 PM shows before a P2 task at 7 AM. 

- How did you decide which constraints mattered most?

I made that call because in a real context, a medication or vet appointment matters more than the exact order things happen in the day. Time should be used as a tiebreaker when priorities are equal.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The conflict detector flags any two tasks within 15 minutes of each other regardless of how long each task actually takes. So a 5-minute medication and a 30-minute walk scheduled 14 minutes apart both get flagged the same way, even though they might not actually overlap in practice.

- Why is that tradeoff reasonable for this scenario?

The tradeoff is simplicity vs accuracy. Tracking actual task durations would require a duration_minutes field on every task and more complex interval math. For a basic pet care app, a flat 15-minute proximity check is good enough and avoids overcomplicating the data model. A false positive conflict warning is a much safer failure mode than missing a real one!

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI throughout basically every phase of the project. In the design phase I used it to brainstorm the class structure and generate the initial Mermaid UML diagram. During implementation I used it to scaffold method logic, catch missing relationships in the skeleton, and suggest algorithmic approaches for things like conflict detection and recurring task generation. I also used it to generate the test suite and help think through edge cases I might have missed.

- What kinds of prompts or questions were most helpful?

The most useful prompts were specific ones that referenced the actual file, like asking it to review the skeleton and flag missing relationships, or asking how the Scheduler should retrieve tasks from pets. Vague prompts gave vague answers, so the more context I gave, the more useful the output was.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

One moment was when AI suggested replacing the conflict detection loop with a combinations version using itertools. It was more Pythonic and shorter but it used 900 as a magic number instead of 15 * 60, which made the intent less obvious to anyone reading the code. I kept the original loop because readability mattered more than cleverness here, and the O(n²) tradeoff is completely fine for a small pet care app.

- How did you evaluate or verify what the AI suggested?

I verified what the AI suggested by reading both versions out loud and asking which one I could explain faster to someone else.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested task completion, task addition, sort order correctness, recurring task generation, conflict detection, and several edge cases including pets with no tasks, filtering when no completed tasks exist, and filtering by pet ID across multiple pets.

- Why were these tests important?

These tests were important because they cover the core behaviors the app promises to a user. Because if sorting or conflict detection is broken, the whole scheduling feature is unreliable.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I'm extremely confident that my scheduler works correctly, especially since I got 100% on all of my test cases.

- What edge cases would you test next if you had more time?

The one area I'd explore next with more time is stress testing the recurring task system with longer chains, like marking a task complete multiple days in a row and confirming no duplicates build up. I'd also test the Streamlit session state behavior more directly since that's harder to unit test but critical for the app to work correctly across reruns.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The backend logic came together really cleanly. The four class structure ended up being exactly right for the problem and nothing felt forced or over-engineered. The CLI demo in main.py also made it easy to verify everything was working before touching the UI, which saved time debugging later.

I also completed Challenge 3 and Challenge 4 from the optional extensions. For Challenge 3, I went beyond simple time sorting by adding priority-based scheduling and color-coded priority badges (🔴 P1, 🟠 P2, 🟡 P3, 🟢 P4, ⚪ P5) to the Streamlit table. And for Challenge 4, I added task type emojis (🦮 walk, 🍽️ feed, 💊 medication, 🏥 appointment) as status indicators throughout the UI including the schedule table, success messages, and conflict warnings. Both significantly improved the readability and overall feel of the app.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd add a duration_minutes field to Task so conflict detection could check for actual time overlap instead of a flat 15-minute proximity window. That's the biggest real limitation in the current scheduler. I'd also add a way to mark tasks complete directly in the Streamlit UI so the recurring task auto-generation is actually usable without going through the code.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is most useful when you already know what you want to build. When I came in with a clear design and specific questions, the output was good and fast. When I asked something vague, I had to do more work to evaluate it. The "lead architect" framing is accurate because the AI never had the full picture of what I was trying to do. I had to hold that context and use the AI as a tool, not a replacement for thinking through the design myself.