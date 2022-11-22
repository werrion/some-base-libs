import requests
import os
from datetime import datetime


class SendSlackMessage:
    """
    Canal - using_utilities : hooks.slack.com/services/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
    Canal - crash_reports : hooks.slack.com/services/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
    """
    def __init__(self, app_name, app_version):
        """
        Generate data for message
        :param app_name:      utility name
        :type app_name:       (str)
        :param app_version:   utility version
        :type  app_version:   (str)
        """
        self.user_name = os.getlogin()
        self.app_name = app_name
        self.app_version = app_version
        self.bot_token = 'xoxb-4028443381488-3998150739366-nBGXzwDivwMq2S3VBPbwvcDs'

    @staticmethod
    def get_location():
        response = requests.get('https://api64.ipify.org?format=json').json()
        ip_address = response["ip"]
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = f"ip: {ip_address}, City: {response.get('city')}, Region: {response.get('region')}, " \
                        f"Country: {response.get('country_name')}"
        return location_data

    def send_crash_message(self, message_text):
        if self.user_name not in {'PC3', 'olegk'}:
            payload = str({"text": f"Exception! \n"
                                   f"User_name: {self.user_name}, Application: {self.app_name}, "
                                   f"Version: {self.app_version} \n"
                                   f"{self.get_location()}\n\n"
                                   f"{message_text}"})
            response = requests.post(
                'https://hooks.slack.com/services/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',
                data=payload,
            )
            print(response.text)

    def send_using_message(self):
        if self.user_name not in {'PC3', 'olegk'}:
            payload = str({"text": f"###################################################################\n"
                                   f"Using utility! Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                   f"{self.get_location()}\n"
                                   f"User_name: {self.user_name}, Application: {self.app_name}, "
                                   f"Version: {self.app_version} \n"})
            response = requests.post(
                'https://hooks.slack.com/services/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',
                data=payload
            )
            print(response.text)

    def send_file_to_crash_channel(self, file_path):
        status = True
        content = str()
        file_name = str(file_path).split('\\')[-1].split('.')[0:-1]
        file_extension = str(file_path).split('\\')[-1].split('.')[-1]

        def get_file_data(file):
            with open(file, "rb") as file:
                file_data = file.read()
            return file_data
        try:
            content = get_file_data(file_path)
        except FileNotFoundError as error_string:
            print('Me so sorry, file not found...')
            self.send_crash_message(f"Fail to send file {file_name}, ERROR {error_string}")

        if status:
            url = "https://slack.com/api/files.upload"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                'token': self.bot_token,
                'channels': '#crashreports',
                'content': content,
                'filetype': file_extension,
                'title': file_name,
            }
            res = requests.post(url=url, data=data, headers=headers)
            if res.status_code == 200:
                print(f'Response: {res.json()}')
            else:
                print(f'Fail to send: {res.json()}')
