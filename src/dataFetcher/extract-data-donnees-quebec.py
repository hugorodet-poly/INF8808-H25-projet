import os
from bs4 import BeautifulSoup
import pandas as pd

input_dir = "borough_reports"
output_dir = "immigration_extracted_csvs"
os.makedirs(output_dir, exist_ok=True)

def extract_csv_from_html(file_path, output_dir):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    textareas = soup.find_all('textarea')
    for idx, textarea in enumerate(textareas):
        csv_content = textarea.get_text(strip=True)
        if csv_content:
            from io import StringIO
            df = pd.read_csv(StringIO(csv_content))

            base_name = os.path.basename(file_path).replace('.html', f'_{idx}.csv')
            output_path = os.path.join(output_dir, base_name)

            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"✅ Extracted and saved: {output_path}")

for filename in os.listdir(input_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(input_dir, filename)
        extract_csv_from_html(file_path, output_dir)

print("🎉 All CSVs extracted and saved.")
