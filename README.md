# 📊 Calculate CPA and Store in SQLite

This project automatically loads data from JSON files, merges it, calculates **CPA (Cost per Action)**, stores the results in a local SQLite database, and supports scheduled runs.

---

## 🚀 Get Started in 3 Minutes

### 🔧 Option 1: Using Docker + Makefile (Recommended)

> Make sure you have `docker` and `make` installed.

1. Clone the repository and enter the project directory:

    ```bash
    git clone https://github.com/yourusername/etl_process.git
    cd etl_process
    git checkout develop
    ```

2. Build the Docker image (Linux):

    ```bash
    make build
    ```

3. Run the ETL manually (Linux):

    ```bash
    make run-main
    ```

    By default, it uses `--start-date=2025-06-04` and `--end-date=2025-06-06`. You can change this in the `Makefile`.

4. Run the scheduler(Linux):

    ```bash
    make run-scheduler
    ```

    The APScheduler job will call `main.py` every day at 15:00 (3 PM)  based on the cron schedule defined in `scheduler.py`.

---

### 💻 Option 2: Run Locally (without Docker)

1. Set up the environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate       # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. Run ETL manually (Windows):

    ```bash
    python main.py --start-date=2025-06-04 --end-date=2025-06-06
    ```

3. Run the scheduler (Windows):

    ```bash
    python scheduler.py
    ```
   Scheduler will run the job every day at 15:00 (3 PM) as defined in scheduler.py

---

## 🧪 Tests & Coverage

1. Install test dependencies:

    ```bash
    pip install pytest pytest-cov
    ```

2. Run tests:

    ```bash
    pytest
    ```

3. Check test coverage:

    ```bash
    pytest --cov=utils --cov-report=term-missing tests/
    ```

---

## 🛠 Makefile Commands

| Command              | Description                                 |
|----------------------|---------------------------------------------|
| `make build`         | Build Docker image                          |
| `make run-main`      | Run the ETL job inside Docker               |
| `make run-scheduler` | Start the scheduled job inside Docker       |

---
Logging is configured to write to `logs/etl.log`. You can change the logging level in `log_config.py`.

---
## Project Structure
   ```
   etL_process/
   ├── data/
   │   ├── daily_stats.db
   │   ├── fb_spend.json
   │   └── network_conv.json
   ├── tests/
   │    └── test_utils.py
   ├── logs/
   │    └── etl.log
   ├── .flake8
   ├── .gitignore
   ├── db.py
   ├── Dockerfile
   ├── log_config.py
   ├── main.py
   ├── Makefile
   ├── pytest.ini
   ├── README.md
   ├── requirements.txt
   ├── scheduler.py
   ├── .pre-commit-config.yaml
   └── utils.py
   ```

## What I would improve:
- Make the scheduler’s cron schedule configurable:
  Instead of hardcoding the cron schedule in `scheduler.py`, use environment variables or a configuration file to allow flexible scheduling without code changes.
- Add end-to-end integration tests:
Implement integration tests that run the entire ETL pipeline inside Docker, verifying the scheduled job execution and data processing flow from start to finish.
- Optimize Docker image:
Reduce image size by multi-stage builds, caching dependencies, and cleaning up intermediate files.
- Add configuration validation:
Validate config inputs early and provide clear error messages for misconfiguration.
- Implement CI/CD pipeline:
Automate tests, linting, builds, and deployment steps using GitHub Actions or similar tools.
