from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

def exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Initialize the message
        message = "An error occurred."

        # Handle validation errors (e.g., non_field_errors)
        if isinstance(response.data, dict):
            non_field_errors = response.data.get('non_field_errors', None)
            if non_field_errors:
                message = non_field_errors[0]  # Use the first error message
        elif isinstance(response.data, list):
            # Handle list of errors (e.g., multiple validation errors)
            if response.data and isinstance(response.data[0], dict):
                non_field_errors = response.data[0].get('non_field_errors', None)
                if non_field_errors:
                    message = non_field_errors[0]  # Use the first error message

        # Build the response data dynamically
        response_data = {
            'status_code': response.status_code,
            'message': message,
        }

        # Only add 'data' to the response if it exists and is not None
        if response.data is not None:
            response_data['data'] = response.data

        # Return the custom response
        return Response(response_data, status=response.status_code)

    # Handle cases where DRF's exception handler returns None
    return Response(
        {
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': "An unknown error occurred.",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )