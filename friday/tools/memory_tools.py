"""
Memory and Task tools — Persistent SQLite storage for FRIDAY.
"""

from friday.memory import (
    remember, recall, get_open_tasks, create_task, complete_task
)

def register(mcp):

    @mcp.tool()
    async def remember_fact(content: str, importance: int = 5) -> str:
        """
        Store a fact or user preference permanently in FRIDAY's memory.
        Use this when the user tells you something you should remember for the future.
        """
        mem_id = remember(content=content, mem_type="fact", importance=importance)
        return f"Stored in memory with ID {mem_id}: {content}"

    @mcp.tool()
    async def search_memory(query: str) -> str:
        """
        Search FRIDAY's permanent memory for past facts or preferences.
        """
        results = recall(query)
        if not results:
            return f"I have no memory of anything related to '{query}', sir."
        
        lines = [f"Found {len(results)} relevant memories:"]
        for r in results:
            lines.append(f"- {r['content']}")
        return "\n".join(lines)

    @mcp.tool()
    async def add_task(title: str, description: str = "", priority: str = "medium") -> str:
        """
        Add a task to the user's to-do list.
        Priority should be 'low', 'medium', or 'high'.
        """
        task_id = create_task(title=title, description=description, priority=priority)
        return f"Task added successfully. (ID: {task_id}, Priority: {priority})"

    @mcp.tool()
    async def list_open_tasks() -> str:
        """
        List all open tasks on the user's to-do list.
        """
        tasks = get_open_tasks()
        if not tasks:
            return "There are no open tasks on the schedule, sir."
        
        lines = ["Current Open Tasks:"]
        for t in tasks:
            lines.append(f"[{t['priority'].upper()}] (ID: {t['id']}) {t['title']}")
            if t['description']:
                lines.append(f"  Details: {t['description']}")
        return "\n".join(lines)

    @mcp.tool()
    async def mark_task_done(task_id: int) -> str:
        """
        Mark a specific task as completed.
        """
        try:
            complete_task(task_id)
            return f"Task {task_id} has been marked as complete, sir."
        except Exception as e:
            return f"Failed to complete task: {e}"
