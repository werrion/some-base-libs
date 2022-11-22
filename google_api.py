import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class GoogleApiData:

    credential_file = 'Path_to_Your_credential_file.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credential_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpauth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpauth)


class WriteInDoc:

    def __init__(self, spreadsheet_id, sell_range, write_type):
        self.spreadsheet_id = spreadsheet_id
        self.sell_range = sell_range
        self.write_type = write_type

    def write_data_to_doc(self, data):
        service = GoogleApiData.service
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": self.sell_range,
                 "majorDimension": self.write_type,
                 "values": data}]})
        response = request.execute()
        print(response)
        return response


class ReadFromDoc:

    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def read_data_from_doc(self, sell_range, read_dimension):
        service = GoogleApiData.service
        values = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=sell_range,
            majorDimension=read_dimension
        )
        response = values.execute()
        print(response)
        information = response['values']
        return information
