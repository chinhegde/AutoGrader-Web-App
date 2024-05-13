# grading.py
import time

def grade_solution(solution):
    """
    Grade the solution against test cases and display test results with execution times.
    """
    # Define the test cases
    test_cases = [
        (7, True),
        (15, True),
        (21, True),
        (33, True),
        (44, False),
        (55, False),
        (127, True),
        (128, False)
    ]
    # Evaluate the student's solution against the test cases
    score = 0
    results = []  # Store test results
    for input_value, expected_output in test_cases:
        start_time = time.time()  # Start timer
        result = autograder(solution, input_value)
        execution_time = round((time.time() - start_time) * 1000)  # Calculate execution time in milliseconds
        test_result = f"Test Case: Input={input_value}, Expected Output={expected_output}, Actual Output={result}, Execution Time={execution_time}ms"
        results.append(test_result)
        if result == expected_output:
            score += 1
    total_test_cases = len(test_cases)
    percentage_score = (score / total_test_cases) * 100
    # Prepare test output for display
    test_output = '\n'.join(results)
    final_output = f"Grading Results:\n{test_output}\n\nScore: {score}/{total_test_cases}, Percentage Score: {percentage_score}%"
    print(final_output)  # Print test output for debugging purposes
    return percentage_score, final_output

def autograder(code_string, k):
    # Split the code string into lines
    code_lines = code_string.split('\n')
    # Indent each line by four spaces
    indented_code_lines = ['    ' + line for line in code_lines]
    # Join the indented lines back into a single string
    indented_code_string = '\n'.join(indented_code_lines)
    # Wrap the indented code in a function called myFunc
    wrapped_code = f"def myFunc(k):\n{indented_code_string}\n    return myFunc(k)"
    
    try:
        # Create a local namespace dictionary to capture the result
        local_namespace = {}
        # Execute the wrapped code within the local namespace
        exec(wrapped_code, {}, local_namespace)
        # Get the result from the local namespace
        result = local_namespace['myFunc'](k)
        return result
    except Exception as e:
        return f"Error: {e}"

