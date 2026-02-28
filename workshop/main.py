import requests
import pandas as pd

def fetch_nyc_taxi_data(base_url):
    all_data = []
    page = 1  # Starting page
    
    print("Starting data extraction...")
    
    while True:
        # Construct the URL with the page parameter
        url = f"{base_url}?page={page}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            
            # Check if the page is empty (Pagination stop condition)
            if not data:
                print(f"\nReached end of data at page {page-1}.")
                break
            
            all_data.extend(data)
            
            if page % 5 == 0:
                print(f"Fetched {page} pages ({len(all_data)} records so far)...")
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    # Convert to Pandas DataFrame
    df = pd.DataFrame(all_data)
    return df

# Configuration
API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

# Execute
df_taxi = fetch_nyc_taxi_data(API_URL)

# Preview and Save
if not df_taxi.empty:
    print("\nData Preview:")
    print(df_taxi.head())
    
    # Save to CSV
    df_taxi.to_csv("nyc_taxi_data.csv", index=False)
    print("\nSuccess! Data saved to 'nyc_taxi_data.csv'.")
else:
    print("No data was retrieved.")