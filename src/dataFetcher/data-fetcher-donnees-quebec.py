import requests
import os

# CKAN API URL
API_URL = "https://www.donneesquebec.ca/recherche/api/3/action/package_show"
DATASET_ID = "vmtl-portrait-thematique-sur-l-immigration"

output_dir = "borough_reports"
os.makedirs(output_dir, exist_ok=True)

response = requests.get(f"{API_URL}?id={DATASET_ID}")
response.encoding = 'utf-8'
data = response.json()

resources = data["result"]["resources"]

for resource in resources:
    borough_name = resource["name"]
    download_url = resource["url"]

    print(f"{borough_name}: {download_url}")

    safe_borough_name = borough_name.encode('ascii', 'ignore').decode('ascii').replace(" ", "_")
    filename = os.path.join(output_dir, f"{safe_borough_name}.html")

    file_response = requests.get(download_url)
    if file_response.status_code == 200:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(file_response.text)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download {borough_name}. Status code: {file_response.status_code}")

print("🎉 All files processed.")
