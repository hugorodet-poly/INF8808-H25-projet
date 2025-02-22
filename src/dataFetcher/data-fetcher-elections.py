import requests

url = "https://donnees.electionsquebec.qc.ca/autres/donnees-circ/data_donneesSocio2021.csv"

output_file = "donneesSocio2021.csv"

response = requests.get(url)

if response.status_code == 200:
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f"Data successfully downloaded and saved to {output_file}")
else:
    print(f"Failed to download data. Status code: {response.status_code}")
