#!/usr/bin/env python3
"""
Status of Wells API Client
Connects to the Indian Government's oil wells data API
API Documentation: https://data.gov.in/resource/status-wells-01042021
"""

import requests
import json
import csv
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Union
import argparse
import sys
from datetime import datetime


class WellsAPIClient:
    """Client for interacting with the Status of Wells API"""
    
    def __init__(self, api_key: str = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"):
        """
        Initialize the API client
        
        Args:
            api_key: API key for authentication (default is sample key)
        """
        self.api_key = api_key
        self.base_url = "https://api.data.gov.in/resource/0b344af7-b389-4e37-bf49-b4f1e59bbc49"
        
    def get_wells_data(self, 
                       format_type: str = "json",
                       offset: int = 0,
                       limit: int = 10,
                       filters: Optional[Dict[str, Union[str, int]]] = None) -> Dict:
        """
        Get wells data from the API
        
        Args:
            format_type: Output format (json, xml, csv)
            offset: Number of records to skip for pagination
            limit: Maximum number of records to return
            filters: Dictionary of filters to apply
            
        Returns:
            Dictionary containing API response
        """
        params = {
            "api-key": self.api_key,
            "format": format_type,
            "offset": offset,
            "limit": limit
        }
        
        # Add filters if provided
        if filters:
            for key, value in filters.items():
                params[f"filters[{key}]"] = value
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            if format_type == "json":
                try:
                    return response.json()
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Response text: {response.text[:200]}...")
                    return {"error": f"JSON decode error: {e}"}
            elif format_type == "xml":
                return ET.fromstring(response.text)
            elif format_type == "csv":
                return response.text
            else:
                return response.text
                
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return {"error": str(e)}
    
    def get_all_wells_data(self, 
                          format_type: str = "json",
                          batch_size: int = 100) -> List[Dict]:
        """
        Get all wells data by making multiple API calls
        
        Args:
            format_type: Output format (json, xml, csv)
            batch_size: Number of records per API call
            
        Returns:
            List of all records
        """
        all_records = []
        offset = 0
        
        while True:
            response = self.get_wells_data(
                format_type=format_type,
                offset=offset,
                limit=batch_size
            )
            
            if "error" in response:
                print(f"Error at offset {offset}: {response['error']}")
                break
                
            if format_type == "json":
                records = response.get("result", {}).get("records", [])
                if not records:
                    break
                all_records.extend(records)
            else:
                # For XML/CSV, we'll return the raw response
                all_records.append(response)
                break
            
            offset += batch_size
            
            # Safety check to prevent infinite loops
            if len(records) < batch_size:
                break
        
        return all_records
    
    def filter_by_state(self, state_name: str, format_type: str = "json") -> Dict:
        """
        Filter wells data by state (returns records where state has wells > 0)
        
        Args:
            state_name: Name of the state to filter by
            format_type: Output format
            
        Returns:
            Filtered data
        """
        state_filters = {
            "gujarat": "gujarat",
            "rajasthan": "rajasthan", 
            "assam": "assam___arunachal_pradesh",
            "tripura": "tripura",
            "andhra_pradesh": "andhra_pradesh",
            "tamilnadu": "tamilnadu",
            "west_bengal": "west_bangal__cbm_",
            "jharkhand": "jharkhand__cbm_",
            "madhya_pradesh": "madhya_pradesh__cbm_",
            "other_states": "other_state__up_hp_mp_bihar__punjab_jk_wb_"
        }
        
        if state_name.lower() not in state_filters:
            return {"error": f"Invalid state name. Available states: {list(state_filters.keys())}"}
        
        # Get all data and filter in Python since API filters work differently
        all_data = self.get_wells_data(format_type=format_type, limit=1000)
        if "error" in all_data:
            return all_data
        
        if format_type == "json":
            records = all_data.get("records", [])
            state_field = state_filters[state_name.lower()]
            filtered_records = [
                record for record in records 
                if float(record.get(state_field, 0)) > 0
            ]
            all_data["records"] = filtered_records
            all_data["count"] = len(filtered_records)
        
        return all_data
    
    def filter_by_status(self, status: str, format_type: str = "json") -> Dict:
        """
        Filter wells data by status
        
        Args:
            status: Status to filter by
            format_type: Output format
            
        Returns:
            Filtered data
        """
        filters = {"status": status}
        return self.get_wells_data(format_type=format_type, filters=filters)
    
    def filter_by_offshore(self, offshore: bool = True, format_type: str = "json") -> Dict:
        """
        Filter wells data by offshore status (returns records where offshore wells > 0)
        
        Args:
            offshore: True for offshore wells, False for onshore
            format_type: Output format
            
        Returns:
            Filtered data
        """
        # Get all data and filter in Python
        all_data = self.get_wells_data(format_type=format_type, limit=1000)
        if "error" in all_data:
            return all_data
        
        if format_type == "json":
            records = all_data.get("records", [])
            if offshore:
                filtered_records = [
                    record for record in records 
                    if float(record.get("offshore", 0)) > 0
                ]
            else:
                filtered_records = [
                    record for record in records 
                    if float(record.get("offshore", 0)) == 0
                ]
            all_data["records"] = filtered_records
            all_data["count"] = len(filtered_records)
        
        return all_data
    
    def save_to_file(self, data: Union[Dict, List], filename: str, format_type: str = "json"):
        """
        Save data to file
        
        Args:
            data: Data to save
            filename: Output filename
            format_type: File format (json, csv, xml)
        """
        try:
            if format_type == "json":
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format_type == "csv":
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(str(data))
            elif format_type == "xml":
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            print(f"Data saved to {filename}")
            
        except Exception as e:
            print(f"Error saving file: {e}")


def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description="Status of Wells API Client")
    parser.add_argument("--api-key", default="579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
                       help="API key for authentication")
    parser.add_argument("--format", choices=["json", "xml", "csv"], default="json",
                       help="Output format")
    parser.add_argument("--offset", type=int, default=0,
                       help="Number of records to skip")
    parser.add_argument("--limit", type=int, default=10,
                       help="Maximum number of records to return")
    parser.add_argument("--state", help="Filter by state name")
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--offshore", action="store_true",
                       help="Filter for offshore wells")
    parser.add_argument("--onshore", action="store_true",
                       help="Filter for onshore wells")
    parser.add_argument("--save", help="Save output to file")
    parser.add_argument("--all", action="store_true",
                       help="Get all records (may take time)")
    
    args = parser.parse_args()
    
    # Initialize client
    client = WellsAPIClient(api_key=args.api_key)
    
    # Determine filters
    filters = {}
    if args.state:
        result = client.filter_by_state(args.state, args.format)
        if "error" in result:
            print(result["error"])
            return
        data = result
    elif args.status:
        result = client.filter_by_status(args.status, args.format)
        if "error" in result:
            print(result["error"])
            return
        data = result
    elif args.offshore:
        data = client.filter_by_offshore(True, args.format)
    elif args.onshore:
        data = client.filter_by_offshore(False, args.format)
    elif args.all:
        data = client.get_all_wells_data(args.format)
    else:
        data = client.get_wells_data(
            format_type=args.format,
            offset=args.offset,
            limit=args.limit
        )
    
    # Handle errors
    if "error" in data:
        print(f"API Error: {data['error']}")
        return
    
    # Output or save data
    if args.save:
        client.save_to_file(data, args.save, args.format)
    else:
        if args.format == "json":
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(data)


if __name__ == "__main__":
    main()
