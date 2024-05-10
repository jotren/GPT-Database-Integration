import requests
import json

class ApplicationAPI:
    def __init__(self, site_id, base_url="http://127.0.0.1:3050/api/v1/"):
        """There are multiple sites, but with each call we will only focus on one site. The database is made up of reports, these reports pertain to a specific system in a specific asset. These reports have all the data and information required to diagnose problems. Each data point in these reports has a severity; 0 = no warning, 1 = early warning, 2 = advanced warning. These severites cascade to the asset level. """
        self.base_url = base_url
        self.site_id = site_id
        self.headers = {"Content-Type": "application/json"}

    def get_asset_ids_names(self):
        """Provides the Asset Id, Name and Location. Example:
        {'id': 1, 'name': 'F1', 'location': 'Robin Rigg F01'}
        """
        url = f"{self.base_url}sites/{self.site_id}/assets"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_all_reports_data(self):
        """Provides all reports in the system. Example: {'id': 1,
          'date': '2023-11-15',
          'fileType': 'application/pdf',
          'asset': {'id': 1, 'name': 'F1'},
          'systems': {'system_id': 1, 'name': 'Hydraulic Pitch Station'},
          'severity': {'sev_id': 1, 'severity': 2, 'severity_count': 3}},"""
        url = f"{self.base_url}sites/{self.site_id}/reports"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_single_report_data(self, report_id):
        """Get summary data for a single report. Need report ID. Example: {'id': 1,
          'date': '2023-11-15',
          'comments': 'Iron is higher than the limit value. Increased number of particles in oil sample. Corrective actions depending on trend observation. Comment on\nbottle: "Pre exchange."\nNo SAMPLE DATE supplied.',
          'fileType': 'application/pdf',
          'asset': {'id': 1, 'name': 'F1'},
          'systems': {'system_id': 1, 'name': 'Hydraulic Pitch Station'},
          'severity': {'sev_id': 1, 'severity': 2, 'severity_count': 3},
          'upload': {'upload_id': 2,
           'filePath': 'C:\\projects\\node\\oil-analysis-backend\\processing\\scans\\files-1712666098870-283268211.pdf'},
          'site': {'site_id': 1,
           'name': 'Robin Rigg',
           'latidute': None,
           'longitude': None}}. """
        url = f"{self.base_url}sites/{self.site_id}/reports/data/{report_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
        
    def get_all_asset_names_from_system_id(self, system_ids):
        """Get all Asset names and ids for a given system. Need a system ID {'name': 'F1', 'asset_id': 1}"""
        url = f"{self.base_url}sites/{self.site_id}/reports/assetlist/{system_ids}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_system_list_for_site(self):
        """All possible systems in a site. Example: 
        {'system_id': 1, 'name': 'Hydraulic Pitch Station'}"""
        url = f"{self.base_url}sites/{self.site_id}/systems"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_all_report_data_from_asset_names(self, asset_name):
        """All report data on specific asset. Example: 
         {'id': 1,
          'date': '2023-11-15',
          'fileType': 'application/pdf',
          'asset': {'id': 1, 'name': 'F1'},
          'systems': {'system_id': 1, 'name': 'Hydraulic Pitch Station'},
          'severity': {'sev_id': 1, 'severity': 2, 'severity_count': 3},
          'site': {'site_id': 1}}, """
        url = f"{self.base_url}sites/{self.site_id}/reports/asset/name/{asset_name}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_all_report_data_from_asset_names_full(self, asset_name):
        """All report data on specific asset. Example: 
         {'id': 1,
          'date': '2023-11-15',
          'fileType': 'application/pdf',
          'asset': {'id': 1, 'name': 'F1'},
          'systems': {'system_id': 1, 'name': 'Hydraulic Pitch Station'},
          'severity': {'sev_id': 1, 'severity': 2, 'severity_count': 3},
          'site': {'site_id': 1}}, """
        url = f"{self.base_url}sites/{self.site_id}/reports/asset/name/full/{asset_name}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_all_asset_severity_data(self):
        """Fetch and truncate the data about assets sorted by severities to ensure the output does not exceed JSON format constraints."""
        url = f"{self.base_url}sites/{self.site_id}/homepage-cards"
        response = requests.get(url, headers=self.headers)
        response_data = response.json()
    
        # Implementing a simple truncation of data at the top level if it's a list
        # Adjust the logic here depending on the actual structure of your response
        if isinstance(response_data, list) and len(response_data) > 10:  # Example limit to first 10 items
            response_data = response_data[:10]
        elif isinstance(response_data, dict):
            for key in response_data:
                if isinstance(response_data[key], list) and len(response_data[key]) > 10:
                    response_data[key] = response_data[key][:10]
    
        # Convert to JSON string
        json_string = json.dumps(response_data)
    
        # If you still need to cut the JSON string to a certain length
        truncated_json_string = json_string[:5000]  # ensure it's less than 5000 characters
    
        return truncated_json_string

    def get_all_system_severity_data(self):
        """Total Severities by all Systems. Example: {'systems': 'Blade Bearing A', 'severity2': 58}"""
        url = f"{self.base_url}sites/{self.site_id}/homepage-graph"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_number_of_assets(self):
        """Number of Assets in the site. Example: {'2': 58}"""
        url = f"{self.base_url}sitepage/summary/{self.site_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_number_of_reports(self):
        """Number of Reports at the site. Example: 1515"""
        url = f"{self.base_url}sitepage/reports/{self.site_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_asset_comments(self, entityId):
        """Return all the comments made against an Asset."""
        url = f"{self.base_url}sites/{self.site_id}/asset/{entityId}/comments"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_report_comments(self, entityId):
        """Return all the comments made against a report"""
        url = f"{self.base_url}sites/{self.site_id}/report/{entityId}/comments"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_all_report_comments(self):
        """Get all comments for reports in a site."""
        url = f"{self.base_url}sites/{self.site_id}/comments"
        response = requests.get(url, headers=self.headers)
        return response.json()
