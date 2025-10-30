# Integration Test Template
# File naming: integration_<feature_name>.tftest.hcl
# Note: Integration tests use command = apply and test real resource creation

# Test: <Describe the integration scenario>
run "test_<feature_name>_integration" {
  command = apply  # Integration tests use apply, not plan

  variables {
    # Provide ALL required variables
    # Use realistic values that match tfvars
    environment = "test"
    region      = "us-east-1"
    # ... add all other required variables
  }

  assert {
    # Can test computed attributes with apply
    condition     = aws_s3_bucket.main.id != null
    error_message = "S3 bucket should be created with valid ID"
  }

  assert {
    # Test resource outputs
    condition     = aws_s3_bucket.main.arn != ""
    error_message = "S3 bucket should have valid ARN"
  }
}

# Test: <Verify outputs work correctly>
run "test_outputs" {
  command = apply

  variables {
    environment = "test"
    region      = "us-east-1"
    # ... all required variables
  }

  assert {
    condition     = output.bucket_name != ""
    error_message = "Bucket name output should be set"
  }

  assert {
    condition     = output.bucket_arn != ""
    error_message = "Bucket ARN output should be set"
  }
}

# Test: <Verify idempotency>
run "first_apply" {
  command = apply

  variables {
    environment = "test"
    region      = "us-east-1"
    # ... all required variables
  }
}

run "verify_idempotent" {
  command = plan

  assert {
    condition     = length(plan.resource_changes) == 0
    error_message = "Configuration should be idempotent - no changes on second plan"
  }
}
