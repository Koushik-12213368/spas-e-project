## Azure CI/CD Analytics Pipeline

This project showcases a **cloud-based analytics pipeline on Azure** with:
- **Azure SQL Database** for structured data storage
- **GitHub Actions CI/CD** for automated deployment and data refresh
- **Power BI** for interactive dashboards and insights

### High‑level architecture

1. **Source data**: Sample CSV dataset committed to the repo.
2. **ETL script**: A small Python job that:
   - Reads the CSV file
   - Creates a table in Azure SQL (if not present)
   - Loads/refreshes data in the table
3. **Azure SQL Database**: Stores cleaned, queryable data for reporting.
4. **Power BI**: Connects to Azure SQL to build interactive dashboards.
5. **CI/CD (GitHub Actions)**:
   - On push to `main`, runs tests on the ETL script
   - Deploys database schema changes (idempotent SQL) to Azure SQL
   - Optionally runs the ETL job to refresh data

> **Note:** All secrets (like connection strings) are expected to be stored as GitHub Actions secrets and are **not** committed to the repository.

### Repository structure

```text
.
├─ data/
│  └─ sample_sales.csv
├─ infra/
│  └─ schema.sql
├─ src/
│  └─ load_data.py
└─ .github/
   └─ workflows/
      └─ ci-cd.yml
```

### Prerequisites

- Azure subscription with:
  - An **Azure SQL Database** and **SQL Server** provisioned
  - Firewall/network configured to allow Azure services and GitHub runner access
- **GitHub repository** with:
  - `AZURE_SQL_CONNECTION_STRING` secret defined (ADO.NET style or ODBC string)
- **Python 3.10+** (for local runs)

### Local setup

1. **Create a virtual environment (recommended)**:

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Set environment variables (for local development)**:

   ```bash
   $env:AZURE_SQL_CONNECTION_STRING="Server=tcp:<server>.database.windows.net,1433;Database=<db>;User ID=<user>;Password=<password>;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;"
   ```

3. **Apply schema and load data locally**:

   ```bash
   python .\src\load_data.py
   ```

### CI/CD with GitHub Actions

The workflow in `.github/workflows/ci-cd.yml`:

- Installs Python dependencies
- Runs a basic lint/test step
- Applies the database schema using `sqlcmd` (or a Python migration step)
- Runs the ETL script to refresh data

All Azure-specific configuration (server name, database name, credentials) is injected via **GitHub Secrets** to keep the repo clean and secure.

### Power BI dashboards

1. Open Power BI Desktop.
2. Use **Get Data → Azure → Azure SQL Database**.
3. Enter your server and database details.
4. Connect using the same credentials used by the pipeline (or an appropriate reporting user).
5. Build visuals (e.g., sales by date, region, product).
6. Publish the report to Power BI Service and configure scheduled refresh (optional).

This end-to-end setup demonstrates a **scalable, automated analytics pipeline** suitable to reference on a resume or portfolio.

