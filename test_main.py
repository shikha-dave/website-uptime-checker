from types import SimpleNamespace
from requests.exceptions import Timeout, ConnectionError, RequestException as RequestException
import csv
import main

def test_successful_response(monkeypatch):
   monkeypatch.setattr(main.requests, "get", lambda url, headers, timeout: SimpleNamespace(status_code=200))
   result = main.check_website_status("http://example.com")
   assert result["status_code"] == 200
   assert result["error"] is None
   assert result["response_time_ms"] is not None
   assert result["timestamp"] is not None

def test_http_error_response(monkeypatch):
   monkeypatch.setattr(main.requests, "get", lambda url, headers, timeout: SimpleNamespace(status_code=404))
   result = main.check_website_status("http://example.com")
   assert result["status_code"] == 404
   assert result["error"] == "HTTP status code: 404"
   assert result["response_time_ms"] is not None
   assert result["timestamp"] is not None

def raise_timeout(url, headers, timeout):
    raise Timeout("Connection timed out")


def test_timeout_exception(monkeypatch):
    monkeypatch.setattr(main.requests, "get", raise_timeout)
    result = main.check_website_status("http://example.com")
    assert result["status_code"] is None
    assert "Connection timed out" in result["error"]
    assert result["response_time_ms"] is None
    assert result["timestamp"] is not None


def connection_error(url, headers, timeout):
    raise ConnectionError("Connection error")


def test_connection_error_exception(monkeypatch):
    monkeypatch.setattr(main.requests, "get", connection_error)
    result = main.check_website_status("http://example.com")
    assert result["status_code"] is None
    assert "Connection error" in result["error"]
    assert result["response_time_ms"] is None
    assert result["timestamp"] is not None

def raise_request_exception(url, headers, timeout):
    raise RequestException("Request exception")

def test_request_exception(monkeypatch):
    monkeypatch.setattr(main.requests, "get", raise_request_exception)
    result = main.check_website_status("http://example.com")
    assert result["status_code"] is None
    assert "Request exception" in result["error"]
    assert result["response_time_ms"] is None
    assert result["timestamp"] is not None

def test_write_to_csv_creates_file(tmp_path):
    data = {
        "results": [
            {
                "url": "http://example.com",
                "status_code": 200,
                "response_time_ms": 123.45,
                "error": None,
                "timestamp": "2024-06-01 12:00:00"
            }
        ]
    }
    filename = tmp_path / "test_output.csv"
    main.write_to_csv(data, str(filename))
    assert filename.exists()
    with open(filename, mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["url"] == "http://example.com"
        assert rows[0]["status_code"] == "200"
        assert rows[0]["response_time_ms"] == "123.45"
        assert rows[0]["error"] == ""
        assert rows[0]["timestamp"] == "2024-06-01 12:00:00"

def test_read_from_csv(tmp_path):
    filename = tmp_path / "test_input.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["url"])
        writer.writeheader()
        writer.writerow({"url": "http://example.com"})
    
    rows = main.read_from_csv(str(filename))
    assert len(rows) == 1
    assert rows[0]["url"] == "http://example.com"

def test_write_to_csv_appends_results(tmp_path):
    data1 = {
        "results": [
            {
                "url": "http://example1.com",
                "status_code": 200,
                "response_time_ms": 100.0,
                "error": None,
                "timestamp": "2024-06-01 12:00:00"
            }
        ]
    }
    data2 = {
        "results": [
            {
                "url": "http://example2.com",
                "status_code": 404,
                "response_time_ms": 200.0,
                "error": None,
                "timestamp": "2024-06-01 12:01:00"
            }
        ]
    }
    filename = tmp_path / "test_output.csv"
    main.write_to_csv(data1, str(filename))
    main.write_to_csv(data2, str(filename))
    
    with open(filename, mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["url"] == "http://example1.com"
        assert rows[1]["url"] == "http://example2.com"

def test_write_to_csv_empty_results(tmp_path):
    data = {
        "results": []
    }
    filename = tmp_path / "test_output.csv"
    main.write_to_csv(data, str(filename))
    assert not filename.exists()  # File should not be created if results are empty

def test_read_from_csv_file_not_found(tmp_path):
    filename = tmp_path / "non_existent_file.csv"
    try:
        main.read_from_csv(str(filename))
    except FileNotFoundError as e:
        assert str(e) == f"The file {filename} does not exist."
    else:
        assert False, "Expected FileNotFoundError was not raised."

def test_read_from_csv_missing_url_column(tmp_path):
    filename = tmp_path / "test_input.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["not_url"])
        writer.writeheader()
        writer.writerow({"not_url": "http://example.com"})
    
    try:
        main.read_from_csv(str(filename))
    except ValueError as e:
        assert str(e) == f"The file {filename} does not contain a 'url' column."
    else:
        assert False, "Expected ValueError was not raised."
