import http

from tests import utils


def _get_values(data, fields):

    if isinstance(fields, tuple):
        values = [utils.get_from_dict(i, fields) for i in data]

    # Combine to field to one validator example(first_name and last_name)
    elif isinstance(fields, list):
        values = [' '.join([i[field] for field in fields]) for i in data]

    else:
        values = [i[fields] for i in data]

    return [i for i in values if i is not None]


def validate_ordering(data, order_by, fields, key=None):
    reverse = True if order_by[0] == '-' else False

    values = _get_values(data, fields)

    try:
        act = sorted(set(values), key=values.index)

    except TypeError:
        values = [i[0] for i in values]
        act = sorted(set(values), key=values.index)

    exp = sorted(set(values), reverse=reverse, key=key)

    assert act == exp


def validate_error_message(
        resp,
        message,
        field=None,
        error_code=http.HTTPStatus.BAD_REQUEST):
    """
    Method for validation error messages from server

    :param resp: response
    :param message: the expected error message
    :param field: field for this error message
    :param error_code: http error code of response. default is 403
    :return:
    """
    assert resp.status_code == error_code

    message = sorted(message) if isinstance(message, (tuple, list)) else [message]

    # Validate Error message, if this is NOT field error
    if field is None:
        assert sorted(resp.json()['errors']) == message

    else:
        # Validate deep error message in field, for example
        # ['field_errors']['user']['email']
        if isinstance(field, (tuple, list)):
            errors = resp.json()['field_errors']
            act_messsage = utils.get_from_dict(errors, field)
            assert act_messsage == message

        # Validate Basic field error
        else:
            assert resp.json()['field_errors'][field] == message
