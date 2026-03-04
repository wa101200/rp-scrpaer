from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import click
from api_service_rp.models.mesocycle import Mesocycle
from hevy_api_service import ApiClient as HevyApiClient
from hevy_api_service import Configuration as HevyConfiguration
from hevy_api_service import WorkoutsApi
from hevy_api_service.models import (
    PostWorkoutsRequestBody as HevyPostWorkoutsRequestBody,
)
from hevy_api_service.models.post_workouts_request_body_workout import (
    PostWorkoutsRequestBodyWorkout,
)
from hevy_api_service.models.post_workouts_request_exercise import (
    PostWorkoutsRequestExercise,
)
from hevy_api_service.models.post_workouts_request_set import PostWorkoutsRequestSet
from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096

DEFAULT_MATCHES_PATH = Path("data/embeddings/llm-matches.yaml")
DEFAULT_MESOCYCLES_PATH = Path("packages/cli/exports/rp/mesocycles.json")


@dataclass
class ExerciseMatch:
    rp_id: str
    rp_name: str
    hevy_best_match_id: str
    hevy_best_match_name: str
    confidence: str


def _load_matches(path: Path) -> list[ExerciseMatch]:
    data = yaml.load(path)
    return [ExerciseMatch(**item) for item in data]


def _load_mesocycles(path: Path) -> list[Mesocycle]:
    raw = json.loads(path.read_text())
    return [Mesocycle.from_dict(m) for m in raw]


@click.command("port-rp-workout-to-hevy")
@click.option(
    "--matches",
    "matches_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_MATCHES_PATH,
    help="Path to llm-matches.yaml file.",
)
@click.option(
    "--mesocycles",
    "mesocycles_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_MESOCYCLES_PATH,
    help="Path to mesocycles.json file.",
)
def port_rp_workout_to_hevy(matches_path: Path, mesocycles_path: Path):
    asyncio.run(_port_rp_workout_to_hevy(matches_path, mesocycles_path))


async def _port_rp_workout_to_hevy(matches_path: Path, mesocycles_path: Path) -> None:
    """Port RP workout data to Hevy format."""
    matches = _load_matches(matches_path)
    mesocycles = _load_mesocycles(mesocycles_path)

    click.echo(f"Loaded {len(matches)} exercise matches")
    click.echo(f"Loaded {len(mesocycles)} mesocycles")

    example_day = mesocycles[0].weeks[3].days[1]

    click.echo(f"Day finished at {example_day.finished_at}")

    hevy_workout_post_req = HevyPostWorkoutsRequestBody(
        workout=PostWorkoutsRequestBodyWorkout(
            is_private=False,
            title=example_day.label,
            description="#import-from-rp",
            start_time=example_day.exercises[0]
            .sets[0]
            .finished_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time=example_day.finished_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            exercises=[],
        )
    )

    for exercise in example_day.exercises:
        click.echo("--------")
        click.echo(f"RP Exercise id {exercise.exercise_id}")

        exercise_mach = next(
            (m for m in matches if str(m.rp_id) == str(exercise.exercise_id)), None
        )

        if exercise_mach is None:
            raise ValueError(
                f"No match found for exercise id {exercise.id}, Mappings are likely out of date."
            )
        click.echo(f"RP Exercise name: {exercise_mach.rp_name}")

        click.echo(f"Hevy best match id: {exercise_mach.hevy_best_match_id}")
        click.echo(f"Hevy best match name: {exercise_mach.hevy_best_match_name}")

        hevy_exercise = PostWorkoutsRequestExercise(
            exercise_template_id=exercise_mach.hevy_best_match_id, sets=[]
        )

        click.echo("Your set for this exercise:")
        for s in exercise.sets:
            if s.status == "skipped":
                click.echo(" set skipped")
                continue
            if s.status == "complete":
                click.echo(f" - {s.weight} {s.unit} x {s.reps} reps")

                weight_kg = s.weight if s.unit == "kg" else s.weight * 0.453592

                # TODO: decide type , if reps == repsTarget it's a failure set else normal
                hevy_set = PostWorkoutsRequestSet(
                    weight_kg=weight_kg, reps=s.reps, type="normal"
                )
                hevy_exercise.sets.append(hevy_set)
            else:
                raise ValueError(f"Unknown set status {s.status}")

        if len(hevy_exercise.sets) > 0:
            hevy_workout_post_req.workout.exercises.append(hevy_exercise)

    click.echo(f"hevy workout: {hevy_workout_post_req}")

    config = HevyConfiguration(host=os.environ.get("HEVY_API_BASE_URL"))
    api_key = os.environ.get("HEVY_API_KEY")

    key = UUID(api_key)

    async with HevyApiClient(config) as client:
        workouts_api = WorkoutsApi(client)

        result = await workouts_api.post_workouts(
            api_key=key, post_workouts_request_body=hevy_workout_post_req
        )

        click.echo(f"Created Hevy workout with id {result.id}")
        click.echo(f"Full Hevy workout: {result}")
