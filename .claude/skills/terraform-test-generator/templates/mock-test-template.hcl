# Mock Test Template with Overrides
# File naming: mock_<feature_name>.tftest.hcl

# Define mock provider at file level
mock_provider "aws" {
  alias = "mock"
}

# Test: <Describe what data source or module is being mocked>
run "test_with_mocked_data_source" {
  command = plan

  providers = {
    aws = aws.mock  # REQUIRED even with overrides
  }

  # Override data source values
  override_data {
    target = data.aws_caller_identity.current
    values = {
      account_id = "123456789012"
      arn        = "arn:aws:iam::123456789012:root"
      user_id    = "AIDACKCEVSQ6C2EXAMPLE"
    }
  }

  variables {
    # Provide ALL required variables
    environment = "test"
    region      = "us-east-1"
    # ... all other required variables
  }

  assert {
    # Test that module uses the mocked data correctly
    condition     = var.environment == "test"
    error_message = "Environment should be test"
  }
}

# Test: <Mock module outputs>
run "test_with_mocked_module" {
  command = plan

  providers = {
    aws = aws.mock
  }

  # Override module outputs
  override_module {
    target = module.vpc
    outputs = {
      vpc_id             = "vpc-12345678"
      private_subnet_ids = ["subnet-123", "subnet-456"]
      public_subnet_ids  = ["subnet-789", "subnet-012"]
    }
  }

  variables {
    environment = "test"
    region      = "us-east-1"
    # ... all required variables
  }

  assert {
    # Test that resources use mocked module outputs
    condition     = length(var.environment) > 0
    error_message = "Should use module outputs"
  }
}

# Test: <Mock resource with specific values>
run "test_with_mocked_resource" {
  command = plan

  providers = {
    aws = aws.mock
  }

  override_resource {
    target = aws_s3_bucket.dependency
    values = {
      id     = "mocked-bucket-id"
      arn    = "arn:aws:s3:::mocked-bucket"
      region = "us-east-1"
    }
  }

  variables {
    environment = "test"
    region      = "us-east-1"
    # ... all required variables
  }

  assert {
    # Test configuration that depends on mocked resource
    # Still test configuration, not computed attributes
    condition     = length(aws_s3_bucket_policy.main) > 0
    error_message = "Bucket policy should be configured"
  }
}
