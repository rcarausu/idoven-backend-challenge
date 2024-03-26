class InvalidUserTokenError(Exception):

    def __init__(self):
        self.message = f"Invalid user token"
        super().__init__(self.message)


class InvalidAdminTokenError(Exception):

    def __init__(self):
        self.message = "Invalid admin token"
        super().__init__(self.message)
