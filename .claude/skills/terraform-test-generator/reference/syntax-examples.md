# Terraform Test Syntax Examples

## Table of Contents
- [Assert Statement Formatting](#assert-statement-formatting)
- [Mock Provider Patterns](#mock-provider-patterns)
- [Override Patterns](#override-patterns)
- [Command Selection Examples](#command-selection-examples)
- [Variable Handling](#variable-handling)

## Assert Statement Formatting

### Correct Format
All conditions must be on a single line:

```hcl
# Simple condition
assert {
  condition = var.environment != ""
  error_message = "Environment variable must not be empty"
}

# Ternary operator on single line
assert {
  condition = var.iam_role_prefix != "" ? can(regex("^arn:aws:iam::[0-9]+:policy/", data.aws_iam_policy.boundary[0].arn)) : true
  error_message = "Permissions boundary policy ARN should follow expected format"
}

# Multiple conditions with AND
assert {
  condition = length(var.security_group_settings.source_security_groups) >= 2 && length(var.additional_security_group_ids) >= 1
  error_message = "Service mesh should have multiple security groups for different service tiers"
}
```

### Incorrect Format (DO NOT USE)
```hcl
# Wrong: Multi-line condition
assert {
  condition = var.iam_role_prefix != "" ?
    can(regex("^arn:aws:iam::[0-9]+:policy/", data.aws_iam_policy.boundary[0].arn)) :
    true
  error_message = "Error message"
}
```

## Mock Provider Patterns

### AWS Mock Provider

```hcl
# Basic mock
mock_provider "aws" {
  alias = "mock"
}

# Mock with resource defaults
mock_provider "aws" {
  alias = "mock"

  mock_resource "aws_s3_bucket" {
    defaults = {
      id     = "test-bucket-123"
      arn    = "arn:aws:s3:::test-bucket-123"
      region = "us-east-1"
    }
  }
}

# Using in test
run "test_with_mocked_provider" {
  providers = {
    aws = aws.mock
  }

  variables {
    region = "us-east-1"
  }

  assert {
    condition     = aws_instance.main.instance_type == "t3.micro"
    error_message = "Instance type should be t3.micro"
  }
}
```

**For Azure and GCP equivalents, see [cloud-providers.md](cloud-providers.md)**

## Override Patterns

### Critical Rule
Even when using `override_resource` or `override_data`, you MUST define a `mock_provider` and reference it in the `providers` block. Otherwise, Terraform will try to initialize the real provider.

### Correct Override Usage (AWS Example)

```hcl
# At file level
mock_provider "aws" {
  alias = "mock"
}

run "test_with_override" {
  command = plan

  providers = {
    aws = aws.mock  # REQUIRED
  }

  override_data {
    target = data.aws_caller_identity.current
    values = {
      account_id = "123456789012"
      arn        = "arn:aws:iam::123456789012:root"
    }
  }

  override_module {
    target = module.vpc
    outputs = {
      vpc_id             = "vpc-12345678"
      private_subnet_ids = ["subnet-123", "subnet-456"]
    }
  }

  # Test configuration, not computed attributes
  assert {
    condition = length(aws_s3_bucket.main.tags) > 0
    error_message = "Bucket should have tags"
  }
}
```

**For Azure and GCP override patterns, see [cloud-providers.md](cloud-providers.md)**

## Command Selection Examples

### Using `plan` for Configuration Testing

```hcl
run "validate_configuration" {
  command = plan

  variables {
    environment = "test"
  }

  assert {
    condition     = var.environment == "test"
    error_message = "Environment should be set to test"
  }
}
```

### Using `apply` for Resource Testing

```hcl
run "test_bucket_creation" {
  command = apply

  variables {
    bucket_name = "test-bucket"
  }

  assert {
    condition     = aws_s3_bucket.main.id != null
    error_message = "S3 bucket should be created"
  }
}
```

### Using `expect_failures` for Validation Testing

```hcl
run "test_validation_rules" {
  command = plan

  variables {
    instance_count = -1  # Invalid value
  }

  expect_failures = [
    var.instance_count
  ]
}
```

## Variable Handling

### Complete Required Variables

```hcl
run "test_with_all_variables" {
  variables {
    region          = "us-east-1"
    environment     = "test"
    vpc_cidr        = "10.0.0.0/16"
    instance_type   = "t3.micro"
    tags = {
      Environment = "test"
      Project     = "terraform-testing"
    }
  }
}
```

### Complex Variable Structures

```hcl
run "test_complex_variables" {
  variables {
    database_config = {
      engine         = "postgres"
      version        = "13.7"
      instance_class = "db.t3.micro"
      storage_size   = 20
    }

    network_config = {
      vpc_id     = "vpc-12345"
      subnet_ids = ["subnet-123", "subnet-456"]
    }
  }
}
```

## Handling Set-Type Attributes

Many Terraform resource attributes are sets, not lists. You CANNOT use index notation `[0]` on sets.

### Wrong
```hcl
assert {
  condition = aws_s3_bucket_server_side_encryption_configuration.main.rule[0].sse_algorithm == "AES256"
  error_message = "Cannot index a set value"
}
```

### Correct - Use `for` expressions
```hcl
assert {
  condition = length([for rule in aws_s3_bucket_server_side_encryption_configuration.main.rule : rule if length([for default in rule.apply_server_side_encryption_by_default : default if default.sse_algorithm == "AES256"]) > 0]) > 0
  error_message = "Encryption algorithm should be AES256"
}
```

## Meaningful vs Meaningless Tests

### Meaningless (DO NOT DO)
```hcl
variables {
  environment = "dev"
}

assert {
  condition = var.environment == "dev"  # You just set this!
  error_message = "Environment should be dev"
}
```

### Meaningful (DO THIS)
```hcl
variables {
  create_security_group = true
  additional_security_group_ids = ["sg-123"]
}

assert {
  # Tests the LOGIC in: concat([aws_security_group.ec2[0].id], var.additional_security_group_ids)
  condition = var.create_security_group ? length(local.security_group_ids) >= 2 : length(local.security_group_ids) == 1
  error_message = "Security group IDs logic is incorrect"
}
```

**For cloud-specific anti-patterns, see [anti-patterns.md](anti-patterns.md)**
