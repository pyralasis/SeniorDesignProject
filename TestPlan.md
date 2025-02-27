# Test Plan Overview

We will be splitting out tests into two major types. Our application is split into a Frontend and a Backend, so we will be splitting our tests into Frontend and Backend tests.

Our Backend tests will largely be composed of API tests. We will directly tests our API endpoints without use of our Frontend. We will test our file management, and integration with Pytorch. We will test our our ability to make Architectures, Pipelines, and Models using Pytorch.

Our Frontend tests will focus on the functionality of the components that make up our Frontend. We will test the functionality our node based editor for Architecture and Pipeline creation as well as our ability to make, train and run Models.



### Test Case 1

- Identifier: backend-json-file-save
- Purpose: Test JSON file saving functionality
- Description: This test will ensure that the JSONFileManager can properly save files.
- Inputs: File Name & Save data
- Expected Outputs/Results: A file will be created on the disk
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 2

- Identifier: backend-json-file-delete
- Purpose: Test JSON file deleting functionality
- Description: This test will ensure that the JSONFileManager can properly delete files.
- Inputs: File Name
- Expected Outputs/Results: A file will be deleted from the disk
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 3

- Identifier: backend-api-invalid-architecture
- Purpose: Test the backend's handling of invalid architecture inputs
- Description: This test will ensure that the backend properly handles and reports errors when invalid architecture data is provided.
- Inputs: Invalid architecture data
- Expected Outputs/Results: An error response indicating the invalid input
- Normal/Abnormal/Boundary: Abnormal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 4

- Identifier: backend-api-create-architecture
- Purpose: Test the backend's ability to create an architecture file using the API.
- Description: This test will ensure that the backend can create and save architecture data.
- Inputs: Valid architecture data
- Expected Outputs/Results: A valid architecture file and successful response.
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 5

- Identifier: backend-api-invalid-pipeline
- Purpose: Test the backend's handling of invalid data pipeline inputs from the API
- Description: This test will ensure that the backend properly handles and reports errors when invalid pipeline data is provided.
- Inputs: Invalid pipeline data
- Expected Outputs/Results: An error response indicating the invalid input
- Normal/Abnormal/Boundary: Abnormal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 6

- Identifier: backend-api-create-model
- Purpose: Tests the backend's ability to create a PyTorch model from an API call.
- Description: This will use the API to create a pytorch model from an architecture file.
- Inputs: An architecture file/id
- Outputs/Results: A valid pytorch model
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration
 
- ### Test Case 7
- Identifier: backend-api-create-pipeline
- Purpose: Test the backend's ability to create a data pipeline using the API.
- Description: This test will ensure that the backend can create and save pipeline data.
- Inputs: Valid pipeline data
- Expected Outputs/Results: A valid pipeline file and successful response.
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 8

- Identifier: backend-registry When a request is made to the api
- Purpose: Tests that values can be saved and retrieved from the Registry class.
- Description: Registers a value to a Registry instance and ensures that it persists.
- Inputs: A registerable value and id normal
- Expected Outputs/Results: The value persists in the registry. blackbox
- Normal/Abnormal/Boundary: Normal functional
- Blackbox/Whitebox: Whitebox
- Functional/Performance: Functional
- Unit/Integration: Unit integration

### Test Case 9

- Identifier: frontend-select-architecture-page-snapshot
- Purpose: Verify the look of the select-architecture remains consistent
- Description: Take a snapshot of the select-architecture and compare it against a master copy to verify that there were no unintended changes made to the visual layout of it.
- Inputs: Playwright simulation instructions to navigate to the page and recreate some expected user interactions.
- Expected Outputs/Results: An image of the select-architecture page that matches our master copy pixel perfectly.
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Unit

### Test Case 10

- Identifier: frontend-home-page-snapshot
- Purpose: Verify the look of the homepage remains consistent
- Description: Take a snapshot of the homepage and compare it against a master copy to verify that there were no unintended changes made to the visual layout of it.
- Inputs: Playwright simulation instructions to navigate to the page and recreate some expected user interactions.
- Expected Outputs/Results: An image of the home page that matches our master copy pixel perfectly.
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Unit

### Test Case 11

- Identifier: frontend-architecture-post-integration-fail
- Purpose: Verify that the frontend correctly handles invalid POST requests to the architecture endpoint.
- Description: Send malformed or incomplete data (e.g., missing required fields) to `/api/architecture` and confirm the frontend properly displays/handles error responses (4xx/5xx).
- Inputs: Invalid JSON body, missing required fields.
- Expected Outputs/Results: 'Failed' response from the backend and proper error handling of a bad response by the front end (reattempt, notify user, etc.)
- Normal/Abnormal/Boundary: Abnormal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Unit

### Test Case 12

- Identifier: frontend-architecture-get-integration-fail
- Purpose: Verify that the frontend correctly handles invalid GET requests to the architecture endpoint.
- Description: Make GET calls to /api/architecture with invalid query parameters, or pointing to non-existent resources, verifying error handling.
- Inputs: Incorrect parameters (?id=invalid), unauthorized credentials, or unreachable endpoint.
- Expected Outputs/Results: Proper error messages on the frontend and no breaking UI behavior
- Normal/Abnormal/Boundary: Abnormal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Unit

### Test Case 13

- Identifier: frontend-architecture-post-integration
- Purpose: Verify that the frontend correctly handles POST requests to the architecture endpoint.
- Description: Trigger a POST to /api/architecture with valid data; confirm 'Success' is returned along with expected fields or values.
- Inputs: Properly formatted JSON payload and necessary headers/authorization.
- Expected Outputs/Results: 'Success' response with expected return values.
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 14

- Identifier: frontend-architecture-get-integration
- Purpose: To test the integration success of the architecture endpoints with the backend
- Description: Make api calls to the backend architecture and verify that the data transform occuring on the frontend produces the expected data structure, with the expected data.
- Inputs: Known backend data, and optional query parameters.
- Expected Outputs/Results: Correctly transformed data matching the expected structure and content.
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Integration

### Test Case 15

- Identifier: frontend-node-creation-snapshot-test
- Purpose: Test that the drag and drop feature that we created as an integration with svelteflow works and produces the expected result within the svelteflow component
- Description:
- Inputs: Playwright drag and drop simulation
- Expected Outputs/Results: Picture of screen showing new node within the svelte flow component
- Normal/Abnormal/Boundary: Normal
- Blackbox/Whitebox: Blackbox
- Functional/Performance: Functional
- Unit/Integration: Unit





# Test Case Matrix
| Identifier                                 	| Normal/Abnormal | Blackbox/Whitebox | Functional/Performance | Unit/Integration |
|-----------------------------------------------|----------------|------------------|----------------------|-----------------|
| backend-json-file-save                    	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| backend-json-file-delete                  	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| backend-api-invalid-architecture          	| Abnormal   	| Blackbox     	| Functional       	| Integration 	|
| backend-api-create-architecture           	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| backend-api-invalid-pipeline              	| Abnormal   	| Blackbox     	| Functional       	| Integration 	|
| backend-api-create-model                  	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| backend-api-create-pipeline               	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| backend-registry                          	| Normal     	| Whitebox     	| Functional       	| Unit        	|
| frontend-select-architecture-page-snapshot	| Normal     	| Blackbox     	| Functional       	| Unit        	|
| frontend-home-page-snapshot               	| Normal     	| Blackbox     	| Functional       	| Unit        	|
| frontend-architecture-post-integration-fail   | Abnormal   	| Blackbox     	| Functional       	| Unit        	|
| frontend-architecture-get-integration-fail	| Abnormal   	| Blackbox     	| Functional       	| Unit        	|
| frontend-architecture-post-integration    	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| frontend-architecture-get-integration     	| Normal     	| Blackbox     	| Functional       	| Integration 	|
| frontend-node-creation-snapshot-test      	| Normal     	| Blackbox     	| Functional       	| Unit        	|


