# Website Uptime Checker

A Python project that checks website availability, captures HTTP status codes, measures response times, and handles request errors. The project also includes automated tests using `pytest` and `monkeypatch`.

## Features

- Check website availability using HTTP requests.
- Capture HTTP status codes.
- Measure request response time.
- Handle request exceptions and timeouts.
- Store results in a CSV file.
- Run automated tests using `pytest`.
- Mock HTTP requests in tests to avoid depending on live websites.

## Technologies Used

- Python
- Requests
- CSV
- Pytest

## Project Structure

```text
website_uptime_checker/
├── data/
│   ├── url_list.csv
│   └── website_status.csv
├── main.py
├── test_main.py
├── requirements.txt
└── README.md
```

*Adjust the file names and structure to match your actual repository.*

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shikha-dave/website-uptime-checker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd website-uptime-checker
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the uptime checker:

```bash
python main.py
```

The script checks the configured websites and records the results, including their HTTP status codes, response times, and any errors encountered.

## Running Tests

Run the automated test suite with:

```bash
pytest -v
```

The tests use mocking to simulate HTTP responses and test different scenarios without relying on actual network requests.

## What I Learned

- Making HTTP requests with Python's `requests` library.
- Measuring execution time using `time.perf_counter()`.
- Handling request exceptions and timeouts.
- Working with CSV files.
- Writing automated tests using `pytest`.
- Using `monkeypatch` to replace dependencies during testing.
- Organizing Python code and using a virtual environment.

## Future Improvements

- Add website URLs through command-line arguments.
- Schedule periodic uptime checks.
- Add structured logging.
- Deploy the checker to AWS and store results in cloud storage.

## Author

Shikha Thakur

[GitHub Profile](https://github.com/shikha-dave)