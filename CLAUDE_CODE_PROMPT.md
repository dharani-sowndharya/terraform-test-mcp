<!-- ####################################################
## Claude Code Prompt ## 
####################################################
Objective: Set up and use the dockerized terraform-test-mcp to generate comprehensive test cases for a Terraform module.

**Prerequisites:**
- Terraform module located at a specific path
- Dockerized terraform-test-mcp container/image available in the machine or pull from remote based on provided config from claude-mcp-config
- Example tfvars file for configuration reference

 **IMPORTANT NOTES:**
 Once this prompt is provided, prompt the user for the terraform repo, mcp image if not available in local and terraform.tfvars file path and edit the mcp config to use the provided terraform repo as a volume mount

**Required Steps:**

1. Understand the terraform-test-mcp structure
  **IMPORTANT NOTES:**
  - This MCP mounts your actual terraform repository directly and writes test files to the `tests/` folder in your terraform project, not to separate directories
  - The container must be run in interactive mode (`-it`) to prevent it from exiting immediately, as MCP servers communicate via stdio
  - The volume mounts actual terraform repo, writes to tests/ folder
2. Build and deploy the containerized MCP
  - Use podman (preferred) or docker to run the image
  - Start container with interactive mode (-it -d) to prevent exit
  - Mount the terraform repository to /terraform-repo in container
  - Example: podman run -it -d --name terraform-test-mcp-server -v /path/to/terraform/repo:/terraform-repo terraform-test-mcp
3. Register the MCP in Claude Code configuration
  - Update ~/.claude/claude_desktop_config.json or equivalent
  - Configure to use podman exec or docker exec to communicate with running container
  - Example config:
  "TerraformTestGenerator": {
  "command": "podman",
  "args": ["exec", "-i", "container-name", "uv", "run", "python", "main.py"]
}
  - To use this MCP server with Claude Code, add the following configuration to your MCP settings:

  **For Podman:**
  ```json
  {
    "mcpServers": {
      "terraform-test-mcp": {
        "command": "podman",
        "args": [
          "exec", 
          "-i", 
          "terraform-test-mcp-server", 
          "uv", "run", "python", "main.py"
        ],
        "env": {}
      }
    }
  }
  ```

  **For Docker:**
  ```json
  {
    "mcpServers": {
      "terraform-test-mcp": {
        "command": "docker",
        "args": [
          "exec", 
          "-i", 
          "terraform-test-mcp-server", 
          "uv", "run", "python", "main.py"
        ],
        "env": {}
      }
    }
  }
  ```
4. Generate comprehensive test cases using the terraform-test-generator agent
  - Use the terraform-test-generator agent with the MCP
  - Provide the terraform module path and tfvars configuration
  - Request test coverage for: basic functionality, variable validation, edge cases, error conditions, and all module-specific features
5. Update documentation
  - Document any configuration changes made
  - Update README files with correct setup instructions
  - Note the requirement for interactive mode and proper volume mounting

Expected Output:
- Running dockerized MCP server
- Registered MCP in Claude Code configuration
- Comprehensive .tftest.hcl files in the terraform module's tests/ directory
- Test coverage report
- Updated documentation

Template Usage:
Please set up the dockerized terraform-test-mcp and generate comprehensive test cases for the Terraform module at [MODULE_PATH].

Use the tfvars configuration from [TFVARS_PATH].

Follow the complete setup process including:
1. Building and deploying the containerized MCP
2. Registering it in Claude Code configuration
3. Using the terraform-test-generator agent to generate comprehensive tests
4. Updating documentation with any changes made

Generate tests covering all module functionality, variable validation, edge cases, and error conditions.

---
Example filled template:
Please user terraform-test-mcp image to spin up a container and generate comprehensive test cases for the Terraform module at
/Users/Username/abcd/aws-api-gw-v2-http.

Use the tfvars configuration from examples/terraform.tfvars.

Follow the complete setup process including building the containerized MCP, registering it in Claude Code, using the terraform-test-generator agent, and updating documentation. -->