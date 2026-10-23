import time, requests, csv, os
from requests.exceptions import RequestException

headers = {
    "User-Agent": "ShikhaPythonLearning/1.0 (stshikhathakur@gmail.com)"
}


def check_website_status(url):
    start_time = time.perf_counter()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        end_time = time.perf_counter()
        # Calculate the elapsed time in milliseconds and round it to 2 decimal places
        elapsed_time = round((end_time - start_time) * 1000, 2)

        error = None
        if response.status_code >= 400:
            error =  f"HTTP status code: {response.status_code}"
        return {
                    "url": url,
                    "status_code": response.status_code,
                    "response_time_ms": elapsed_time,
                    "error": error,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
        
            
    except RequestException as e:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "error": str(e), 
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }


def write_to_csv(data, filename):
    filename = os.fspath(filename)
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    results = data["results"]
    if not results:
        return

    fieldnames = [
        "url", "status_code", "response_time_ms", "error", "timestamp"
    ]

    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    with open(filename, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerows(results)
        
def read_from_csv(filename):
    filename = os.fspath(filename)
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")
    
    with open(filename, mode="r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames or 'url' not in reader.fieldnames:
            raise ValueError(f"The file {filename} does not contain a 'url' column.")
        return list(reader)

def main():
    rows = read_from_csv("data/url_list.csv")
    url_list = [row['url'] for row in rows]
    response_data = {"results": [check_website_status(url) for url in url_list]}    
    write_to_csv(response_data, "data/website_status.csv")
    print("Website status check completed. Results written to website_status.csv.")

if __name__ == "__main__":
    main()