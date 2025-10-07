  * Generate test cases for the terraform code present in the <folder>. 
  * For tfvars, use the <terraform.tfvars> in the <folder>
  * The following compliance should be checked as part of the test cases and should fail if it is not met
    * The security group should not allow "0.0.0.0/0" in the ingress
    * All the resources created should have "Environment" and "Owner" tags. 

  
Use the terraform-test-mcp to generate test cases. Upon using the terraform-test-mcp, follow the instructions provided by the terraform-test-mcp
   SEQUENTIALLY AND COMPLETELY.

  MANDATORY PROCESS:
  1. After reading the terraform-test-mcp instructions, DO NOT immediately start generating tests
  2. For EACH test file you plan to generate, FIRST show me:
     - What you plan to test
     - **EVERY SINGLE assert statement** (complete list, not samples)
     - **Line-by-line validation** against ALL good/bad examples from terraform-test-mcp
  3. Wait for my approval before writing ANY files
  4. Generate files using ONLY the exact assertions I approved - no additions, no variations
  5. **MANDATORY PRE-WRITE CHECK**: Before calling Write tool, verify the content against terraform-test-mcp's forbidden patterns. If ANY
  violation found, STOP and show me for review.

  If you write files without showing COMPLETE assertion lists, or if generated files differ from approved assertions, you are violating this
  instruction.

  The key changes:
  - ✅ "EVERY SINGLE assert statement" (not "sample")
  - ✅ "Line-by-line validation against ALL good/bad examples" (forces comprehensive check)
  - ✅ "MANDATORY PRE-WRITE CHECK" (one final gate before file creation)
  - ✅ Explicit consequences for violations