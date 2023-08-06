from ._app import get_app_config

__all__ = ['create_response', 'get_status_msg']


def create_response(success, data, wrapper=False):
    """
    Create the response json result.
    :param success:
    :param data:
    :param wrapper:
    :return:
    """
    if success is True:
        return _create_success_response(data, wrapper)
    else:
        return _create_fail_response(data)


def _create_success_response(data, wrapper=False):
    """
    :param data:
    :param wrapper:
    :return:
    """
    status = get_app_config('FLASKZ_RES_SUCCESS_STATUS')
    if wrapper is True:
        _data = {
            'status': status,
        }
        _data.update(data)
        return _data
    else:
        return {
            'status': status,
            'data': data
        }


def _create_fail_response(status_code, msg=None):
    """
    :param msg:
    :param status_code:
    :return:
    """
    status = get_app_config('FLASKZ_RES_FAIL_STATUS')
    msg = msg or get_status_msg(status_code)

    if type(status_code) == tuple:
        status_code = status_code[0]

    return {
        'status': status,
        'status_code': status_code,
        'message': str(msg),
    }


def get_status_msg(status_code):
    """
    Get the specified message by status_code.
    Can be used to return internationalized text, Local can be fixed, or get the local from request
    :param status_code:
    :return:
    """
    if type(status_code) == tuple:
        len_ = len(status_code)
        if len_ > 1:
            return status_code[1] or status_code[0]
        elif len_ > 0:
            return status_code[0]
    return status_code
