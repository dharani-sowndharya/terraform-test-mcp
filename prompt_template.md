# Terraform Test Case Generator MCP Prompt

## 📋 MANDATORY TODO LIST - COMPLETE IN ORDER

**You MUST use the TodoWrite tool to create and manage this exact checklist:**

```
1. [pending] Collect tfvars file contents from user
2. [pending] Collect compliance requirements from user
3. [pending] Read and analyze Terraform files
4. [pending] Detect cloud provider(s) from Terraform files (AWS/Azure/GCP)
5. [pending] Refer to terraform test documentation links to understand the terraform test syntax
6. [pending] **CRITICAL** - Read and internalize STEP 4 (Syntax Examples). Test cases must follow good example patterns only
7. [pending] Refer to the list of valid test cases for ideas
8. [pending] Refer to the Command Selection Logic Table for clarity on command use cases
9. [pending] Generate unit tests with mock providers (verify against Step 4 patterns)
10. [pending] Generate integration tests with real providers (verify against Step 4 patterns)
11. [pending] Generate mock tests with override patterns (verify against Step 4 patterns)
12. [pending] Generate variable validation tests with expect_failures (verify against Step 4 patterns)
13. [pending] Create coverage report
14. [pending] Create README documentation
15. [pending] Use the Best Practices Checklist to verify generated test cases
16. [pending] Use the MANDATORY COMPLETION CHECKLIST to verify all components
```

**🚫 NEVER mark a TODO as completed until you have FULLY finished that step**
**🚫 NEVER skip ahead to later TODOs without completing earlier ones**
**📖 ALWAYS follow the detailed instructions provided in this template for each step**

## ⚠️ STEP 1: MANDATORY USER INFORMATION COLLECTION ⚠️

### 🛑 COLLECT THESE REQUIREMENTS FIRST:

1. **tfvars File** (REQUIRED):
   - Ask the user: "Please provide your .tfvars file contents or sample variable values"
   - Ask for: file path OR copy/paste the variable assignments
   - Use these values in ALL test cases for realistic testing
   - Example request: "I need your terraform.tfvars values like:
     ```
     region = "eu-west-1"
     environment = "prod"
     vpc_name = "my-production-vpc"
     ```"

2. **Compliance Requirements** (REQUIRED):
   - Ask the user: "What compliance requirements should I include in the tests?"
   - Request specific examples like:
     - "All resources must have mandatory tags: Environment, Project, Owner"
     - "KMS encryption must be enabled for all storage resources"
     - "IAM roles must use permissions boundaries"
     - "Security groups must not allow unrestricted access (0.0.0.0/0)"
   - If user says "none", use standard security best practices

3. **Terraform Code Path Validation** (AUTO-HANDLED):
   - Path is provided by the MCP: {terraform_code_path}

### 🚫 DO NOT PROCEED WITHOUT THIS INFORMATION

If the user has not provided tfvars and compliance requirements:
```
❌ MISSING REQUIRED INFORMATION ❌

I need the following before generating tests:

1. **tfvars values**: Please provide your variable values or .tfvars file content
2. **Compliance requirements**: What security/compliance checks should I include?

Please provide this information so I can create comprehensive, realistic test cases.
```

## ⚠️ STEP 2: TERRAFORM CODE ANALYSIS ⚠️

**ONLY AFTER collecting user requirements above:**

### Input Processing
```hcl
# Path for Terraform code to be tested will be provided here
{terraform_code_path}
```

### Analysis Tasks
- Read and analyze all .tf files in the specified folder
- **Detect cloud provider(s)** from `required_providers` and `provider` blocks:
  - AWS: Look for `provider "aws"` or `source = "hashicorp/aws"`
  - Azure: Look for `provider "azurerm"` or `source = "hashicorp/azurerm"`
  - GCP: Look for `provider "google"` or `source = "hashicorp/google"`
  - **Note:** Multiple providers may exist in the same project (multi-cloud)
- Understand resources, modules, variables, data sources, and their relationships
- Identify key components that need testing coverage
- Map variable requirements to collected tfvars values
- Identify compliance requirements based on user specifications and detected cloud provider(s)
- **Adapt all subsequent test generation** based on detected provider(s)

## ⚠️ STEP 3: SEQUENTIAL TEST GENERATION ⚠️

**ONLY AFTER completing Steps 1 and 2:**

## Role Definition
You are an expert Terraform test case generator specializing in creating comprehensive, syntactically correct test suites following HashiCorp's official testing standards.

## Core Requirements

### 1. Documentation References

**Core Terraform Testing (Provider-Agnostic):**
- **Primary Reference for terraform syntax**: Fetch latest syntax from `https://developer.hashicorp.com/terraform/language/`
- **Terraform Testing Documentation**: Use `https://developer.hashicorp.com/terraform/language/tests` for test and mock syntax
- **Mocking**: Use `https://developer.hashicorp.com/terraform/language/tests/mocking`
- **Override Patterns**: Reference `https://developer.hashicorp.com/terraform/language/tests/mocking#overrides`
- **terraform test command**: Use `https://developer.hashicorp.com/terraform/cli/commands/test`
- **Terraform Test tutorial**: Use `https://developer.hashicorp.com/terraform/tutorials/configuration-language/test`

**Cloud Provider Documentation:**
- **AWS Provider**: `https://registry.terraform.io/providers/hashicorp/aws/latest/docs`
- **Azure Provider (AzureRM)**: `https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs`
- **GCP Provider (Google)**: `https://registry.terraform.io/providers/hashicorp/google/latest/docs`

### 2. File Management
- Create all test files inside a `tests` folder using the `filesystem` MCP
- Organize tests by type (unit, integration, mock)
- Generate accompanying documentation

**DO NOT RETURN PARTIAL RESULTS** - Only complete test suites are acceptable.

### 1. Unit Tests
**Specifications:**
- Mock each resource individually
- Use `'tftest'` as environment variable value
- Include proper mock overrides
- Test resource isolation and configuration
- **FILE NAMING**: `unit_*.tftest.hcl`
- **CHECKPOINT**: Must include provider-specific mock blocks:
  - AWS: `mock_provider "aws"`
  - Azure: `mock_provider "azurerm"`
  - GCP: `mock_provider "google"`

### 2. Integration Tests
**Specifications:**
- Use `command = apply` for actual infrastructure testing
- No mocks - test real resource creation
- Provide sensible dummy values for variables
- Separate files for each integration test scenario
- **FILE NAMING**: `integration_*.tftest.hcl`
- **CHECKPOINT**: Must include real provider blocks (not mock_provider):
  - AWS: `provider "aws"`
  - Azure: `provider "azurerm"`
  - GCP: `provider "google"`
- **CHECKPOINT**: Must use `command = apply` (not plan)

### 3. Mock Tests
**Specifications:**
- Follow official Terraform mocking syntax
- Test resource configurations and dependencies
- Validate input parameters and outputs
- Mock external data sources appropriately

### 4. Variable Validation Tests
**Specifications:**
- Use `expect_failures` to test invalid inputs
- Test all variable validation rules
- Verify type constraints work correctly
- Test edge cases and boundary conditions

### 5. Coverage Report
**Format:** Simple markdown table listing what was tested:
| Test File | Resources/Components Tested | Test Type |
|-----------|----------------------------|-----------|

**Instructions:**
- List each generated test file name
- Note which resources, modules, or variables each test covers
- Indicate test type (unit/integration/mock/validation)
- Keep it simple - just document what tests exist
- DO NOT calculate coverage percentages
- DO NOT perform complex analysis

### 6. README Documentation
**Required Sections:**
- Test suite execution instructions
- Directory structure explanation
- Prerequisites and environment setup
- Variable configuration guidelines
- Example test commands

## ⚠️ STEP 4: Comprehensive Syntax Examples ⚠️

### COMMAND vs RESOURCE ACCESS RULES (CRITICAL)

**NEVER TEST COMPUTED RESOURCE ATTRIBUTES WITH `command = plan`**

THE MOST COMMON MISTAKE - NEVER DO THIS (applies to ALL cloud providers):

**AWS Example:**
```hcl
run "test_security_group" {
  command = plan  # ← Plan cannot access computed attributes!

  assert {
    condition = aws_security_group.lambda_sg.name_prefix == "test"  # ← FAILS!
    error_message = "This will always fail with plan command"
  }
}

run "test_caller_identity" {
  command = plan  # ← Plan cannot access computed attributes!

  assert {
    condition     = data.aws_caller_identity.current.account_id == "123456789012"  # ← FAILS!
    error_message = "This will always fail with plan command"
  }
}
```

**Azure Example:**
```hcl
run "test_storage_account" {
  command = plan  # ← Plan cannot access computed attributes!

  assert {
    condition = azurerm_storage_account.main.id != null  # ← FAILS!
    error_message = "This will always fail with plan command"
  }
}

run "test_client_config" {
  command = plan  # ← Plan cannot access computed attributes!

  assert {
    condition = data.azurerm_client_config.current.subscription_id != ""  # ← FAILS!
    error_message = "This will always fail with plan command"
  }
}
```

**GCP Example:**
```hcl
run "test_storage_bucket" {
  command = plan  # ← Plan cannot access computed attributes!

  assert {
    condition = google_storage_bucket.main.self_link != ""  # ← FAILS!
    error_message = "This will always fail with plan command"
  }
}

run "test_project" {
  command = plan  # ← Plan cannot access computed attributes!

  assert {
    condition = data.google_project.current.number != ""  # ← FAILS!
    error_message = "This will always fail with plan command"
  }
}
```

**Why this fails:** Computed attributes like `.id`, `.arn` (AWS), `.id` (Azure), `.self_link` (GCP) are only available after resource creation (apply), not during planning.

**CRITICAL: Even with mock_provider, certain attributes are computed at plan time:**

WRONG - NEVER DO THIS (even with mocks):

**AWS Example:**
```hcl
run "test_encryption" {
  command = plan

  providers = {
    aws = aws.mock
  }

  assert {
    # ❌ FAILS: .bucket references aws_s3_bucket.main.id which is computed
    condition = aws_s3_bucket_server_side_encryption_configuration.main.bucket != null
    error_message = "This will fail - bucket attribute is computed"
  }

  assert {
    # ❌ FAILS: Cannot check null on string attributes that reference computed values
    condition = aws_s3_bucket_server_side_encryption_configuration.main.bucket != ""
    error_message = "This will also fail - bucket is computed from main.id"
  }
}
```

**Azure Example:**
```hcl
run "test_network_security_rule" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  assert {
    # ❌ FAILS: .resource_group_name references azurerm_resource_group.main.name which is computed
    condition = azurerm_network_security_rule.main.resource_group_name != ""
    error_message = "This will fail - resource_group_name is computed"
  }
}
```

**GCP Example:**
```hcl
run "test_compute_disk" {
  command = plan

  providers = {
    google = google.mock
  }

  assert {
    # ❌ FAILS: .self_link is computed
    condition = google_compute_disk.main.self_link != ""
    error_message = "This will fail - self_link is computed"
  }
}
```

CORRECT - Test configuration, not computed references:

**AWS Example:**
```hcl
run "test_encryption" {
  command = plan

  providers = {
    aws = aws.mock
  }

  assert {
    # ✅ CORRECT: Check the configuration exists
    condition = length(aws_s3_bucket_server_side_encryption_configuration.main.rule) > 0
    error_message = "Encryption configuration should be present"
  }

  assert {
    # ✅ CORRECT: Check configuration values using for expressions (rule is a set)
    condition = length([for rule in aws_s3_bucket_server_side_encryption_configuration.main.rule : rule if length([for default in rule.apply_server_side_encryption_by_default : default if default.sse_algorithm == "AES256"]) > 0]) > 0
    error_message = "Encryption algorithm should be AES256"
  }
}
```

**Azure Example:**
```hcl
run "test_network_security_rule" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  assert {
    # ✅ CORRECT: Test the configuration value directly
    condition = azurerm_network_security_rule.main.priority >= 100 && azurerm_network_security_rule.main.priority <= 4096
    error_message = "NSG rule priority should be between 100 and 4096"
  }
}
```

**GCP Example:**
```hcl
run "test_compute_disk" {
  command = plan

  providers = {
    google = google.mock
  }

  assert {
    # ✅ CORRECT: Test the configuration value directly
    condition = google_compute_disk.main.type == "pd-ssd"
    error_message = "Disk type should be pd-ssd"
  }
}
```

CORRECT - Test variables and locals:
```hcl
run "test_variables" {
  command = plan

  assert {
    condition = var.environment != ""  # ← Variables/locals only!
    error_message = "Environment must be set"
  }
}
```

**Key Rule:** With `command = plan`, test the CONFIGURATION (what you're setting), not the RESULT (computed IDs, ARNs, or attributes that reference other resources).

### HANDLING SET-TYPE ATTRIBUTES

Many Terraform resource attributes are **sets**, not lists. You CANNOT use index notation `[0]` on sets.

WRONG:
```hcl
assert {
  condition = aws_s3_bucket_server_side_encryption_configuration.main.rule[0].sse_algorithm == "AES256"
  error_message = "Cannot index a set value"
}
```

CORRECT - Use `for` expressions:
```hcl
assert {
  condition = length([for rule in aws_s3_bucket_server_side_encryption_configuration.main.rule : rule if length([for default in rule.apply_server_side_encryption_by_default : default if default.sse_algorithm == "AES256"]) > 0]) > 0
  error_message = "Encryption algorithm should be AES256"
}
```

### BEFORE GENERATING ANY TEST - MANDATORY CHECK:

For EVERY assert statement, ask:
1. Am I using `command = plan`?
2. If YES: Am I testing a resource attribute (aws_*.something)?
3. If YES to #2: **Is this attribute computed or does it reference another resource's ID/ARN?**
4. If YES to #3: **STOP - This will fail!**

**What you CAN test with `command = plan`:**
- ✅ Variables: `var.environment`, `var.project_name`
- ✅ Locals: `local.computed_value`
- ✅ Resource configuration blocks: `length(aws_s3_bucket.main.rule)`
- ✅ Static configuration values: `aws_s3_bucket.main.tags["Name"]`
- ✅ Conditional logic: `length(aws_s3_bucket_versioning.main)` (tests count)

**What you CANNOT test with `command = plan` (even with mocks):**
- ❌ Computed IDs: `aws_s3_bucket.main.id`
- ❌ Computed ARNs: `aws_s3_bucket.main.arn`
- ❌ Attributes referencing computed values: `aws_s3_bucket_encryption.main.bucket` (if it references `main.id`)
- ❌ Any `!= null` or `!= ""` checks on attributes that reference other resources

**When in doubt:** Use `command = apply` for integration tests, or test the configuration structure (like `length(resource.rule)`) instead of computed attributes.

### Assert Statement Formatting

#### ✅ **CORRECT Examples:**
```hcl
# Example 1: Simple condition
assert {
  condition = var.environment != ""
  error_message = "Environment variable must not be empty"
}

# Example 2: Ternary operator on single line
assert {
  condition = var.iam_role_prefix != "" ? can(regex("^arn:aws:iam::[0-9]+:policy/", data.aws_iam_policy.boundary[0].arn)) : true
  error_message = "Permissions boundary policy ARN should follow expected format"
}

# Example 3: Multiple conditions with AND
assert {
  condition = length(var.security_group_settings.source_security_groups) >= 2 && length(var.additional_security_group_ids) >= 1
  error_message = "Service mesh should have multiple security groups for different service tiers"
}

# Example 4: Complex regex validation
assert {
  condition = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.bucket_name))
  error_message = "Bucket name must follow S3 naming conventions"
}

# Example 5: List validation
assert {
  condition = contains(["dev", "staging", "prod"], var.environment)
  error_message = "Environment must be one of: dev, staging, prod"
}
```

#### ❌ **INCORRECT Examples:**
```hcl
# Wrong 1: Multi-line condition with ternary
assert {
  condition = var.iam_role_prefix != "" ? 
    can(regex("^arn:aws:iam::[0-9]+:policy/", data.aws_iam_policy.boundary[0].arn)) :
    true
  error_message = "Error message"
}

# Wrong 2: Multi-line AND condition
assert {
  condition = length(var.security_group_settings.source_security_groups) >= 2 && 
              length(var.additional_security_group_ids) >= 1
  error_message = "Service mesh should have multiple security groups"
}

# Wrong 3: Line break in function call
assert {
  condition = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", 
                       var.bucket_name))
  error_message = "Invalid bucket name"
}

# Wrong 4: Multi-line OR condition
assert {
  condition = var.create_vpc || 
              var.use_existing_vpc
  error_message = "Either create or use existing VPC"
}
```

### Meaningful Condition Logic

#### ✅ **CORRECT - Meaningful Conditions:**
```hcl
# Example 1: Variable validation
assert {
  condition     = var.instance_count > 0 && var.instance_count <= 10
  error_message = "Instance count must be between 1 and 10"
}

# Example 2: Resource reference
assert {
  condition     = aws_s3_bucket.main.versioning[0].status == "Enabled"
  error_message = "S3 bucket versioning must be enabled"
}

# Example 3: Module output validation
assert {
  condition     = length(module.vpc.private_subnets) >= 2
  error_message = "VPC must have at least 2 private subnets for HA"
}

# Example 4: Data source validation
assert {
  condition     = data.aws_kms_key.rds.arn != null
  error_message = "Valid KMS key must be available for RDS encryption"
}

# Example 5: Complex business logic
assert {
  condition     = var.enable_monitoring ? var.retention_days >= 7 : true
  error_message = "When monitoring is enabled, retention must be at least 7 days"
}
```

#### ❌ **INCORRECT - Static or Invalid Conditions:**
```hcl
# Wrong 1: Always true
assert {
  condition     = true
  error_message = "This test always passes"
}

# Wrong 2: Always false
assert {
  condition     = false
  error_message = "This test always fails"
}

# Wrong 3: Testing AWS-returned format (unnecessary)
assert {
  condition     = can(regex("^arn:aws:kms:", data.aws_kms_key.rds.arn))
  error_message = "RDS KMS key ARN should have correct format"
}

# Wrong 4: No actual validation
assert {
  condition     = 1 == 1
  error_message = "Basic math should work"
}

# Wrong 5: Does not assert anything useful.
run "environment_secret_naming_consistency" {
  command = plan
  variables {
    environment = "uat"
  }

  # This tests that the naming pattern follows environment/key format
  assert {
    condition     = var.environment == "uat"
    error_message = "Environment should be properly set for secret naming"
  }
}
```

### 🛑 MANDATORY PRE-GENERATION VALIDATION CHECKLIST for variable validation🛑

Before writing ANY assert statement, answer these questions:

  1. **Am I testing user-provided input against itself?**
     - ❌ BAD: `var.instance_type == "t3.micro"` (when you set instance_type = "t3.micro" in the variables section)

  2. **What am I actually validating?**
     - ✅ Conditional logic (if/else, ternary operators, count logic)
     - ✅ Computed values (locals, concatenations, merges)
     - ✅ Resource relationships (dependencies, references)
     - ✅ Business rules (size limits, naming patterns, required combinations)
     - ✅ Variable validations by using `expect failures` in case of wrong inputs
     - ❌ NOT: Variable equals the value I just set it to

  ### Examples of MEANINGFUL vs MEANINGLESS Tests:

  #### ❌ MEANINGLESS (DO NOT DO THIS):
  ```hcl
  variables {
    environment = "dev"
  }

  assert {
    condition = var.environment == "dev"  # ← You just set this!
    error_message = "Environment should be dev"
  }

  ✅ MEANINGFUL (DO THIS):

  variables {
    create_security_group = true
    additional_security_group_ids = ["sg-123"]
  }

  assert {
    # Tests the LOGIC in: concat([aws_security_group.ec2[0].id], var.additional_security_group_ids)
    condition = var.create_security_group ? length(local.security_group_ids) >= 2 : length(local.security_group_ids) == 1
    error_message = "Security group IDs logic is incorrect"
  }

  What Makes a Good Unit Test:

  1. Tests conditional resource creation (count/for_each logic)
  2. Tests local variable computations (merges, conditionals, transformations)
  3. Tests that resource configurations use the right computed values
  4. Tests edge cases (empty lists, null values, boundary conditions)
  5. Tests variable validations by giving wrong values in variables and using `expect_failures`

🚫 NEVER TEST:

- Variable value == The exact value you just assigned
- Static equality checks with no logic
- Anything that always evaluates to true/false

### SELF-REVIEW QUESTIONS (Ask Before Submitting Each Test):

For each assert statement you write, ask:

**Question 1**: "Am I testing the Terraform code's logic, or just my test data?"
- Should be: Terraform code's logic
- If you're testing test data → Delete this test

**Question 2**: "Does this test verify a transformation, calculation, or decision made by the Terraform code?"
- If NO → Delete this test

**Example Self-Review:**

```hcl
# TEST CASE:
variables { instance_type = "t3.micro" }
assert { condition = var.instance_type == "t3.micro" }

# SELF-REVIEW:
# Q1: If I change instance_type to "t3.small", does this validate different behavior?
#     → NO, it just fails because I hardcoded "t3.micro"
# Q2: Am I testing Terraform logic or test data?
#     → Test data only
# Q3: Does this verify a transformation/calculation?
#     → NO
# VERDICT: ❌ DELETE THIS TEST
```

### Error Message Correlation Examples

#### ✅ **CORRECT - Aligned Messages:**
```hcl
# Example 1: Direct correlation
assert {
  condition     = var.create_cloudfront && var.create_waf
  error_message = "Both CloudFront and WAF must be enabled together"
}

# Example 2: Specific validation message
assert {
  condition     = length(var.availability_zones) >= 2
  error_message = "At least 2 availability zones required for high availability"
}

# Example 3: Configuration requirement
assert {
  condition     = var.backup_enabled ? var.backup_retention_days > 0 : true
  error_message = "Backup retention days must be set when backups are enabled"
}

# Example 4: Security requirement
assert {
  condition     = var.encryption_enabled
  error_message = "Encryption must be enabled for production workloads"
}

# Example 5: Naming convention
assert {
  condition     = can(regex("^${var.environment}-", var.resource_name))
  error_message = "Resource name must start with environment prefix"
}
```

#### ❌ **INCORRECT - Misaligned Messages:**
```hcl
# Wrong 1: Unrelated message
assert {
  condition     = var.create_cloudfront && var.create_waf
  error_message = "CloudFront should redirect HTTP to HTTPS"
}

# Wrong 2: Generic message for specific condition
assert {
  condition     = length(var.subnets) == 3
  error_message = "Configuration error"
}

# Wrong 3: Wrong context
assert {
  condition     = var.instance_type != ""
  error_message = "Security group must be configured"
}
```

### Provider Mocking Examples

CORRECT Mock Patterns:

**AWS Examples:**
```hcl
# Example 1: Basic AWS provider mock
mock_provider "aws" {
  alias = "mock"
}

# Example 2: AWS provider with resource mocks
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

# Example 3: Using mocked AWS provider in test
run "test_with_mocked_aws_provider" {
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

**Azure Examples:**
```hcl
# Example 1: Basic Azure provider mock
mock_provider "azurerm" {
  alias = "mock"
}

# Example 2: Azure provider with resource mocks
mock_provider "azurerm" {
  alias = "mock"

  mock_resource "azurerm_storage_account" {
    defaults = {
      id                   = "/subscriptions/12345/resourceGroups/test-rg/providers/Microsoft.Storage/storageAccounts/teststorage"
      name                 = "teststorage"
      location             = "eastus"
      resource_group_name  = "test-rg"
    }
  }
}

# Example 3: Using mocked Azure provider in test
run "test_with_mocked_azure_provider" {
  providers = {
    azurerm = azurerm.mock
  }

  variables {
    location = "eastus"
    resource_group_name = "test-rg"
  }

  assert {
    condition     = azurerm_storage_account.main.account_tier == "Standard"
    error_message = "Storage account tier should be Standard"
  }
}
```

**GCP Examples:**
```hcl
# Example 1: Basic GCP provider mock
mock_provider "google" {
  alias = "mock"
}

# Example 2: GCP provider with resource mocks
mock_provider "google" {
  alias = "mock"

  mock_resource "google_storage_bucket" {
    defaults = {
      id       = "test-bucket"
      name     = "test-bucket"
      location = "US"
      project  = "test-project-123"
      self_link = "https://www.googleapis.com/storage/v1/b/test-bucket"
    }
  }
}

# Example 3: Using mocked GCP provider in test
run "test_with_mocked_gcp_provider" {
  providers = {
    google = google.mock
  }

  variables {
    project = "test-project-123"
    region  = "us-central1"
  }

  assert {
    condition     = google_storage_bucket.main.storage_class == "STANDARD"
    error_message = "Storage class should be STANDARD"
  }
}
```

### Command Selection Examples

#### ✅ **CORRECT Command Usage:**
```hcl
# Example 1: Plan for validation
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

# Example 2: Apply for resource creation
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

# Example 3: Apply for module outputs
run "test_vpc_outputs" {
  command = apply
  
  assert {
    condition     = length(module.vpc.private_subnet_ids) == 3
    error_message = "VPC should have 3 private subnets"
  }
}

# Example 4: Plan with expect_failures
run "test_validation_rules" {
  command = plan
  
  variables {
    instance_count = -1  # Invalid value
  }
  
  expect_failures = [
    var.instance_count
  ]
}

# Example 5: Apply with module testing
run "test_complete_infrastructure" {
  command = apply
  
  module {
    source = "./modules/networking"
  }
  
  assert {
    condition     = module.networking.vpc_id != ""
    error_message = "VPC should be created"
  }
}
```

#### ❌ **INCORRECT Command Usage:**
```hcl
# Wrong 1: Using plan to check computed values
run "test_api_creation" {
  command = plan  # Should be apply
  
  assert {
    condition = aws_api_gateway_rest_api.main.id != null
    error_message = "API Gateway ID should exist"
  }
}

# Wrong 2: Missing command when needed
run "test_resources" {
  # No command specified, defaults may not work as expected
  
  assert {
    condition = aws_instance.main.id != null
  }
}
```

### Variable Handling Examples

#### ✅ **CORRECT Variable Usage:**
```hcl
# Example 1: Complete required variables
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

# Example 2: Respecting validation rules
run "test_valid_environment" {
  variables {
    environment = "prod"  # Must match validation: dev, staging, prod
  }
}

# Example 3: Complex variable structures
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

# Example 4: List variables
run "test_list_variables" {
  variables {
    availability_zones = ["us-east-1a", "us-east-1b"]
    security_group_ids = ["sg-123", "sg-456", "sg-789"]
    allowed_ips       = ["10.0.0.0/8", "172.16.0.0/12"]
  }
}

# Example 5: Optional with defaults
run "test_optional_variables" {
  variables {
    # Required variables
    region      = "us-east-1"
    environment = "test"
    
    # Optional - using defaults
    # backup_enabled = true  # Has default in variables.tf
    # monitoring_enabled = false  # Has default in variables.tf
  }
}
```

#### ❌ **INCORRECT Variable Usage:**
```hcl
# Wrong 1: Missing required variables
run "test_incomplete" {
  variables {
    region = "us-east-1"
    # Missing required 'environment' variable
  }
}

# Wrong 2: Invalid enum value
run "test_invalid_enum" {
  variables {
    environment = "production"  # Must be: dev, staging, prod
  }
}

# Wrong 3: Wrong data type
run "test_wrong_type" {
  variables {
    instance_count = "three"  # Should be number
    tags = "Environment=test"  # Should be map
  }
}
```

### Override Examples and Mock Provider Requirements

**CRITICAL: Mock tests MUST use mock_provider**

Even when using `override_resource` or `override_data`, you MUST define a `mock_provider` and reference it in the `providers` block. Otherwise, Terraform will try to initialize the real provider and require actual credentials.

WRONG - This will fail and ask for AWS credentials:
```hcl
run "test_with_override" {
  command = plan

  override_resource {
    target = aws_s3_bucket.main
    values = {
      id = "test-bucket"
    }
  }

  assert {
    # This test will fail - no mock_provider defined!
    condition = aws_s3_bucket.main.id == "test-bucket"
    error_message = "Test"
  }
}
```

CORRECT - Define mock_provider at file level and use it:
```hcl
# At the top of your test file
mock_provider "aws" {
  alias = "mock"
}

run "test_with_override" {
  command = plan

  providers = {
    aws = aws.mock  # ← REQUIRED!
  }

  override_resource {
    target = aws_s3_bucket.main
    values = {
      id = "test-bucket"
    }
  }

  # Now you can test configuration (not computed attributes!)
  assert {
    condition = length(aws_s3_bucket.main.tags) > 0
    error_message = "Bucket should have tags"
  }
}
```

CORRECT Override Usage Examples:

**AWS Override Examples:**
```hcl
# Example 1: Override AWS data source (requires mock_provider)
mock_provider "aws" {
  alias = "mock"
}

run "test_with_override_data" {
  command = plan

  providers = {
    aws = aws.mock
  }

  override_data {
    target = data.aws_caller_identity.current
    values = {
      account_id = "123456789012"
      arn        = "arn:aws:iam::123456789012:root"
    }
  }
}

# Example 2: Override AWS module outputs
run "test_module_override" {
  command = plan

  providers = {
    aws = aws.mock
  }

  override_module {
    target = module.vpc
    outputs = {
      vpc_id             = "vpc-12345678"
      private_subnet_ids = ["subnet-123", "subnet-456"]
      public_subnet_ids  = ["subnet-789", "subnet-012"]
    }
  }
}
```

**Azure Override Examples:**
```hcl
# Example 1: Override Azure data source
mock_provider "azurerm" {
  alias = "mock"
}

run "test_with_azure_override_data" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  override_data {
    target = data.azurerm_client_config.current
    values = {
      subscription_id = "12345678-1234-1234-1234-123456789012"
      tenant_id       = "87654321-4321-4321-4321-210987654321"
      client_id       = "abcdefgh-abcd-abcd-abcd-abcdefghijkl"
    }
  }
}

# Example 2: Override Azure resource group module
run "test_azure_module_override" {
  command = plan

  providers = {
    azurerm = azurerm.mock
  }

  override_module {
    target = module.resource_group
    outputs = {
      resource_group_name = "test-rg"
      location            = "eastus"
      resource_group_id   = "/subscriptions/12345/resourceGroups/test-rg"
    }
  }
}
```

**GCP Override Examples:**
```hcl
# Example 1: Override GCP data source
mock_provider "google" {
  alias = "mock"
}

run "test_with_gcp_override_data" {
  command = plan

  providers = {
    google = google.mock
  }

  override_data {
    target = data.google_project.current
    values = {
      project_id = "test-project-123"
      number     = "123456789012"
      name       = "Test Project"
    }
  }
}

# Example 2: Override GCP network module
run "test_gcp_module_override" {
  command = plan

  providers = {
    google = google.mock
  }

  override_module {
    target = module.vpc
    outputs = {
      network_name       = "test-vpc"
      network_self_link  = "https://www.googleapis.com/compute/v1/projects/test-project/global/networks/test-vpc"
      subnet_names       = ["test-subnet-1", "test-subnet-2"]
    }
  }
}
```

**Key Rule:** `override_resource` and `override_data` do NOT eliminate the need for `mock_provider`. They work together - the mock provider prevents real AWS calls, while overrides provide specific test values.

### Module Testing Examples

#### ✅ **CORRECT Module Tests:**
```hcl
# Example 1: Testing module outputs
run "test_vpc_module_outputs" {
  command = apply
  
  assert {
    condition     = length(module.vpc.private_subnets) >= 2
    error_message = "VPC module should create at least 2 private subnets"
  }
  
  assert {
    condition     = module.vpc.vpc_id != ""
    error_message = "VPC module should output a VPC ID"
  }
}

# Example 2: Module with configuration
run "test_database_module" {
  command = apply
  
  variables {
    db_instance_class = "db.t3.micro"
    db_name          = "testdb"
  }
  
  assert {
    condition     = module.database.endpoint != ""
    error_message = "Database module should provide endpoint"
  }
}

# Example 3: Nested module testing
run "test_nested_modules" {
  command = apply
  
  assert {
    condition     = module.networking.module.vpc.vpc_id != ""
    error_message = "Nested VPC module should create VPC"
  }
}
```

### Complex Scenario Examples

#### ✅ **CORRECT Complex Tests:**
```hcl
# Example 1: Multi-resource validation
run "test_complete_stack" {
  command = apply
  
  variables {
    environment = "test"
    region      = "us-east-1"
  }
  
  # VPC validation
  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR should be 10.0.0.0/16"
  }
  
  # Subnet validation
  assert {
    condition     = length(aws_subnet.private) == 3
    error_message = "Should have 3 private subnets"
  }
  
  # Security group validation
  assert {
    condition     = length(aws_security_group.web.ingress) > 0
    error_message = "Web security group should have ingress rules"
  }
}

# Example 2: Conditional resource testing
run "test_conditional_resources" {
  command = apply
  
  variables {
    create_bastion = true
    environment    = "prod"
  }
  
  assert {
    condition     = var.create_bastion ? aws_instance.bastion[0].id != "" : true
    error_message = "Bastion should be created when enabled"
  }
  
  assert {
    condition     = var.environment == "prod" ? aws_kms_key.main[0].id != "" : true
    error_message = "KMS key should exist in production"
  }
}

# Example 3: Cross-resource dependencies
run "test_resource_dependencies" {
  command = apply
  
  assert {
    condition     = aws_instance.app.subnet_id == aws_subnet.private[0].id
    error_message = "App instance should be in private subnet"
  }
  
  assert {
    condition     = contains(aws_instance.app.security_groups, aws_security_group.app.id)
    error_message = "App instance should use app security group"
  }
}
```

### Error Handling Examples

#### ✅ **CORRECT Error Handling:**
```hcl
# Example 1: Expected failures
run "test_validation_failure" {
  command = plan
  
  variables {
    instance_count = 100  # Exceeds max
  }
  
  expect_failures = [
    var.instance_count
  ]
}

# Example 2: Multiple expected failures
run "test_multiple_failures" {
  command = plan
  
  variables {
    environment = "invalid"
    region      = "invalid-region"
  }
  
  expect_failures = [
    var.environment,
    var.region
  ]
}

# Example 3: Resource failure testing
run "test_resource_validation" {
  command = apply
  
  variables {
    bucket_name = "invalid bucket name with spaces"
  }
  
  expect_failures = [
    aws_s3_bucket.main
  ]
}
```

## ⚠️ STEP 5: List of Valid test cases ⚠️
### Variable Validation Tests

- Test that required variables reject invalid inputs using expect_failures
- Validate variable type constraints work correctly
- Test default values are applied when variables aren't specified
- Verify complex variable validation rules (regex patterns, ranges, allowed values)
- Test sensitive variables are properly masked in outputs

### Output Validation Tests

- Verify outputs return expected values and formats
- Test conditional outputs based on input variables
- Validate output descriptions are present
- Test sensitive output marking
- Verify computed outputs calculate correctly

### Resource Configuration Tests

- Test resource counts with for_each and count meta-arguments
- Validate conditional resource creation (count = var.enabled ? 1 : 0)
- Test resource naming conventions follow patterns
- Verify resource dependencies are correctly established
- Test lifecycle rules (create_before_destroy, prevent_destroy)

**Provider-Specific Resource Tests:**
- **AWS:** Test security group rules, IAM policy attachments, S3 bucket configurations
- **Azure:** Test resource group dependencies, network security group associations, storage account configurations
- **GCP:** Test project references, network peering configurations, service account bindings

### Logic and Computation Tests
#### Function Testing

- Test built-in functions produce correct results (cidrsubnet, format, lookup)
- Validate string manipulation functions (split, join, replace)
- Test collection functions (merge, concat, flatten)
- Verify type conversion functions work correctly
- Test conditional expressions (condition ? true_val : false_val)

#### Local Values Testing

- Verify computed locals calculate correctly
- Test complex data transformations in locals
- Validate local value dependencies resolve properly

#### Dynamic Block Testing

- Test dynamic blocks generate correct number of nested blocks
- Validate conditional dynamic blocks based on variables
- Test iteration over complex data structures

### Module Interface Tests
#### Input Contract Testing

- Test module accepts valid input combinations
- Verify module rejects invalid input combinations using expect_failures
- Test optional vs required variables
- **Multi-Cloud:** Test provider-specific required inputs (AWS region, Azure location, GCP project)

#### Output Contract Testing

- Test module produces all expected outputs
- Verify output types match documentation
- Test outputs are accessible to parent modules
- **Multi-Cloud:** Validate provider-specific output formats:
  - **AWS:** ARNs, resource IDs (e.g., `vpc-123`)
  - **Azure:** Resource IDs (full path format), locations
  - **GCP:** Self-links, project-qualified names

#### Precondition/Postcondition Testing

- Test preconditions catch invalid configurations before apply
- Verify postconditions validate resource state after creation
- Test custom error messages display correctly
- **Provider-Specific:** Test cloud-specific validation rules:
  - **AWS:** Region validation, account ID checks
  - **Azure:** Location validation, subscription checks
  - **GCP:** Project validation, zone/region checks

### Provider and Version Tests
#### Provider Configuration

- Test required provider versions are specified
- Validate provider aliases work correctly
- Test provider feature flags and settings
- Verify provider authentication (using mocked providers)

#### Version Constraints

- Test minimum Terraform version requirements
- Validate module version compatibility
- Test with different provider versions (if critical)

## State and Planning Tests
#### Idempotency Testing
```hcl
run "first_apply" {
  command = apply
}

run "verify_idempotent" {
  command = plan
  
  assert {
    condition     = length(plan.resource_changes) == 0
    error_message = "Configuration is not idempotent"
  }
}
```
#### Plan Validation

- Test that plans show expected resource changes
- Verify no unintended resources are created/destroyed
- Test resource replacement scenarios
- Validate import blocks work correctly

### Mock Testing (Terraform 1.7+)
#### Provider Mocking
```hcl
mock_provider "aws" {
  mock_resource "aws_instance" {
    defaults = {
      id = "i-mockedinstance"
      arn = "arn:aws:ec2:region:account:instance/i-mocked"
    }
  }
}
```

- Test expensive resources without deployment costs
- Validate resource configuration without provider calls
- Test error handling with mocked provider failures
- Verify module logic independent of provider behavior

#### Data Source Mocking
```hcl
mock_provider "aws" {
  mock_data "aws_ami" {
    defaults = {
      id = "ami-12345678"
    }
  }
}
```

- Test modules dependent on data sources
- Validate data source error handling
- Test with various data source return values

### Multi-Stage Testing
#### Setup and Teardown Tests
```hcl
run "setup" {
  command = apply
  
  module {
    source = "./tests/setup"
  }
}

run "test_with_dependencies" {
  command = apply
  
  variables {
    vpc_id = run.setup.vpc_id
  }
}
```

#### Integration Pattern Tests

- Test module composition with actual dependencies
- Verify inter-module communication via outputs
- Test with real prerequisite infrastructure
- Validate end-to-end workflows

### Error Handling Tests
#### Negative Testing
```hcl
run "invalid_input" {
  command = plan
  
  variables {
    instance_type = "invalid.type"
  }
  
  expect_failures = [
    var.instance_type
  ]
}
```

- Test invalid configurations fail appropriately
- Verify error messages are helpful
- Test resource limit scenarios
- Validate timeout and retry behavior

#### Partial Failure Testing

- Test behavior when some resources fail
- Verify rollback scenarios
- Test state consistency after failures

### Compliance and Standards Tests

#### Tagging/Labeling Validation (All Providers)

- **AWS:** Test all resources have required tags (`Environment`, `Project`, `Owner`)
- **Azure:** Test all resources have required tags (same format as AWS)
- **GCP:** Test all resources have required labels (key-value pairs in lowercase)
- Verify tag/label format and naming conventions

```hcl
run "verify_tags" {
  command = plan

  assert {
    condition = alltrue([
      for r in plan.resource_changes :
      contains(keys(r.after.tags), "Environment")
      if can(r.after.tags)
    ])
    error_message = "Missing required Environment tag"
  }
}
```

#### Naming Convention Tests (All Providers)

- Test resources follow cloud-specific naming patterns
- **AWS:** Verify naming includes required prefixes/suffixes
- **Azure:** Test naming complies with Azure resource naming rules (length, characters)
- **GCP:** Test naming follows GCP conventions (lowercase, hyphens, project prefixes)

#### Security Baseline Tests (Provider-Specific)

**AWS Security Tests:**
- Test KMS encryption is enabled for S3, EBS, RDS
- Verify security groups don't allow unrestricted access (0.0.0.0/0)
- Test IAM roles use permissions boundaries
- Validate S3 buckets block public access
- Test VPC flow logs are enabled

**Azure Security Tests:**
- Test Azure Disk Encryption is enabled for VMs
- Verify Network Security Groups follow least privilege
- Test storage accounts use customer-managed keys
- Validate storage accounts disable public blob access
- Test Azure Policy assignments are in place
- Verify managed identities are used (no service principals with secrets)

**GCP Security Tests:**
- Test storage buckets use customer-managed encryption keys (CMEK)
- Verify firewall rules don't allow unrestricted access (0.0.0.0/0)
- Test service accounts follow least privilege
- Validate Cloud Storage buckets have uniform access control
- Test VPC Flow Logs are enabled
- Verify Organization Policy constraints are applied

### Performance Tests
#### Resource Limits

- Test with maximum expected resource counts
- Verify module handles large datasets efficiently
- Test pagination and batching logic

#### Timeout Testing

- Test resources complete within expected timeframes
- Verify appropriate timeout values are set

### Platform-Specific Tests
#### Cloud Provider Specific

- Test region/zone availability configurations
- Verify cloud-specific resource settings
- Test provider-specific features (AWS tags, Azure resource groups, GCP labels)

### For a specific resource - Example - AWS Lambda:

- Test runtime version validity
- Verify memory/timeout within AWS limits
- Test VPC configuration has multiple subnets
- Verify IAM role has correct permissions
- Test event source mappings are configured correctly
- Validate environment variables are set
- Test Lambda layers are correctly attached

#### Test Organization Examples
```hcl
# tests/unit.tftest.hcl
run "validate_variables" {
  command = plan
  # Fast tests without infrastructure
}

# tests/integration.tftest.hcl  
run "full_deployment" {
  command = apply
  # Tests requiring real resources
}

# tests/compliance.tftest.hcl
run "security_compliance" {
  command = plan
  # Policy and standards validation
}
```
## ⚠️ STEP 6: Command Selection Logic Table ⚠️

| Command | Use Case | Can Test | Cannot Test | Multi-Cloud Examples |
|---------|----------|----------|-------------|---------------------| | `plan` | Variable validation, configuration checks, conditional logic | Variables (`var.x`), Locals (`local.y`), Configuration structure (`length(resource.rule)`), Static values (`resource.tags["Name"]`), Conditional counts (`length(resource)`) | Computed IDs/ARNs, Attributes referencing other resources, Any null/empty checks on computed attributes | ✅ **AWS:** `var.region != ""`, `length(aws_s3_bucket.main.rule) > 0` <br> ✅ **Azure:** `var.location != ""`, `length(azurerm_storage_account.main.network_rules) > 0` <br> ✅ **GCP:** `var.project != ""`, `length(google_storage_bucket.main.lifecycle_rule) > 0` <br> ❌ **AWS:** `aws_instance.web.id != ""` <br> ❌ **Azure:** `azurerm_storage_account.main.id != null` <br> ❌ **GCP:** `google_storage_bucket.main.self_link != ""` |
| `apply` | Full resource testing, output validation, real infrastructure | Everything including computed attributes, resource IDs, outputs, cross-resource references | N/A (creates real resources, may cost money) | ✅ **AWS:** `aws_instance.web.id != ""`, `aws_s3_bucket.main.arn != ""` <br> ✅ **Azure:** `azurerm_storage_account.main.id != null`, `azurerm_resource_group.main.location == "eastus"` <br> ✅ **GCP:** `google_storage_bucket.main.self_link != ""`, `google_compute_instance.main.instance_id != ""` |

**Critical Notes:**
- Even with `mock_provider`, `command = plan` cannot access attributes that reference computed values from other resources
- Use `for` expressions to iterate over set-type attributes (cannot use `[0]` indexing on sets)
- When testing encryption/configuration always exists: check `length(resource.rule) > 0`, NOT `resource.bucket != null`

**Provider-Specific Computed Attributes to Avoid with `command = plan`:**
- **AWS:** `.id`, `.arn`, `.dns_name`, `.endpoint`, `.hosted_zone_id`
- **Azure:** `.id`, `.resource_group_name` (when referencing), `.principal_id`, `.identity`
- **GCP:** `.id`, `.self_link`, `.instance_id`, `.number`, `.member`

## ⚠️ STEP 7: Best Practices Checklist ⚠️

### ✓ Test Independence
- Each test must be self-contained
- Include all required variables
- Mock all external dependencies
- No cross-test dependencies

### ✓ Variable Handling
- Always provide ALL required variables
- Respect validation rules from `variables.tf`
- Use allowed enum values only
- Match exact data types (string vs object vs list)

### ✓ Mock Data Consistency
- Mock data must match expected patterns
- Use realistic values that pass validation
- Align with naming conventions

### ✓ Assertion Scope
- Test visible outputs and behavior
- Avoid testing internal implementation
- Focus on module interface contracts
- Use meaningful error messages

### ✓ Coverage Completeness
- Test all resources
- Cover edge cases
- Validate error conditions
- Test with minimal and maximal configurations

## Output Validation

Before finalizing:
1. Verify all test files are syntactically correct
2. Ensure no multi-line conditions in assert blocks
3. Confirm all required variables are provided
4. Check that mock data aligns with test expectations
5. Validate that error messages correlate with conditions
6. Ensure all conditions reference actual resources/variables (not just `true`/`false`)
7. Verify command selection matches what's being tested

## Execution Flow - SEQUENTIAL ENFORCEMENT

### Phase 1: User Requirements Collection
1. **STOP** - Do not proceed until user provides tfvars and compliance requirements
2. **Request** user to provide variable values and compliance specifications
3. **Validate** user has provided both required pieces of information

### Phase 2: Code Analysis
4. **Read** provided Terraform code from specified path
5. **Analyze** resources, modules, variables, data sources, and relationships
6. **Map** user-provided variable values to Terraform variable requirements

### Phase 3: Test Generation
7. **Fetch** latest documentation for syntax verification
8. **Generate** comprehensive test suite using user-provided values
9. **Create** files in `tests/` directory structure
10. **Document** test execution in README and CODE_COVERAGE.md
11. **Validate** all generated code for correctness

**🚫 CRITICAL: Each phase must be completed before proceeding to the next**

## ⚠️ STEP 8: MANDATORY COMPLETION CHECKLIST - ALL MUST BE GENERATED ⚠️

Before submitting ANY test file:
- [ ] **CRITICAL**: No `command = plan` tests contain computed resource attribute assertions (even with mocks)
- [ ] **CRITICAL**: No assertions check provider-specific computed attributes with `command = plan`:
  - AWS: `.bucket`, `.id`, `.arn`, `.dns_name`, `.endpoint`
  - Azure: `.id`, `.resource_group_name` (when referencing), `.principal_id`
  - GCP: `.id`, `.self_link`, `.instance_id`, `.number`
- [ ] **CRITICAL**: Set-type attributes use `for` expressions, NOT index notation `[0]`
- [ ] All `command = plan` tests only assert variables, locals, configuration structure, or static values
- [ ] All computed attribute tests (IDs, ARNs, cross-resource refs) use `command = apply`
- [ ] **CLOUD PROVIDER**: Detected cloud provider(s) and adapted test syntax accordingly
- [ ] Unit Tests with correct mock_provider for detected cloud:
  - AWS: `mock_provider "aws"` (unit_*.tftest.hcl)
  - Azure: `mock_provider "azurerm"` (unit_*.tftest.hcl)
  - GCP: `mock_provider "google"` (unit_*.tftest.hcl)
- [ ] Integration Tests with real provider + command = apply (integration_*.tftest.hcl)
- [ ] Mock Tests with override patterns (mock_*.tftest.hcl)
- [ ] Variable validation tests with expect_failures
- [ ] Coverage report table (coverage_report.md) - SIMPLE format, no complex calculations
- [ ] README documentation (README.md) with provider-specific setup instructions

**Common Mistakes to Avoid (Multi-Cloud):**
- ❌ AWS: `condition = resource.encryption.bucket != null` with `command = plan`
- ❌ Azure: `condition = azurerm_storage_account.main.id != null` with `command = plan`
- ❌ GCP: `condition = google_storage_bucket.main.self_link != ""` with `command = plan`
- ❌ `condition = resource.rule[0].algorithm == "AES256"` (sets need for expressions)
- ❌ Using `override_resource` without defining `mock_provider` (will ask for cloud credentials)
- ❌ Forgetting provider-specific syntax in run blocks:
  - AWS: `providers = { aws = aws.mock }`
  - Azure: `providers = { azurerm = azurerm.mock }`
  - GCP: `providers = { google = google.mock }`
- ✅ `condition = length(resource.encryption.rule) > 0` with `command = plan`
- ✅ `condition = length([for rule in resource.rule : rule if rule.algorithm == "AES256"]) > 0`
- ✅ Always define `mock_provider` at file level for mock tests
- ✅ Always include correct `providers = { ... }` mapping in every run block using mocks

---

**Note:** If uncertain about any syntax or pattern, reference the official documentation rather than making assumptions. Quality and correctness take precedence over speed. Always check provider-specific documentation for the detected cloud provider(s).