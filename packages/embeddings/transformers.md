# Sentence Transformer Candidates for Exercise Embedding

## Task Characteristics

- **Very short texts** (5-15 tokens each)
- **Domain-specific** fitness/exercise vocabulary
- **Synonym-heavy**: "pullup (underhand grip)" <-> "chin up", "machine flye" <-> "butterfly (pec deck)"
- **~317 RP x ~434 Hevy** = small corpus, inference speed is not critical
- Similarity is **asymmetric** — RP strings include equipment type, Hevy strings include secondary muscle groups

## Tier 1 — Best for Short, Domain-Specific Text

| Model | Dim | Size | Why |
|-------|-----|------|-----|
| `all-MiniLM-L6-v2` | 384 | 80MB | Strategy baseline. Great for short sentences, fast, well-tested |
| `all-MiniLM-L12-v2` | 384 | 120MB | Deeper version, better synonym handling at minimal cost |
| `all-mpnet-base-v2` | 768 | 420MB | Best quality among general-purpose SBERT models. Stronger semantic understanding |

## Tier 2 — Better Semantic Matching (Synonyms, Paraphrases)

| Model | Dim | Size | Why |
|-------|-----|------|-----|
| `sentence-transformers/paraphrase-MiniLM-L6-v2` | 384 | 80MB | Trained specifically on paraphrase detection — ideal for "chin up" <-> "pullup underhand" |
| `sentence-transformers/paraphrase-mpnet-base-v2` | 768 | 420MB | Best paraphrase model. Would likely nail the synonym cases |
| `sentence-transformers/multi-qa-MiniLM-L6-cos-v1` | 384 | 80MB | Trained on question-answer pairs; good at asymmetric similarity (RP query -> Hevy candidate) |

## Tier 3 — Modern / State-of-the-Art

| Model | Dim | Size | Why |
|-------|-----|------|-----|
| `BAAI/bge-small-en-v1.5` | 384 | 130MB | Top MTEB benchmark performer in the small category. Supports instruction prefixes |
| `BAAI/bge-base-en-v1.5` | 768 | 440MB | Stronger version, still practical. Can prefix with `"Represent this exercise:"` |
| `intfloat/e5-small-v2` | 384 | 130MB | Microsoft's E5 model, strong on short text similarity |
| `intfloat/e5-base-v2` | 768 | 440MB | Better quality E5. Requires `"query: "` / `"passage: "` prefixes |
| `nomic-ai/nomic-embed-text-v1.5` | 768 | 550MB | Matryoshka embeddings — can truncate dimensions (768->256->128) for speed without retraining |

## Tier 4 — Maximum Quality (Overkill but Interesting)

| Model | Dim | Size | Why |
|-------|-----|------|-----|
| `Alibaba-NLP/gte-large-en-v1.5` | 1024 | 1.3GB | Near top of MTEB, handles short text extremely well |
| `mixedbread-ai/mxbai-embed-large-v1` | 1024 | 1.3GB | Top MTEB performer, Matryoshka support |

## Recommendation: Benchmark These 3

1. **`all-MiniLM-L6-v2`** — baseline (already planned in strategy)
2. **`paraphrase-mpnet-base-v2`** — best for synonym matching ("chin up" <-> "pullup underhand")
3. **`BAAI/bge-small-en-v1.5`** — modern, strong on short text, supports instruction prefixes like `"Represent this exercise for matching:"`

### Why These 3

- The **paraphrase-trained models** are particularly well-suited because the core challenge is recognizing that differently-named exercises are the same movement.
- **BGE models** support instruction prefixes which can steer the embedding toward exercise-matching semantics.
- With only ~137k pairs to score, even the largest model runs in seconds — **quality should win over speed**.
