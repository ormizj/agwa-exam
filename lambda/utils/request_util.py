import json

def success_result(status_code, data)->dict:
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'is_success': True,
            'data': data
        }),
    };

def error_result(status_code, data)->dict:
    return {
        'statusCode': status_code,
        'body': json.dumps({
            'is_success': False,
            'data': data
        }),
    };
    
def send_email_to_admin()->None:
    # sends an email to the admin
    # this function should not throw an exception
    pass