# Set


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**day_exercise_id** | **int** |  | [optional] 
**position** | **int** |  | [optional] 
**set_type** | **str** |  | [optional] 
**weight** | **float** |  | [optional] 
**weight_target** | **float** |  | [optional] 
**weight_target_min** | **float** |  | [optional] 
**weight_target_max** | **float** |  | [optional] 
**reps** | **int** |  | [optional] 
**reps_target** | **int** |  | [optional] 
**bodyweight** | **float** |  | [optional] 
**unit** | **str** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**status** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 

## Example

```python
from api_service_rp.models.set import Set

# TODO update the JSON string below
json = "{}"
# create an instance of Set from a JSON string
set_instance = Set.from_json(json)
# print the JSON string representation of the object
print(Set.to_json())

# convert the object into a dict
set_dict = set_instance.to_dict()
# create an instance of Set from a dict
set_from_dict = Set.from_dict(set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


