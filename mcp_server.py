from fastmcp import FastMCP, Client

mcp = FastMCP("My MCP Server")
print("=== Server code running")

@mcp.tool()
def greet(name: str) -> str:
    """
    Greet a person by their name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message including the person's name.
    """
    return f"Hello, {name}!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of the two numbers.
    """
    return a * b
    

@mcp.tool()
def get_my_value() -> str:
    """
    Get my value

    Returns:
        str: Value of MY, MY-VALUE.
    """
    return "MY-VALUE"


if __name__ == "__main__":
    mcp.run(transport="stdio")
    # mcp.run(transport="sse")
