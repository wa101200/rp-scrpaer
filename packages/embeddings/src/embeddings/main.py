import json
from pprint import pprint

import polars as pl

from embeddings.schemas import hevy_schema, rp_schema

rp_exercises: pl.DataFrame = pl.read_json("data/rp/exercises.json", schema=rp_schema)

hevy_exercises = pl.read_json("data/hevy/exercises.json", schema=hevy_schema)

mappings = json.load(open("data/muscle_group_mapping.json"))


pprint(mappings)
