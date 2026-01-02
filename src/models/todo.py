"""Todo model representing a single todo item."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Todo:
    """Represents a single todo item with text content, completion status, and unique ID."""

    id: int
    title: str
    completed: bool = False

    def __post_init__(self):
        """Validate the todo item after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Todo title cannot be empty or contain only whitespace")
        if self.id <= 0:
            raise ValueError("Todo ID must be a positive integer")

    def mark_complete(self) -> None:
        """Mark the todo item as complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the todo item as incomplete."""
        self.completed = False

    def update_title(self, new_title: str) -> None:
        """Update the title of the todo item."""
        if not new_title or not new_title.strip():
            raise ValueError("Todo title cannot be empty or contain only whitespace")
        self.title = new_title.strip()

    def __str__(self) -> str:
        """Return a string representation of the todo item."""
        status = "x" if self.completed else " "
        return f"{self.id}. [{status}] {self.title}"