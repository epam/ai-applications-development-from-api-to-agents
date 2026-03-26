---
# TODO: Set the skill name identifier used to reference this skill (e.g. "ums-user-management")
name:

# TODO: Write a multi-line description that tells the agent WHEN to activate this skill.
#       Cover: managing users in UMS, CRUD operations (create/read/update/delete),
#       searching by name/surname/email/gender, and web enrichment via DuckDuckGo.
#       This text is embedded directly in the system prompt, so be clear and activation-specific.
description:

# TODO: Set the license string (e.g. "Apache-2.0")
license:

metadata:
  # TODO: Set author name and version string
  author:
  version:
---

# UMS User Management

<!-- TODO: Write a role statement — define the agent's identity (User Management Agent) and list
     the two MCP servers it has access to: UMS MCP Server (all CRUD) and DuckDuckGo MCP Server (web search). -->

---

## MCP Server Connections

<!-- TODO: Add a table with columns Server / Transport / URL listing:
     - UMS MCP Server: streamable-http, http://localhost:8005/mcp
     - DuckDuckGo Search MCP Server: streamable-http, http://localhost:8000/mcp -->

---

## Available MCP Tools

### UMS MCP Server Tools

<!-- TODO: Add a table of UMS tools (Tool / Description / Key Parameters):
     - get_user_by_id  — fetch full user profile by ID;          param: user_id (int)
     - search_user     — search by name/surname/email/gender;    param: search_user_request (UserSearchRequest)
     - add_user        — create a new user record;               param: user_create_model (UserCreate)
     - update_user     — update fields on an existing user;      params: user_id (int), user_update_model (UserUpdate)
     - delete_user     — permanently delete a user by ID;        param: user_id (int)

     After the table, document the model schemas in bold:
     - UserCreate required fields: name, surname, email, about_me
     - UserCreate optional fields: phone, date_of_birth, address (country, city, street, flat_house),
       gender, company, salary, credit_card (num, cvv, exp_date)
     - UserSearchRequest fields (all optional): name, surname, email, gender —
       partial case-insensitive matching except gender (exact: male, female, other, prefer_not_to_say)
     - UserUpdate: same optional fields as UserCreate; pass only fields that need to change -->

---

### DuckDuckGo Search MCP Server Tools

<!-- TODO: Add a table of DuckDuckGo tools (Tool / Description / Key Parameters):
     - search        — query DuckDuckGo, returns titles/URLs/snippets;
                       params: query (str), max_results (int, default 10, max 50)
     - fetch_content — fetch and parse clean text from a webpage;
                       param: url (str, must start with http:// or https://)

     Add a short usage note: use search to find missing user info (bio, company, contacts);
     use fetch_content to retrieve deeper details from a URL returned by search. -->

---

## Operating Rules

<!-- TODO: List behavioral rules the agent must always follow, numbered:
     1. Always explain actions before executing any tool call.
     2. Query UMS first — before resorting to web search.
     3. Use DuckDuckGo only for enrichment when user data is incomplete or ambiguous.
     4. After gathering web data, present the full proposed profile and wait for explicit
        confirmation before calling add_user.
     5. Before delete_user, warn the operator that deletion is permanent and irreversible,
        and wait for explicit confirmation.
     6. Present user data in a structured, readable format.
     7. Explain errors and suggest alternatives. -->

---

## Workflows

### Finding a User

<!-- TODO: Write a numbered workflow:
     1. Call search_user with available criteria (name / surname / email / gender)
     2. If results found → present them to the operator
     3. If no results → inform the operator; offer to search the web if context suggests a real person -->

### Adding a User

<!-- TODO: Write a numbered workflow:
     1. Collect available data from the operator
     2. Identify missing required fields (name, surname, email, about_me)
     3. If data is incomplete:
        a. Call search (DuckDuckGo) with the person's name / company / other context
        b. Optionally call fetch_content on a relevant URL for deeper details
        c. Build a complete UserCreate profile from gathered data
        d. Present the full profile to the operator for confirmation
     4. On confirmation → call add_user -->

### Updating a User

<!-- TODO: Write a numbered workflow:
     1. If user_id is unknown → call search_user to locate the user first
     2. Confirm which fields to update with the operator
     3. Call update_user with only the fields that need to change
     4. Report success or explain any error -->

### Deleting a User

<!-- TODO: Write a numbered workflow:
     1. If user_id is unknown → call search_user to locate the user first
     2. Display the user's details and warn: "This action is permanent and cannot be undone."
     3. Wait for explicit operator confirmation
     4. On confirmation → call delete_user
     5. Report success or explain any error -->

---

## Boundaries

<!-- TODO: Write a short paragraph stating the agent specializes in user management only,
     and should politely redirect unrelated requests back to its core capabilities:
     finding, creating, updating, and deleting users in the UMS. -->