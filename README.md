# Terraform Test Prompt Generator MCP

A lightweight MCP (Model Context Protocol) server that acts as an intelligent prompt generator for creating comprehensive Terraform test cases. This MCP generates detailed instructions for Claude Code to analyze Terraform infrastructure and create thorough test suites.

## Purpose

This MCP serves as a **prompt generator only** - it does not create files or perform infrastructure analysis. Instead, it:

1. **Validates Terraform folder paths** to ensure they contain .tf files
2. **Loads comprehensive testing guidelines** from template files
3. **Generates structured prompts** for Claude Code to process
4. **Returns detailed instructions** for test case generation

## Architecture

```
User Request → MCP Prompt Generator → Claude Code → Test Files
     ↓                ↓                    ↓           ↓
   Folder Path    Validates Path    Reads Terraform  Creates Tests
                 Loads Template     Analyzes Code    Writes Files
                 Returns Prompt     Follows Guide    In tests/
```

## Quick Start

### 1. Install Dependencies

```bash
cd /path/to/terraform-test-mcp
pip install -e .
```

### 2. Test CLI Mode

```bash
python main.py cli /path/to/your/terraform/project
```

### 3. Configure with Claude Code

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

## Available Tools

### `generate_test_prompt`

The single MCP tool that generates comprehensive testing prompts.

**Parameters:**
- `folder_path` (string): Path to Terraform project folder

**Returns:**
- Detailed prompt for Claude Code to generate test cases
- Instructions for unit, integration, and mock tests
- Guidelines for documentation and coverage reports

**Example Usage:**
```python
# In Claude Code, this will be called automatically when you use the MCP
result = await generate_test_prompt("/path/to/terraform/project")
```

## How It Works

1. **Path Validation**: Verifies the folder exists and contains .tf files
2. **Template Loading**: Loads comprehensive testing guidelines from `prompt_template.md`
3. **Prompt Generation**: Creates structured instructions for Claude Code
4. **Return Instructions**: Provides detailed guidance for:
   - Infrastructure analysis
   - Unit test creation with mocks
   - Integration test creation with real providers
   - Mock test creation with overrides
   - Documentation and coverage reports

## Example Workflow

1. **User**: "Generate test cases for my Terraform infrastructure in `/infra`"
2. **MCP**: Validates path, loads template, generates comprehensive prompt
3. **Claude Code**: Receives prompt, reads Terraform files, analyzes infrastructure
4. **Claude Code**: Creates unit, integration, mock tests plus documentation
5. **Claude Code**: Writes all files to `/infra/tests/` directory

## File Structure

```
terraform-test-mcp/
├── main.py                 # Main MCP server with single tool
├── prompt_template.md      # Comprehensive testing guidelines
├── README.md              # This file
├── pyproject.toml         # Project dependencies
└── logs/                  # Logging output
```

## Key Features

✅ **Lightweight**: Single tool, no file operations
✅ **Intelligent**: Comprehensive testing guidelines
✅ **Flexible**: Works with any Terraform project structure
✅ **Structured**: Clear instructions for Claude Code
✅ **Complete**: Covers all test types and documentation

## Troubleshooting

### MCP Not Responding
- Check that Python dependencies are installed
- Verify the path in Claude Code configuration
- Check logs in the `logs/` directory

### Invalid Folder Path
- Ensure the folder exists and contains .tf files
- Check folder permissions
- Use absolute paths when possible

### Template Loading Issues
- Verify `prompt_template.md` exists in the project root
- Check file permissions and encoding

## Development

To modify the prompt template:
1. Edit `prompt_template.md` with new testing guidelines
2. Restart the MCP server
3. Test with CLI mode: `python main.py cli /test/folder`

## Logging

The MCP logs to both console and `/tmp/terraform-test-mcp.log` for debugging purposes.

---

**Note**: This MCP is designed to work with Claude Code for the actual file creation and infrastructure analysis. It serves purely as an intelligent prompt generator to ensure comprehensive test coverage.

---
## Remove the mcp
claude mcp remove terraform-test-mcp

## Add the mcp
claude mcp add terraform-test-mcp python3 /Users/<folder>/terraform-test-mcp/main.py