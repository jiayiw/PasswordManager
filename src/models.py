import uuid
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class PasswordEntry:
    id: str
    site: str
    username: str
    password: str
    notes: str = ""

    @classmethod
    def create(
        cls, site: str, username: str, password: str, notes: str = ""
    ) -> "PasswordEntry":
        return cls(
            id=str(uuid.uuid4()),
            site=site,
            username=username,
            password=password,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PasswordEntry":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            site=data.get("site", ""),
            username=data.get("username", ""),
            password=data.get("password", ""),
            notes=data.get("notes", ""),
        )


@dataclass
class Vault:
    entries: List[PasswordEntry]

    def __init__(self, entries: Optional[List[PasswordEntry]] = None):
        self.entries = entries or []

    def add_entry(self, entry: PasswordEntry) -> None:
        self.entries.append(entry)

    def update_entry(self, entry: PasswordEntry) -> None:
        for i, e in enumerate(self.entries):
            if e.id == entry.id:
                self.entries[i] = entry
                break

    def delete_entry(self, entry_id: str) -> None:
        self.entries = [e for e in self.entries if e.id != entry_id]

    def get_entry(self, entry_id: str) -> Optional[PasswordEntry]:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None

    def search(self, query: str) -> List[PasswordEntry]:
        if not query:
            return self.entries
        query_lower = query.lower()
        return [e for e in self.entries if query_lower in e.site.lower()]

    def to_dict(self) -> dict:
        return {"entries": [e.to_dict() for e in self.entries]}

    @classmethod
    def from_dict(cls, data: dict) -> "Vault":
        entries = [PasswordEntry.from_dict(e) for e in data.get("entries", [])]
        return cls(entries=entries)
