# 🛢️ Indian Oil Wells Interactive Dashboard

A comprehensive web application for visualizing and analyzing oil wells data across India, featuring interactive maps and an AI-powered chatbot assistant.

## 🌟 Features

- **🗺️ Interactive Maps**: Multiple visualization views including main map, offshore wells, and company locations
- **🤖 AI Chatbot**: Intelligent assistant that answers questions about oil wells data
- **📊 Real-time Data**: Live integration with Indian government API
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎯 State-wise Analysis**: Detailed breakdown by Indian states
- **🏢 Company Operations**: Information about major oil companies and their operations

## 🚀 Live Demo

- **Main Dashboard with Chatbot**: `oil_wells_chatbot_dashboard.html`
- **Original Dashboard**: `oil_wells_dashboard.html`
- **Interactive Map**: `interactive_oil_wells_map.html`

## 📊 Data Overview

- **Total Wells**: 7,490
- **Oil Wells**: 6,092
- **Gas Wells**: 1,398
- **Offshore Wells**: 1,496 (20%)
- **Onshore Wells**: 5,994 (80%)

### 🏆 Top States by Well Count

1. **Gujarat**: 3,547 wells (47.4%)
2. **Assam & Arunachal Pradesh**: 903 wells (12.1%)
3. **Rajasthan**: 459 wells (6.1%)
4. **West Bengal (CBM)**: 362 wells (4.8%)
5. **Madhya Pradesh (CBM)**: 294 wells (3.9%)

### 🏢 Major Companies

- **ONGC**: 7,315 wells
- **Oil India Limited**: 455 wells
- **PSC/RSC Companies**: 1,344 wells

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- Web browser with JavaScript enabled

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KrishPatell/-Indian-Oil-Wells-Interactive-Dashboard.git
   cd -Indian-Oil-Wells-Interactive-Dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run local server**:
   ```bash
   python3 -m http.server 8000
   ```

4. **Open in browser**:
   ```
   http://localhost:8000/oil_wells_chatbot_dashboard.html
   ```

## 📁 Project Structure

```
├── oil_wells_chatbot_dashboard.html    # Main dashboard with AI chatbot
├── oil_wells_dashboard.html            # Original dashboard
├── interactive_oil_wells_map.html       # Interactive map
├── main_oil_map.html                   # Main map view
├── offshore_oil_map.html               # Offshore wells map
├── company_oil_map.html                # Company locations map
├── wells_api_client.py                 # Python API client
├── advanced_oil_dashboard.py           # Dashboard generator
├── example_usage.py                    # Usage examples
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
└── MAP_README.md                       # Map documentation
```

## 🤖 Chatbot Usage

The AI chatbot can answer questions about:

- **General Statistics**: "How many total wells are there in India?"
- **State-specific Data**: "How many wells are in Gujarat?"
- **Company Information**: "Which companies operate wells?"
- **Rankings**: "Which state has the most wells?"
- **Offshore/Onshore**: "How many offshore wells are there?"

### Example Queries

- "How many total wells are there in India?"
- "Show me Gujarat wells data"
- "Which companies operate wells?"
- "Rank states by well count"
- "How many offshore wells are there?"

## 🔧 API Integration

The application integrates with the Indian government's oil wells API:

- **API Endpoint**: `https://api.data.gov.in/resource/0b344af7-b389-4e37-bf49-b4f1e59bbc49`
- **Data Source**: Ministry of Petroleum and Natural Gas
- **Last Updated**: April 1, 2021

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Maps**: Folium (Python), Leaflet.js
- **Data Visualization**: Interactive markers, heatmaps, clustering
- **Backend**: Python, Requests library
- **API**: RESTful API integration
- **Icons**: Font Awesome

## 📊 Map Features

- **Interactive Markers**: Clickable state and company markers
- **Zoom Controls**: Pan and zoom functionality
- **Multiple Layers**: Different tile layers and overlays
- **Heatmap Visualization**: Density-based color coding
- **Detailed Popups**: Rich information on marker click
- **Responsive Design**: Mobile-friendly interface

## 🚀 Deployment

### GitHub Pages

1. Push code to GitHub repository
2. Enable GitHub Pages in repository settings
3. Select source branch (main)
4. Access via: `https://krishpatell.github.io/-Indian-Oil-Wells-Interactive-Dashboard/`

### Local Server

```bash
python3 -m http.server 8000
open http://localhost:8000/oil_wells_chatbot_dashboard.html
```

## 📈 Future Enhancements

- [ ] Real-time data updates
- [ ] Advanced filtering options
- [ ] Export functionality
- [ ] Mobile app version
- [ ] Additional data sources
- [ ] Enhanced chatbot capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

- **GitHub**: [@KrishPatell](https://github.com/KrishPatell)
- **Repository**: [Indian Oil Wells Interactive Dashboard](https://github.com/KrishPatell/-Indian-Oil-Wells-Interactive-Dashboard)

## 🙏 Acknowledgments

- **Data Source**: Ministry of Petroleum and Natural Gas, Government of India
- **API**: data.gov.in
- **Maps**: Folium, Leaflet.js
- **Icons**: Font Awesome
- **Framework**: Bootstrap

---

**Made with ❤️ for Indian Oil Industry Analysis**