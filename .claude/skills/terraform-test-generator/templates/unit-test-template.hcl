# Unit Test Template
# File naming: unit_<feature_name>.tftest.hcl

# Define mock provider at file level (replace with azurerm or google as needed)
mock_provider "aws" {
  alias = "mock"
}

# Test: <Describe what this test validates>
run "test_<feature_name>" {
  command = plan

  providers = {
    aws = aws.mock  # Use aws.mock, azurerm.mock, or google.mock
  }

  variables {
    # Provide ALL required variables
    # Use realistic values that match tfvars
    environment = "test"
    region      = "us-east-1"
    # ... add all other required variables
  }

  assert {
    # Test configuration, conditional logic, or computed locals
    # Do NOT test computed resource attributes with plan
    condition     = var.environment == "test"
    error_message = "Environment should be test"
  }

  assert {
    # Test resource configuration structure
    condition     = length(aws_instance.main) > 0
    error_message = "Instance should be created"
  }
}

# Test: <Another unit test scenario>
run "test_<another_feature>" {
  command = plan

  providers = {
    aws = aws.mock
  }

  variables {
    # Different variable values to test edge cases
    environment = "prod"
    region      = "us-west-2"
    # ... all required variables
  }

  assert {
    condition     = aws_instance.main.instance_type == "t3.micro"
    error_message = "Instance type should be t3.micro"
  }
}
