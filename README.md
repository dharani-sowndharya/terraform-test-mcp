# Terraform Test Generator

An intelligent test case generator for Terraform infrastructure that creates comprehensive test suites following HashiCorp's official testing standards. Supports AWS, Azure, and GCP with multi-cloud test generation.

## Two Ways to Use This Project

### Option 1: MCP Server (Recommended for Multi-Project Use)

A lightweight MCP (Model Context Protocol) server that acts as an intelligent prompt generator. The MCP generates detailed instructions for Claude Code to analyze Terraform infrastructure and create thorough test suites.

**Best for:** Using across multiple Terraform projects with centralized updates.

### Option 2: Claude Code Skill (Recommended for Single Project)

A Claude Code skill that can be copied directly into your project's `.claude/skills/` directory for project-specific test generation.

**Best for:** Single-project use with direct invocation and no server setup required.

## Quick Start

### Using the MCP Server

#### 1. Install Dependencies

```bash
cd /path/to/terraform-test-mcp
pip install -e .
```

#### 2. Test CLI Mode

```bash
python main.py cli /path/to/your/terraform/project
```

#### 3. Configure with Claude Code

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "terraform-test-mcp": {
      "command": "python",
      "args": ["/path/to/terraform-test-mcp/main.py"],
      "cwd": "/path/to/terraform-test-mcp"
    }
  }
}
```

Or use the CLI command:

```bash
# Add the MCP
claude mcp add terraform-test-mcp python3 /path/to/terraform-test-mcp/main.py

# Remove the MCP (if needed)
claude mcp remove terraform-test-mcp
```

### Using the Claude Code Skill

#### 1. Copy Skill to Your Project

```bash
# From this repository
cp -r .claude /path/to/your/terraform/project/

# Or manually create the structure
mkdir -p /path/to/your/terraform/project/.claude/skills/
cp -r .claude/skills/terraform-test-generator /path/to/your/terraform/project/.claude/skills/
```

#### 2. Use the Skill in Claude Code

The skill is automatically available in your project. Simply invoke it:

```
/terraform-test-generator
```

Or mention it naturally:
```
"Use the terraform-test-generator skill to create tests for my infrastructure"
```

#### 3. Provide Required Information

The skill will ask you for:
1. **tfvars file** or variable values
2. **Compliance requirements** (e.g., tagging standards, encryption requirements)
3. **Terraform folder path** (automatically detected from your project)

## How It Works

### MCP Server Workflow

1. **User Request**: "Generate test cases for my Terraform infrastructure in `/infra`"
2. **MCP Server**: Validates path, loads template, generates comprehensive prompt
3. **Claude Code**: Receives prompt, reads Terraform files, analyzes infrastructure
4. **Claude Code**: Creates unit, integration, mock tests plus documentation
5. **Claude Code**: Writes all files to `/infra/tests/` directory

### Claude Skill Workflow

1. **User Invocation**: `/terraform-test-generator` in Claude Code
2. **Skill Activation**: Loads comprehensive testing guidelines
3. **User Input**: Provides tfvars and compliance requirements
4. **Infrastructure Analysis**: Detects cloud providers (AWS/Azure/GCP)
5. **Test Generation**: Creates provider-specific tests
6. **File Creation**: Writes all test files to `tests/` directory

## What Gets Generated

Both approaches generate comprehensive test suites:

### Test Files
- **Unit Tests** (`unit_*.tftest.hcl`): Mock provider tests for isolated validation
- **Integration Tests** (`integration_*.tftest.hcl`): Real provider tests with `command = apply`
- **Mock Tests** (`mock_*.tftest.hcl`): Override pattern tests
- **Variable Validation Tests**: Tests with `expect_failures` for invalid inputs

### Documentation
- **coverage_report.md**: Simple table of what was tested
- **README.md**: Test execution instructions and setup guide

### Multi-Cloud Support
- Automatically detects AWS, Azure, and/or GCP providers
- Generates provider-specific test syntax
- Includes cloud-specific compliance and security tests

## File Structure

```
terraform-test-mcp/
├── .claude/
│   └── skills/
│       └── terraform-test-generator/
│           └── skill.md           # Claude Code skill definition
├── main.py                        # Main MCP server with single tool
├── prompt_template.md             # Comprehensive testing guidelines (MCP)
├── README.md                      # This file
├── pyproject.toml                 # Project dependencies
└── logs/                          # Logging output
```

## Comparison: MCP vs Skill

| Feature | MCP Server | Claude Code Skill |
|---------|-----------|-------------------|
| **Setup** | One-time global install | Copy to each project |
| **Invocation** | Automatic via MCP tool | Manual `/terraform-test-generator` |
| **Updates** | Central location for all projects | Update per-project |
| **Dependencies** | Requires Python & pip install | No dependencies |
| **Best For** | Multiple Terraform projects | Single project or team sharing |
| **Portability** | Server must be running | Travels with project code |
| **Sharing** | Share server config | Share `.claude/` directory |

## Key Features

✅ **Multi-Cloud Support**: AWS, Azure, and GCP with provider-specific tests
✅ **Comprehensive Coverage**: Unit, integration, mock, and validation tests
✅ **Smart Detection**: Automatically detects cloud providers and resources
✅ **Best Practices**: Follows HashiCorp's official testing standards
✅ **Self-Review**: Built-in validation to prevent common test mistakes
✅ **Flexible Deployment**: Use as MCP server or Claude Code skill

## Troubleshooting

### MCP Server Issues

**MCP Not Responding:**
- Check that Python dependencies are installed: `pip install -e .`
- Verify the path in Claude Code configuration
- Check logs in `/tmp/terraform-test-mcp.log`

**Invalid Folder Path:**
- Ensure the folder exists and contains .tf files
- Check folder permissions
- Use absolute paths when possible

**Template Loading Issues:**
- Verify `prompt_template.md` exists in the project root
- Check file permissions and encoding

### Claude Skill Issues

**Skill Not Found:**
- Verify `.claude/skills/terraform-test-generator/skill.md` exists
- Check file is not empty (should be ~40KB)
- Restart Claude Code if recently added

**Test Generation Fails:**
- Ensure you provide tfvars values when asked
- Specify compliance requirements (or say "use standard best practices")
- Verify Terraform files are valid syntax

**Provider Detection Issues:**
- Check that `required_providers` or `provider` blocks exist
- Ensure provider blocks use standard names: `aws`, `azurerm`, `google`

## Development

### Modifying the MCP Template

1. Edit `prompt_template.md` with new testing guidelines
2. Restart the MCP server
3. Test with CLI mode: `python main.py cli /test/folder`

### Modifying the Claude Skill

1. Edit `.claude/skills/terraform-test-generator/skill.md`
2. Changes take effect immediately (no restart needed)
3. Test by invoking `/terraform-test-generator` in Claude Code

### Keeping Templates in Sync

Both `prompt_template.md` (MCP) and `skill.md` (Claude Skill) contain similar testing guidelines. When updating:

1. Apply changes to `skill.md` first (more comprehensive)
2. Selectively merge critical improvements to `prompt_template.md`
3. Test both approaches to ensure consistency

## Logging

- **MCP Server**: Logs to console and `/tmp/terraform-test-mcp.log`
- **Claude Skill**: Uses Claude Code's built-in logging

---

## Contributing

Contributions are welcome! Please:

1. Test changes with both MCP and Skill approaches
2. Update documentation for both methods
3. Ensure multi-cloud examples work (AWS, Azure, GCP)
4. Follow HashiCorp's official testing standards

---

**Note**: This project provides two deployment options for flexibility. Choose the MCP server for managing multiple Terraform projects, or use the Claude Code skill for project-specific test generation that travels with your codebase.