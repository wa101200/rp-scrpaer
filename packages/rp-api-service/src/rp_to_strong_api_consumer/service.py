from __future__ import annotations

import asyncio
import os

import aiohttp

from .models import (
    BootstrapResponse,
    Exercise,
    ExerciseHistoryEntry,
    MesocycleDetail,
    MesocycleSummary,
    SecondMesoMeta,
    TemplateSummary,
    UserProfile,
    UserSubscriptions,
)

RP_APP_BASE_URL = os.environ.get("RP_APP_BASE_URL")
RPP_APP_VERSION = os.environ.get("RP_APP_VERSION")

assert RP_APP_BASE_URL is not None
assert RPP_APP_VERSION is not None


class RPClient:
    def __init__(self, token: str) -> None:
        self._token = token
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> RPClient:
        self._session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self._token}",
                "accept-version": RPP_APP_VERSION,
            },
        )
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._session:
            await self._session.close()

    async def _get(self, path: str, **params: str) -> dict | list:
        assert self._session is not None
        params.setdefault("v", RPP_APP_VERSION)
        async with self._session.get(f"{RP_APP_BASE_URL}{path}", params=params) as resp:
            resp.raise_for_status()
            return await resp.json()

    # --- User ---

    async def get_user_profile(self) -> UserProfile:
        data = await self._get("/user/profile")
        return UserProfile.model_validate(data)

    async def get_user_subscriptions(self) -> UserSubscriptions:
        data = await self._get("/user/subscriptions")
        return UserSubscriptions.model_validate(data)

    # --- Training ---

    async def get_bootstrap(self) -> BootstrapResponse:
        data = await self._get("/training/bootstrap")
        return BootstrapResponse.model_validate(data)

    async def get_exercises(self) -> list[Exercise]:
        data = await self._get("/training/exercises")
        return [Exercise.model_validate(e) for e in data]

    async def get_mesocycles(self) -> list[MesocycleSummary]:
        data = await self._get("/training/mesocycles")
        return [MesocycleSummary.model_validate(m) for m in data]

    async def get_mesocycle(self, key: str) -> MesocycleDetail:
        data = await self._get(f"/training/mesocycles/{key}")
        return MesocycleDetail.model_validate(data)

    async def get_all_mesocycles(self) -> list[MesocycleDetail]:
        summaries = await self.get_mesocycles()
        results = await asyncio.gather(*(self.get_mesocycle(m.key) for m in summaries))
        return list(results)

    async def get_templates(self) -> list[TemplateSummary]:
        data = await self._get("/training/templates")
        return [TemplateSummary.model_validate(t) for t in data]

    async def get_exercise_history(
        self, exercise_id: int
    ) -> list[ExerciseHistoryEntry]:
        data = await self._get(f"/training/exercises/{exercise_id}/history")
        return [ExerciseHistoryEntry.model_validate(e) for e in data]

    async def get_user_exercise_history(self) -> dict[str, str]:
        data = await self._get("/training/user-exercise-history")
        return data

    async def get_second_meso_meta(self) -> SecondMesoMeta:
        data = await self._get("/training/meta/second-meso")
        return SecondMesoMeta.model_validate(data)

    # --- Bulk export ---

    async def export_all(self) -> dict:
        (
            profile,
            subscriptions,
            bootstrap,
            templates,
            exercise_history,
        ) = await asyncio.gather(
            self.get_user_profile(),
            self.get_user_subscriptions(),
            self.get_bootstrap(),
            self.get_templates(),
            self.get_user_exercise_history(),
        )

        mesocycles = await asyncio.gather(
            *(self.get_mesocycle(m.key) for m in bootstrap.mesocycles)
        )

        return {
            "profile": profile,
            "subscriptions": subscriptions,
            "exercises": sorted(bootstrap.exercises, key=lambda e: e.id),
            "mesocycles": sorted(
                list(mesocycles),
                key=lambda m: m.created_at.timestamp(),
                reverse=True,
            ),
            "templates": sorted(templates, key=lambda t: t.id),
            "exercise_history": exercise_history,
        }
