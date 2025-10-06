import os
import sys
import logging
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('/tmp/terraform-test-mcp.log', mode='a')
    ]
)

logger = logging.getLogger("TerraformTestMCP")

mcp = FastMCP("TerraformTestPromptGenerator")

# Path validation helpers
def validate_folder_path(folder_path: str) -> tuple[bool, str]:
    """
    Validate that the provided folder path exists and contains Terraform files.

    Args:
        folder_path: Path to validate
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not folder_path or not isinstance(folder_path, str):
        return False, "Folder path must be a non-empty string"

    folder_path = folder_path.strip()
    if not folder_path:
        return False, "Folder path cannot be empty or only whitespace"

    if not os.path.exists(folder_path):
        return False, f"Folder path '{folder_path}' does not exist"

    if not os.path.isdir(folder_path):
        return False, f"Path '{folder_path}' is not a directory"

    # Check for .tf files
    try:
        tf_files = [f for f in os.listdir(folder_path) if f.endswith('.tf')]
        if not tf_files:
            return False, "No Terraform (.tf) files found in the specified folder"
    except PermissionError:
        return False, f"Permission denied accessing folder '{folder_path}'"

    return True, ""

logger.info("Initializing Terraform Test Prompt Generator MCP")
logger.info(f"Server started at: {datetime.now().isoformat()}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Available tools will be: generate_test_prompt")

# Load the prompt template from a file
async def load_prompt_template(filepath: str = "prompt_template.md") -> str: 
    """ 
    Async function to load prompt template from file.
    
    Why async: Prevents blocking the MCP server when reading large template files.
    This allows the server to handle other requests concurrently.
    
    Args:
        filepath: Path to the template file
    Returns:
        Template content as string
    """ 
    logger.info(f"Loading prompt template from: {filepath}")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filepath)
    
    try:
        logger.debug(f"Attempting to load template from: {full_path}")
        # Use asyncio.to_thread to run file I/O in thread pool
        # This prevents blocking the event loop during file reads
        def _read_file(path: str) -> str:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
                
        template_content = await asyncio.to_thread(_read_file, full_path)
        logger.info(f"Successfully loaded template ({len(template_content)} characters)")
        return template_content
        
    except FileNotFoundError as e:
        logger.warning(f"Template not found at {full_path}, trying fallback: {filepath}")
        try:
            template_content = await asyncio.to_thread(_read_file, filepath)
            logger.info(f"Successfully loaded template from fallback ({len(template_content)} characters)")
            return template_content
        except FileNotFoundError as fallback_error:
            logger.error(f"Failed to load template from both locations: {e}, {fallback_error}")
            raise


# Generate Claude Code prompt for Terraform test cases
async def generate_terraform_test_prompt(folder_path: str) -> str:
    """
    Generate an intelligent prompt for Claude Code to create comprehensive Terraform test cases.

    This function:
    1. Loads the comprehensive prompt template with testing instructions
    2. Creates a structured request for Claude Code to process
    3. Returns detailed instructions for Claude Code to analyze infrastructure and generate tests

    Args:
        folder_path (str): Path to the Terraform folder to analyze
    Returns:
        str: Comprehensive prompt for Claude Code to generate test cases
    """
    logger.info("Preparing Terraform test generation request for Claude Code")
    logger.info(f"Target folder: {folder_path}")

    try:
        # Load the prompt template
        logger.info("Loading prompt template for Claude Code processing")
        prompt_template = await load_prompt_template()

        # Replace the placeholder with folder path reference
        logger.debug("Preparing comprehensive prompt for Claude Code")
        prompt_with_path = prompt_template.replace(
            "{terraform_code_path}",
            f"TERRAFORM_FOLDER_PATH: {folder_path}"
        )

        # Return a comprehensive prompt for Claude Code to process
        claude_request = f"""🎯 **TERRAFORM TEST GENERATION REQUEST**

Claude Code, I need you to generate comprehensive Terraform test cases for the infrastructure located at: `{folder_path}`

## Your Tasks:

### 1. Infrastructure Analysis
- Read and analyze all .tf files in the folder: `{folder_path}`
- Understand resources, modules, variables, data sources, and their relationships
- Identify key components that need testing coverage

### 2. Test Generation
Using the comprehensive prompt below as your guide, generate:
- **Unit tests** with mock providers (unit_*.tftest.hcl)
- **Integration tests** with real providers (integration_*.tftest.hcl)
- **Mock tests** with override patterns (mock_*.tftest.hcl)
- **Variable validation tests** with expect_failures
- **Coverage report** (coverage_report.md)
- **README documentation** (README.md)

### 3. File Creation
Write all test files directly to: `{folder_path}/tests/`

---

## COMPREHENSIVE TESTING GUIDE:

{prompt_with_path}

---

🤖 **Start by reading the Terraform files, then generate the complete test suite following the above guidelines.**
"""

        logger.info("Successfully prepared comprehensive testing prompt for Claude Code")
        return claude_request

    except Exception as e:
        logger.error(f"Failed to prepare testing prompt: {e}")
        raise



# Main tool - generates comprehensive prompt for Claude Code
@mcp.tool()
async def generate_test_prompt(folder_path: str) -> str:
    """
    Generate comprehensive testing prompt for Claude Code to create Terraform test cases.

    This tool acts as an intelligent prompt generator that provides Claude Code with
    detailed instructions for analyzing Terraform infrastructure and generating
    comprehensive test suites.

    Args:
        folder_path (str): Path to folder containing Terraform files to test
                          Example: "/path/to/terraform/modules/vpc"
    Returns:
        str: Comprehensive prompt for Claude Code to process
    """
    logger.info(f"=== MCP TOOL CALLED: generate_test_prompt ===")
    logger.info(f"Request timestamp: {datetime.now().isoformat()}")
    logger.info(f"Generating prompt for folder: {folder_path}")

    try:
        # Validate input
        is_valid, error_msg = validate_folder_path(folder_path)
        if not is_valid:
            logger.warning(f"Invalid folder path: {error_msg}")
            return f"Error: {error_msg}"

        logger.info(f"Folder validation passed, preparing comprehensive testing prompt")

        # Quick file count for logging
        tf_files = [f for f in os.listdir(folder_path) if f.endswith('.tf')]
        logger.info(f"Found {len(tf_files)} Terraform files: {tf_files}")

        # Generate the comprehensive prompt
        result = await generate_terraform_test_prompt(folder_path=folder_path)

        logger.info(f"Successfully generated prompt ({len(result)} characters)")
        logger.info("=== RETURNING COMPREHENSIVE TESTING PROMPT FOR CLAUDE CODE ===")

        return result

    except Exception as e:
        logger.error(f"=== MCP TOOL FAILED ===")
        logger.error(f"Error in generate_test_prompt: {e}")
        logger.exception("Full exception details:")
        return f"Error generating test prompt: {str(e)}"

    
if __name__ == "__main__": 
    # Check for CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # CLI Mode - Generate prompt and display
        if len(sys.argv) != 3:
            print("Usage: python main.py cli <folder_path>", file=sys.stderr)
            sys.exit(1)

        folder_path = sys.argv[2]
        logger.info(f"=== CLI MODE: Generating test prompt for {folder_path} ===")

        async def cli_main():
            try:
                result = await generate_test_prompt(folder_path)
                print(result)

            except Exception as e:
                logger.error(f"CLI mode failed: {e}")
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

        asyncio.run(cli_main())

    else:
        # MCP Server Mode
        logger.info("=== TERRAFORM TEST PROMPT GENERATOR MCP SERVER STARTING ===")
        logger.info(f"Process ID: {os.getpid()}")
        logger.info(f"Environment variables:")
        for key, value in os.environ.items():
            if 'MCP' in key or 'TERRAFORM' in key or 'DOCKER' in key:
                logger.info(f"  {key}={value}")

        logger.info("Registering MCP tools...")
        logger.info("Available MCP tools: generate_test_prompt")

        print("Starting Terraform Test Prompt Generator MCP Server...", file=sys.stderr)
        logger.info("Starting MCP server main loop...")

        try:
            mcp.run()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            logger.error(f"MCP server error: {e}")
            logger.exception("Full exception details:")
            raise
        finally:
            logger.info("=== TERRAFORM TEST PROMPT GENERATOR MCP SERVER STOPPED ===")
            logger.info(f"Shutdown timestamp: {datetime.now().isoformat()}")