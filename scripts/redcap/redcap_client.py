# Description: This script is used to interact with the REDCap API.
# The REDCap API is used to pull data from the REDCap database.

import redcap

class RedcapClient():
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.api = redcap.Project(url, token)

    def get_records(self, fields=None, forms=None, events=None):
        return self.api.export_records(fields=fields, forms=forms, events=events)

    def get_metadata(self):
        return self.api.export_metadata()
    
    def get_instruments(self):
        return self.api.export_instruments()
    
    def get_events(self):
        return self.api.export_events()
    
    def get_arm(self):
        return self.api.export_arms()
    