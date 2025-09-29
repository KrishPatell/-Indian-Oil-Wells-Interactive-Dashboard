#!/usr/bin/env python3
"""
Interactive Oil Wells Map of India
Creates an interactive map showing oil wells data with clickable states,
zoom functionality, and visual data representation.
"""

import folium
import json
import pandas as pd
from folium import plugins
from folium.plugins import MarkerCluster, HeatMap
import webbrowser
import os
from wells_api_client import WellsAPIClient


class InteractiveOilMap:
    """Creates interactive map of India with oil wells data"""
    
    def __init__(self):
        self.client = WellsAPIClient()
        self.map = None
        self.state_data = {}
        self.company_data = {}
        
    def get_oil_wells_data(self):
        """Fetch oil wells data from API"""
        print("🔄 Fetching oil wells data...")
        data = self.client.get_wells_data(limit=1000)
        
        if 'error' in data:
            print(f"Error fetching data: {data['error']}")
            return None
            
        # Find the record with total flowing wells
        records = data.get('records', [])
        for record in records:
            if 'Total Flowing Wells' in record.get('status', ''):
                self.state_data = record
                break
        
        return self.state_data
    
    def get_state_coordinates(self):
        """Define state coordinates and boundaries"""
        return {
            'Gujarat': {'lat': 23.0225, 'lon': 72.5714, 'zoom': 7},
            'Rajasthan': {'lat': 27.0238, 'lon': 74.2179, 'zoom': 6},
            'Assam & Arunachal Pradesh': {'lat': 26.2006, 'lon': 92.9376, 'zoom': 7},
            'Tripura': {'lat': 23.9408, 'lon': 91.9882, 'zoom': 8},
            'Andhra Pradesh': {'lat': 15.9129, 'lon': 79.7400, 'zoom': 7},
            'Tamil Nadu': {'lat': 11.1271, 'lon': 78.6569, 'zoom': 7},
            'West Bengal (CBM)': {'lat': 22.9868, 'lon': 87.8550, 'zoom': 7},
            'Jharkhand (CBM)': {'lat': 23.6102, 'lon': 85.2799, 'zoom': 7},
            'Madhya Pradesh (CBM)': {'lat': 22.9734, 'lon': 78.6569, 'zoom': 7},
            'Other States': {'lat': 28.6139, 'lon': 77.2090, 'zoom': 6}
        }
    
    def get_company_locations(self):
        """Define major company locations"""
        return {
            'ONGC': [
                {'name': 'ONGC Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'wells': 7315},
                {'name': 'ONGC Dehradun', 'lat': 30.3165, 'lon': 78.0322, 'wells': 2000},
                {'name': 'ONGC Ahmedabad', 'lat': 23.0225, 'lon': 72.5714, 'wells': 3316}
            ],
            'Oil India Limited': [
                {'name': 'OIL Duliajan', 'lat': 27.3692, 'lon': 95.3269, 'wells': 455},
                {'name': 'OIL Noida', 'lat': 28.5355, 'lon': 77.3910, 'wells': 100}
            ],
            'Reliance Industries': [
                {'name': 'RIL KG-D6 Block', 'lat': 16.1667, 'lon': 81.1333, 'wells': 200}
            ],
            'Cairn Oil & Gas': [
                {'name': 'Cairn Rajasthan', 'lat': 26.2389, 'lon': 73.0243, 'wells': 300}
            ]
        }
    
    def create_base_map(self):
        """Create the base map centered on India"""
        print("🗺️ Creating base map...")
        self.map = folium.Map(
            location=[20.5937, 78.9629],  # Center of India
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add different tile layers
        folium.TileLayer('CartoDB positron').add_to(self.map)
        folium.TileLayer('CartoDB dark_matter').add_to(self.map)
        
        # Add layer control
        folium.LayerControl().add_to(self.map)
        
        return self.map
    
    def add_state_markers(self):
        """Add clickable state markers with oil wells data"""
        print("📍 Adding state markers...")
        
        coordinates = self.get_state_coordinates()
        
        # Create marker cluster for better performance
        marker_cluster = MarkerCluster().add_to(self.map)
        
        for state, data in self.state_data.items():
            if state in coordinates and isinstance(data, (int, float)) and data > 0:
                coord = coordinates[state]
                wells_count = int(data)
                
                # Determine color based on well count
                if wells_count > 1000:
                    color = 'red'
                    icon = 'oil-well'
                elif wells_count > 100:
                    color = 'orange'
                    icon = 'industry'
                elif wells_count > 10:
                    color = 'blue'
                    icon = 'industry'
                else:
                    color = 'green'
                    icon = 'industry'
                
                # Create popup content
                popup_content = f"""
                <div style="width: 250px;">
                    <h3 style="color: {color}; margin-bottom: 10px;">{state}</h3>
                    <p><strong>Oil Wells:</strong> {wells_count:,}</p>
                    <p><strong>Percentage:</strong> {(wells_count/7490)*100:.1f}%</p>
                    <hr>
                    <p><em>Click to zoom in for detailed view</em></p>
                </div>
                """
                
                # Add marker
                folium.Marker(
                    location=[coord['lat'], coord['lon']],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=f"{state}: {wells_count:,} wells",
                    icon=folium.Icon(color=color, icon=icon, prefix='fa')
                ).add_to(marker_cluster)
        
        return marker_cluster
    
    def add_company_markers(self):
        """Add company location markers"""
        print("🏢 Adding company markers...")
        
        company_locations = self.get_company_locations()
        
        for company, locations in company_locations.items():
            for location in locations:
                folium.Marker(
                    location=[location['lat'], location['lon']],
                    popup=f"""
                    <div style="width: 200px;">
                        <h4 style="color: #2E86AB;">{location['name']}</h4>
                        <p><strong>Company:</strong> {company}</p>
                        <p><strong>Wells:</strong> {location['wells']:,}</p>
                    </div>
                    """,
                    tooltip=f"{company} - {location['name']}",
                    icon=folium.Icon(color='purple', icon='building', prefix='fa')
                ).add_to(self.map)
    
    def add_heatmap(self):
        """Add heatmap overlay for well density"""
        print("🔥 Adding heatmap...")
        
        coordinates = self.get_state_coordinates()
        heat_data = []
        
        for state, data in self.state_data.items():
            if state in coordinates and isinstance(data, (int, float)) and data > 0:
                coord = coordinates[state]
                wells_count = int(data)
                # Add multiple points for better heatmap visualization
                for _ in range(min(wells_count // 100, 50)):  # Limit points for performance
                    heat_data.append([coord['lat'], coord['lon']])
        
        if heat_data:
            HeatMap(heat_data, name='Well Density Heatmap').add_to(self.map)
    
    def add_charts_and_stats(self):
        """Add charts and statistics to the map"""
        print("📊 Adding charts and statistics...")
        
        # Create statistics HTML
        stats_html = """
        <div style="position: fixed; top: 10px; right: 10px; width: 300px; 
                    background: white; padding: 15px; border-radius: 10px; 
                    box-shadow: 0 0 15px rgba(0,0,0,0.2); z-index: 1000;">
            <h3 style="margin-top: 0; color: #2E86AB;">📈 Oil Wells Statistics</h3>
            <p><strong>Total Wells:</strong> 7,490</p>
            <p><strong>Oil Wells:</strong> 6,092</p>
            <p><strong>Gas Wells:</strong> 1,398</p>
            <hr>
            <h4>🏆 Top States:</h4>
            <p>1. Gujarat: 3,547 wells</p>
            <p>2. Assam & Arunachal: 903 wells</p>
            <p>3. Rajasthan: 459 wells</p>
            <hr>
            <h4>🌊 Offshore vs Onshore:</h4>
            <p>Offshore: 1,496 wells (20%)</p>
            <p>Onshore: 5,994 wells (80%)</p>
        </div>
        """
        
        # Add statistics as HTML
        self.map.get_root().html.add_child(folium.Element(stats_html))
    
    def add_legend(self):
        """Add legend to the map"""
        print("🎨 Adding legend...")
        
        legend_html = """
        <div style="position: fixed; bottom: 50px; left: 10px; width: 200px; 
                    background: white; padding: 15px; border-radius: 10px; 
                    box-shadow: 0 0 15px rgba(0,0,0,0.2); z-index: 1000;">
            <h4 style="margin-top: 0;">Legend</h4>
            <p><i class="fa fa-industry" style="color: red;"></i> 1000+ wells</p>
            <p><i class="fa fa-industry" style="color: orange;"></i> 100-999 wells</p>
            <p><i class="fa fa-industry" style="color: blue;"></i> 10-99 wells</p>
            <p><i class="fa fa-industry" style="color: green;"></i> 1-9 wells</p>
            <hr>
            <p><i class="fa fa-building" style="color: purple;"></i> Company Offices</p>
        </div>
        """
        
        self.map.get_root().html.add_child(folium.Element(legend_html))
    
    def add_interactive_features(self):
        """Add interactive features like zoom controls and plugins"""
        print("🎮 Adding interactive features...")
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(self.map)
        
        # Add measure control
        plugins.MeasureControl().add_to(self.map)
        
        # Add draw plugin
        plugins.Draw().add_to(self.map)
        
        # Add minimap
        minimap = plugins.MiniMap()
        self.map.add_child(minimap)
    
    def create_state_detail_maps(self):
        """Create detailed maps for major states"""
        print("🔍 Creating detailed state maps...")
        
        major_states = {
            'Gujarat': {'lat': 23.0225, 'lon': 72.5714, 'wells': 3547},
            'Assam & Arunachal Pradesh': {'lat': 26.2006, 'lon': 92.9376, 'wells': 903},
            'Rajasthan': {'lat': 27.0238, 'lon': 74.2179, 'wells': 459}
        }
        
        for state, data in major_states.items():
            state_map = folium.Map(
                location=[data['lat'], data['lon']],
                zoom_start=8,
                tiles='OpenStreetMap'
            )
            
            # Add state-specific data
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=f"""
                <div style="width: 250px;">
                    <h3>{state}</h3>
                    <p><strong>Oil Wells:</strong> {data['wells']:,}</p>
                    <p><strong>Percentage of Total:</strong> {(data['wells']/7490)*100:.1f}%</p>
                </div>
                """,
                icon=folium.Icon(color='red', icon='industry', prefix='fa')
            ).add_to(state_map)
            
            # Save individual state map
            state_map.save(f'oil_wells_{state.replace(" ", "_").replace("&", "and")}.html')
    
    def generate_map(self):
        """Generate the complete interactive map"""
        print("🚀 Generating interactive oil wells map...")
        
        # Get data
        if not self.get_oil_wells_data():
            print("❌ Failed to fetch data")
            return None
        
        # Create base map
        self.create_base_map()
        
        # Add all features
        self.add_state_markers()
        self.add_company_markers()
        self.add_heatmap()
        self.add_charts_and_stats()
        self.add_legend()
        self.add_interactive_features()
        
        # Create detailed state maps
        self.create_state_detail_maps()
        
        # Save main map
        map_file = 'interactive_oil_wells_map.html'
        self.map.save(map_file)
        
        print(f"✅ Interactive map saved as: {map_file}")
        print("🌐 Opening map in browser...")
        
        # Open in browser
        webbrowser.open(f'file://{os.path.abspath(map_file)}')
        
        return map_file


def main():
    """Main function to create and display the interactive map"""
    print("🗺️ Interactive Oil Wells Map of India")
    print("=" * 50)
    
    # Create map instance
    oil_map = InteractiveOilMap()
    
    # Generate the map
    map_file = oil_map.generate_map()
    
    if map_file:
        print(f"\n🎉 Success! Interactive map created: {map_file}")
        print("\n📋 Features included:")
        print("   • Clickable state markers with well counts")
        print("   • Company location markers")
        print("   • Heatmap overlay for well density")
        print("   • Interactive statistics panel")
        print("   • Legend and zoom controls")
        print("   • Detailed state maps")
        print("   • Fullscreen and measurement tools")
        
        print(f"\n🌐 Open {map_file} in your browser to explore!")
    else:
        print("❌ Failed to create map")


if __name__ == "__main__":
    main()
