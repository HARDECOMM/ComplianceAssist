# memory.py
import json
import sqlite3
import threading
from typing import Dict, List, Literal
from contextlib import contextmanager
from config import settings
import logging

log = logging.getLogger("memory")

Role = Literal["QA", "QC", "Regulatory", "PV", "MarketAccess", "General"]

class MemoryRepository:
    def __init__(self):
        self.backend = settings.memory_backend
        if self.backend == "sqlite":
            self._init_sqlite()
        else:
            self._lock = threading.Lock()

    def _init_sqlite(self):
        conn = sqlite3.connect(settings.sqlite_path)
        conn.execute("""
          CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            value TEXT NOT NULL
          )
        """)
        conn.commit()
        conn.close()
        log.info("SQLite memory initialized at %s", settings.sqlite_path)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(settings.sqlite_path)
        try:
            yield conn
        finally:
            conn.close()

    def remember_fact(self, role: Role, value: str) -> None:
        if self.backend == "sqlite":
            with self._conn() as conn:
                conn.execute("INSERT INTO facts (role, value) VALUES (?, ?)", (role, value))
                conn.commit()
        else:
            with self._lock:
                data = self._load_file()
                key = f"{role}_facts"
                data.setdefault(key, []).append(value)
                self._save_file(data)

    def recall_facts(self, role: Role) -> List[str]:
        if self.backend == "sqlite":
            with self._conn() as conn:
                cur = conn.execute("SELECT value FROM facts WHERE role = ?", (role,))
                return [row[0] for row in cur.fetchall()]
        else:
            with self._lock:
                data = self._load_file()
                return data.get(f"{role}_facts", [])

    def recall_all(self) -> Dict[str, List[str]]:
        if self.backend == "sqlite":
            out: Dict[str, List[str]] = {}
            with self._conn() as conn:
                cur = conn.execute("SELECT role, value FROM facts")
                for role, value in cur.fetchall():
                    key = f"{role}_facts"
                    out.setdefault(key, []).append(value)
            return out
        else:
            with self._lock:
                return self._load_file()

    def _load_file(self) -> Dict[str, List[str]]:
        try:
            with open(settings.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            log.warning("Memory file corrupted; starting fresh.")
            return {}

    def _save_file(self, data: Dict[str, List[str]]) -> None:
        with open(settings.memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

memory_repo = MemoryRepository()
