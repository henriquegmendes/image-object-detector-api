class GenericException(Exception):
    def __init__(self, todo_id):
        self.message = f'Generic error: {self}'
