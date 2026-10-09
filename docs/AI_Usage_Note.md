# AI Usage Note – Team 14
## Mock Data Generator Agent | UC ID: DE-15
### Infinite Computer Solutions Placement Drive | June 2026

---

## What AI Helped With

- **Architecture Design** – Claude AI suggested the agent loop structure: Parse → Map → Generate → Validate → Export
- **Schema Parser** – AI helped write regex patterns to extract column names and types from SQL DDL
- **Type Mapping Logic** – AI recommended mapping strategy: column name hints + data type → Faker generator
- **Streamlit UI** – AI generated the dark-themed UI layout with sidebar, columns, and live agent log
- **Test Cases** – AI wrote comprehensive pytest test cases covering unit, integration, and happy path scenarios
- **README** – AI helped structure the README with setup instructions, architecture overview, and assumptions
- **SQL INSERT Generator** – AI helped handle edge cases: booleans, NULLs, quotes in string values

---

## What AI Got Wrong

- **Model name** – Initially suggested `gemini-1.5-flash` which was not available; had to switch models
- **API quota** – Recommended Gemini API which had free tier limits; pivoted to fully local Faker-based generation
- **DDL Regex** – First regex missed columns with constraints like `NOT NULL` and `DEFAULT`; required refinement
- **YAML parsing** – Initially did not handle nested constraints (min/max) for numeric columns correctly

---

## Best Prompts Used

**Prompt 1 – Agent Loop Design:**
> "Design a Python agent loop for a mock data generator. It should: (1) parse SQL DDL or YAML schema, (2) map column types to Faker generators, (3) generate N rows respecting constraints, (4) validate primary key uniqueness, (5) export CSV and SQL INSERT. Show the architecture."

**Prompt 2 – Schema Parser:**
> "Write a Python regex function to parse a SQL CREATE TABLE statement and extract column names and data types. Handle INT, VARCHAR, DECIMAL, BOOLEAN, DATE, DATETIME types. Return a list of dicts with 'name' and 'type'."

**Prompt 3 – Faker Type Mapping:**
> "Write a Python function that takes a column dict with 'name' and 'type' fields and returns a realistic fake value using the Faker library. Use column name hints (e.g. if 'email' in name, return fake.email()). Handle Indian locale."

**Prompt 4 – Streamlit UI:**
> "Build a Streamlit app with dark theme for a mock data generator. Show a live agent log using st.empty() that updates as rows are generated. Include download buttons for CSV and SQL."

**Prompt 5 – Test Cases:**
> "Write pytest test cases for a mock data generator agent. Cover: DDL parsing, YAML parsing, value generation for all types, agent loop row count, primary key uniqueness, and full end-to-end pipeline tests."

---

## Tools Used
| Tool | Purpose |
|---|---|
| Claude AI (claude.ai) | Architecture, code generation, debugging |
| Python Faker library | Realistic data generation |
| Streamlit | Web UI |
| GitHub | Version control & submission |
| pytest | Test cases |

---

*Document prepared by Team 14 – Malla Hemanjali, Pentakota Charishma, Padala Kuladeep Satya Kishore, Madisa Thanu Sri*
