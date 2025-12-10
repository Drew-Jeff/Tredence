class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name):
        def decorator(func):
            self._tools[name] = func
            return func
        return decorator

    def get_tool(self, name):
        return self._tools.get(name)

registry = ToolRegistry()

# --- Example Tools for Option A (Code Review) ---

@registry.register("extract_functions")
def extract_functions(code: str):
    # Mock regex extraction
    return ["def hello():", "def world():"]

@registry.register("calculate_complexity")
def calculate_complexity(code_snippet: str):
    # Mock complexity calculation
    return len(code_snippet)

@registry.register("lint_code")
def lint_code(code: str):
    if "bad_var" in code:
        return ["Variable name 'bad_var' is ambiguous"]
    return []