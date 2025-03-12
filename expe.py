from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import time
import os
import getpass

def analyze_code(input_code):
    """
    Analyzes the given code and returns a comprehensive report with issues and fixes.
    
    Args:
        input_code (str): The code to be analyzed
        
    Returns:
        str: Final report containing analysis, issues, fixes, and recommendations
    """
    # Initialize Google API key if not set
    if "GOOGLE_API_KEY" not in os.environ:
        # os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
        os.environ["GOOGLE_API_KEY"] = "AIzaSyBJuSTfgV3RTOlHe59MH6zDfwS-Ve4pnIo"

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Code Parser Prompt and Chain
    code_parser_prompt = ChatPromptTemplate.from_template("""
        *Code Input*: {user_code}
        Analyze this code and break it into:
        Intent:
        Components:
        Dependencies:
    """)
    code_parser_chain = LLMChain(llm=llm, prompt=code_parser_prompt, output_key="parsed_output")

    # Code Analyzer Prompt and Chain
    code_analyzer_prompt = ChatPromptTemplate.from_template("""
        {parsed_output}
        Analyze the code for the following:
        1. List potential issues (e.g., security vulnerabilities, bugs, inefficiencies).
        2. Identify code patterns relevant to the intent.
        
        Example Response:
        Issues: ["Hardcoded API key in login()", "No input validation in User class"]
        Patterns: ["Basic authentication flow", "Use of bcrypt for password hashing"]
    """)
    code_analyzer_chain = LLMChain(llm=llm, prompt=code_analyzer_prompt, output_key="analyzed_output")

    # Fix Generator Prompt and Chain
    fix_generator_prompt = ChatPromptTemplate.from_template("""
        {analyzed_output}
        Find "issues Found in (issues)" and "Patterns in (patterns)" in the analyzed output.
        For each issue:
        1. Explain why it is a problem.
        2. Suggest 1-2 fixes with code examples.
        3. Flag any risks in the fixes.
    """)
    fix_generator_chain = LLMChain(llm=llm, prompt=fix_generator_prompt, output_key="fixes_output")

    # Report Generator Prompt and Chain
    report_generator_prompt = ChatPromptTemplate.from_template("""
        *Fixes Suggested*: {fixes_output}
        *Objective*: Summarize the findings and recommendations in a way that is clear, actionable, and strategic for managers and CTOs.
        
        1. *Criticality of each issue* (Low/Medium/High)
        2. *Priority Order for Fixes*
        3. *Estimated Effort for Implementation*
        
        *Additional Considerations for Managers and CTOs*:
        - Address resource-heavy fixes
        - Minimize technical complexity
        - Provide clear actionable steps
        - Clarify the business impact
    """)
    report_generator_chain = LLMChain(llm=llm, prompt=report_generator_prompt, output_key="final_report")

    # Helper function to execute chain with delay
    def execute_chain_with_delay(chain, inputs):
        time.sleep(5)
        result = chain.invoke(inputs)
        time.sleep(5)
        return result

    # Execute the analysis pipeline
    try:
        # Step 1: Parse the code
        parsed_output = execute_chain_with_delay(code_parser_chain, {"user_code": input_code})
        
        # Step 2: Analyze the code
        analyzed_output = execute_chain_with_delay(code_analyzer_chain, parsed_output)
        
        # Step 3: Generate fixes
        fixes_output = execute_chain_with_delay(fix_generator_chain, analyzed_output)
        
        # Step 4: Generate final report
        final_output = execute_chain_with_delay(report_generator_chain, fixes_output)
        
        return final_output["final_report"]
    
    except Exception as e:
        return f"Error during code analysis: {str(e)}"

# Example usage
if __name__ == "__main__":
    example_code = """
    from flask import Flask, request, jsonify
    app = Flask(_name_)
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if data['username'] == 'admin' and data['password'] == 'secret':
            return jsonify({'message': 'Logged in'})
        return jsonify({'message': 'Invalid'}), 401
    
    if __name__ == '_main_':
        app.run(debug=True)
    """
    
    report = analyze_code(example_code)
    print("Final Report:")
    print(report)