#!/usr/bin/env python3
"""
Example usage of the Wells API Client
Demonstrates various ways to interact with the Status of Wells API
"""

from wells_api_client import WellsAPIClient
import json


def main():
    """Demonstrate various API usage patterns"""
    
    # Initialize the client with the sample API key
    client = WellsAPIClient()
    
    print("=== Status of Wells API Client Examples ===\n")
    
    # Example 1: Get basic data (first 10 records)
    print("1. Getting first 5 records:")
    data = client.get_wells_data(limit=5)
    if "error" not in data:
        records = data.get("records", [])
        print(f"   Found {len(records)} records")
        if records:
            print(f"   Sample record: {json.dumps(records[0], indent=2)}")
    else:
        print(f"   Error: {data['error']}")
    print()
    
    # Example 2: Filter by state (Gujarat)
    print("2. Filtering by Gujarat state:")
    gujarat_data = client.filter_by_state("gujarat")
    if "error" not in gujarat_data:
        records = gujarat_data.get("records", [])
        print(f"   Found {len(records)} records for Gujarat")
        if records:
            print(f"   Gujarat wells in first record: {records[0].get('gujarat', 0)}")
    else:
        print(f"   Error: {gujarat_data['error']}")
    print()
    
    # Example 3: Filter by offshore wells
    print("3. Filtering offshore wells:")
    offshore_data = client.filter_by_offshore(True)
    if "error" not in offshore_data:
        records = offshore_data.get("records", [])
        print(f"   Found {len(records)} offshore wells")
        if records:
            print(f"   Offshore wells in first record: {records[0].get('offshore', 0)}")
    else:
        print(f"   Error: {offshore_data['error']}")
    print()
    
    # Example 4: Get data in different formats
    print("4. Getting data in CSV format:")
    csv_data = client.get_wells_data(format_type="csv", limit=3)
    if isinstance(csv_data, str) and "error" not in csv_data:
        print("   CSV data preview:")
        print(csv_data[:200] + "..." if len(csv_data) > 200 else csv_data)
    elif isinstance(csv_data, dict) and "error" in csv_data:
        print(f"   Error: {csv_data['error']}")
    else:
        print("   Unexpected response format")
    print()
    
    # Example 5: Save data to file
    print("5. Saving sample data to file:")
    sample_data = client.get_wells_data(limit=5)
    if "error" not in sample_data:
        client.save_to_file(sample_data, "sample_wells_data.json", "json")
        print("   Data saved to sample_wells_data.json")
    else:
        print(f"   Error: {sample_data['error']}")
    print()
    
    # Example 6: Get data with custom filters
    print("6. Using custom filters:")
    custom_filters = {
        "gujarat": 1,
        "offshore": 1
    }
    filtered_data = client.get_wells_data(filters=custom_filters, limit=3)
    if "error" not in filtered_data:
        records = filtered_data.get("records", [])
        print(f"   Found {len(records)} records matching Gujarat + Offshore filter")
        if records:
            print(f"   Sample record status: {records[0].get('status', 'N/A')}")
    else:
        print(f"   Error: {filtered_data['error']}")
    print()
    
    # Example 7: Show available states
    print("7. Available states for filtering:")
    states = [
        "gujarat", "rajasthan", "assam", "tripura", "andhra_pradesh",
        "tamilnadu", "west_bengal", "jharkhand", "madhya_pradesh", "other_states"
    ]
    for state in states:
        print(f"   - {state}")
    print()
    
    print("=== Examples completed ===")
    print("\nTo run the client from command line, use:")
    print("python wells_api_client.py --help")
    print("\nExample commands:")
    print("python wells_api_client.py --state gujarat --limit 5")
    print("python wells_api_client.py --offshore --format csv --save offshore_wells.csv")
    print("python wells_api_client.py --all --save all_wells_data.json")


if __name__ == "__main__":
    main()
