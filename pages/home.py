"""
pages/home.py
Overview and About the Project page.
"""
import streamlit as st

st.set_page_config(page_title="Home | Cricbuzz LiveStats", page_icon="🏠", layout="wide")

st.title("🏠 Home")
    if st.button("Initialise database"):
       from utils.db_connection import init_db init_db()
       st.success("Database initialized!") 

st.markdown("""
## About This Project

**Cricbuzz LiveStats** is a comprehensive cricket analytics dashboard that
combines live data from the Cricbuzz API with a SQL database to deliver:

- ⚡ Real-time match updates
- 📊 Detailed player statistics
- 🔍 SQL-driven analytics (25 queries, beginner → advanced)
- 🛠 Full CRUD operations on player & match data

### Tools Used
| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite / MySQL / PostgreSQL |
| Data Source | Cricbuzz Cricket API (REST) |

### Setup Instructions
1. `pip install -r requirements.txt`
2. Set your API credentials as environment variables:
   ```
   export CRICBUZZ_API_KEY="your_rapidapi_key"
   ```
3. Initialize the database:
   ```python
   from utils.db_connection import init_db
   init_db()
   ```
4. Launch the app:
   ```
   streamlit run app.py
   ```

### Folder Structure
```
cricbuzz_livestats/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── pages/
│   ├── home.py
│   ├── live_matches.py
│   ├── top_stats.py
│   ├── sql_queries.py
│   └── crud_operations.py
├── utils/
│   ├── db_connection.py
│   └── api_client.py
├── sql/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── queries.sql
└── notebooks/
    └── data_fetching.ipynb
```
""")
