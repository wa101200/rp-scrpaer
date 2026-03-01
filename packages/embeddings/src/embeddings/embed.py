# from main import rp_exercises, hevy_exercises


from sentence_transformers import SentenceTransformer

paraphase = SentenceTransformer("sentence-transformers/paraphrase-mpnet-base-v2")


TEST_STR = "Incline Dumbbell Press, Strength, Chest, Shoulders, Triceps"


def embed_str(s: str) -> list[float]:
    return paraphase.encode(s).tolist()
