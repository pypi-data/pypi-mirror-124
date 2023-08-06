import http.client
import json
import urllib.request
from copy import copy
from dataclasses import asdict
from typing import List, Dict

from dacite import from_dict

from .model import (
    Group,
    Err,
    Auth,
    CreateGroupResponse,
    User,
    CreateUserResponse,
    CreateGroupApiCallResult,
    CreateUserApiCallResult,
    ApiCallResultBase,
    ListUsersArguments,
    ListNetworksApiCallResult,
    Network,
    NetworkHealth,
    GetNetworksHealthApiCallResult
)


"""
P81 API
"""
_AUTH_URL = 'https://api.perimeter81.com/api/v1/auth/authorize'
_BASE_URL = 'https://api.perimeter81.com/api/rest'
_AUTH_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json',
                 'Authorization': '<REPLACE_ME>'}


def authenticate(api_key: str) -> Auth:
    """
    Authenticate
    """
    def _make_headers(token: str) -> Auth:
        result: Dict = copy(_AUTH_HEADERS)
        result['Authorization'] = f'Bearer {token}'
        return result

    data: Dict = {'grantType': 'api_key', 'apiKey': api_key}
    headers: Dict = {'Content-type': 'application/json', 'accept': 'application/json'}
    auth: Dict = _post(_AUTH_URL, headers, data)
    return _make_headers(auth['data']['accessToken'])


def create_user(auth: Auth, user: User) -> CreateUserApiCallResult:
    """
    Create a User
    """
    return create_users(auth, [user])


def create_users(auth: Auth, users: List[User]) -> CreateUserApiCallResult:
    """
    Create a few Users
    """
    url: str = f'{_BASE_URL}/v1/users'
    errors: List[Err] = []
    results: List[CreateUserResponse] = []
    for user in users:
        payload = asdict(user)
        try:
            response: Dict = _post(url, auth, payload, 201)
            results.append(CreateUserResponse(**response))
        except Exception as e:
            errors.append(str(e))
    return CreateUserApiCallResult(len(errors) == 0, errors, results)


def delete_user(auth: Auth, user_id: str) -> ApiCallResultBase:
    """
    Delete a User
    """
    return delete_users(auth, [user_id])


def delete_users(auth: Auth, user_ids: List[str]) -> ApiCallResultBase:
    """
    Delete a few Users
    """
    return _do_delete(auth, user_ids, '{}/v1/groups/{}')


def _list_users(auth: Auth, list_users_args: ListUsersArguments):
    # TODO: implement
    # see https://perimeter81.slack.com/archives/D02HSK04B8B/p1634457043001200
    pass


def get_network_health(auth: Auth, network_id: str) -> GetNetworksHealthApiCallResult:
    """
    Get Network health
    """
    return get_networks_health(auth, [network_id])


def get_networks_health(auth: Auth, network_ids: List[str]) -> GetNetworksHealthApiCallResult:
    """
    Get a few Networks health
    """
    url_template: str = '{}/v1/networks/{}/health'
    errors: List[Err] = []
    results: List[NetworkHealth]
    for _id in network_ids:
        url: str = url_template.format(_BASE_URL, _id)
        try:
            temp_result: Dict = _get(url, auth)
            results.append(from_dict(NetworkHealth, temp_result['data']))
        except Exception as e:
            errors.append(str(e))
    return GetNetworksHealthApiCallResult(len(errors) == 0, errors, results)


def list_networks(auth: Auth) -> ListNetworksApiCallResult:
    """
    List Networks
    """
    url: str = f'{_BASE_URL}/v1/networks'
    try:
        temp_results: List[Dict] = _get(url, auth)
        results: List[Network] = [from_dict(Network, x) for x in temp_results['data']]
        print(temp_results)
        return ListNetworksApiCallResult(True, None, results)
    except Exception as e:
        return ListNetworksApiCallResult(False, [str(e)], None)


def create_group(auth: Auth, group: Group) -> CreateGroupApiCallResult:
    """
    Create a Group
    """
    return create_groups(auth, [group])


def create_groups(auth: Auth, groups: List[Group]) -> CreateGroupApiCallResult:
    """
    Create a few Groups
    """

    url: str = f'{_BASE_URL}/v1/groups'
    errors: List[Err] = []
    results: List[CreateGroupResponse] = []
    for group in groups:
        payload = asdict(group)
        try:
            response: Dict = _post(url, auth, payload, 201)
            results.append(CreateGroupResponse(**response))
        except Exception as e:
            errors.append(str(e))
    return CreateGroupApiCallResult(len(errors) == 0, errors, results)


def delete_group(auth: Auth, group_id: str) -> ApiCallResultBase:
    return delete_groups(auth, [group_id])


def delete_groups(auth: Auth, group_ids: List[str]) -> ApiCallResultBase:
    return _do_delete(auth, group_ids, '{}/v1/groups/{}')


def _do_delete(auth: Auth, ids: List[str], url_template: str) -> ApiCallResultBase:
    errors: List[Err] = []
    for _id in ids:
        url: str = url_template.format(_BASE_URL, _id)
        try:
            _delete(url, auth)
        except Exception as e:
            errors.append(str(e))
    return ApiCallResultBase(len(errors) == 0, errors)


def _get(url: str, headers: Dict, expected_status_code: int = 200) -> List[Dict]:
    request: urllib.request.Request = urllib.request.Request(url=url, method='GET', headers=headers)
    response: http.client.HTTPResponse = urllib.request.urlopen(request)
    if response.getcode() != expected_status_code:
        reason: str = response.read()
        raise Exception(
            f'Expected status code: {expected_status_code}. Actual status code: {response.getcode()}. Reason: {reason}')
    else:
        return json.loads(response.read().decode('utf8'))


def _delete(url: str, headers: Dict, expected_status_code: int = 200) -> None:
    request: urllib.request.Request = urllib.request.Request(url=url, method='DELETE', headers=headers)
    response: http.client.HTTPResponse = urllib.request.urlopen(request)
    if response.getcode() != expected_status_code:
        reason: str = response.read()
        raise Exception(
            f'Expected status code: {expected_status_code}. Actual status code: {response.getcode()}. Reason: {reason}')


def _post(url: str, headers: Dict, payload: Dict, expected_status_code: int = 200) -> Dict:
    params: str = json.dumps(payload).encode('utf8')
    request: urllib.request.Request = urllib.request.Request(url, data=params, headers=headers)
    response: http.client.HTTPResponse = urllib.request.urlopen(request)
    if response.getcode() != expected_status_code:
        reason: str = response.read()
        raise Exception(
            f'Expected status code: {expected_status_code}. Actual status code: {response.getcode()}. Reason: {reason}')
    else:
        return json.loads(response.read().decode('utf8'))
