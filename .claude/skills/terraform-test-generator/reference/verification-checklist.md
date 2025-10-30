# Test Verification Checklist

Use this checklist before finalizing any Terraform test suite to ensure all tests meet quality standards and follow best practices.

## Pre-Generation Checklist

Before writing ANY tests, verify:

- [ ] Read `reference/anti-patterns.md` in full
- [ ] User requirements collected (tfvars values and compliance requirements)
- [ ] All Terraform files analyzed
- [ ] Cloud provider(s) detected (AWS/Azure/GCP)
- [ ] ALL data sources identified and documented
- [ ] Appropriate reference files reviewed for detected provider

## Anti-Pattern Compliance (MANDATORY)

Verify NO tests contain these anti-patterns:

### Command Selection
- [ ] NO computed attributes (`.id`, `.arn`, `.self_link`) tested with `command = plan`
- [ ] NO cross-resource references tested with `command = plan`
- [ ] All computed attribute tests use `command = apply`

### Mock Provider Usage
- [ ] NO override_data/override_resource blocks without `mock_provider` definition
- [ ] ALL mock providers defined at file level
- [ ] ALL mock providers referenced in `providers = { }` block

### Assertion Syntax
- [ ] NO indexing of set-type attributes with `[0]` notation
- [ ] ALL set-type attributes use `for` expressions
- [ ] NO multi-line conditions in assert blocks
- [ ] ALL assert conditions on single lines
- [ ] NO nullable boolean comparisons with `== false`
- [ ] Use `!= true` instead of `== false` for nullable booleans

### Data Source Mocking
- [ ] ALL data sources have `override_data` blocks in unit/mock tests
- [ ] NO missing data source mocks in unit tests
- [ ] All mock values are realistic and properly formatted

## Syntax Requirements

- [ ] All assert conditions are single-line (no multi-line ternary or AND/OR)
- [ ] No syntax errors in HCL
- [ ] All blocks properly closed
- [ ] Proper indentation (2 spaces)
- [ ] Valid Terraform identifiers used

## Mock Provider Requirements (Unit & Mock Tests)

- [ ] Mock provider declared at file level with `alias`
- [ ] Mock provider referenced in every `run` block's `providers = { }` section
- [ ] Realistic mock values provided
- [ ] Azure: All UUIDs in valid format (8-4-4-4-12)
- [ ] AWS: Valid ARN formats used
- [ ] GCP: Valid project IDs and resource paths

## Data Source Mocking (CRITICAL)

- [ ] ALL data sources identified from Terraform code
- [ ] Every data source has corresponding `override_data` block
- [ ] Mock values match expected data types
- [ ] `for_each` data sources mocked for each instance
- [ ] Azure: Each `for_each` data instance mocked with exact key

## Command Selection Validation

### Unit Tests
- [ ] Use `command = plan`
- [ ] Test configuration structure, NOT computed attributes
- [ ] Test variables and locals
- [ ] Test conditional logic and resource counts

### Integration Tests
- [ ] Use `command = apply`
- [ ] Test computed attributes (IDs, ARNs, endpoints)
- [ ] Test cross-resource references
- [ ] Test outputs
- [ ] Include cleanup/destroy where appropriate

### Mock Tests
- [ ] Use `command = plan` (unless testing specific apply scenarios)
- [ ] Include override_data for all data sources
- [ ] Include override_module for external modules

### Validation Tests
- [ ] ONLY generated if validations exist in code
- [ ] Use `command = plan` for variable validations
- [ ] Use `command = apply` for postconditions
- [ ] Correct `expect_failures` targets specified

## Variable Handling

- [ ] ALL required variables provided in every test
- [ ] Variables use tfvars values for realistic testing
- [ ] No missing required variables
- [ ] No undefined variable references
- [ ] Variable types match declarations

## Test Quality Standards

### Naming
- [ ] File names follow convention: `unit_*.tftest.hcl`, `integration_*.tftest.hcl`, etc.
- [ ] Test names are descriptive: `test_<feature>_<scenario>`
- [ ] Names use underscores, not hyphens

### Error Messages
- [ ] All assert blocks have `error_message`
- [ ] Error messages are descriptive and actionable
- [ ] Messages explain WHAT failed and WHY it matters
- [ ] No generic messages like "Test failed"

### Test Isolation
- [ ] Each test focuses on one concern
- [ ] Tests don't depend on other tests
- [ ] Tests can run in any order
- [ ] No shared state between tests

### Coverage
- [ ] At least one unit test per feature
- [ ] At least one integration test per resource type
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Compliance requirements covered

## Cloud Provider-Specific Checks

### AWS
- [ ] Set-type attributes (security_group.ingress, etc.) use `for` expressions
- [ ] No hardcoded account IDs (use variables or data sources)
- [ ] ARN formats are valid
- [ ] Region-specific resources use correct regions

### Azure
- [ ] All UUIDs in 8-4-4-4-12 format
- [ ] Resource group names are realistic
- [ ] `for_each` data sources mocked individually
- [ ] azurerm AND azuread providers mocked if both used

### GCP
- [ ] Project IDs are valid format
- [ ] Service account emails are properly formatted
- [ ] Self-link URLs are complete and valid
- [ ] Labels use lowercase (not Tags with capital T)

## Compliance Test Validation

Based on user requirements:

- [ ] All mandatory tags/labels tested
- [ ] Encryption requirements tested
- [ ] Network security requirements tested
- [ ] IAM/access control requirements tested
- [ ] Logging requirements tested
- [ ] Backup/retention requirements tested

## Documentation Completeness

- [ ] `tests/README.md` created with:
  - [ ] Overview of test suite
  - [ ] Prerequisites listed
  - [ ] Running tests instructions
  - [ ] Test organization explained
  - [ ] Compliance requirements documented

- [ ] `tests/COVERAGE.md` created with:
  - [ ] Test summary table
  - [ ] Test categories breakdown
  - [ ] Resource coverage table
  - [ ] Compliance coverage checklist
  - [ ] Known limitations documented

## Final Pre-Delivery Checklist

- [ ] ALL user requirements addressed
- [ ] NO anti-patterns present in any test
- [ ] All tests syntactically correct
- [ ] All cross-references to templates and reference files valid
- [ ] Test suite is complete (unit + integration + compliance minimum)
- [ ] Documentation is complete and accurate
- [ ] Tests can be executed with `terraform test`

## Common Failure Patterns to Avoid

### Top 4 Causes of Test Failures

1. **Missing Data Source Mocks**
   - [ ] Verified ALL data sources have override_data in unit tests
   - [ ] No "data source not found" errors

2. **Indexing Set-Type Attributes**
   - [ ] No `[0]` indexing on sets (security_group.ingress, etc.)
   - [ ] Using `for` expressions for all set-type access

3. **Testing Computed Attributes with Plan**
   - [ ] No `.id`, `.arn`, `.self_link` tests with `command = plan`
   - [ ] Computed attributes only tested with `command = apply`

4. **Multi-Line Assert Conditions**
   - [ ] All conditions on single line
   - [ ] No multi-line ternary operators
   - [ ] No multi-line AND/OR chains

## If Tests Fail

When tests fail, check in this order:

1. **Missing Data Source Mocks**: Run `grep "data\." *.tf` and verify all have `override_data`
2. **Command Selection**: Are you testing computed attributes with `command = plan`?
3. **Set Indexing**: Search for `\[0\]` in test files - are any on set-type attributes?
4. **Syntax**: Are all assert conditions single-line?
5. **Variables**: Are ALL required variables provided in the test?
6. **Mock Provider**: Is mock_provider defined AND referenced in providers block?

## Quality Gates

Do not mark work complete unless:

- [ ] Zero anti-patterns detected
- [ ] All syntax validated
- [ ] All data sources mocked
- [ ] All variables provided
- [ ] Documentation complete
- [ ] Coverage meets minimum requirements (unit + integration + compliance)
- [ ] User requirements fully addressed

---

**Remember**: Taking 5 minutes to verify against this checklist saves hours of debugging failed tests.
