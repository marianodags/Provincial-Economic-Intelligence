# Provincial Economic Intelligence

A comprehensive analytics, data engineering, and business intelligence project focused on regional and provincial economic data tracking, analysis, and visualization.

## Project Directory Structure

```text
Provincial-Economic-Intelligence/
├── data/
│   ├── raw/         # Immutable, original data files (CSV, API dumps, government stats)
│   ├── processed/   # Cleaned, transformed, and aggregated datasets ready for analysis
│   └── reference/   # Geographic codes, region definitions, and industry taxonomies
├── notebooks/       # Jupyter notebooks for Exploratory Data Analysis (EDA) and prototyping
├── src/             # Modular Python scripts for ETL pipelines and data cleaning
├── sql/             # SQL scripts, queries, and data models (dbt)
├── powerbi/         # Power BI project files (.pbix) and DAX measure libraries
├── reports/         # Generated PDF exports, executive briefs, and analytical summaries
├── docs/            # Data dictionaries, architecture diagrams, and methodologies
└── README.md        # Project overview and instructions
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Provincial-Economic-Intelligence.git
   cd Provincial-Economic-Intelligence
   ```

2. **Set up the Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Data Pipeline & Analysis:**
   - Place raw data sources into `data/raw/`.
   - Run ETL scripts in `src/` to process datasets into `data/processed/`.
   - Explore data using notebooks in `notebooks/`.
   - Open reports in `powerbi/` for interactive dashboarding.
