# Exercise Matching Strategy: RP → Hevy

## Problem

Match exercises from `data/rp/exercises.json` to `data/hevy/exercises.json`. The naming conventions differ significantly:

- **RP**: `"Bench Press (Medium Grip)"` with equipment in `exerciseType: "barbell"`
- **Hevy**: `"Bench Press (Barbell)"` with equipment in the title

Not all RP exercises will have a Hevy match — that's acceptable.

## Data Shapes

### RP Exercise

```json
{
  "id": 6,
  "name": "Bench Press (Medium Grip)",
  "muscleGroupId": 1,
  "mgSubType": "non-incline",
  "exerciseType": "barbell"
}
```

### Hevy Exercise

```json
{
  "id": "79D0BB3A",
  "title": "Bench Press (Barbell)",
  "primary_muscle_group": "chest",
  "secondary_muscle_groups": ["triceps", "shoulders"]
}
```

## Approaches (ordered by complexity)

### 1. Rule-based normalization + exact match

Normalize both names: append equipment to RP names, strip parentheticals, lowercase, then exact-match.
Fast but brittle — misses synonyms like "Pullup (Underhand Grip)" <-> "Chin Up".

### 2. Token overlap / Jaccard similarity

Tokenize names, compute set overlap. Handles word reordering but still misses semantic equivalence.

### 3. Fuzzy string matching (Levenshtein / Jaro-Winkler)

Score all pairs by edit distance. Works for near-identical names, fails on semantic synonyms.

### 4. TF-IDF + cosine similarity

Treat each name as a "document", weight rare tokens higher (e.g., "Skullcrusher" is more discriminating than "Dumbbell"). Better than raw token overlap.

### 5. Semantic embeddings

Encode enriched exercise descriptions using a sentence transformer (e.g., `all-MiniLM-L6-v2`). Build the input string from all available fields:

- RP: `"Bench Press Medium Grip, barbell, chest, non-incline"`
- Hevy: `"Bench Press Barbell, chest, triceps, shoulders"`

Then cosine-similarity match. Catches synonyms ("Pullup Underhand" ~ "Chin Up") and handles noisy naming.

### 6. Hybrid: embeddings + muscle group constraint (recommended)

Use embeddings for scoring but **filter candidates by muscle group** first (map RP's `muscleGroupId` to Hevy's `primary_muscle_group`). This reduces false positives — a "Press" in chest won't match a "Press" in shoulders.

## Recommended Approach: Hybrid (Approach 6)

### Step 1 — Build muscle group mapping

Map RP's numeric `muscleGroupId` to Hevy's string `primary_muscle_group`:

| muscleGroupId | RP Muscle Group | Hevy primary_muscle_group |
|---------------|-----------------|---------------------------|
| 1             | Chest           | chest                     |
| 2             | Back            | lats, upper_back          |
| 3             | Triceps         | triceps                   |
| 4             | Biceps          | biceps                    |
| 5             | Shoulders       | shoulders                 |
| ...           | ...             | ...                       |

This mapping needs to be completed by inspecting the full dataset.

### Step 2 — Build enriched name strings

For each exercise, construct a rich text representation:

**RP:**
```
"{name}, {exerciseType}, {mgSubType}"
→ "Bench Press Medium Grip, barbell, non-incline"
```

**Hevy:**
```
"{title}, {primary_muscle_group}, {secondary_muscle_groups}"
→ "Bench Press Barbell, chest, triceps, shoulders"
```

### Step 3 — Filter candidates by muscle group

For each RP exercise, only consider Hevy exercises whose `primary_muscle_group` maps to the same RP `muscleGroupId`. This narrows the search space and prevents cross-muscle-group false matches.

### Step 4 — Compute embedding similarity

Encode all enriched strings using a sentence transformer. For each RP exercise, compute cosine similarity against filtered Hevy candidates.

### Step 5 — Apply confidence threshold

Take the top Hevy match only if similarity exceeds a threshold (e.g., 0.7). Exercises below the threshold remain unmatched.

### Step 6 — Manual review

Export low-confidence matches (e.g., 0.5-0.7) for manual review. Some may be valid matches with unusual naming.

## Expected Edge Cases

- **Many-to-one**: Multiple RP exercises (grip/angle variants) may map to a single Hevy exercise
- **Synonyms**: "Pullup (Underhand Grip)" <-> "Chin Up", "Machine Flye" <-> "Butterfly (Pec Deck)"
- **Custom exercises**: Hevy has `is_custom: true` entries that may or may not match
- **Missing categories**: RP may have exercise types (e.g., freemotion) with no Hevy equivalent
