import requests


class SpreadSheetService:
    class Error(Exception):
        pass

    class NotAuthenticated(Error):
        pass

    class PermissionDenied(Error):
        pass

    class NotFound(Error):
        pass

    class QuotaExceeded(Error):
        pass

    @staticmethod
    def normalize_spreadsheet_url(url):
        if url.startswith('https://'):
            return url
        return 'https://' + url

    @classmethod
    def extract_spreadsheet_id(cls, url):
        "Extracts the spreadsheets id from its url."
        url = cls.normalize_spreadsheet_url(url)
        if url.startswith('https://docs.google.com/spreadsheets/d/'):
            sub_url = url.replace('https://docs.google.com/spreadsheets/d/', "")
            return sub_url.split('/')[0]
        if url.startswith('https://docs.google.com/a/'):
            sub_url = url.replace('https://docs.google.com/a/', "")
            return sub_url.split('/')[3]
        raise ValueError("Wrong spreadsheet url: {}".format(url))

    @classmethod
    def check_response(cls, response):
        if response.status_code == 401:
            raise cls.NotAuthenticated("Not authenticated or authentication failed.")
        if response.status_code == 404:
            raise cls.NotFound("Google spreadsheet not found.")
        if response.status_code == 403:
            raise cls.PermissionDenied("You have no access to this spreadsheet.")
        if response.status_code == 429:
            error_data = response.json()
            if error_data['error']['status'] == 'RESOURCE_EXHAUSTED':
                raise cls.QuotaExceeded("Quota exceeded")
        if response.status_code == 200:
            return response.json()
        raise cls.Error("Unknown response status code.")

    @classmethod
    def get_spreadsheet_metadata(cls, token, url):
        "Returns the metadata of the spreadsheet in the url."
        spreadsheet_id = cls.extract_spreadsheet_id(url)
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        url = 'https://sheets.googleapis.com/v4/spreadsheets/{}?includeGridData=false'.format(spreadsheet_id)
        response = requests.get(url, headers=headers)
        return cls.check_response(response)

    @classmethod
    def get_worksheet_range(cls, token, url, data_range):
        "Returns the data in the range"
        spreadsheet_id = cls.extract_spreadsheet_id(url)
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        url = 'https://sheets.googleapis.com/v4/spreadsheets/{}/values/{}?majorDimension=ROWS'.format(spreadsheet_id, data_range)
        response = requests.get(url, headers=headers)
        response =  cls.check_response(response)
        try:
            return response['values']
        except KeyError:
            return []
