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

# rp: add rich text representation for embeddings
rp_exercises = rp_exercises.with_columns(
    pl.format(
        "{}, {}, {}",
        pl.col("rp_name"),
        pl.col("rp_exerciseType"),
        pl.col("hevy_primary").list.join(", "),
    )
    .str.to_lowercase()
    .alias("rich_text_representation")
)

# hevy: add rich text representation for embeddings
hevy_exercises = hevy_exercises.with_columns(
    pl.format(
        "{}, {}, {}",
        pl.col("hevy_title"),
        pl.col("hevy_primary_muscle_group"),
        pl.col("hevy_secondary_muscle_groups").list.join(", "),
    )
    .str.to_lowercase()
    .alias("rich_text_representation")
)

pprint(rp_exercises[:10].to_dicts())
# pprint(hevy_exercises[:10].to_dicts())
