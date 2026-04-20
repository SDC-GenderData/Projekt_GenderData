import pandas as pd
import requests
import os

# fix paths for folders
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(script_path))
output_path = os.path.join(project_root, "data", "raw", "lgbtq_analysis_table.csv")

# wikipedia link
url = "https://en.wikipedia.org/wiki/List_of_dramatic_television_series_with_LGBTQ_characters:_2020s"

def run_download():
    print("loading data from wikipedia...")
    
    try:
        # check if data/raw folder exists
        data_folder = os.path.dirname(output_path)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # simple header to avoid 403 error
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=h)
        
        # get all tables from the page
        tables = pd.read_html(r.text)
        
        # find the actual data tables
        valid_tables = []
        for t in tables:
            if 'Show' in t.columns and 'Character' in t.columns:
                valid_tables.append(t)
        
        if not valid_tables:
            print("no data tables found")
            return

        # merge everything into one df
        df = pd.concat(valid_tables, ignore_index=True)
        
        # rename columns for the analysis
        df = df.rename(columns={
            'Show': 'Series', 
            'Gender / Orientation': 'Identity'
        })
        
        # export to csv
        df.to_csv(output_path, index=False)
        print(f"success. saved {len(df)} rows to: {output_path}")

    except Exception as e:
        print(f"failed: {e}")

if __name__ == "__main__":
    run_download()