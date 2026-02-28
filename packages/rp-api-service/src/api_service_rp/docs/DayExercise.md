# DayExercise


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**day_id** | **str** |  | [optional] 
**exercise_id** | **str** |  | [optional] 
**position** | **int** |  | [optional] 
**joint_pain** | **bool** |  | [optional] 
**muscle_group_id** | **str** |  | [optional] 
**source_day_exercise_id** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**sets** | [**List[Set]**](Set.md) |  | [optional] 

## Example

```python
from api_service_rp.models.day_exercise import DayExercise

# TODO update the JSON string below
json = "{}"
# create an instance of DayExercise from a JSON string
day_exercise_instance = DayExercise.from_json(json)
# print the JSON string representation of the object
print(DayExercise.to_json())

# convert the object into a dict
day_exercise_dict = day_exercise_instance.to_dict()
# create an instance of DayExercise from a dict
day_exercise_from_dict = DayExercise.from_dict(day_exercise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


