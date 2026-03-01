import json
from pprint import pprint

import polars as pl

from embeddings.schemas import (
    MuscleGroupMapping,
    hevy_schema,
    muscleGroupMappingSchema,
    rp_schema,
)

rp_exercises: pl.DataFrame = pl.read_json("data/rp/exercises.json", schema=rp_schema)

hevy_exercises = pl.read_json("data/hevy/exercises.json", schema=hevy_schema)

mappings = json.load(open("data/muscle_group_mapping.json"))


normalized_mapping: list[MuscleGroupMapping] = [
    {
        "rpMuscleGroupId": k,
        **v,
        "hevy_primary": (
            v["hevy_primary"]
            if isinstance(v["hevy_primary"], list)
            else [v["hevy_primary"]]
        ),
    }
    for k, v in mappings.items()
]

normalized_mapping_df = pl.DataFrame(
    normalized_mapping, schema=muscleGroupMappingSchema
)

rp_exercises_with_muscle_mapping = rp_exercises.join(
    normalized_mapping_df,
    left_on="muscleGroupId",
    right_on="rpMuscleGroupId",
    how="right",
)


pprint(rp_exercises_with_muscle_mapping[0].to_dicts())
