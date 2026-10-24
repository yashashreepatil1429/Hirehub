class HireHubError(Exception):
    def __init__(self, message, error_code='GENERAL_ERROR'):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class UserAlreadyExistsError(HireHubError):
    def __init__(self, message='User already exists'):
        super().__init__(message, 'USER_ALREADY_EXISTS')


class InvalidCredentialsError(HireHubError):
    def __init__(self, message='Invalid credentials'):
        super().__init__(message, 'INVALID_CREDENTIALS')


class UserNotFoundError(HireHubError):
    def __init__(self, message='User not found'):
        super().__init__(message, 'USER_NOT_FOUND')


class UnauthorizedError(HireHubError):
    def __init__(self, message='Unauthorized'):
        super().__init__(message, 'UNAUTHORIZED')


class JobNotFoundError(HireHubError):
    def __init__(self, message='Job not found'):
        super().__init__(message, 'JOB_NOT_FOUND')


class JobClosedError(HireHubError):
    def __init__(self, message='Job is closed'):
        super().__init__(message, 'JOB_CLOSED')


class DuplicateApplicationError(HireHubError):
    def __init__(self, message='Duplicate application'):
        super().__init__(message, 'DUPLICATE_APPLICATION')


class ApplicationNotFoundError(HireHubError):
    def __init__(self, message='Application not found'):
        super().__init__(message, 'APPLICATION_NOT_FOUND')


class InvalidApplicationStatusError(HireHubError):
    def __init__(self, message='Invalid application status'):
        super().__init__(message, 'INVALID_APPLICATION_STATUS')


class ResumeUploadError(HireHubError):
    def __init__(self, message='Resume upload failed'):
        super().__init__(message, 'RESUME_UPLOAD_ERROR')


class ValidationError(HireHubError):
    def __init__(self, message='Invalid request data', error_code='VALIDATION_ERROR'):
        super().__init__(message, error_code)
