class Response():
    def error(self, message, code):
        return {
            'status': 'error', 
            'message': message
            }, code

    def success(self, message, data, token, code):
        return {
            'status': 'success',
            'message': message,
            'data': data,
            'token': token
            }, code