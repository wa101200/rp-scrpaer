import json
from pprint import pprint  # noqa

import polars as pl

from embeddings.schemas import (
    MuscleGroupMapping,
    hevy_schema,
    muscleGroupMappingSchema,
    rp_schema,
)

rp_exercises: pl.DataFrame = pl.read_json("data/rp/exercises.json", schema=rp_schema)
rp_exercises = rp_exercises.select(pl.all().name.prefix("rp_"))

hevy_exercises = pl.read_json("data/hevy/exercises.json", schema=hevy_schema)
hevy_exercises = hevy_exercises.select(pl.all().name.prefix("hevy_"))

mappings = json.load(open("data/muscle_group_mapping.json"))


normalized_mapping: list[MuscleGroupMapping] = [
    {
        "rp_muscleGroupId": k,
        "hevy_primary": (
            v["hevy_primary"]
            if isinstance(v["hevy_primary"], list)
            else [v["hevy_primary"]]
        ),
        "rp_muscleGroup": v["name"],
    }
    for k, v in mappings.items()
]

normalized_mapping_df = pl.DataFrame(
    normalized_mapping, schema=muscleGroupMappingSchema
)

rp_exercises = rp_exercises.join(
    normalized_mapping_df,
    on="rp_muscleGroupId",
    how="right",
)


pprint(rp_exercises[:].to_dicts())

# # now build the rich text representation for each exercise
# rp_exercises["rich_text_representation"] = (
#     rp_exercises["name"] + ", " + rp_exercises["hevy_primary"]


#     + rp_exercises["exerciseType"]
# )
