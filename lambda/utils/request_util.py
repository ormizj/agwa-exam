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