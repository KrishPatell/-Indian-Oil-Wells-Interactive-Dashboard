# 🗺️ Interactive Oil Wells Maps of India

This directory contains interactive maps and dashboards for visualizing oil wells data across India.

## 📁 Files Created

### 🗺️ Interactive Maps
- **`interactive_oil_wells_map.html`** - Main interactive map with all features
- **`oil_wells_dashboard.html`** - Comprehensive dashboard with multiple views
- **`main_oil_map.html`** - Main map view
- **`offshore_oil_map.html`** - Offshore wells focused map
- **`company_oil_map.html`** - Company locations map

### 🐍 Python Scripts
- **`interactive_oil_map.py`** - Creates the main interactive map
- **`advanced_oil_dashboard.py`** - Creates the comprehensive dashboard
- **`wells_api_client.py`** - API client for fetching data

## 🚀 How to Use

### Quick Start
1. **Open the Dashboard**: Double-click `oil_wells_dashboard.html` to open in your browser
2. **Explore Maps**: Use the tabs to switch between different map views
3. **Interactive Features**: Click on markers, zoom, pan, and use tools

### Features Available

#### 🗺️ Main Interactive Map (`interactive_oil_wells_map.html`)
- **Clickable State Markers**: Click on any state to see detailed information
- **Color-Coded Markers**: 
  - 🔴 Red: 1000+ wells
  - 🟠 Orange: 100-999 wells  
  - 🔵 Blue: 10-99 wells
  - 🟢 Green: 1-9 wells
- **Company Markers**: Purple markers show major company locations
- **Heatmap Overlay**: Shows well density across India
- **Statistics Panel**: Real-time statistics on the right side
- **Legend**: Color coding explanation
- **Interactive Tools**: Fullscreen, measurement, drawing tools

#### 📊 Comprehensive Dashboard (`oil_wells_dashboard.html`)
- **Multiple Map Views**: 
  - Main Map: Complete overview
  - Offshore Wells: Focus on offshore operations
  - Companies: Company headquarters and facilities
- **Statistics Cards**: Key metrics and rankings
- **Responsive Design**: Works on desktop and mobile
- **Bootstrap UI**: Professional, modern interface

## 🎮 Interactive Features

### 🖱️ Navigation
- **Zoom**: Mouse wheel or zoom controls
- **Pan**: Click and drag to move around
- **Fullscreen**: Click fullscreen button for immersive view

### 📍 Markers
- **State Markers**: Click to see well counts, percentages, and rankings
- **Company Markers**: Click to see company information and well counts
- **Tooltips**: Hover over markers for quick information

### 🛠️ Tools
- **Measurement**: Measure distances between points
- **Drawing**: Draw shapes and add notes
- **Layer Control**: Toggle different map layers
- **Marker Clustering**: Automatically groups nearby markers

## 📊 Data Visualization

### 🎨 Color Coding
- **Well Count**: Colors indicate number of wells
- **Company Type**: Different colors for public/private companies
- **Heatmap**: Density visualization of well locations

### 📈 Statistics
- **Total Wells**: 7,490 across India
- **Top States**: Gujarat leads with 3,547 wells
- **Offshore vs Onshore**: 20% offshore, 80% onshore
- **Company Breakdown**: ONGC dominates with 7,315 wells

## 🔧 Technical Details

### Libraries Used
- **Folium**: Interactive map creation
- **Bootstrap**: Responsive UI framework
- **Font Awesome**: Icons and symbols
- **OpenStreetMap**: Base map tiles
- **CartoDB**: Alternative map styles

### Data Source
- **API**: data.gov.in Status of Wells API
- **Date**: April 1, 2021
- **Source**: Ministry of Petroleum and Natural Gas, Government of India

### Browser Compatibility
- ✅ Chrome (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ Internet Explorer (Limited support)

## 🎯 Use Cases

### 📚 Educational
- Learn about India's oil industry
- Understand geographical distribution
- Study company operations

### 💼 Business
- Market analysis
- Investment decisions
- Competitive analysis

### 🏛️ Government
- Policy planning
- Resource allocation
- Infrastructure development

## 🚀 Running from Command Line

```bash
# Create main interactive map
python3 interactive_oil_map.py

# Create comprehensive dashboard
python3 advanced_oil_dashboard.py

# Fetch data only
python3 wells_api_client.py --limit 10
```

## 📱 Mobile Usage

The maps are fully responsive and work on:
- 📱 Smartphones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

## 🔄 Updates

To update the data:
1. Run the Python scripts again
2. The maps will automatically fetch latest data
3. New HTML files will be generated

## 🆘 Troubleshooting

### Map Not Loading
- Check internet connection (required for map tiles)
- Try refreshing the page
- Clear browser cache

### Data Not Showing
- Verify API connection
- Check browser console for errors
- Ensure JavaScript is enabled

### Performance Issues
- Close other browser tabs
- Use Chrome for best performance
- Disable heatmap if needed

## 📞 Support

For issues or questions:
- Check the Python console output
- Verify all files are in the same directory
- Ensure Python dependencies are installed

## 🎉 Enjoy Exploring!

The interactive maps provide a comprehensive view of India's oil industry. Click around, zoom in on interesting areas, and discover the fascinating world of oil wells across the country!
