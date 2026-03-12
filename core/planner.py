"""
execution planner — converts decomposed plans into dependency graphs.
resolves ordering, identifies parallelism, validates feasibility.
"""

from dataclasses import dataclass, field


@dataclass
class Subtask:
    id: str
    description: str
    tentacle: str
    depends_on: list[str] = field(default_factory=list)
    parallel: bool = True
    status: str = "pending"  # pending | running | completed | failed
    output: str | None = None


@dataclass
class ExecutionPlan:
    task: str
    summary: str
    subtasks: list[Subtask]

    @classmethod
    def from_dict(cls, task: str, data: dict) -> "ExecutionPlan":
        subtasks = [
            Subtask(
                id=s["id"],
                description=s["description"],
                tentacle=s["tentacle"],
                depends_on=s.get("depends_on", []),
                parallel=s.get("parallel", True),
            )
            for s in data.get("plan", [])
        ]
        return cls(task=task, summary=data.get("summary", ""), subtasks=subtasks)

    def ready_subtasks(self) -> list[Subtask]:
        """Return subtasks whose dependencies are all completed."""
        completed_ids = {s.id for s in self.subtasks if s.status == "completed"}
        return [
            s
            for s in self.subtasks
            if s.status == "pending"
            and all(dep in completed_ids for dep in s.depends_on)
        ]

    def is_complete(self) -> bool:
        return all(s.status in ("completed", "failed") for s in self.subtasks)

    def results(self) -> list[dict]:
        return [
            {
                "subtask_id": s.id,
                "tentacle": s.tentacle,
                "output": s.output or "(no output)",
            }
            for s in self.subtasks
            if s.status == "completed"
        ]
