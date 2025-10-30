# Compliance Test Patterns

## Table of Contents
- [Tagging and Labeling Requirements](#tagging-and-labeling-requirements)
- [Encryption Requirements](#encryption-requirements)
- [Network Security Requirements](#network-security-requirements)
- [IAM and Access Control](#iam-and-access-control)
- [Logging and Monitoring](#logging-and-monitoring)
- [Data Protection](#data-protection)

## Tagging and Labeling Requirements

### AWS & Azure - Mandatory Tags Pattern

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

### GCP - Mandatory Labels Pattern

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

### Tag Value Format Validation

```hcl
assert {
  condition = can(regex("^(dev|staging|prod)$", aws_instance.main.tags["Environment"]))
  error_message = "Environment tag must be dev, staging, or prod"
}

assert {
  condition = length(aws_instance.main.tags["CostCenter"]) > 0
  error_message = "CostCenter tag is required and cannot be empty"
}
```

## Encryption Requirements

### Storage Encryption with KMS/CMK

**AWS S3:**
```hcl
assert {
  condition = aws_s3_bucket_server_side_encryption_configuration.main.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "aws:kms"
  error_message = "S3 bucket must use KMS encryption"
}

assert {
  condition = aws_s3_bucket_server_side_encryption_configuration.main.rule[0].apply_server_side_encryption_by_default[0].kms_master_key_id != null
  error_message = "S3 bucket must specify KMS key ID"
}
```

**Azure Storage:**
```hcl
assert {
  condition = length(azurerm_storage_account.main.customer_managed_key) > 0
  error_message = "Storage account must use customer-managed keys"
}

assert {
  condition = azurerm_storage_account.main.customer_managed_key[0].key_vault_key_id != null
  error_message = "Storage account must specify Key Vault key ID"
}
```

**GCP Storage:**
```hcl
assert {
  condition = length(google_storage_bucket.main.encryption) > 0
  error_message = "Storage bucket must have encryption configured"
}

assert {
  condition = google_storage_bucket.main.encryption[0].default_kms_key_name != null
  error_message = "Storage bucket must use customer-managed encryption keys"
}
```

### Database Encryption

**AWS RDS:**
```hcl
assert {
  condition = aws_db_instance.main.storage_encrypted == true
  error_message = "RDS instance must have storage encryption enabled"
}

assert {
  condition = aws_db_instance.main.kms_key_id != null
  error_message = "RDS instance must use KMS encryption"
}
```

**Azure Database:**
```hcl
assert {
  condition = azurerm_postgresql_flexible_server.main.customer_managed_key[0].key_vault_key_id != null
  error_message = "PostgreSQL server must use customer-managed keys"
}
```

**GCP Database:**
```hcl
assert {
  condition = google_sql_database_instance.main.settings[0].disk_encryption_configuration[0].kms_key_name != null
  error_message = "SQL instance must use customer-managed encryption keys"
}
```

### Encryption in Transit

```hcl
# AWS - Require TLS
assert {
  condition = aws_lb_listener.main.protocol == "HTTPS"
  error_message = "Load balancer listener must use HTTPS"
}

# Azure - Minimum TLS version
assert {
  condition = azurerm_storage_account.main.min_tls_version == "TLS1_2"
  error_message = "Storage account must require TLS 1.2 or higher"
}

# GCP - Enforce SSL
assert {
  condition = google_sql_database_instance.main.settings[0].ip_configuration[0].require_ssl == true
  error_message = "SQL instance must require SSL connections"
}
```

## Network Security Requirements

### Restrictive Security Group/Firewall Rules

**AWS Security Groups:**
```hcl
assert {
  condition = length([for rule in aws_security_group.main.ingress : rule if contains(rule.cidr_blocks, "0.0.0.0/0")]) == 0
  error_message = "Security groups must not allow unrestricted ingress (0.0.0.0/0)"
}

assert {
  condition = length([for rule in aws_security_group.main.ingress : rule if rule.from_port == 22 && contains(rule.cidr_blocks, "0.0.0.0/0")]) == 0
  error_message = "SSH (port 22) must not be open to the internet"
}
```

**Azure NSG Rules:**
```hcl
assert {
  condition = azurerm_network_security_rule.main.source_address_prefix != "*"
  error_message = "NSG rule must not allow traffic from any source (*)"
}

assert {
  condition = azurerm_network_security_rule.main.priority >= 100 && azurerm_network_security_rule.main.priority <= 4096
  error_message = "NSG rule priority must be between 100 and 4096"
}
```

**GCP Firewall Rules:**
```hcl
assert {
  condition = length([for range in google_compute_firewall.main.source_ranges : range if range == "0.0.0.0/0"]) == 0
  error_message = "Firewall rules must not allow unrestricted access (0.0.0.0/0)"
}

assert {
  condition = length(google_compute_firewall.main.target_tags) > 0 || length(google_compute_firewall.main.target_service_accounts) > 0
  error_message = "Firewall rules must specify target tags or service accounts"
}
```

### Public Access Controls

**AWS:**
```hcl
assert {
  condition = aws_s3_bucket_public_access_block.main.block_public_acls == true
  error_message = "S3 bucket must block public ACLs"
}

assert {
  condition = aws_s3_bucket_public_access_block.main.block_public_policy == true
  error_message = "S3 bucket must block public policies"
}
```

**Azure:**
```hcl
assert {
  condition = azurerm_storage_account.main.allow_nested_items_to_be_public == false
  error_message = "Storage account must disable public blob access"
}

assert {
  condition = azurerm_storage_account.main.public_network_access_enabled == false
  error_message = "Storage account must disable public network access"
}
```

**GCP:**
```hcl
assert {
  condition = google_storage_bucket.main.uniform_bucket_level_access[0].enabled == true
  error_message = "Storage bucket must use uniform bucket-level access"
}

assert {
  condition = length([for binding in google_storage_bucket_iam_binding.main : binding if binding.member == "allUsers" || binding.member == "allAuthenticatedUsers"]) == 0
  error_message = "Storage bucket must not grant public access via IAM"
}
```

## IAM and Access Control

### Least Privilege Principles

**AWS:**
```hcl
assert {
  condition = length([for statement in jsondecode(aws_iam_policy.main.policy).Statement : statement if statement.Effect == "Allow" && statement.Action == "*"]) == 0
  error_message = "IAM policy must not allow all actions (*)"
}

assert {
  condition = length([for statement in jsondecode(aws_iam_policy.main.policy).Statement : statement if statement.Effect == "Allow" && statement.Resource == "*"]) == 0
  error_message = "IAM policy must not grant access to all resources (*)"
}
```

**Azure:**
```hcl
assert {
  condition = azurerm_role_assignment.main.role_definition_name != "Owner"
  error_message = "Should not assign Owner role unless absolutely necessary"
}

assert {
  condition = length(azurerm_linux_virtual_machine.main.identity) > 0
  error_message = "Virtual machine must use managed identity"
}
```

**GCP:**
```hcl
assert {
  condition = google_project_iam_member.main.role != "roles/owner"
  error_message = "Should not grant Owner role at project level"
}

assert {
  condition = !startswith(google_service_account.main.account_id, "Compute Engine default")
  error_message = "Must use custom service account, not default Compute Engine account"
}
```

### Permissions Boundaries

**AWS:**
```hcl
assert {
  condition = aws_iam_role.main.permissions_boundary != null
  error_message = "IAM role must have permissions boundary attached"
}
```

**Azure:**
```hcl
assert {
  condition = azurerm_management_lock.main.lock_level == "CanNotDelete"
  error_message = "Critical resources must have deletion lock"
}
```

## Logging and Monitoring

### Audit Logging

**AWS:**
```hcl
assert {
  condition = aws_s3_bucket_logging.main.target_bucket != null
  error_message = "S3 bucket must have access logging enabled"
}

assert {
  condition = aws_db_instance.main.enabled_cloudwatch_logs_exports != null
  error_message = "RDS instance must export logs to CloudWatch"
}
```

**Azure:**
```hcl
assert {
  condition = length(azurerm_monitor_diagnostic_setting.main) > 0
  error_message = "Resource must have diagnostic settings configured"
}

assert {
  condition = azurerm_storage_account.main.queue_properties[0].logging[0].delete == true
  error_message = "Storage account must log delete operations"
}
```

**GCP:**
```hcl
assert {
  condition = length(google_compute_subnetwork.main.log_config) > 0
  error_message = "Subnet must have VPC Flow Logs enabled"
}

assert {
  condition = google_storage_bucket.main.logging[0].log_bucket != null
  error_message = "Storage bucket must have access logging enabled"
}
```

### Retention Policies

```hcl
# AWS CloudWatch Logs
assert {
  condition = aws_cloudwatch_log_group.main.retention_in_days >= 90
  error_message = "CloudWatch log group must retain logs for at least 90 days"
}

# Azure Storage
assert {
  condition = azurerm_storage_management_policy.main.rule[0].actions[0].base_blob[0].delete_after_days_since_modification_greater_than >= 90
  error_message = "Storage lifecycle policy must retain data for at least 90 days"
}
```

## Data Protection

### Backup Requirements

**AWS:**
```hcl
assert {
  condition = aws_db_instance.main.backup_retention_period >= 7
  error_message = "RDS instance must retain backups for at least 7 days"
}

assert {
  condition = aws_ebs_volume.main.encrypted == true
  error_message = "EBS volume must be encrypted"
}
```

**Azure:**
```hcl
assert {
  condition = azurerm_backup_policy_vm.main.retention_daily[0].count >= 7
  error_message = "Backup policy must retain daily backups for at least 7 days"
}

assert {
  condition = azurerm_postgresql_flexible_server.main.backup_retention_days >= 7
  error_message = "Database must retain backups for at least 7 days"
}
```

**GCP:**
```hcl
assert {
  condition = google_sql_database_instance.main.settings[0].backup_configuration[0].enabled == true
  error_message = "SQL instance must have automated backups enabled"
}

assert {
  condition = google_compute_disk.main.disk_encryption_key != null
  error_message = "Compute disk must be encrypted"
}
```

### Versioning and Soft Delete

**AWS S3:**
```hcl
assert {
  condition = aws_s3_bucket_versioning.main.versioning_configuration[0].status == "Enabled"
  error_message = "S3 bucket must have versioning enabled"
}
```

**Azure Storage:**
```hcl
assert {
  condition = azurerm_storage_account.main.blob_properties[0].delete_retention_policy[0].days >= 7
  error_message = "Storage account must enable soft delete with minimum 7 days retention"
}
```

**GCP Storage:**
```hcl
assert {
  condition = google_storage_bucket.main.versioning[0].enabled == true
  error_message = "Storage bucket must have versioning enabled"
}
```

## Multi-Compliance Framework Examples

### SOC 2 Compliance Checks

```hcl
run "test_soc2_encryption_requirements" {
  command = plan

  providers = {
    aws = aws.mock
  }

  variables {
    # ... all required variables
  }

  # Encryption at rest
  assert {
    condition = aws_s3_bucket_server_side_encryption_configuration.main.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "aws:kms"
    error_message = "SOC 2: Data at rest must be encrypted with KMS"
  }

  # Encryption in transit
  assert {
    condition = aws_lb_listener.main.protocol == "HTTPS"
    error_message = "SOC 2: Data in transit must use HTTPS"
  }

  # Audit logging
  assert {
    condition = aws_s3_bucket_logging.main.target_bucket != null
    error_message = "SOC 2: Access logs must be enabled"
  }
}
```

### HIPAA Compliance Checks

```hcl
run "test_hipaa_requirements" {
  command = plan

  providers = {
    aws = aws.mock
  }

  variables {
    # ... all required variables
  }

  # PHI encryption
  assert {
    condition = aws_db_instance.main.storage_encrypted == true
    error_message = "HIPAA: Database storing PHI must be encrypted"
  }

  # Backup retention
  assert {
    condition = aws_db_instance.main.backup_retention_period >= 7
    error_message = "HIPAA: Must retain backups for at least 7 days"
  }

  # Network isolation
  assert {
    condition = aws_db_instance.main.publicly_accessible == false
    error_message = "HIPAA: Database must not be publicly accessible"
  }
}
```

### PCI-DSS Compliance Checks

```hcl
run "test_pci_dss_requirements" {
  command = plan

  providers = {
    aws = aws.mock
  }

  variables {
    # ... all required variables
  }

  # Strong encryption
  assert {
    condition = aws_db_instance.main.storage_encrypted == true
    error_message = "PCI-DSS: Cardholder data must be encrypted"
  }

  # Network segmentation
  assert {
    condition = length([for rule in aws_security_group.main.ingress : rule if contains(rule.cidr_blocks, "0.0.0.0/0")]) == 0
    error_message = "PCI-DSS: Must segment cardholder data environment"
  }

  # Access logging
  assert {
    condition = aws_s3_bucket_logging.main.target_bucket != null
    error_message = "PCI-DSS: Must log all access to cardholder data"
  }
}
```

## Custom Compliance Requirements

### Organizational Policy Examples

```hcl
# Cost center tagging
assert {
  condition = contains(keys(aws_instance.main.tags), "CostCenter")
  error_message = "Organization policy: All resources must have CostCenter tag"
}

# Naming convention
assert {
  condition = can(regex("^${var.organization_prefix}-[a-z0-9-]+$", aws_instance.main.tags["Name"]))
  error_message = "Organization policy: Resource names must follow naming convention"
}

# Environment separation
assert {
  condition = contains(["dev", "staging", "prod"], var.environment)
  error_message = "Organization policy: Environment must be dev, staging, or prod"
}

# Approved regions
assert {
  condition = contains(["us-east-1", "us-west-2", "eu-west-1"], var.region)
  error_message = "Organization policy: Must deploy to approved regions only"
}
```
