#!/usr/bin/env python3
"""
Advanced Oil Wells Dashboard
Creates a comprehensive web dashboard with multiple interactive maps,
charts, and data visualizations for Indian oil wells.
"""

import folium
import json
import pandas as pd
from folium import plugins
from folium.plugins import MarkerCluster, HeatMap, TimeSliderChoropleth
import webbrowser
import os
from wells_api_client import WellsAPIClient
# Removed plotly imports for simpler implementation


class AdvancedOilDashboard:
    """Creates advanced dashboard with multiple visualizations"""
    
    def __init__(self):
        self.client = WellsAPIClient()
        self.data = {}
        self.maps = {}
        
    def fetch_all_data(self):
        """Fetch comprehensive data from API"""
        print("🔄 Fetching comprehensive oil wells data...")
        
        # Get all data
        all_data = self.client.get_wells_data(limit=1000)
        if 'error' in all_data:
            print(f"Error: {all_data['error']}")
            return False
        
        self.data = all_data
        return True
    
    def create_main_map(self):
        """Create the main interactive map"""
        print("🗺️ Creating main interactive map...")
        
        # Create map centered on India
        main_map = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add multiple tile layers
        folium.TileLayer('CartoDB positron', name='Light Mode').add_to(main_map)
        folium.TileLayer('CartoDB dark_matter', name='Dark Mode').add_to(main_map)
        
        # Get state data
        records = self.data.get('records', [])
        state_data = {}
        for record in records:
            if 'Total Flowing Wells' in record.get('status', ''):
                state_data = record
                break
        
        # State coordinates and data
        def safe_int(value):
            if isinstance(value, str):
                try:
                    return float(value)
                except:
                    return 0
            return value
        
        state_info = {
            'Gujarat': {'lat': 23.0225, 'lon': 72.5714, 'wells': safe_int(state_data.get('gujarat', 0))},
            'Rajasthan': {'lat': 27.0238, 'lon': 74.2179, 'wells': safe_int(state_data.get('rajasthan', 0))},
            'Assam & Arunachal Pradesh': {'lat': 26.2006, 'lon': 92.9376, 'wells': safe_int(state_data.get('assam___arunachal_pradesh', 0))},
            'Tripura': {'lat': 23.9408, 'lon': 91.9882, 'wells': safe_int(state_data.get('tripura', 0))},
            'Andhra Pradesh': {'lat': 15.9129, 'lon': 79.7400, 'wells': safe_int(state_data.get('andhra_pradesh', 0))},
            'Tamil Nadu': {'lat': 11.1271, 'lon': 78.6569, 'wells': safe_int(state_data.get('tamilnadu', 0))},
            'West Bengal (CBM)': {'lat': 22.9868, 'lon': 87.8550, 'wells': safe_int(state_data.get('west_bangal__cbm_', 0))},
            'Jharkhand (CBM)': {'lat': 23.6102, 'lon': 85.2799, 'wells': safe_int(state_data.get('jharkhand__cbm_', 0))},
            'Madhya Pradesh (CBM)': {'lat': 22.9734, 'lon': 78.6569, 'wells': safe_int(state_data.get('madhya_pradesh__cbm_', 0))},
            'Other States': {'lat': 28.6139, 'lon': 77.2090, 'wells': safe_int(state_data.get('other_state__up_hp_mp_bihar__punjab_jk_wb_', 0))}
        }
        
        # Create marker clusters
        oil_cluster = MarkerCluster(name='Oil Wells').add_to(main_map)
        company_cluster = MarkerCluster(name='Companies').add_to(main_map)
        
        # Add state markers
        for state, info in state_info.items():
            if info['wells'] > 0:
                wells = int(info['wells'])
                
                # Color coding based on well count
                if wells > 1000:
                    color = 'red'
                    size = 20
                elif wells > 100:
                    color = 'orange'
                    size = 15
                elif wells > 10:
                    color = 'blue'
                    size = 10
                else:
                    color = 'green'
                    size = 8
                
                # Create popup with detailed information
                popup_html = f"""
                <div style="width: 300px; font-family: Arial;">
                    <h3 style="color: {color}; margin-bottom: 15px;">🛢️ {state}</h3>
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <p><strong>Total Wells:</strong> {wells:,}</p>
                        <p><strong>Percentage:</strong> {(wells/7490)*100:.1f}%</p>
                        <p><strong>Rank:</strong> #{self.get_state_rank(state, state_info)}</p>
                    </div>
                    <div style="background: #e3f2fd; padding: 10px; border-radius: 5px;">
                        <h4 style="margin-top: 0;">📊 Quick Stats</h4>
                        <p>• Wells per 1000 sq km: {(wells/self.get_state_area(state)):.1f}</p>
                        <p>• Major Companies: {self.get_major_companies(state)}</p>
                    </div>
                    <hr>
                    <p style="text-align: center; color: #666;">
                        <em>Click marker for more details</em>
                    </p>
                </div>
                """
                
                folium.Marker(
                    location=[info['lat'], info['lon']],
                    popup=folium.Popup(popup_html, max_width=350),
                    tooltip=f"{state}: {wells:,} wells",
                    icon=folium.Icon(color=color, icon='industry', prefix='fa')
                ).add_to(oil_cluster)
        
        # Add company markers
        companies = {
            'ONGC Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'wells': 7315, 'type': 'Public'},
            'ONGC Dehradun': {'lat': 30.3165, 'lon': 78.0322, 'wells': 2000, 'type': 'Public'},
            'Oil India Duliajan': {'lat': 27.3692, 'lon': 95.3269, 'wells': 455, 'type': 'Public'},
            'Reliance KG-D6': {'lat': 16.1667, 'lon': 81.1333, 'wells': 200, 'type': 'Private'},
            'Cairn Rajasthan': {'lat': 26.2389, 'lon': 73.0243, 'wells': 300, 'type': 'Private'}
        }
        
        for company, info in companies.items():
            folium.Marker(
                location=[info['lat'], info['lon']],
                popup=f"""
                <div style="width: 250px;">
                    <h4 style="color: #2E86AB;">🏢 {company}</h4>
                    <p><strong>Type:</strong> {info['type']}</p>
                    <p><strong>Wells:</strong> {info['wells']:,}</p>
                    <p><strong>Market Share:</strong> {(info['wells']/7490)*100:.1f}%</p>
                </div>
                """,
                tooltip=f"{company} - {info['wells']:,} wells",
                icon=folium.Icon(color='purple', icon='building', prefix='fa')
            ).add_to(company_cluster)
        
        # Add heatmap
        heat_data = []
        for state, info in state_info.items():
            if info['wells'] > 0:
                for _ in range(min(int(info['wells']) // 50, 100)):
                    heat_data.append([info['lat'], info['lon']])
        
        if heat_data:
            HeatMap(heat_data, name='Well Density Heatmap', show=False).add_to(main_map)
        
        # Add layer control
        folium.LayerControl().add_to(main_map)
        
        # Add plugins
        plugins.Fullscreen().add_to(main_map)
        plugins.MeasureControl().add_to(main_map)
        plugins.Draw().add_to(main_map)
        
        self.maps['main'] = main_map
        return main_map
    
    def create_offshore_map(self):
        """Create specialized offshore wells map"""
        print("🌊 Creating offshore wells map...")
        
        offshore_map = folium.Map(
            location=[15.0, 80.0],  # Focus on offshore areas
            zoom_start=6,
            tiles='CartoDB positron'
        )
        
        # Offshore well locations (approximate)
        offshore_locations = [
            {'name': 'Mumbai High', 'lat': 19.5, 'lon': 72.0, 'wells': 800},
            {'name': 'KG-D6 Block', 'lat': 16.0, 'lon': 81.0, 'wells': 200},
            {'name': 'Cauvery Basin', 'lat': 11.0, 'lon': 79.0, 'wells': 150},
            {'name': 'Krishna-Godavari', 'lat': 16.5, 'lon': 81.5, 'wells': 100},
            {'name': 'Cambay Basin', 'lat': 22.0, 'lon': 72.5, 'wells': 200},
            {'name': 'Assam Shelf', 'lat': 24.0, 'lon': 93.0, 'wells': 46}
        ]
        
        for location in offshore_locations:
            folium.Marker(
                location=[location['lat'], location['lon']],
                popup=f"""
                <div style="width: 250px;">
                    <h4 style="color: #1976D2;">🌊 {location['name']}</h4>
                    <p><strong>Offshore Wells:</strong> {location['wells']:,}</p>
                    <p><strong>Water Depth:</strong> 50-2000m</p>
                    <p><strong>Production:</strong> Active</p>
                </div>
                """,
                tooltip=f"{location['name']} - {location['wells']:,} wells",
                icon=folium.Icon(color='blue', icon='anchor', prefix='fa')
            ).add_to(offshore_map)
        
        self.maps['offshore'] = offshore_map
        return offshore_map
    
    def create_company_map(self):
        """Create company-focused map"""
        print("🏢 Creating company-focused map...")
        
        company_map = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Company headquarters and major facilities
        company_locations = {
            'ONGC': [
                {'name': 'ONGC HQ - New Delhi', 'lat': 28.6139, 'lon': 77.2090, 'type': 'Headquarters'},
                {'name': 'ONGC Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'type': 'Regional Office'},
                {'name': 'ONGC Dehradun', 'lat': 30.3165, 'lon': 78.0322, 'type': 'Technical Center'},
                {'name': 'ONGC Ahmedabad', 'lat': 23.0225, 'lon': 72.5714, 'type': 'Regional Office'}
            ],
            'Reliance Industries': [
                {'name': 'RIL Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'type': 'Headquarters'},
                {'name': 'RIL Jamnagar', 'lat': 22.4707, 'lon': 70.0577, 'type': 'Refinery Complex'},
                {'name': 'RIL KG-D6', 'lat': 16.1667, 'lon': 81.1333, 'type': 'Offshore Block'}
            ],
            'Cairn Oil & Gas': [
                {'name': 'Cairn Gurugram', 'lat': 28.4595, 'lon': 77.0266, 'type': 'Headquarters'},
                {'name': 'Cairn Rajasthan', 'lat': 26.2389, 'lon': 73.0243, 'type': 'Production Block'}
            ]
        }
        
        colors = {'ONGC': 'red', 'Reliance Industries': 'blue', 'Cairn Oil & Gas': 'green'}
        
        for company, locations in company_locations.items():
            for location in locations:
                folium.Marker(
                    location=[location['lat'], location['lon']],
                    popup=f"""
                    <div style="width: 250px;">
                        <h4 style="color: {colors[company]};">🏢 {location['name']}</h4>
                        <p><strong>Company:</strong> {company}</p>
                        <p><strong>Type:</strong> {location['type']}</p>
                        <p><strong>Status:</strong> Active</p>
                    </div>
                    """,
                    tooltip=f"{company} - {location['name']}",
                    icon=folium.Icon(color=colors[company], icon='building', prefix='fa')
                ).add_to(company_map)
        
        self.maps['company'] = company_map
        return company_map
    
    def create_dashboard_html(self):
        """Create comprehensive HTML dashboard"""
        print("📊 Creating comprehensive dashboard...")
        
        # Save individual maps
        self.maps['main'].save('main_oil_map.html')
        self.maps['offshore'].save('offshore_oil_map.html')
        self.maps['company'].save('company_oil_map.html')
        
        # Create dashboard HTML
        dashboard_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Indian Oil Wells Interactive Dashboard</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; }
                .dashboard-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; }
                .map-container { height: 600px; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                .stats-card { background: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; }
                .nav-pills .nav-link.active { background-color: #667eea; }
                .nav-pills .nav-link { color: #667eea; }
            </style>
        </head>
        <body>
            <div class="dashboard-header text-center">
                <div class="container">
                    <h1><i class="fas fa-oil-can"></i> Indian Oil Wells Interactive Dashboard</h1>
                    <p class="lead">Comprehensive visualization of oil wells across India</p>
                    <p><strong>Data Source:</strong> Ministry of Petroleum and Natural Gas (as of April 1, 2021)</p>
                </div>
            </div>
            
            <div class="container mt-4">
                <div class="row">
                    <div class="col-md-3">
                        <div class="stats-card">
                            <h5><i class="fas fa-chart-bar text-primary"></i> Key Statistics</h5>
                            <hr>
                            <p><strong>Total Wells:</strong> 7,490</p>
                            <p><strong>Oil Wells:</strong> 6,092</p>
                            <p><strong>Gas Wells:</strong> 1,398</p>
                            <p><strong>Offshore:</strong> 1,496 (20%)</p>
                            <p><strong>Onshore:</strong> 5,994 (80%)</p>
                        </div>
                        
                        <div class="stats-card">
                            <h5><i class="fas fa-trophy text-warning"></i> Top States</h5>
                            <hr>
                            <p><strong>1. Gujarat:</strong> 3,547 wells</p>
                            <p><strong>2. Assam & Arunachal:</strong> 903 wells</p>
                            <p><strong>3. Rajasthan:</strong> 459 wells</p>
                            <p><strong>4. West Bengal:</strong> 362 wells</p>
                            <p><strong>5. Madhya Pradesh:</strong> 294 wells</p>
                        </div>
                        
                        <div class="stats-card">
                            <h5><i class="fas fa-building text-info"></i> Major Companies</h5>
                            <hr>
                            <p><strong>ONGC:</strong> 7,315 wells</p>
                            <p><strong>Oil India:</strong> 455 wells</p>
                            <p><strong>PSC/RSC Regime:</strong> 1,344 wells</p>
                        </div>
                    </div>
                    
                    <div class="col-md-9">
                        <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="main-tab" data-bs-toggle="pill" data-bs-target="#main" type="button">
                                    <i class="fas fa-map"></i> Main Map
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="offshore-tab" data-bs-toggle="pill" data-bs-target="#offshore" type="button">
                                    <i class="fas fa-anchor"></i> Offshore Wells
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="company-tab" data-bs-toggle="pill" data-bs-target="#company" type="button">
                                    <i class="fas fa-building"></i> Companies
                                </button>
                            </li>
                        </ul>
                        
                        <div class="tab-content" id="pills-tabContent">
                            <div class="tab-pane fade show active" id="main" role="tabpanel">
                                <div class="map-container">
                                    <iframe src="main_oil_map.html" width="100%" height="100%" frameborder="0"></iframe>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="offshore" role="tabpanel">
                                <div class="map-container">
                                    <iframe src="offshore_oil_map.html" width="100%" height="100%" frameborder="0"></iframe>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="company" role="tabpanel">
                                <div class="map-container">
                                    <iframe src="company_oil_map.html" width="100%" height="100%" frameborder="0"></iframe>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mt-4">
                    <div class="col-12">
                        <div class="stats-card">
                            <h5><i class="fas fa-info-circle text-success"></i> Map Features</h5>
                            <div class="row">
                                <div class="col-md-4">
                                    <h6>🗺️ Interactive Features</h6>
                                    <ul>
                                        <li>Clickable state markers</li>
                                        <li>Zoom and pan controls</li>
                                        <li>Multiple tile layers</li>
                                        <li>Fullscreen mode</li>
                                    </ul>
                                </div>
                                <div class="col-md-4">
                                    <h6>📊 Data Visualization</h6>
                                    <ul>
                                        <li>Color-coded markers</li>
                                        <li>Heatmap overlay</li>
                                        <li>Detailed popups</li>
                                        <li>Statistics panel</li>
                                    </ul>
                                </div>
                                <div class="col-md-4">
                                    <h6>🔧 Tools</h6>
                                    <ul>
                                        <li>Measurement tools</li>
                                        <li>Drawing tools</li>
                                        <li>Layer controls</li>
                                        <li>Marker clustering</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
        
        with open('oil_wells_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        return 'oil_wells_dashboard.html'
    
    def get_state_rank(self, state, state_info):
        """Get rank of state by well count"""
        sorted_states = sorted(state_info.items(), key=lambda x: x[1]['wells'], reverse=True)
        for i, (s, _) in enumerate(sorted_states, 1):
            if s == state:
                return i
        return 0
    
    def get_state_area(self, state):
        """Get approximate area of state in sq km"""
        areas = {
            'Gujarat': 196024,
            'Rajasthan': 342239,
            'Assam & Arunachal Pradesh': 78438,
            'Tripura': 10486,
            'Andhra Pradesh': 160205,
            'Tamil Nadu': 130058,
            'West Bengal (CBM)': 88752,
            'Jharkhand (CBM)': 79714,
            'Madhya Pradesh (CBM)': 308252,
            'Other States': 500000
        }
        return areas.get(state, 100000)
    
    def get_major_companies(self, state):
        """Get major companies operating in state"""
        companies = {
            'Gujarat': 'ONGC, Reliance, Cairn',
            'Rajasthan': 'Cairn, ONGC',
            'Assam & Arunachal Pradesh': 'ONGC, Oil India',
            'Tripura': 'ONGC',
            'Andhra Pradesh': 'ONGC',
            'Tamil Nadu': 'ONGC',
            'West Bengal (CBM)': 'Various PSC',
            'Jharkhand (CBM)': 'Various PSC',
            'Madhya Pradesh (CBM)': 'Various PSC',
            'Other States': 'Various'
        }
        return companies.get(state, 'Various')
    
    def generate_dashboard(self):
        """Generate complete dashboard"""
        print("🚀 Generating advanced oil wells dashboard...")
        
        if not self.fetch_all_data():
            return None
        
        # Create all maps
        self.create_main_map()
        self.create_offshore_map()
        self.create_company_map()
        
        # Create dashboard
        dashboard_file = self.create_dashboard_html()
        
        print(f"✅ Dashboard created: {dashboard_file}")
        print("🌐 Opening dashboard in browser...")
        
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        
        return dashboard_file


def main():
    """Main function"""
    print("📊 Advanced Oil Wells Dashboard")
    print("=" * 50)
    
    dashboard = AdvancedOilDashboard()
    dashboard_file = dashboard.generate_dashboard()
    
    if dashboard_file:
        print(f"\n🎉 Success! Dashboard created: {dashboard_file}")
        print("\n📋 Features included:")
        print("   • Interactive main map with state data")
        print("   • Specialized offshore wells map")
        print("   • Company-focused map")
        print("   • Comprehensive statistics")
        print("   • Bootstrap-based responsive design")
        print("   • Multiple visualization modes")
        
        print(f"\n🌐 Open {dashboard_file} in your browser!")
    else:
        print("❌ Failed to create dashboard")


if __name__ == "__main__":
    main()
