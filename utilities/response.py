class Response():
    def error(self, message, code):
        return {
            'status': 'error', 
            'message': message
            }, code

    def success(self, message, data, code):
        return {
            'status': 'success',
            'message': message,
            'data': data,
            }, code