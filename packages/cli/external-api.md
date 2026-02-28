# RP Strength Training API

Base URL: `https://training.rpstrength.com/api`

Authentication: `Authorization: Bearer <token>` header on all requests.

## GET Endpoints

### User

| Endpoint | Description |
|---|---|
| `/user/profile` | Profile data (email, name, photo, Google/Apple/Facebook IDs, role, attributes, preferences) |
| `/user/subscriptions` | Active subscriptions, purchase history, Stripe customer IDs, consumed IAPs |

### Training Data

| Endpoint | Description |
|---|---|
| `/training/bootstrap` | **Main endpoint (~235KB)** - Full exercise catalog + all mesocycles (summary) + current mesocycle with complete weeks/days/exercises/sets |
| `/training/exercises` | Full exercise catalog (315 exercises with name, muscleGroupId, youtubeId, exerciseType, mgSubType) |
| `/training/mesocycles` | List of all mesocycles (summary: id, key, name, days, weeks, unit, timestamps) |
| `/training/mesocycles/{key}` | **Full mesocycle detail (~150-185KB)** - weeks > days > exercises > sets with weight, reps, targets, bodyweight, timestamps |
| `/training/templates` | All training templates (113 templates with id, key, name, emphasis, sex, frequency) |
| `/training/templates/{id}` | Specific template detail |
| `/training/exercises/{id}/history` | Set history for a specific exercise across all mesocycles (grouped by meso, includes weight, reps, targets, week, day) |
| `/training/user-exercise-history` | Map of exerciseId -> last performed timestamp |
| `/training/meta/second-meso` | Meta info about second mesocycle (key, startedAt) |

### App / Products

| Endpoint | Description |
|---|---|
| `/apps/training/rp/{version}/config.json?v={version}` | App config, version changelog, feature flags, latest client version |
| `/products.json?apps=training` | Subscription product/pricing catalog (Stripe product IDs, prices, billing periods) |
| `/training/app.webmanifest?v={version}` | PWA web manifest |
| `/userReview` | User review data |

## POST Endpoints

### Training

| Endpoint | Description |
|---|---|
| `/training/mesocycles` | Create a new mesocycle |
| `/training/mesocycles/{key}/add-micro` | Add a micro-cycle (week) to a mesocycle |
| `/training/mesocycles/{key}/day-exercises/delete` | Bulk delete exercises from mesocycle days |
| `/training/mesocycles/{key}/notes` | Add a note to a mesocycle |
| `/training/days/{dayId}/exercises` | Add an exercise to a training day |
| `/training/days/{dayId}/exercises/{dayExerciseId}/sets` | Add sets to an exercise |
| `/training/days/{dayId}/notes` | Add a note to a training day |
| `/training/exercises` | Create a custom exercise |
| `/training/exercises/{exerciseId}/notes` | Add a note to an exercise |
| `/training/templates` | Create a training template |
| `/training/track` | Track/log a training event |
| `/training/user-attributes` | Update user attributes |

### Auth / Account

| Endpoint | Description |
|---|---|
| `/login` | Login |
| `/login/link` | Magic link login |
| `/user` | Create/update user |
| `/userReview` | Submit user review |

### Purchases

| Endpoint | Description |
|---|---|
| `/apps/training/{platform}/verifyTransactions` | Verify IAP transactions |
| `/purchase/checkout?redirect={url}` | Start checkout flow |
| `/purchase/complete/{id}` | Complete a purchase |
| `/referrals/enter/{code}?isUserEntry={0\|1}&associateOnly={0\|1}` | Enter a referral code |

## PUT Endpoints

| Endpoint | Description |
|---|---|
| `/training/mesocycles/{key}` | Update mesocycle metadata |
| `/training/mesocycles/{key}/priorities` | Update muscle group priorities |
| `/training/mesocycles/{key}/notes/{noteId}` | Update a mesocycle note |
| `/training/days/{dayId}` | Update a training day |
| `/training/days/{dayId}/bodyweight` | Update bodyweight for a day |
| `/training/days/{dayId}/label` | Update day label |
| `/training/days/{dayId}/exercises/{dayExerciseId}` | Update a day exercise |
| `/training/days/{dayId}/exercises/{dayExerciseId}/move` | Move exercise position within a day |
| `/training/exercises/{id}` | Update an exercise |
| `/training/exercises/{exerciseId}/notes/{noteId}` | Update an exercise note |
| `/training/sets/{setId}` | Update a set (weight, reps, etc.) |
| `/training/templates/{id}` | Update a template |
| `/user/{id}` | Update user profile |

## DELETE Endpoints

| Endpoint | Description |
|---|---|
| `/training/mesocycles/{key}` | Delete a mesocycle |
| `/training/mesocycles/{key}/remove-micro` | Remove a micro-cycle (week) |
| `/training/mesocycles/{key}/notes/{noteId}` | Delete a mesocycle note |
| `/training/days/{dayId}/notes/{noteId}` | Delete a day note |
| `/training/exercises/{id}` | Delete a custom exercise |
| `/training/exercises/{exerciseId}/notes/{noteId}` | Delete an exercise note |
| `/training/sets/{setId}` | Delete a set |
| `/training/templates/{id}` | Delete a template |

## Data Model

### Mesocycle (full detail via `/training/mesocycles/{key}`)

```
mesocycle
├── id, key, userId, name, days, unit, weeks (count)
├── sourceTemplateId, sourceMesoId
├── microRirs
├── timestamps (createdAt, updatedAt, finishedAt, deletedAt)
├── activity timestamps (firstSetCompletedAt, lastWorkoutFinishedAt, etc.)
├── priorities: { muscleGroupId -> { id, muscleGroupId, mgPriorityType } }
├── notes: []
├── status: "complete" | "ready" | ...
├── generatedFrom: string (template name)
└── weeks[]
    └── days[]
        ├── id, mesoId, week, position
        ├── bodyweight, bodyweightAt, unit
        ├── label (e.g. "Saturday")
        ├── finishedAt
        ├── status: "complete" | "skipped" | ...
        ├── notes: []
        ├── muscleGroups: []
        └── exercises[]
            ├── id, dayId, exerciseId, position
            ├── jointPain
            ├── muscleGroupId
            ├── sourceDayExerciseId
            ├── status: "complete" | "skipped" | ...
            └── sets[]
                ├── id, dayExerciseId, position
                ├── setType: "regular" | ...
                ├── weight, weightTarget, weightTargetMin, weightTargetMax
                ├── reps, repsTarget
                ├── bodyweight, unit
                ├── finishedAt
                └── status: "skipped" | ...
```

### Exercise (from `/training/exercises`)

```
exercise
├── id, name
├── muscleGroupId, mgSubType (e.g. "vertical")
├── exerciseType (e.g. "cable", "barbell", "dumbbell", "machine", "bodyweight-only")
├── youtubeId
├── userId (null for built-in, user ID for custom)
├── notes: []
└── timestamps (createdAt, updatedAt, deletedAt)
```

### Exercise History (from `/training/exercises/{id}/history`)

```
[
  {
    name: string,          // mesocycle name
    key: string,           // mesocycle key
    setGroups: [           // grouped by week/day occurrence
      [
        {
          id, dayExerciseId, position,
          setType: "regular",
          weight, weightTarget, weightTargetMin, weightTargetMax,
          reps, repsTarget,
          bodyweight, unit,
          createdAt, finishedAt,
          week, day
        }
      ]
    ]
  }
]
```

### User Profile (from `/user/profile`)

```
user
├── id, email, displayName, photoUrl
├── googleId, appleId, facebookId
├── roleId, stripeId, klaviyoId
├── timestamps (createdAt, updatedAt, firstSeenAt)
└── attributes
    ├── BIRTHDATE, SEX, TRAINING_YEARS
    ├── TRAINING_PREFERENCE_EXERCISE_TYPES (JSON string)
    ├── ATTRIBUTION_SURVEY, CREATED_ON_PLATFORM
    ├── TRAINING_FEATURE_AUTO_APPLY_WEIGHTS
    ├── TRAINING_APPLY_EXERCISE_TYPES
    └── various TRAINING_*_AT timestamps
```

### User Subscriptions (from `/user/subscriptions`)

```
subscriptions
├── activeSubscriptions[]
│   ├── platform, iapId, iapPurchaseType, iapPlatformId, iapName
│   ├── isFreeTrial, isIntroPriced
│   ├── referralId, referralCode, referralType
│   ├── purchaseDate, expirationDate, cancellationDate
│   ├── access: ["training"]
│   └── subscriptionId
├── consumedIaps[]
│   ├── platform, purchaseType, platformId
│   ├── subscriptionGroupId, subscriptionGroupKey
│   ├── access: ["training"]
│   └── accessEndsAt
├── stripeIds: []
└── trainingLastAccessAddedAt
```

## Key Endpoints for Personal Data Export

1. **`GET /user/profile`** - Account info
2. **`GET /user/subscriptions`** - Payment/subscription history
3. **`GET /training/mesocycles`** - List all mesocycle keys
4. **`GET /training/mesocycles/{key}`** - Full workout data per mesocycle (every set with weight/reps/timestamps)
5. **`GET /training/exercises`** - Exercise catalog (to resolve exercise names from IDs)
6. **`GET /training/exercises/{id}/history`** - Per-exercise history across mesocycles
7. **`GET /training/user-exercise-history`** - Last performed timestamp per exercise
8. **`GET /training/templates`** - All templates

Alternatively, **`GET /training/bootstrap`** returns exercises + mesocycle summaries + current mesocycle detail in a single call.
