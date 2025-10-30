# Cloud Provider-Specific Patterns

## Table of Contents
- [AWS Patterns](#aws-patterns)
- [Azure (azurerm) Patterns](#azure-azurerm-patterns)
- [GCP (google) Patterns](#gcp-google-patterns)
- [Data Source Mocking Patterns](#data-source-mocking-patterns)
- [Provider-Specific Computed Attributes](#provider-specific-computed-attributes)
- [Cloud-Specific Security Tests](#cloud-specific-security-tests)

## AWS Patterns

### AWS Mock Provider

```hcl
mock_provider "aws" {
  alias = "mock"
}

# With resource mocks
mock_provider "aws" {
  alias = "mock"

  mock_resource "aws_s3_bucket" {
    defaults = {
      id                    = "test-bucket"
      bucket                = "test-bucket"
      arn                   = "arn:aws:s3:::test-bucket"
      region                = "us-east-1"
      bucket_domain_name    = "test-bucket.s3.amazonaws.com"
    }
  }

  mock_resource "aws_instance" {
    defaults = {
      id                    = "i-1234567890abcdef0"
      arn                   = "arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0"
      instance_type         = "t3.micro"
      availability_zone     = "us-east-1a"
    }
  }
}
```

### AWS Set-Type Attributes

**CRITICAL:** AWS security groups, route tables, and other resources use set-type collections. NEVER index with `[0]`.

**Incorrect:**
```hcl
# ❌ WRONG - Will fail with set-type error
assert {
  condition = aws_security_group.main.ingress[0].from_port == 443
  error_message = "Should allow HTTPS"
}
```

**Correct:**
```hcl
# ✅ CORRECT - Use for expression
assert {
  condition = length([for rule in aws_security_group.main.ingress : rule if rule.from_port == 443]) > 0
  error_message = "Should allow HTTPS"
}
```

## Azure (azurerm) Patterns

### Azure Mock Provider

```hcl
mock_provider "azurerm" {
  alias = "mock"
}

# With resource mocks
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
```

### Azure UUID Validation Requirements

**CRITICAL:** Azure providers strictly validate UUID format for identity fields.

**Required UUID Format:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (8-4-4-4-12 hex digits)

**Fields requiring valid UUIDs:**
- `object_id` - User/group/service principal object IDs
- `tenant_id` - Azure AD tenant identifiers
- `subscription_id` - Azure subscription identifiers
- `client_id` - Application/service principal client IDs

### Azure Override Data with Valid UUIDs

```hcl
mock_provider "azurerm" {
  alias = "mock"
}

mock_provider "azuread" {
  alias = "mock_ad"
}

run "test_with_entra_groups" {
  command = plan

  providers = {
    azurerm = azurerm.mock
    azuread = azuread.mock_ad
  }

  # Mock Azure AD group data
  override_data {
    target = data.azuread_group.admin_groups["TestGroup"]
    values = {
      display_name     = "TestGroup"
      object_id        = "11111111-1111-1111-1111-111111111111"  # Valid UUID
      security_enabled = true
    }
  }

  # Mock client config
  override_data {
    target = data.azurerm_client_config.current
    values = {
      tenant_id       = "87654321-4321-4321-4321-210987654321"  # Valid UUID
      subscription_id = "12345678-1234-1234-1234-123456789012"  # Valid UUID
      object_id       = "abcdefab-abcd-abcd-abcd-abcdefabcdef"  # Valid UUID
      client_id       = "11111111-2222-3333-4444-555555555555"  # Valid UUID
    }
  }

  variables {
    enable_entra_id_auth = true
    entra_id_admin_group_display_names = ["TestGroup"]
  }

  assert {
    condition     = length(azurerm_postgresql_flexible_server_active_directory_administrator.entra_admin_groups) == 1
    error_message = "Should create one admin group configuration"
  }
}
```

### Azure for_each Data Source Mocking

When data sources use `for_each`, mock EACH instance using the exact key:

```hcl
# Module has: data "azuread_group" "admin_groups" { for_each = toset(var.group_names) }

run "test_multiple_groups" {
  providers = {
    azurerm = azurerm.mock
    azuread = azuread.mock_ad
  }

  # Mock each group individually
  override_data {
    target = data.azuread_group.admin_groups["Azure_PostgreSQL_Admin"]
    values = {
      display_name     = "Azure_PostgreSQL_Admin"
      object_id        = "44444444-4444-4444-4444-444444444444"
      security_enabled = true
    }
  }

  override_data {
    target = data.azuread_group.admin_groups["Azure_PostgreSQL_DevOps"]
    values = {
      display_name     = "Azure_PostgreSQL_DevOps"
      object_id        = "55555555-5555-5555-5555-555555555555"
      security_enabled = true
    }
  }

  variables {
    entra_id_admin_group_display_names = [
      "Azure_PostgreSQL_Admin",
      "Azure_PostgreSQL_DevOps"
    ]
  }
}
```

## Data Source Mocking Patterns

**CRITICAL:** ALL data sources MUST be mocked in unit tests using `override_data` blocks. Integration tests use real providers and don't need mocking.

### AWS Data Source Mocking

```hcl
# Mock availability zones
override_data {
  target = data.aws_availability_zones.available
  values = {
    names = ["us-east-1a", "us-east-1b", "us-east-1c"]
    zone_ids = ["use1-az1", "use1-az2", "use1-az3"]
  }
}

# Mock caller identity
override_data {
  target = data.aws_caller_identity.current
  values = {
    account_id = "123456789012"
    arn        = "arn:aws:iam::123456789012:root"
    user_id    = "AIDAI1234567890EXAMPLE"
  }
}

# Mock region
override_data {
  target = data.aws_region.current
  values = {
    name        = "us-east-1"
    endpoint    = "ec2.us-east-1.amazonaws.com"
    description = "US East (N. Virginia)"
  }
}

# Mock VPC
override_data {
  target = data.aws_vpc.main
  values = {
    id         = "vpc-12345678"
    cidr_block = "10.0.0.0/16"
    arn        = "arn:aws:ec2:us-east-1:123456789012:vpc/vpc-12345678"
  }
}

# Mock AMI
override_data {
  target = data.aws_ami.ubuntu
  values = {
    id               = "ami-12345678"
    arn              = "arn:aws:ec2:us-east-1::image/ami-12345678"
    architecture     = "x86_64"
    image_id         = "ami-12345678"
    name             = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20231201"
  }
}
```

### Azure Data Source Mocking

```hcl
# Mock client config
override_data {
  target = data.azurerm_client_config.current
  values = {
    tenant_id       = "12345678-1234-1234-1234-123456789012"
    subscription_id = "87654321-4321-4321-4321-210987654321"
    object_id       = "abcdefab-abcd-abcd-abcd-abcdefabcdef"
    client_id       = "11111111-2222-3333-4444-555555555555"
  }
}

# Mock AD group (single instance)
override_data {
  target = data.azuread_group.admin_group
  values = {
    display_name     = "AdminGroup"
    object_id        = "11111111-1111-1111-1111-111111111111"
    security_enabled = true
    mail_enabled     = false
  }
}

# Mock AD groups with for_each (EACH instance must be mocked)
override_data {
  target = data.azuread_group.admin_groups["GroupA"]
  values = {
    display_name     = "GroupA"
    object_id        = "22222222-2222-2222-2222-222222222222"
    security_enabled = true
  }
}

override_data {
  target = data.azuread_group.admin_groups["GroupB"]
  values = {
    display_name     = "GroupB"
    object_id        = "33333333-3333-3333-3333-333333333333"
    security_enabled = true
  }
}

# Mock resource group
override_data {
  target = data.azurerm_resource_group.main
  values = {
    id       = "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/test-rg"
    name     = "test-rg"
    location = "eastus"
  }
}

# Mock subscription
override_data {
  target = data.azurerm_subscription.current
  values = {
    subscription_id = "12345678-1234-1234-1234-123456789012"
    display_name    = "Test Subscription"
    tenant_id       = "87654321-4321-4321-4321-210987654321"
  }
}
```

### GCP Data Source Mocking

```hcl
# Mock project
override_data {
  target = data.google_project.current
  values = {
    project_id = "my-project-123"
    number     = "123456789012"
    name       = "My Project"
  }
}

# Mock client config
override_data {
  target = data.google_client_config.current
  values = {
    project = "my-project-123"
    region  = "us-central1"
    zone    = "us-central1-a"
  }
}

# Mock compute zones
override_data {
  target = data.google_compute_zones.available
  values = {
    names = ["us-central1-a", "us-central1-b", "us-central1-c"]
  }
}

# Mock compute network
override_data {
  target = data.google_compute_network.main
  values = {
    id         = "projects/my-project-123/global/networks/test-network"
    name       = "test-network"
    self_link  = "https://www.googleapis.com/compute/v1/projects/my-project-123/global/networks/test-network"
  }
}

# Mock service account
override_data {
  target = data.google_service_account.main
  values = {
    account_id = "test-sa"
    email      = "test-sa@my-project-123.iam.gserviceaccount.com"
    unique_id  = "123456789012345678901"
  }
}
```

## GCP (google) Patterns

### GCP Mock Provider

```hcl
mock_provider "google" {
  alias = "mock"
}

# With resource mocks
mock_provider "google" {
  alias = "mock"

  mock_resource "google_storage_bucket" {
    defaults = {
      id        = "test-bucket"
      name      = "test-bucket"
      location  = "US"
      project   = "test-project-123"
      self_link = "https://www.googleapis.com/storage/v1/b/test-bucket"
    }
  }
}
```

### GCP Override Patterns

```hcl
mock_provider "google" {
  alias = "mock"
}

run "test_with_gcp_override" {
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

  override_module {
    target = module.vpc
    outputs = {
      network_name       = "test-vpc"
      network_self_link  = "https://www.googleapis.com/compute/v1/projects/test-project/global/networks/test-vpc"
      subnet_names       = ["test-subnet-1", "test-subnet-2"]
    }
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

## Provider-Specific Computed Attributes

### Attributes to AVOID with `command = plan`

**AWS Computed Attributes:**
- `.id` - Resource ID
- `.arn` - Amazon Resource Name
- `.dns_name` - DNS endpoints
- `.endpoint` - Service endpoints
- `.hosted_zone_id` - Route53 zone IDs
- Any attribute referencing another resource's computed value

**Azure Computed Attributes:**
- `.id` - Resource ID (full path format)
- `.resource_group_name` (when referencing another resource)
- `.principal_id` - Managed identity principal ID
- `.identity` - Identity blocks (computed)
- Any cross-resource references

**GCP Computed Attributes:**
- `.id` - Resource ID
- `.self_link` - Full resource URL
- `.instance_id` - Instance identifiers
- `.number` - Project number
- `.member` - IAM member identifiers
- Any attribute referencing other resources

### What You CAN Test with `command = plan`

**All Providers:**
- ✅ Variables: `var.region`, `var.location`, `var.project`
- ✅ Locals: `local.computed_value`
- ✅ Configuration structure: `length(resource.rule)`
- ✅ Static values: `resource.tags["Name"]` (AWS/Azure) or `resource.labels["name"]` (GCP)
- ✅ Conditional counts: `length(resource)` tests if resource exists

## Cloud-Specific Security Tests

### AWS Security Baseline

```hcl
# KMS encryption for S3
assert {
  condition = length([for rule in aws_s3_bucket_server_side_encryption_configuration.main.rule : rule if length([for default in rule.apply_server_side_encryption_by_default : default if default.sse_algorithm == "aws:kms"]) > 0]) > 0
  error_message = "S3 bucket must use KMS encryption"
}

# Security group restrictive rules
assert {
  condition = length([for rule in aws_security_group.main.ingress : rule if rule.cidr_blocks[0] == "0.0.0.0/0"]) == 0
  error_message = "Security groups must not allow unrestricted access"
}

# S3 public access block
assert {
  condition = aws_s3_bucket_public_access_block.main.block_public_acls == true
  error_message = "S3 bucket must block public ACLs"
}
```

### Azure Security Baseline

```hcl
# Storage account encryption with CMK
assert {
  condition = azurerm_storage_account.main.customer_managed_key[0].key_vault_key_id != null
  error_message = "Storage account must use customer-managed keys"
}

# Network security group rules
assert {
  condition = azurerm_network_security_rule.main.priority >= 100 && azurerm_network_security_rule.main.priority <= 4096
  error_message = "NSG rule priority should be between 100 and 4096"
}

# Disable public blob access
assert {
  condition = azurerm_storage_account.main.allow_nested_items_to_be_public == false
  error_message = "Storage account must disable public blob access"
}

# Managed identity usage
assert {
  condition = length(azurerm_linux_virtual_machine.main.identity) > 0
  error_message = "VM must use managed identity"
}
```

### GCP Security Baseline

```hcl
# Storage bucket CMEK
assert {
  condition = google_storage_bucket.main.encryption[0].default_kms_key_name != null
  error_message = "Storage bucket must use customer-managed encryption keys"
}

# Firewall restrictive rules
assert {
  condition = length([for range in google_compute_firewall.main.source_ranges : range if range == "0.0.0.0/0"]) == 0
  error_message = "Firewall rules must not allow unrestricted access"
}

# Uniform bucket access
assert {
  condition = google_storage_bucket.main.uniform_bucket_level_access[0].enabled == true
  error_message = "Storage bucket must use uniform access control"
}

# VPC Flow Logs
assert {
  condition = google_compute_subnetwork.main.log_config[0].aggregation_interval != null
  error_message = "Subnet must have VPC Flow Logs enabled"
}
```

## Tagging/Labeling Requirements

### AWS & Azure - Tags
```hcl
assert {
  condition = alltrue([
    contains(keys(aws_instance.main.tags), "Environment"),
    contains(keys(aws_instance.main.tags), "Project"),
    contains(keys(aws_instance.main.tags), "Owner")
  ])
  error_message = "Resource must have Environment, Project, and Owner tags"
}
```

### GCP - Labels
```hcl
assert {
  condition = alltrue([
    contains(keys(google_storage_bucket.main.labels), "environment"),
    contains(keys(google_storage_bucket.main.labels), "project"),
    contains(keys(google_storage_bucket.main.labels), "owner")
  ])
  error_message = "Resource must have environment, project, and owner labels (lowercase)"
}
```

## Naming Conventions by Provider

### AWS Naming
```hcl
assert {
  condition = can(regex("^[a-z0-9-]+$", var.resource_name))
  error_message = "AWS resource names should use lowercase letters, numbers, and hyphens"
}
```

### Azure Naming
```hcl
assert {
  condition = length(var.storage_account_name) >= 3 && length(var.storage_account_name) <= 24
  error_message = "Azure storage account names must be 3-24 characters"
}

assert {
  condition = can(regex("^[a-z0-9]+$", var.storage_account_name))
  error_message = "Azure storage account names must be lowercase alphanumeric only"
}
```

### GCP Naming
```hcl
assert {
  condition = can(regex("^[a-z][a-z0-9-]*[a-z0-9]$", var.bucket_name))
  error_message = "GCP bucket names must start with letter, contain lowercase letters/numbers/hyphens, end with letter/number"
}
```
