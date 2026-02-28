from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


def _to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


# --- Sets ---


class Set(BaseModel):
    id: int
    day_exercise_id: int
    position: int
    set_type: str
    weight: float | None = None
    weight_target: float | None = None
    weight_target_min: float | None = None
    weight_target_max: float | None = None
    reps: int | None = None
    reps_target: int | None = None
    bodyweight: float | None = None
    unit: str
    created_at: datetime
    finished_at: datetime | None = None
    status: str | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class HistorySet(BaseModel):
    id: int
    day_exercise_id: int
    position: int
    set_type: str
    weight: float | None = None
    weight_target: float | None = None
    weight_target_min: float | None = None
    weight_target_max: float | None = None
    reps: int | None = None
    reps_target: int | None = None
    bodyweight: float | None = None
    unit: str
    created_at: datetime
    finished_at: datetime | None = None
    week: int
    day: int

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Exercises ---


class Note(BaseModel):
    id: int | None = None
    text: str | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class DayExercise(BaseModel):
    id: int
    day_id: int
    exercise_id: int
    position: int
    joint_pain: int | None = None
    muscle_group_id: int
    source_day_exercise_id: int | None = None
    created_at: datetime
    updated_at: datetime
    sets: list[Set] = []
    status: str | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class Exercise(BaseModel):
    id: int
    name: str
    muscle_group_id: int
    youtube_id: str | None = None
    exercise_type: str
    user_id: int | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    mg_sub_type: str | None = None
    notes: list[Note] = []

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Days ---


class MuscleGroup(BaseModel):
    id: int | None = None
    name: str | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class Day(BaseModel):
    id: int
    meso_id: int
    week: int
    position: int
    created_at: datetime
    updated_at: datetime | None = None
    bodyweight: float | None = None
    bodyweight_at: datetime | None = None
    unit: str | None = None
    finished_at: datetime | None = None
    label: str | None = None
    notes: list[Note] = []
    exercises: list[DayExercise] = []
    muscle_groups: list[MuscleGroup] = []
    status: str | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class Week(BaseModel):
    days: list[Day]


# --- Mesocycles ---


class MgPriority(BaseModel):
    id: int
    muscle_group_id: int
    mg_priority_type: str

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class MesocycleSummary(BaseModel):
    id: int
    key: str
    user_id: int
    name: str
    days: int
    unit: str
    source_template_id: int | None = None
    source_meso_id: int | None = None
    micro_rirs: int | None = None
    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None = None
    deleted_at: datetime | None = None
    first_micro_completed_at: datetime | None = None
    first_workout_completed_at: datetime | None = None
    first_exercise_completed_at: datetime | None = None
    first_set_completed_at: datetime | None = None
    last_micro_finished_at: datetime | None = None
    last_set_completed_at: datetime | None = None
    last_set_skipped_at: datetime | None = None
    last_workout_completed_at: datetime | None = None
    last_workout_finished_at: datetime | None = None
    last_workout_skipped_at: datetime | None = None
    last_workout_partialed_at: datetime | None = None
    weeks: int
    notes: list[Note] = []

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class MesocycleDetail(BaseModel):
    id: int
    key: str
    user_id: int
    name: str
    days: int
    unit: str
    source_template_id: int | None = None
    source_meso_id: int | None = None
    micro_rirs: int | None = None
    created_at: datetime
    updated_at: datetime
    finished_at: datetime | None = None
    deleted_at: datetime | None = None
    first_micro_completed_at: datetime | None = None
    first_workout_completed_at: datetime | None = None
    first_exercise_completed_at: datetime | None = None
    first_set_completed_at: datetime | None = None
    last_micro_finished_at: datetime | None = None
    last_set_completed_at: datetime | None = None
    last_set_skipped_at: datetime | None = None
    last_workout_completed_at: datetime | None = None
    last_workout_finished_at: datetime | None = None
    last_workout_skipped_at: datetime | None = None
    last_workout_partialed_at: datetime | None = None
    weeks: list[Week]
    notes: list[Note] = []
    status: str | None = None
    generated_from: str | None = None
    priorities: dict[str, MgPriority] = {}

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Templates ---


class TemplateSummary(BaseModel):
    id: int
    key: str
    name: str
    emphasis: str | None = None
    sex: str | None = None
    user_id: int | None = None
    source_template_id: int | None = None
    source_meso_id: int | None = None
    prev_template_id: int | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    frequency: int | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Exercise History ---


class ExerciseHistoryEntry(BaseModel):
    name: str
    key: str
    set_groups: list[list[HistorySet]]

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- User ---


class UserAttributes(BaseModel):
    training_years: str | None = None
    training_preference_exercise_types: str | None = None
    attribution_survey: str | None = None
    created_on_platform: str | None = None
    birthdate: str | None = None
    sex: str | None = None
    training_feature_auto_apply_weights: bool | None = None
    training_apply_exercise_types: bool | None = None
    training_acc_last_finished_at: str | None = None
    training_day_last_finished_at: str | None = None
    training_last_access_added_at: str | None = None
    training_last_activity: str | None = None
    training_meso_last_created_at: str | None = None
    training_meso_last_finished_at: str | None = None
    training_acc_first_finished_at: str | None = None
    training_day_first_finished_at: str | None = None
    training_meso_first_created_at: str | None = None
    training_meso_first_finished_at: str | None = None
    training_has_seen_exercise_chooser_guide: bool | None = None
    training_has_seen_board_guide: bool | None = None
    training_has_completed_onboarding: bool | None = None
    training_has_seen_templates_guide: bool | None = None

    model_config = {
        "alias_generator": lambda s: s.upper(),
        "populate_by_name": True,
        "extra": "allow",
    }


class UserProfile(BaseModel):
    id: int
    email: str
    display_name: str
    photo_url: str | None = None
    apple_id: str | None = None
    facebook_id: str | None = None
    google_id: str | None = None
    migrated_firebase_id: str | None = None
    role_id: int
    klaviyo_id: str | None = None
    stripe_id: str | None = None
    created_at: datetime
    updated_at: datetime
    first_seen_at: datetime | None = None
    attributes: UserAttributes = UserAttributes()

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Subscriptions ---


class ActiveSubscription(BaseModel):
    platform: str
    iap_id: int
    iap_purchase_type: str
    iap_platform_id: str
    iap_name: str
    is_free_trial: bool
    is_intro_priced: bool
    referral_id: int | None = None
    referral_code: str | None = None
    referral_type: str | None = None
    purchase_date: datetime
    expiration_date: datetime | None = None
    cancellation_date: datetime | None = None
    access: list[str] = []
    subscription_id: str | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class ConsumedIap(BaseModel):
    platform: str
    purchase_type: str
    platform_id: str
    subscription_group_id: str | None = None
    subscription_group_key: str | None = None
    access: list[str] = []
    access_ends_at: datetime | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


class UserSubscriptions(BaseModel):
    active_subscriptions: list[ActiveSubscription] = []
    consumed_iaps: list[ConsumedIap] = []
    stripe_ids: list[str] = []
    training_last_access_added_at: datetime | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Bootstrap ---


class BootstrapResponse(BaseModel):
    exercises: list[Exercise]
    mesocycles: list[MesocycleSummary]
    current_mesocycle: MesocycleDetail | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


# --- Second Meso Meta ---


class SecondMesoMeta(BaseModel):
    key: str
    started_at: datetime | None = None

    model_config = {"alias_generator": lambda s: _to_camel(s), "populate_by_name": True}


