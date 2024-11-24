from vellum.workflows.errors import VellumError, VellumErrorCode


class NodeException(Exception):
    def __init__(self, message: str, code: VellumErrorCode):
        self.message = message
        self.code = code
        super().__init__(message)

    @property
    def error(self) -> VellumError:
        return VellumError(
            message=self.message,
            code=self.code,
        )
