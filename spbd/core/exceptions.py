from fastapi import HTTPException, status


class HTTPNotFound(HTTPException):
    def __init__(self, detail=None, headers=None):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class HTTPError(HTTPException):
    def __init__(self, detail=None, headers=None):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)


class HTTPBadRequest(HTTPException):
    def __init__(self, detail=None, headers=None):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class EntityNotFound(Exception):
    pass
