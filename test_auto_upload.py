import requests
import os
BASE_URL = "http://127.0.0.1:8000"

# Enter your JWT access token locally when prompted.
access_token = os.getenv("STUDYMATE_ACCESS_TOKEN")

if not access_token:
    raise ValueError(
        "JWT token not found. Set STUDYMATE_ACCESS_TOKEN in PowerShell."
    )

pdf_path = input("Enter the full path of a PDF: ").strip().strip('"')

headers = {
    "Authorization": f"Bearer {access_token}",
}

try:
    with open(pdf_path, "rb") as pdf_file:
        files = {
            "file": (
                pdf_path.split("\\")[-1],
                pdf_file,
                "application/pdf",
            )
        }

        data = {
            "title": "Automatic Processing Test",
        }

        response = requests.post(
            f"{BASE_URL}/api/documents/upload/",
            headers=headers,
            files=files,
            data=data,
            timeout=300,
        )

    print("\nHTTP Status:", response.status_code)
    print("Response:")

    try:
        result = response.json()
        print(result)

        if response.ok:
            print("\nDocument status:", result.get("status"))
    except ValueError:
        print(response.text)

except requests.RequestException as error:
    print("Request failed:", error)
except OSError as error:
    print("Could not open PDF:", error)