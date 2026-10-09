"""
Test Cases for Mock Data Generator Agent - Team 14
UC ID: DE-15 | Infinite Computer Solutions Placement Drive
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import parse_ddl, parse_yaml_schema, generate_value, run_agent
import pandas as pd
import streamlit as st

# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_DDL = """
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(15),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    city VARCHAR(50),
    is_active BOOLEAN
);
"""

SAMPLE_YAML = """
table_name: students
columns:
  - name: id
    type: integer
    primary_key: true
  - name: name
    type: string
  - name: email
    type: email
  - name: grade
    type: string
    values: [A, B, C, D]
  - name: score
    type: decimal
    min: 0
    max: 100
"""

# ── DDL Parser Tests ──────────────────────────────────────────────────────────

def test_ddl_parse_returns_columns():
    """Agent Step 1: DDL parser should return a list of columns."""
    columns = parse_ddl(SAMPLE_DDL)
    assert isinstance(columns, list)
    assert len(columns) > 0

def test_ddl_parse_detects_correct_count():
    """DDL parser should detect all 9 columns."""
    columns = parse_ddl(SAMPLE_DDL)
    assert len(columns) == 9

def test_ddl_parse_column_names():
    """DDL parser should correctly extract column names."""
    columns = parse_ddl(SAMPLE_DDL)
    names = [c['name'].lower() for c in columns]
    assert 'id' in names
    assert 'name' in names
    assert 'email' in names
    assert 'salary' in names

def test_ddl_parse_column_types():
    """DDL parser should correctly extract column types."""
    columns = parse_ddl(SAMPLE_DDL)
    type_map = {c['name'].lower(): c['type'].lower() for c in columns}
    assert type_map['id'] in ('int', 'integer')
    assert type_map['is_active'] in ('boolean', 'bool')
    assert type_map['salary'] in ('decimal', 'float')

# ── YAML Parser Tests ─────────────────────────────────────────────────────────

def test_yaml_parse_returns_columns():
    """Agent Step 1: YAML parser should return columns and table name."""
    columns, table_name = parse_yaml_schema(SAMPLE_YAML)
    assert isinstance(columns, list)
    assert len(columns) > 0
    assert table_name == 'students'

def test_yaml_parse_column_count():
    """YAML parser should detect all 5 columns."""
    columns, _ = parse_yaml_schema(SAMPLE_YAML)
    assert len(columns) == 5

def test_yaml_parse_values_list():
    """YAML parser should preserve enum values list."""
    columns, _ = parse_yaml_schema(SAMPLE_YAML)
    grade_col = next(c for c in columns if c['name'] == 'grade')
    assert grade_col['values'] == ['A', 'B', 'C', 'D']

def test_yaml_parse_min_max():
    """YAML parser should preserve min/max constraints."""
    columns, _ = parse_yaml_schema(SAMPLE_YAML)
    score_col = next(c for c in columns if c['name'] == 'score')
    assert score_col['min'] == 0
    assert score_col['max'] == 100

# ── Value Generator Tests ─────────────────────────────────────────────────────

def test_generate_email():
    """Agent Step 2: Email type should generate valid email."""
    col = {'name': 'email', 'type': 'email', 'values': None, 'min': None, 'max': None, 'primary_key': False}
    val = generate_value(col, 0)
    assert '@' in str(val)

def test_generate_boolean():
    """Boolean type should return True or False."""
    col = {'name': 'is_active', 'type': 'boolean', 'values': None, 'min': None, 'max': None, 'primary_key': False}
    val = generate_value(col, 0)
    assert val in (True, False)

def test_generate_integer():
    """Integer type should return an int."""
    col = {'name': 'age', 'type': 'integer', 'values': None, 'min': 18, 'max': 60, 'primary_key': False}
    val = generate_value(col, 0)
    assert isinstance(val, int)

def test_generate_decimal():
    """Decimal type should return a float."""
    col = {'name': 'salary', 'type': 'decimal', 'values': None, 'min': 30000, 'max': 200000, 'primary_key': False}
    val = generate_value(col, 0)
    assert isinstance(val, float)
    assert 30000 <= val <= 200000

def test_generate_date():
    """Date type should return a valid date string."""
    col = {'name': 'hire_date', 'type': 'date', 'values': None, 'min': None, 'max': None, 'primary_key': False}
    val = generate_value(col, 0)
    assert len(str(val)) == 10  # YYYY-MM-DD

def test_generate_enum_values():
    """Column with fixed values should only return from that list."""
    col = {'name': 'department', 'type': 'string', 'values': ['HR', 'Finance', 'Engineering'], 'min': None, 'max': None, 'primary_key': False}
    for i in range(20):
        val = generate_value(col, i)
        assert val in ['HR', 'Finance', 'Engineering']

def test_generate_primary_key_unique():
    """Primary key should be unique across rows."""
    col = {'name': 'id', 'type': 'integer', 'values': None, 'min': None, 'max': None, 'primary_key': True}
    vals = [generate_value(col, i) for i in range(50)]
    assert len(vals) == len(set(vals))  # All unique

# ── Agent Loop Tests ──────────────────────────────────────────────────────────

class MockPlaceholder:
    """Mock Streamlit placeholder for testing."""
    def markdown(self, *args, **kwargs): pass

def test_agent_returns_correct_row_count():
    """Agent loop should generate exactly the requested number of rows."""
    columns = parse_ddl(SAMPLE_DDL)
    for col in columns:
        col.setdefault('values', None)
        col.setdefault('min', None)
        col.setdefault('max', None)
        col.setdefault('primary_key', col['name'].lower() == 'id')
    rows = run_agent(columns, 10, 'employees', MockPlaceholder())
    assert len(rows) == 10

def test_agent_returns_correct_column_count():
    """Each row should have the same number of values as columns."""
    columns = parse_ddl(SAMPLE_DDL)
    for col in columns:
        col.setdefault('values', None)
        col.setdefault('min', None)
        col.setdefault('max', None)
        col.setdefault('primary_key', col['name'].lower() == 'id')
    rows = run_agent(columns, 5, 'employees', MockPlaceholder())
    for row in rows:
        assert len(row) == len(columns)

def test_agent_no_null_rows():
    """Agent should not generate completely empty rows."""
    columns = parse_ddl(SAMPLE_DDL)
    for col in columns:
        col.setdefault('values', None)
        col.setdefault('min', None)
        col.setdefault('max', None)
        col.setdefault('primary_key', col['name'].lower() == 'id')
    rows = run_agent(columns, 10, 'employees', MockPlaceholder())
    for row in rows:
        assert any(v is not None for v in row)

def test_agent_yaml_schema():
    """Agent should work correctly with YAML schema too."""
    columns, table_name = parse_yaml_schema(SAMPLE_YAML)
    rows = run_agent(columns, 15, table_name, MockPlaceholder())
    assert len(rows) == 15
    assert table_name == 'students'

# ── Integration Test ──────────────────────────────────────────────────────────

def test_full_pipeline_ddl():
    """Full pipeline: DDL → parse → generate → DataFrame."""
    columns = parse_ddl(SAMPLE_DDL)
    for col in columns:
        col.setdefault('values', None)
        col.setdefault('min', None)
        col.setdefault('max', None)
        col.setdefault('primary_key', col['name'].lower() == 'id')
    rows = run_agent(columns, 20, 'employees', MockPlaceholder())
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    assert len(df) == 20
    assert 'email' in df.columns
    assert df['email'].str.contains('@').all()

def test_full_pipeline_yaml():
    """Full pipeline: YAML → parse → generate → DataFrame."""
    columns, table_name = parse_yaml_schema(SAMPLE_YAML)
    rows = run_agent(columns, 10, table_name, MockPlaceholder())
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    assert len(df) == 10
    assert 'grade' in df.columns
    assert df['grade'].isin(['A', 'B', 'C', 'D']).all()
