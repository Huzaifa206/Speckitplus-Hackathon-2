# Simple Task ID System

## What Changed

Tasks are now numbered **1, 2, 3, etc.** for easy reference, instead of using complex database IDs.

## How It Works

### In the UI
- Each task shows a numbered circle (1, 2, 3...) in indigo color
- The number represents the task's position in your list
- Easy to identify: "Task 1", "Task 2", etc.

### In the Chatbot
1. **List tasks first** to see the numbers:
   ```
   User: "list my tasks"
   Bot:
   Here are your tasks:
   1. Party (Priority: medium, ○ Pending)
   2. Prepare presentation (Priority: high, ○ Pending)
   ```

2. **Use the numbers** to delete or complete:
   ```
   User: "delete 1"
   Bot: Task 1 deleted successfully!
   ```

   ```
   User: "complete 2"
   Bot: Task 2 marked as complete!
   ```

## Examples

### Delete a Task
```
User: list tasks
Bot: [shows numbered list]
User: delete 2
Bot: Task 2 deleted successfully!
```

### Complete a Task
```
User: complete 1
Bot: Task 1 marked as complete!
```

### Natural Language
The chatbot understands:
- "delete 2"
- "remove task 1"
- "complete 3"
- "mark 2 as done"
- "finish task 1"

## Important Notes

1. **Always list tasks first** when starting a conversation with the chatbot
2. The numbers reset based on your current filtered view
3. The numbers in the UI match the numbers the chatbot uses
4. If a task is deleted, the remaining tasks are renumbered

## Technical Details

### Frontend
- `task-item.tsx`: Shows display index in a circular badge
- `task-list.tsx`: Passes `index + 1` as `displayIndex` to each task

### Backend
- `agent.py`: Creates a mapping between display indices (1, 2, 3) and database IDs
- Mapping is stored per conversation
- When user says "delete 2", it looks up what database ID corresponds to display index 2
- This way users never need to know the complex database IDs

## Restart Required

After making these changes:
1. Restart the backend server
2. Refresh the frontend
3. Try it out:
   - Say "list my tasks" to the chatbot
   - Note the numbers (1, 2, 3...)
   - Say "delete 1" or "complete 2"
