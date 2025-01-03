import requests
import json

def fetch_headers(url):
    try:
        print(f"\nFetching headers for: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response, response.headers
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers: {e}")
        return None, {"Error": str(e)}

def save_headers_to_file(headers, filename="headers.json"):
    try:
        headers_dict = dict(headers)
        with open(filename, "w") as file:
            json.dump(headers_dict, file, indent=4)
        print(f"Headers saved to {filename}")
    except Exception as e:
        print(f"Error saving headers: {e}")

def extract_set_cookie_header(headers):
    set_cookie = headers.get("Set-Cookie", None)
    if set_cookie:
        print(f"\nSet-Cookie Header: {set_cookie}")
        cookies = set_cookie.split(";")[0]
        return cookies
    print("No Set-Cookie header found.")
    return None

def send_request_with_cookie(url, cookie):
    try:
        headers = {"Cookie": cookie}
        print(f"\nSending request to {url} with cookie: {cookie}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error sending request with cookie: {e}"

def print_headers(headers):
    print("\nHTTP Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

def handle_cookie_flow_with_modification(url):
    response, headers = fetch_headers(url)
    print_headers(headers)
    cookie = extract_set_cookie_header(headers)
    if cookie:
        print(f"\nCurrent cookie: {cookie}")
        key, value = cookie.split("=", 1)
        print(f"Current key: {key}, Current value: {value}")
        new_key = input(f"Enter a new key (press Enter to keep '{key}'): ").strip() or key
        new_value = input(f"Enter a new value (press Enter to keep '{value}'): ").strip() or value
        modified_cookie = f"{new_key}={new_value}"
        print(f"\nModified cookie: {modified_cookie}")
        response_text = send_request_with_cookie(url, modified_cookie)
        print("\nResponse using modified cookie:")
        print(response_text)
    else:
        print("No valid cookie found. Cannot proceed with cookie-based request.")

def main():
    print("Welcome to the HTTP Header Identifier Tool!")
    while True:
        print("\nMenu:")
        print("1. Fetch headers for a single URL")
        print("2. Fetch headers for a sample URL")
        print("3. Fetch headers for multiple URLs from a file")
        print("4. Extract and automatically reuse cookies")
        print("5. Modify a cookie and reuse it")
        print("6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ").strip()

        if choice == "1":
            url = input("Enter the URL: ").strip()
            _, headers = fetch_headers(url)
            print_headers(headers)
            save_choice = input("Do you want to save the headers to a file? (yes/no): ").strip().lower()
            if save_choice == "yes":
                filename = input("Enter the filename (default: headers.json): ").strip()
                save_headers_to_file(headers, filename if filename else "headers.json")

        elif choice == "2":
            sample_url = "https://jsonplaceholder.typicode.com/posts/1"
            print(f"\nUsing sample URL: {sample_url}")
            _, headers = fetch_headers(sample_url)
            print_headers(headers)
            save_choice = input("Do you want to save the headers to a file? (yes/no): ").strip().lower()
            if save_choice == "yes":
                filename = input("Enter the filename (default: sample_headers.json): ").strip()
                save_headers_to_file(headers, filename if filename else "sample_headers.json")

        elif choice == "3":
            file_path = input("Enter the file path containing URLs: ").strip()
            try:
                with open(file_path, "r") as file:
                    urls = file.readlines()
                for url in urls:
                    url = url.strip()
                    if url:
                        _, headers = fetch_headers(url)
                        print_headers(headers)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing file: {e}")

        elif choice == "4":
            url = input("Enter the URL to fetch headers and reuse cookies: ").strip()
            response, headers = fetch_headers(url)
            print_headers(headers)
            cookie = extract_set_cookie_header(headers)
            if cookie:
                print("\nAutomatically reusing the extracted cookie...")
                response_text = send_request_with_cookie(url, cookie)
                print("\nResponse using cookie:")
                print(response_text)
            else:
                print("No valid cookie found. Cannot proceed with cookie-based request.")

        elif choice == "5":
            url = input("Enter the URL to fetch headers and modify cookies: ").strip()
            handle_cookie_flow_with_modification(url)

        elif choice == "6":
            print("Exiting the tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
