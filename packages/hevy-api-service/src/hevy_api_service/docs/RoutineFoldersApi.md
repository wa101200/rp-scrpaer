# hevy_api_service.RoutineFoldersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_routine_folder**](RoutineFoldersApi.md#create_routine_folder) | **POST** /v1/routine_folders | Create a new routine folder. The folder will be created at index 0, and all other folders will have their indexes incremented.
[**get_routine_folder_by_id**](RoutineFoldersApi.md#get_routine_folder_by_id) | **GET** /v1/routine_folders/{folderId} | Get a single routine folder by id.
[**get_routine_folders**](RoutineFoldersApi.md#get_routine_folders) | **GET** /v1/routine_folders | Get a paginated list of routine folders available on the account.


# **create_routine_folder**
> RoutineFolder create_routine_folder(api_key, post_routine_folder_request_body)

Create a new routine folder. The folder will be created at index 0, and all other folders will have their indexes incremented.



### Example

```python
import time
import os
import hevy_api_service
from hevy_api_service.models.post_routine_folder_request_body import PostRoutineFolderRequestBody
from hevy_api_service.models.routine_folder import RoutineFolder
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutineFoldersApi(api_client)
    api_key = 'api_key_example' # str | 
    post_routine_folder_request_body = hevy_api_service.PostRoutineFolderRequestBody() # PostRoutineFolderRequestBody | 

    try:
        # Create a new routine folder. The folder will be created at index 0, and all other folders will have their indexes incremented.
        api_response = api_instance.create_routine_folder(api_key, post_routine_folder_request_body)
        print("The response of RoutineFoldersApi->create_routine_folder:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutineFoldersApi->create_routine_folder: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **str**|  | 
 **post_routine_folder_request_body** | [**PostRoutineFolderRequestBody**](PostRoutineFolderRequestBody.md)|  | 

### Return type

[**RoutineFolder**](RoutineFolder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The routine folder was successfully created |  -  |
**400** | Invalid request body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_routine_folder_by_id**
> RoutineFolder get_routine_folder_by_id(api_key, folder_id)

Get a single routine folder by id.



### Example

```python
import time
import os
import hevy_api_service
from hevy_api_service.models.routine_folder import RoutineFolder
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutineFoldersApi(api_client)
    api_key = 'api_key_example' # str | 
    folder_id = 'folder_id_example' # str | The id of the routine folder

    try:
        # Get a single routine folder by id.
        api_response = api_instance.get_routine_folder_by_id(api_key, folder_id)
        print("The response of RoutineFoldersApi->get_routine_folder_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutineFoldersApi->get_routine_folder_by_id: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **str**|  | 
 **folder_id** | **str**| The id of the routine folder | 

### Return type

[**RoutineFolder**](RoutineFolder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Routine folder not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_routine_folders**
> GetRoutineFolders200Response get_routine_folders(api_key, page=page, page_size=page_size)

Get a paginated list of routine folders available on the account.



### Example

```python
import time
import os
import hevy_api_service
from hevy_api_service.models.get_routine_folders200_response import GetRoutineFolders200Response
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.RoutineFoldersApi(api_client)
    api_key = 'api_key_example' # str | 
    page = 1 # int | Page number (Must be 1 or greater) (optional) (default to 1)
    page_size = 5 # int | Number of items on the requested page (Max 10) (optional) (default to 5)

    try:
        # Get a paginated list of routine folders available on the account.
        api_response = api_instance.get_routine_folders(api_key, page=page, page_size=page_size)
        print("The response of RoutineFoldersApi->get_routine_folders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutineFoldersApi->get_routine_folders: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **str**|  | 
 **page** | **int**| Page number (Must be 1 or greater) | [optional] [default to 1]
 **page_size** | **int**| Number of items on the requested page (Max 10) | [optional] [default to 5]

### Return type

[**GetRoutineFolders200Response**](GetRoutineFolders200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paginated list of routine folders |  -  |
**400** | Invalid page size |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

