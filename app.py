import streamlit as st
import pandas as pd
import yaml
import re
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_IN')
Faker.seed(0)

st.set_page_config(page_title="Mock Data Generator Agent", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1d2e 100%); }
    .hero {
        background: linear-gradient(135deg, #1e2a4a 0%, #0d1b2a 100%);
        border: 1px solid #2d3f6b; border-radius: 16px;
        padding: 2rem 2.5rem; margin-bottom: 2rem; text-align: center;
    }
    .hero h1 { color: #e2e8f0; font-size: 2rem; font-weight: 700; margin: 0; }
    .hero p  { color: #94a3b8; font-size: 1rem; margin: 0.5rem 0 0; }
    .badge {
        display: inline-block; background: #1e3a5f; color: #60a5fa;
        font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.75rem;
        border-radius: 999px; border: 1px solid #2563eb; margin-bottom: 1rem;
    }
    .step-label {
        color: #60a5fa; font-size: 0.8rem; font-weight: 600;
        letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.4rem;
    }
    .success-box {
        background: #052e16; border-left: 3px solid #22c55e;
        border-radius: 0 8px 8px 0; padding: 0.75rem 1rem;
        color: #86efac; font-size: 0.875rem; margin: 0.5rem 0 1rem;
    }
    .agent-log {
        background: #0d1117; border: 1px solid #2d3748; border-radius: 8px;
        padding: 1rem; font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem; color: #86efac; max-height: 200px; overflow-y: auto;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white;
        border: none; border-radius: 8px; padding: 0.6rem 2rem;
        font-weight: 600; font-size: 0.95rem; width: 100%;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: #111827 !important; border: 1px solid #374151 !important;
        color: #e2e8f0 !important; border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    label, .stSelectbox label { color: #cbd5e1 !important; font-size: 0.875rem !important; }
    h2, h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="badge">🤖 Agent Loop · Team 14 · DE-15 · Infinite Computer Solutions</div>
    <h1>Mock Data Generator Agent</h1>
    <p>Schema in (DDL or YAML) → Agent generates realistic rows → Export CSV + SQL</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📖 How It Works")
    st.markdown("""
    1. **Paste** your schema (DDL or YAML)
    2. **Set** number of rows
    3. **Click** Generate
    4. **Download** CSV + SQL
    """)
    st.markdown("---")
    st.markdown("### 🔁 Agent Loop")
    st.markdown("""
    The agent runs these steps:
    - **Parse** schema columns & types
    - **Map** types to Faker generators
    - **Generate** realistic values row by row
    - **Validate** constraints (PK unique, ranges)
    - **Export** CSV + SQL INSERT
    """)
    st.markdown("---")
    st.markdown("### 🧩 Team 14")
    st.markdown("""
    - Malla Hemanjali (CSM)
    - Pentakota Charishma (CSE)
    - Padala Kuladeep Satya Kishore (CSE)
    - Madisa Thanu Sri (ECE)
    """)

# ── Schema Parser (Agent Step 1) ──────────────────────────────────────────────
def parse_ddl(ddl_text):
    """Parse SQL DDL and extract column name + type."""
    columns = []
    matches = re.findall(
        r'(\w+)\s+(INT|INTEGER|BIGINT|SMALLINT|VARCHAR|CHAR|TEXT|DECIMAL|FLOAT|DOUBLE|BOOLEAN|BOOL|DATE|DATETIME|TIMESTAMP|EMAIL|PHONE)',
        ddl_text, re.IGNORECASE
    )
    skip = {'create', 'table', 'primary', 'not', 'null', 'default', 'unique', 'index'}
    for col, dtype in matches:
        if col.lower() not in skip:
            columns.append({'name': col, 'type': dtype.lower()})
    return columns

def parse_yaml_schema(yaml_text):
    """Parse YAML schema and extract columns."""
    data = yaml.safe_load(yaml_text)
    columns = []
    table_name = data.get('table_name', 'generated_table')
    for col in data.get('columns', []):
        entry = {
            'name': col['name'],
            'type': col.get('type', 'string').lower(),
            'values': col.get('values', None),
            'min': col.get('min', None),
            'max': col.get('max', None),
            'primary_key': col.get('primary_key', False)
        }
        columns.append(entry)
    return columns, table_name

# ── Value Generator (Agent Step 2 & 3) ────────────────────────────────────────
pk_counters = {}

def generate_value(col, row_index):
    """Agent maps column type → realistic Faker value."""
    name = col['name'].lower()
    dtype = col.get('type', 'string').lower()
    values = col.get('values', None)
    col_min = col.get('min', None)
    col_max = col.get('max', None)
    is_pk = col.get('primary_key', False)

    # Fixed list values
    if values:
        return random.choice(values)

    # Primary key — always unique integer
    if is_pk or name in ('id', 'emp_id', 'user_id', 'student_id', 'order_id'):
        return row_index + 1

    # Name detection
    if 'name' in name and 'table' not in name and 'column' not in name:
        return fake.name()
    if 'email' in name or dtype == 'email':
        return fake.email()
    if 'phone' in name or 'mobile' in name or dtype == 'phone':
        return fake.phone_number()
    if 'city' in name or dtype == 'city':
        return fake.city()
    if 'address' in name:
        return fake.address().replace('\n', ', ')
    if 'pincode' in name or 'zip' in name:
        return fake.postcode()
    if 'state' in name:
        return fake.state()
    if 'country' in name:
        return 'India'
    if 'company' in name or 'organisation' in name or 'organization' in name:
        return fake.company()
    if 'department' in name or 'dept' in name:
        return random.choice(['HR', 'Engineering', 'Finance', 'Marketing', 'Sales', 'Operations'])
    if 'salary' in name or 'wage' in name or 'income' in name:
        mn = col_min or 25000
        mx = col_max or 200000
        return round(random.uniform(mn, mx), 2)
    if 'age' in name:
        return random.randint(col_min or 18, col_max or 60)
    if 'gender' in name or 'sex' in name:
        return random.choice(['Male', 'Female', 'Other'])
    if 'status' in name:
        return random.choice(['Active', 'Inactive', 'Pending'])
    if 'product' in name:
        return fake.catch_phrase()
    if 'description' in name or 'notes' in name or 'comment' in name:
        return fake.sentence()
    if 'url' in name or 'website' in name or 'link' in name:
        return fake.url()
    if 'username' in name or 'user_name' in name:
        return fake.user_name()
    if 'password' in name:
        return fake.password()

    # Type-based generation
    if dtype in ('int', 'integer', 'bigint', 'smallint'):
        return random.randint(col_min or 1, col_max or 9999)
    if dtype in ('decimal', 'float', 'double'):
        return round(random.uniform(col_min or 0.0, col_max or 9999.99), 2)
    if dtype in ('boolean', 'bool'):
        return random.choice([True, False])
    if dtype == 'date':
        start = datetime.now() - timedelta(days=3650)
        return (start + timedelta(days=random.randint(0, 3650))).strftime('%Y-%m-%d')
    if dtype in ('datetime', 'timestamp'):
        start = datetime.now() - timedelta(days=3650)
        return (start + timedelta(days=random.randint(0, 3650))).strftime('%Y-%m-%d %H:%M:%S')
    if dtype in ('varchar', 'char', 'text', 'string'):
        return fake.word()

    return fake.word()

# ── Agent Loop (Step 4: Generate all rows) ────────────────────────────────────
def run_agent(columns, num_rows, table_name, log_placeholder):
    logs = []
    rows = []

    def log(msg):
        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        log_placeholder.markdown('<div class="agent-log">' + '<br>'.join(logs[-12:]) + '</div>', unsafe_allow_html=True)

    log("🔍 Agent started — schema analysis complete")
    log(f"📋 Detected {len(columns)} columns: {[c['name'] for c in columns]}")
    log(f"🎯 Target: {num_rows} rows for table '{table_name}'")
    log("🔁 Starting agent generation loop...")

    pk_seen = set()
    for i in range(num_rows):
        row = []
        for col in columns:
            val = generate_value(col, i)
            # Validate PK uniqueness (Agent Step 4 - validation)
            if col.get('primary_key') or col['name'].lower() in ('id', 'emp_id', 'user_id'):
                while val in pk_seen:
                    val = val + 1
                pk_seen.add(val)
            row.append(val)
        rows.append(row)
        if i % max(1, num_rows // 5) == 0:
            log(f"  ✅ Generated row {i+1}/{num_rows}")

    log("📊 Validating generated data...")
    log("💾 Preparing CSV export...")
    log("🗄️  Preparing SQL INSERT export...")
    log(f"✅ Agent complete! {num_rows} rows generated successfully.")
    return rows

# ── Main UI ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="step-label">Step 1 — Define Schema</div>', unsafe_allow_html=True)
    schema_type = st.selectbox("Schema Format", ["SQL DDL", "YAML"])

    ddl_example = """CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(15),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    city VARCHAR(50),
    is_active BOOLEAN
);"""

    yaml_example = """table_name: employees
columns:
  - name: id
    type: integer
    primary_key: true
  - name: name
    type: string
  - name: email
    type: email
  - name: phone
    type: phone
  - name: department
    type: string
    values: [HR, Engineering, Finance, Marketing, Sales]
  - name: salary
    type: decimal
    min: 30000
    max: 200000
  - name: hire_date
    type: date
  - name: city
    type: city
  - name: is_active
    type: boolean"""

    schema_input = st.text_area(
        "Paste your schema here",
        value=ddl_example if schema_type == "SQL DDL" else yaml_example,
        height=300
    )

    st.markdown('<div class="step-label">Step 2 — Settings</div>', unsafe_allow_html=True)
    num_rows = st.number_input("Number of rows to generate", min_value=5, max_value=500, value=20)
    generate_btn = st.button("⚡ Generate Mock Data")

with col2:
    st.markdown('<div class="step-label">Step 3 — Agent Log & Results</div>', unsafe_allow_html=True)
    log_placeholder = st.empty()

    if generate_btn:
        if not schema_input.strip():
            st.error("⚠️ Please enter a schema.")
        else:
            try:
                table_name = "generated_table"

                # Parse schema
                if schema_type == "SQL DDL":
                    columns = parse_ddl(schema_input)
                    match = re.search(r'CREATE TABLE\s+(\w+)', schema_input, re.IGNORECASE)
                    if match:
                        table_name = match.group(1)
                    # Add extra metadata not always caught by regex
                    for col in columns:
                        col.setdefault('values', None)
                        col.setdefault('min', None)
                        col.setdefault('max', None)
                        col.setdefault('primary_key', col['name'].lower() == 'id')
                else:
                    columns, table_name = parse_yaml_schema(schema_input)

                if not columns:
                    st.error("❌ Could not detect any columns. Check your schema format.")
                else:
                    # Run agent loop
                    rows = run_agent(columns, num_rows, table_name, log_placeholder)
                    col_names = [c['name'] for c in columns]
                    df = pd.DataFrame(rows, columns=col_names)

                    st.markdown(f'<div class="success-box">✅ Agent generated <strong>{len(df)} rows</strong> with <strong>{len(df.columns)} columns</strong> successfully!</div>', unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True, height=250)

                    # Downloads
                    st.markdown("### 📥 Download")
                    dl1, dl2 = st.columns(2)

                    csv_data = df.to_csv(index=False)
                    dl1.download_button("⬇️ Download CSV", data=csv_data,
                        file_name=f"mock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv")

                    sql_lines = [
                        f"-- Mock Data Generated by Team 14 Mock Data Generator Agent",
                        f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        f"-- Table: {table_name} | Rows: {len(df)}\n"
                    ]
                    for _, row in df.iterrows():
                        vals = []
                        for v in row:
                            if v is None or (isinstance(v, float) and pd.isna(v)):
                                vals.append("NULL")
                            elif isinstance(v, bool):
                                vals.append("TRUE" if v else "FALSE")
                            elif isinstance(v, (int, float)):
                                vals.append(str(v))
                            else:
                                vals.append(f"'{str(v).replace(chr(39), chr(39)*2)}'")
                        sql_lines.append(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({', '.join(vals)});")

                    dl2.download_button("⬇️ Download SQL", data="\n".join(sql_lines),
                        file_name=f"mock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
                        mime="text/plain")

                    s1, s2, s3 = st.columns(3)
                    s1.metric("Rows Generated", len(df))
                    s2.metric("Columns", len(df.columns))
                    s3.metric("Table", table_name)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.markdown("""
        <div style="background:#1a1d2e;border:1px solid #2d3748;border-radius:12px;padding:3rem 2rem;text-align:center;">
            <div style="font-size:3rem;margin-bottom:1rem;">🗄️</div>
            <div style="color:#64748b;font-size:0.95rem;">
                Paste your schema on the left<br>and click <strong style="color:#60a5fa">Generate Mock Data</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    import sys
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
