import pandas as pd
import requests
import os
import re

# Path configuration: working relative to the script location
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(script_path))

# File paths
raw_csv = os.path.join(project_root, "data", "raw", "lgbtq_series_wiki_table.csv")
output_csv = os.path.join(project_root, "data", "processed", "final_labeled_data.csv")

# Wikidata SPARQL endpoint
WIKIDATA_URL = "https://query.wikidata.org/sparql"

def clean_wiki_text(text):
    """ Removes citations and parentheses for cleaner character name matching """
    if pd.isna(text): return ""
    text = re.sub(r'\[.*?\]', '', str(text))
    text = re.sub(r'\(.*?\)', '', text)
    return text.strip()

def get_label_from_text(text):
    """ Keyword matching for identity labels in descriptions """
    t = str(text).lower()
    keywords = {
        "lesbian": "Lesbian",
        "gay": "Gay",
        "bisexual": "Bisexual",
        " bi ": "Bisexual",
        "transgender": "Transgender",
        "trans woman": "Transgender",
        "trans man": "Transgender",
        "non-binary": "Non-binary",
        "pansexual": "Pansexual",
        "queer": "Queer"
    }
    for key, val in keywords.items():
        if key in t:
            return val
    return None

def fetch_wikidata_labels():
    """ Fetches identity labels from Wikidata via SPARQL """
    query = """
    SELECT ?characterLabel ?identityLabel WHERE {
      ?character wdt:P10348 ?identity.
      FILTER(?identity IN (wd:Q6649, wd:Q10359, wd:Q10398, wd:Q271530, wd:Q189125, wd:Q181315))
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """
    try:
        headers = {"User-Agent": "StudentProject/1.0", "Accept": "application/sparql-results+json"}
        r = requests.get(WIKIDATA_URL, params={'format': 'json', 'query': query}, timeout=15, headers=headers)
        r.raise_for_status()
        data = r.json()
        return {item['characterLabel']['value'].lower().strip(): item['identityLabel']['value'] 
                for item in data['results']['bindings']}
    except:
        return {}

def run_enrichment():
    print("--- Starting data enrichment ---")
    
    if not os.path.exists(raw_csv):
        print(f"Error: Source file missing at {raw_csv}")
        return

    df = pd.read_csv(raw_csv)
    
    # Identify the correct column for identity/notes
    identity_col = None
    for col in ['Identity', 'Gender / Orientation', 'Notes']:
        if col in df.columns:
            identity_col = col
            break
    
    df['Match_Name'] = df['Character'].apply(clean_wiki_text)
    wd_results = fetch_wikidata_labels()

    final_labels = []
    
    print(f"Processing {len(df)} records...")
    for _, row in df.iterrows():
        char_name = row['Match_Name'].lower().strip()
        desc = str(row.get(identity_col, '')) if identity_col else ""
        
        # Priority 1: Exact Wikidata Match
        if char_name in wd_results:
            final_labels.append(wd_results[char_name])
        else:
            # Priority 2: Keyword search in description
            guessed = get_label_from_text(desc)
            if guessed:
                final_labels.append(guessed)
            else:
                # Placeholder for manual entry in CSV
                final_labels.append('[MANUAL_ENTRY_REQUIRED]')

    df['Final_Label'] = final_labels

    # Column Selection: Keeping only necessary columns and removing helper/source columns
    cols_to_keep = ['Character', 'Final_Label', 'Series', 'Year', 'Network']
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    df_final = df[existing_cols]

    # Save to CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_final.to_csv(output_csv, index=False)
    
    # Summary of processed data
    total = len(df_final)
    auto_count = len(df_final[df_final['Final_Label'] != '[MANUAL_ENTRY_REQUIRED]'])
    manual_count = total - auto_count
    
    print("\n--- Summary ---")
    print(f"Total characters: {total}")
    print(f"Automatically labeled: {auto_count}")
    print(f"Pending manual entry: {manual_count}")
    print(f"\nSuccess! Final clean data saved to: {output_csv}")

if __name__ == "__main__":
    run_enrichment()