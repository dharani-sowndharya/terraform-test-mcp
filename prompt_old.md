* Ignore the cache from all the previous chat and start fresh 
* Fetch content from https://developer.hashicorp.com/terraform/language/ for the correct Terraform syntax
* Fetch content from https://developer.hashicorp.com/terraform/language/tests for the correct test syntax and mock syntax. Use overrides where necessary. 
* Fetch content from https://developer.hashicorp.com/terraform/language/tests/mocking#overrides 
* Based on the content from above, create a prompt to write test cases for terraform files using the correct syntax that is mentioned in the docs. Use few shot prompting to generate accurate results. Store the prompt you create under folder shared by user
* Generate test cases for the terraform files located under user provided folder* For the sample values to variables refer the tfvars present in user provided folder
* The prompt should cross verify if the generated files are following the correct terraform syntax and prompt me if you are not sure instead of hallucinating so that I can supply more content that might help 
* Generate integration tests that creates actual infrastructure without mocks that uses 'command = apply' and place them on a separate file. Generate dummy value for the variables. The user will go and change the values that will work 
* Generate unit tests, integration tests, mock tests and give me a coverage report indicating the code that is covered with the test cases you are generating as a table 
* Coverage report should show the coverage percent in details and talks about what is missing as part of these tests. 
* Use 'tftest' as the value for the environment variable 
* Update the README.md with all the relevant details collected for running the test suite