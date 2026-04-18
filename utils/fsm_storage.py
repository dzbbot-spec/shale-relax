"""Файловый FSM-storage: состояния диалогов сохраняются в JSON и переживают перезапуск бота."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, Optional

from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey


class JsonFileStorage(BaseStorage):
    """Хранит FSM-состояния в файле data/fsm_storage.json.

    В отличие от MemoryStorage, не теряет данные при перезапуске процесса.
    """

    def __init__(self, path: str = "data/fsm_storage.json") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()

    # ── Внутренние хелперы ────────────────────────────────────────────────

    def _load(self) -> dict:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _dump(self, data: dict) -> None:
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _key(key: StorageKey) -> str:
        return f"{key.bot_id}:{key.chat_id}:{key.user_id}"

    # ── Реализация BaseStorage ────────────────────────────────────────────

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        async with self._lock:
            data = self._load()
            k = self._key(key)
            if k not in data:
                data[k] = {"state": None, "data": {}}
            # state — это State-объект или None; сохраняем строку вида "Group:state"
            data[k]["state"] = state.state if hasattr(state, "state") else state
            self._dump(data)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        data = self._load()
        return data.get(self._key(key), {}).get("state")

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with self._lock:
            storage = self._load()
            k = self._key(key)
            if k not in storage:
                storage[k] = {"state": None, "data": {}}
            storage[k]["data"] = data
            self._dump(storage)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        data = self._load()
        return dict(data.get(self._key(key), {}).get("data", {}))

    async def close(self) -> None:
        pass  # Файл уже сохранён после каждой записи — ничего закрывать не нужно
