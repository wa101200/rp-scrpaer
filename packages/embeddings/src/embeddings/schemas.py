from typing import TypedDict

import polars as pl

rp_schema = {
    "id": pl.UInt32,
    "name": pl.String,
    "muscleGroupId": pl.UInt32,
    "mgSubType": pl.String,
    "exerciseType": pl.String,
    "youtubeId": pl.String,
    "userId": pl.Int64,
    "notes": pl.List(
        pl.Struct(
            [
                pl.Field("id", pl.UInt32),
                pl.Field("exerciseId", pl.UInt32),
                pl.Field("userId", pl.Int64),
                pl.Field("noteId", pl.UInt32),
                pl.Field("dayExerciseId", pl.UInt32),
                pl.Field("createdAt", pl.String),
                pl.Field("updatedAt", pl.String),
                pl.Field("text", pl.String),
            ]
        )
    ),
    "createdAt": pl.String,
    "updatedAt": pl.String,
    "deletedAt": pl.String,
}


hevy_schema = {
    "id": pl.String,
    "title": pl.String,
    "type": pl.String,
    "primary_muscle_group": pl.String,
    "secondary_muscle_groups": pl.List(pl.String),
    "is_custom": pl.Boolean,
}


class Subtypes(TypedDict, total=False):
    incline: str
    horizontal: str
    vertical: str
    compound: str
    raise_: str  # 'raise' is a keyword in some contexts, used raise_ or keep as 'raise'
    heavy_axial: str
    non_heavy_axial: str


SubtypeDict = dict[str, str]


class MuscleGroupMapping(TypedDict):
    hevy_primary: list[str]
    name: str
    rpMuscleGroupId: str
    subtypes: SubtypeDict | None
    note: str | None


# The resulting type for your data
MuscleGroupsData = list[MuscleGroupMapping]
