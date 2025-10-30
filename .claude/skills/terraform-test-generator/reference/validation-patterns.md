# Variable Validation Test Patterns

## Table of Contents
- [When to Generate Validation Tests](#when-to-generate-validation-tests)
- [Detection Workflow](#detection-workflow)
- [Common Validation Patterns](#common-validation-patterns)
- [Test Generation Strategy](#test-generation-strategy)

## When to Generate Validation Tests

### CRITICAL REQUIREMENT

`expect_failures` works ONLY with:
1. Variable validation blocks (`validation { }`)
2. Resource/data/output/check preconditions
3. Resource/data/output/check postconditions

`expect_failures` does NOT work with provider-side resource validations.

**Only generate validation tests when the module already has these blocks. Do NOT modify module code.**

### Common Error Pattern

```hcl
# Test file
run "test_empty_name_fails" {
  command = plan
  variables {
    name = ""
  }
  expect_failures = [var.name]  # ← FAILS if no validation block exists
}
```

**Error Message Pattern:**
```
Error: length should equal to or greater than 3, got ""
  with azurerm_postgresql_flexible_server.psql_server

Error: Missing expected failure
  The checkable object, var.name, was expected to report an error but did not.
```

This indicates validation happened at **provider resource level**, not **Terraform validation level**.

## Detection Workflow

### Step 1: Scan for Variable Validations

Look for variables with `validation { }` blocks:

```hcl
variable "name" {
  description = "Server name"
  type        = string

  validation {
    condition     = length(var.name) >= 3
    error_message = "Server name must be at least 3 characters long."
  }
}
```

**Generate test:**
```hcl
run "test_empty_server_name_fails" {
  command = plan

  variables {
    name = ""  # Invalid: fails length >= 3
    # ... all other required variables
  }

  expect_failures = [var.name]
}
```

### Step 2: Scan for Resource Preconditions

Look for `lifecycle { precondition { } }` blocks:

```hcl
resource "azurerm_storage_account" "main" {
  name = var.storage_account_name

  lifecycle {
    precondition {
      condition     = var.enable_encryption == true
      error_message = "Encryption must be enabled."
    }

    precondition {
      condition     = length(var.allowed_ips) > 0
      error_message = "At least one allowed IP required."
    }
  }
}
```

**Generate tests:**
```hcl
run "test_encryption_disabled_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    storage_account_name = "teststorage"
    enable_encryption    = false  # Violates precondition
    allowed_ips          = ["10.0.0.1"]
    # ... other required variables
  }

  expect_failures = [azurerm_storage_account.main]
}

run "test_empty_allowed_ips_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    storage_account_name = "teststorage"
    enable_encryption    = true
    allowed_ips          = []  # Violates precondition
    # ... other required variables
  }

  expect_failures = [azurerm_storage_account.main]
}
```

### Step 3: Scan for Output Preconditions

Look for `precondition { }` blocks in outputs:

```hcl
output "database_endpoint" {
  description = "Database connection endpoint"
  value       = azurerm_postgresql_flexible_server.main.fqdn

  precondition {
    condition     = var.enable_public_access == false
    error_message = "Public access must be disabled."
  }
}
```

**Generate test:**
```hcl
run "test_public_access_enabled_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    name                 = "test-server"
    enable_public_access = true  # Violates output precondition
    # ... other required variables
  }

  expect_failures = [output.database_endpoint]
}
```

### Step 4: Scan for Check Blocks

Look for `check { }` blocks with assertions:

```hcl
check "security_compliance" {
  assert {
    condition     = var.encryption_enabled == true
    error_message = "Encryption must be enabled."
  }

  assert {
    condition     = var.backup_retention_days >= 7
    error_message = "Backup retention must be at least 7 days."
  }
}
```

**Generate tests:**
```hcl
run "test_encryption_compliance_fails" {
  command = plan

  variables {
    encryption_enabled    = false  # Violates check
    backup_retention_days = 7
    # ... other required variables
  }

  expect_failures = [check.security_compliance]
}

run "test_backup_retention_compliance_fails" {
  command = plan

  variables {
    encryption_enabled    = true
    backup_retention_days = 5  # Violates check
    # ... other required variables
  }

  expect_failures = [check.security_compliance]
}
```

### Step 5: Scan for Postconditions

Look for `lifecycle { postcondition { } }` blocks:

**Note:** Postconditions require `command = apply` because they validate after resource creation.

```hcl
resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  lifecycle {
    postcondition {
      condition     = self.versioning[0].enabled == true
      error_message = "S3 bucket versioning must be enabled."
    }
  }
}
```

**Generate test:**
```hcl
run "test_versioning_not_enabled_fails" {
  command = apply  # Postconditions require apply

  providers = {
    aws = aws.mock
  }

  variables {
    bucket_name       = "test-bucket"
    enable_versioning = false  # Causes postcondition to fail
    # ... other required variables
  }

  expect_failures = [aws_s3_bucket.main]
}
```

## Common Validation Patterns

### String Length
```hcl
validation {
  condition     = length(var.name) >= 3
  error_message = "Name must be at least 3 characters long."
}
# Test: name = "" or name = "ab"
```

### Enumerated Values
```hcl
validation {
  condition     = contains(["11", "12", "13", "14"], var.version)
  error_message = "Version must be one of: 11, 12, 13, 14."
}
# Test: version = "999"
```

### Pattern Matching
```hcl
validation {
  condition     = can(regex("^[a-z0-9-]+$", var.name))
  error_message = "Name must contain only lowercase letters, numbers, and hyphens."
}
# Test: name = "INVALID_NAME"
```

### Cross-Variable Dependencies
```hcl
validation {
  condition     = var.workspace_id != null || var.enable_diagnostics == false
  error_message = "Workspace ID required when diagnostics enabled."
}
# Test: enable_diagnostics = true, workspace_id = null
```

### Conditional Requirements
```hcl
lifecycle {
  precondition {
    condition     = var.create_backup ? var.backup_retention_days >= 7 : true
    error_message = "When backups enabled, retention must be at least 7 days."
  }
}
# Test: create_backup = true, backup_retention_days = 3
```

### Security Requirements
```hcl
lifecycle {
  precondition {
    condition     = var.public_access_enabled == false
    error_message = "Public access must be disabled for security compliance."
  }
}
# Test: public_access_enabled = true
```

## Test Generation Strategy

### Scan Phase
1. Parse all `.tf` files in the module
2. Extract all variable declarations and check for `validation { }` blocks
3. Scan all resources/data sources for `lifecycle { precondition { } }` and `lifecycle { postcondition { } }`
4. Scan all outputs for `precondition { }` blocks
5. Scan for standalone `check { }` blocks

### Analysis Phase
For each validation/precondition/postcondition found:
- Parse the condition expression
- Determine what invalid inputs would trigger the validation error
- Extract the error message
- Identify whether it needs `command = plan` or `command = apply`

### Test Generation Phase
- Generate `expect_failures` tests for each identified validation/precondition
- Use `command = plan` for variable validations, preconditions, and check blocks
- Use `command = apply` for postconditions
- Create descriptive test names: `test_<validation_type>_<reason>_fails`

### File Structure
```hcl
# File: tests/validation_variable_constraints.tftest.hcl

mock_provider "azurerm" {
  alias = "mock"
}

# Variable validation test
run "test_name_too_short_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    name = "ab"  # Fails validation
    # ... all other required variables with valid values
  }

  expect_failures = [var.name]
}

# Resource precondition test
run "test_encryption_disabled_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    name              = "valid-name"
    enable_encryption = false  # Fails precondition
    # ... other required variables
  }

  expect_failures = [azurerm_storage_account.main]
}

# Output precondition test
run "test_ssl_not_enforced_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    name            = "valid-name"
    ssl_enforcement = false  # Fails output precondition
    # ... other required variables
  }

  expect_failures = [output.connection_string]
}

# Check block test
run "test_compliance_check_fails" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  variables {
    name               = "valid-name"
    encryption_enabled = false  # Fails check assertion
    # ... other required variables
  }

  expect_failures = [check.security_compliance]
}

# Postcondition test
run "test_versioning_postcondition_fails" {
  command = apply

  providers = {
    aws = aws.mock
  }

  variables {
    bucket_name       = "test-bucket"
    enable_versioning = false  # Fails postcondition
    # ... other required variables
  }

  expect_failures = [aws_s3_bucket.main]
}
```

## Best Practices

**DO Generate Tests When:**
- ✅ Variables have `validation { }` blocks
- ✅ Resources/data sources have `lifecycle { precondition { } }` blocks
- ✅ Outputs have `precondition { }` blocks
- ✅ Check blocks with assertions exist
- ✅ Resources/data/outputs have `lifecycle { postcondition { } }` blocks

**DO NOT Generate Tests When:**
- ❌ Variables have no validation blocks
- ❌ Resources rely only on provider-side validation
- ❌ No preconditions/postconditions/checks exist

**Test Quality:**
- ✅ Always provide ALL required variables in each test
- ✅ Use valid values for non-tested variables to isolate the validation
- ✅ Include provider mocking even for validation tests
- ✅ Use `command = plan` for validations, preconditions, and checks
- ✅ Use `command = apply` for postconditions
- ✅ Test each validation/precondition/postcondition separately
- ❌ Do NOT modify the module code to add validation blocks
