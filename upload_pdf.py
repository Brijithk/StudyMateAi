import requests
import getpass

base_url = "http://127.0.0.1:8000"

username = input("Enter your Django username: ")
password = getpass.getpass("Enter your Django password: ")

try:
    token_response = requests.post(
        f"{base_url}/api/auth/token/",
        json={
            "username": username,
            "password": password
        },
        timeout=30
    )

    if token_response.status_code != 200:
        print("Login failed:", token_response.status_code)
        print(token_response.text)
        raise SystemExit

    access_token = token_response.json()["access"]

    file_path = r"C:\Users\RC\Downloads\pythonNotes.pdf"

    with open(file_path, "rb") as pdf_file:
        upload_response = requests.post(
            f"{base_url}/api/documents/upload/",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data={
                "title": "Python Notes"
            },
            files={
                "file": ("pythonNotes.pdf", pdf_file, "application/pdf")
            },
            timeout=60
        )

    print("\nUpload status:", upload_response.status_code)
    print("Response:", upload_response.text)

except requests.RequestException as error:
    print("Request failed:", error)
except FileNotFoundError:
    print("PDF file not found. Check the file path.")
