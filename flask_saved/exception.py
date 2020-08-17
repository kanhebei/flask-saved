class UploadNotAllowed(Exception):
    """This exception is raised if the upload was not allowed."""

class UploadFileExists(Exception):
    """This exception is raised when the uploaded file exits."""

class UploadNotSizeMax(Exception):
    """This exception is raised when the uploaded file not size."""