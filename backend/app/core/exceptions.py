class EmailDeliveryError(Exception):
    def __init__(self, message: str = "Email delivery failed") -> None:
        self.code = "email_delivery_failed"
        self.message = message
        super().__init__(message)
