# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML had four classes connected in a simple one-directional hierarchy.

- 'Task' is a dataclass that holds all the info about a single care action, things like the title, type (feed, walk, medication, appointment), scheduled time, priority level, whether it repeats, and whether it's been completed. It also has methods to mark itself done, reschedule, and generate the next occurrence if it's recurring.
- 'Pet' is also a dataclass and owns a list of Tasks. It handles adding and removing tasks and can return a sorted list of what's coming up next.
- 'Owner' is a dataclass that holds a list of Pets. Its main job is grouping pets under one person and being able to pull all tasks across every pet they own.
- 'Scheduler' is a plain class because it's pure logic with no identity of its own. It takes in a list of Pets and handles the algorithmic work: filtering tasks for today, sorting by priority, detecting scheduling conflicts, and generating next occurrences for recurring tasks.

In the diagram, the relationships flow as: Owner owns Pets (one to many), Pet has Tasks (one to many), and Scheduler connects to both Pet and Task with dashed lines since it reads from them but doesn't own them.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the skeleton, I noticed two missing relationships that would cause problems later.

First, Task had no reference back to which pet it belonged to. So if the Scheduler ever flattens all tasks into one list, there's no way to trace a task back to its pet without looping through everything. I added a pet_id field to Task to fix that.

Second, Pet had no reference back to its Owner. I added an owner_id field so that relationship is traceable in both directions when needed.

Neither of these changed the overall structure of the classes. They just filled in some gaps that the UML didn't make explicit.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
