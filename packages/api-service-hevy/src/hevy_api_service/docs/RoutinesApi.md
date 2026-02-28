# hevy_api_service.RoutinesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_routine**](RoutinesApi.md#create_routine) | **POST** /v1/routines | Create a new routine
[**get_routine_by_id**](RoutinesApi.md#get_routine_by_id) | **GET** /v1/routines/{routineId} | Get a routine by its Id
[**get_routines**](RoutinesApi.md#get_routines) | **GET** /v1/routines | Get a paginated list of routines
[**update_routine**](RoutinesApi.md#update_routine) | **PUT** /v1/routines/{routineId} | Update an existing routine


# **create_routine**
> Routine create_routine(api_key, post_routines_request_body)

Create a new routine

### Example


```python
import hevy_api_service
from hevy_api_service.models.post_routines_request_body import PostRoutinesRequestBody
from hevy_api_service.models.routine import Routine
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutinesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    post_routines_request_body = hevy_api_service.PostRoutinesRequestBody() # PostRoutinesRequestBody | 

    try:
        # Create a new routine
        api_response = await api_instance.create_routine(api_key, post_routines_request_body)
        print("The response of RoutinesApi->create_routine:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutinesApi->create_routine: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **post_routines_request_body** | [**PostRoutinesRequestBody**](PostRoutinesRequestBody.md)|  | 

### Return type

[**Routine**](Routine.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The routine was successfully created |  -  |
**400** | Invalid request body |  -  |
**403** | Routine limit exceeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_routine_by_id**
> GetRoutineById200Response get_routine_by_id(api_key, routine_id)

Get a routine by its Id

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_routine_by_id200_response import GetRoutineById200Response
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutinesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    routine_id = 'routine_id_example' # str | The id of the routine

    try:
        # Get a routine by its Id
        api_response = await api_instance.get_routine_by_id(api_key, routine_id)
        print("The response of RoutinesApi->get_routine_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutinesApi->get_routine_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **routine_id** | **str**| The id of the routine | 

### Return type

[**GetRoutineById200Response**](GetRoutineById200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The routine with the provided id |  -  |
**400** | Invalid request body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_routines**
> GetRoutines200Response get_routines(api_key, page=page, page_size=page_size)

Get a paginated list of routines

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_routines200_response import GetRoutines200Response
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutinesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    page = 1 # int | Page number (Must be 1 or greater) (optional) (default to 1)
    page_size = 5 # int | Number of items on the requested page (Max 10) (optional) (default to 5)

    try:
        # Get a paginated list of routines
        api_response = await api_instance.get_routines(api_key, page=page, page_size=page_size)
        print("The response of RoutinesApi->get_routines:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutinesApi->get_routines: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **page** | **int**| Page number (Must be 1 or greater) | [optional] [default to 1]
 **page_size** | **int**| Number of items on the requested page (Max 10) | [optional] [default to 5]

### Return type

[**GetRoutines200Response**](GetRoutines200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paginated list of routines |  -  |
**400** | Invalid page size |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_routine**
> Routine update_routine(api_key, routine_id, put_routines_request_body)

Update an existing routine

### Example


```python
import hevy_api_service
from hevy_api_service.models.put_routines_request_body import PutRoutinesRequestBody
from hevy_api_service.models.routine import Routine
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutinesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    routine_id = 'routine_id_example' # str | The id of the routine
    put_routines_request_body = hevy_api_service.PutRoutinesRequestBody() # PutRoutinesRequestBody | 

    try:
        # Update an existing routine
        api_response = await api_instance.update_routine(api_key, routine_id, put_routines_request_body)
        print("The response of RoutinesApi->update_routine:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutinesApi->update_routine: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **routine_id** | **str**| The id of the routine | 
 **put_routines_request_body** | [**PutRoutinesRequestBody**](PutRoutinesRequestBody.md)|  | 

### Return type

[**Routine**](Routine.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The routine was successfully updated |  -  |
**400** | Invalid request body |  -  |
**404** | Routine doesn&#39;t exist or doesn&#39;t belong to the user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

