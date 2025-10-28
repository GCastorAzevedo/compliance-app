import os
from langchain.agents import create_agent
from langchain.tools import tool

import prompts
from corpus import LawCode, get_law_code_raw_content


@tool
def get_law_content(law_code: LawCode) -> str:
    """Return the raw legislative text for a given law code.

    Parameters
    ----------
    law_code : LawCode
        Identifier (typically an enum or value of type LawCode) specifying which body of legislation
        to retrieve.

    Returns
    -------
    str
        Raw concatenated legislation for the specified law code as returned by
        get_law_code_raw_content. The string may include section headings, annotations,
        markup, or jurisdictional metadata and is not modified or parsed by this function.

    Raises
    ------
    TypeError
        If `law_code` is not of the expected LawCode type.
    ValueError
        If `law_code` refers to an unknown or unsupported code.

    Notes
    -----
    This function is a thin wrapper around get_law_code_raw_content and does not perform any
    normalization, caching, or sanitization. Callers should parse or clean the returned text
    as required for downstream processing.

    Examples
    --------
    >> get_law_content(LawCode.CIVIL)
    '...raw legislative text...'
    """
    return get_law_code_raw_content(law_code)


agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[get_law_content],
    system_prompt=prompts.compliance_assistant_system_prompt,
)

if __name__ == "__main__":
    project_description = (
        "The client intends to build a house next to a forest reserve in Teresópolis."
        "The space has 2km^2 and has native trees within."
        "The building is expected to cover 400m2, has a 50m2 swimming pool, a football field, and a garden."
    )
    document = (
        "List the legal obligations and any compliance requirements needed to implement the following project description:\n"
        f"{project_description}"
    )
    agent.invoke({"messages": [{"role": "user", "content": document}]})
