import atlassian_jwt
import requests


class AddonGetTask:
    def __init__(self, baseUrl, secure, key):
        self.baseUrl = baseUrl
        self.secure = secure
        self.key = key
        self.__apiPath = '/rest/api/3/issue/'

    def get_data(self, task):
        """Make request and get task info

        Args:
            task (string): task id

        Returns:
            string: task full text
        """
        token = atlassian_jwt.encode_token('GET', self.__apiPath + task, self.key, self.secure)
        data = self.__make_request(task, token)
        return self.parse_response(data.json())

    def __make_request(self, task, token):
        """Make request to Atlassian with jwt-token

        Args:
            task (string): task id
            token (string): jwt token

        Returns:
            requests.Response: response object
        """
        return requests.get(self.baseUrl + self.__apiPath + task, params={'jwt': token})

    @staticmethod
    def parse_response(data):
        """Parse text in TASK info

        Args:
            data (requests.Response): task id

        Returns:
            string: full text string
        """
        res = []
        stack = []

        if data['fields'].get('description'):
            stack.append(data['fields']['description'])

        while len(stack):
            v = stack.pop()

            if len(v.get('content', [])) > 0:
                for item in v['content']:
                    stack.append(item)
            else:
                if v.get('text', False):
                    res.insert(0, v['text'])

        return ';'.join(res)
