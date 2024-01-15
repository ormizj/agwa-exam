import json


def success_result(status_code, data) -> dict:
    """
    creates a success result dictionary with the given status code and data

    Args:
        status_code (int): the HTTP status code
        data (any): the data to be included in the response body

    Returns:
        dict: the success result dictionary
    """
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'is_success': True,
            'data': data
        }),
    };


def error_result(status_code, data) -> dict:
    """
    creates an error result dictionary with the given status code and data

    Args:
        status_code (int): the HTTP status code
        data (any): the data to be included in the response body

    Returns:
        dict: the error result dictionary
    """
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'is_success': False,
            'data': data
        }),
    };


def send_email_to_admin() -> None:
    # sends an email to the admin
    # this function should not throw an exception
    pass
