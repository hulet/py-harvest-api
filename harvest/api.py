import requests
from harvest import logger


class Endpoint(object):
    def __init__(self, credential, *args, **kwargs):
        self.credential = credential
        self.path_vars = kwargs

    def get_domain(self):
        return self.domain

    def get_path(self):
        if self.path_vars:
            return self.path.format(**self.path_vars)
        return self.path

    def get_url(self):
        return "{}{}".format(self.get_domain(), self.get_path())

    def get_headers(self):
        return self.headers or {}

    def get(self, *args, **kwargs):
        return self.request("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("post", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request("patch", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("delete", *args, **kwargs)

    def request(self, http_method, *args, **kwargs):
        verb = http_method
        url = self.get_url()
        params = self.credential.get_params()
        params.update(kwargs.get("params", {}))
        headers = self.credential.get_headers()
        headers.update(kwargs.get("headers", {}))
        data = kwargs.get("data", {})
        logger.debug("HTTP - {} - Request - URL {}".format(verb, url))
        logger.debug("HTTP - {} - Request - Params ".format(verb, params))
        logger.debug("HTTP - {} - Request - Headers {}".format(verb, headers))
        fn = getattr(requests, verb)
        if data:
            resp = fn(url=url, headers=headers, params=params, data=data,)
        else:
            resp = fn(url=url, headers=headers, params=params,)
        logger.debug(
            "HTTP - {} - Response - status code - {}".format(
                verb, resp.status_code
                )
        )
        logger.debug(
            "HTTP - {} - Response - content - {}".format(verb, resp.content)
        )
        return resp


class OAuth2Endpoint(Endpoint):

    domain = "https://id.getharvest.com"


class OAuth2AccessTokenEndpoint(OAuth2Endpoint):

    """
    Request:
        POST (exchange authorization code):
            code=$AUTHORIZATION_CODE"
            client_id=$CLIENT_ID"
            client_secret=$CLIENT_SECRET"
            grant_type=authorization_code"

        POST (refresh token):
            "refresh_token=$REFRESH_TOKEN"
            "client_id=$CLIENT_ID"
            "client_secret=$CLIENT_SECRET"
            "grant_type=refresh_token"

    Response:
        POST:
            {
              "access_token":  "{ACCESS_TOKEN}",
              "refresh_token": "{REFRESH_TOKEN}",
              "token_type":    "bearer",
              "expires_in":    1209600
            }
    """

    path = "/api/v2/oauth2/token"

    def post(self, *args, **kwargs):
        if kwargs.get("grant_type") == "refresh_token":
            self.headers.update({"Accept": "application/json"})
        super(OAuth2AccessTokenEndpoint, self).post(*args, **kwargs)


class ApiEndpoint(Endpoint):

    domain = "https://api.harvestapp.com/v2"
    headers = {
        "Accept": "application/json",
    }


class UsersEndpoint(ApiEndpoint):

    path = "/users"


class UsersMeEndpoint(ApiEndpoint):

    """
    Entity:
        {
            "id":1782884,
            "first_name":"Bob",
            "last_name":"Powell",
            "email":"bobpowell@example.com",
            "telephone":"",
            "timezone":"Mountain Time (US & Canada)",
            "has_access_to_all_future_projects":false,
            "is_contractor":false,
            "is_admin":true,
            "is_project_manager":false,
            "can_see_rates":true,
            "can_create_projects":true,
            "can_create_invoices":true,
            "is_active":true,
            "created_at":"2017-06-26T20:41:00Z",
            "updated_at":"2017-06-26T20:42:25Z",
            "weekly_capacity":126000,
            "default_hourly_rate":100.0,
            "cost_rate":75.0,
            "roles":["Founder", "CEO"],
            "avatar_url":"https://cache.harvestapp.com/assets/profile_images/allen_bradley_clock_tower.png?1498509661"
        }
    HTTP Methods:
        GET:
    """

    path = "/users/me"


class UsersAssignmentsEndpoint(ApiEndpoint):

    path = "/users/{user_id}/project_assignments"


class ProjectsEndpoint(ApiEndpoint):

    path = "/projects"


class TasksEndpoint(ApiEndpoint):

    path = "/tasks"

    """
    Entity:
        {
          "id":8083800,
          "name":"Business Development",
          "billable_by_default":false,
          "default_hourly_rate":0.0,
          "is_default":false,
          "is_active":true,
          "created_at":"2017-06-26T22:08:25Z",
          "updated_at":"2017-06-26T22:08:25Z"
        }

    HTTP Methods:
        GET:
            is_active (boolean):
                Pass true to only return active tasks and false to return
                inactive tasks.
            updated_since (datetime):
                Only return tasks that have been updated since the given date
                and time.
            page (integer):
                The page number to use in pagination. For instance, if you
                make a list request and receive 100 records, your subsequent
                call can include page=2 to retrieve the next page of the list.
                (Default: 1)
            per_page (integer):
                The number of records to return per page. Can range between 1
                and 100. (Default: 100)

        POST:
    """


class TimeEntryEndpoint(ApiEndpoint):

    path = "/time_entries"

    """
    HTTP Methods:
        GET:
            user_id (integer):
                Only return time entries belonging to the user with the
                given ID.
            client_id (integer):
                Only return time entries belonging to the client with the
                given ID.
            project_id (integer):
                Only return time entries belonging to the project with the
                given ID.
            is_billed (str):
                Pass "true" to only return time entries that have been invoiced
                and "false" to return time entries that have not been invoiced.
            is_running (str):
                Pass "true" to only return running time entries and "false" to
                return non-running time entries.
            updated_since (datetime str):
                Only return time entries that have been updated since the given
                date and time.
            from (date str):
                Only return time entries with a spent_date on or after the
                given date.
            to (date str):
                Only return time entries with a spent_date on or before the
                given date.
            page (integer):
                The page number to use in pagination. For instance, if you make
                a list request and receive 100 records, your subsequent call
                can include page=2 to retrieve the next page of the list.
                (Default: 1)
            per_page (integer):
                The number of records to return per page. Can range between
                1 and 100. (Default: 100)
        POST:
            user_id (integer / optional):
                The ID of the user to associate with the time entry. Defaults
                to the currently authenticated user's ID.
            project_id  (integer / required):
                The ID of the project to associate with the time entry.
            task_id (integer / required):
                The ID of the task to associate with the time entry.
            spent_date (date / required):
                The ISO 8601 formatted date the time entry was spent.
            hours (decimal / optional):
                The current amount of time tracked. If provided, the time entry
                will be created with the specified hours and is_running will be
                set to false. If not provided, hours will be set to 0.0 and
                is_running will be set to true.
            notes (string / optional):
                Any notes to be associated with the time entry.
            external_reference (object / optional):
                An object containing the id, group_id, and permalink of the
                external reference.
    """


class TimeEntryUpdateEndpoint(ApiEndpoint):

    path = "/time_entries/{time_entry_id}"

    """
    HTTP Methods:
        PATCH:
            user_id (integer / optional):
                The ID of the user to associate with the time entry. Defaults
                to the currently authenticated user's ID.
            project_id  (integer / required):
                The ID of the project to associate with the time entry.
            task_id (integer / required):
                The ID of the task to associate with the time entry.
            spent_date (date / required):
                The ISO 8601 formatted date the time entry was spent.
            hours (decimal / optional):
                The current amount of time tracked. If provided, the time entry
                will be created with the specified hours and is_running will be
                set to false. If not provided, hours will be set to 0.0 and
                is_running will be set to true.
            notes (string / optional):
                Any notes to be associated with the time entry.
            external_reference (object / optional):
                An object containing the id, group_id, and permalink of the
                external reference.
    """


class TimeEntryStopEndpoint(ApiEndpoint):

    path = "/time_entries/{time_entry_id}/stop"

    """
    HTTP Methods:
        PATCH:
            user_id (integer / optional):
                The ID of the user to associate with the time entry. Defaults
                to the currently authenticated user's ID.
            project_id  (integer / required):
                The ID of the project to associate with the time entry.
            task_id (integer / required):
                The ID of the task to associate with the time entry.
            spent_date (date / required):
                The ISO 8601 formatted date the time entry was spent.
            hours (decimal / optional):
                The current amount of time tracked. If provided, the time entry
                will be created with the specified hours and is_running will be
                set to false. If not provided, hours will be set to 0.0 and
                is_running will be set to true.
            notes (string / optional):
                Any notes to be associated with the time entry.
            external_reference (object / optional):
                An object containing the id, group_id, and permalink of the
                external reference.
    """


class TimeEntryRestartEndpoint(ApiEndpoint):

    path = "/time_entries/{time_entry_id}/restart"

    """
    HTTP Methods:
        PATCH:
            user_id (integer / optional):
                The ID of the user to associate with the time entry. Defaults
                to the currently authenticated user's ID.
            project_id  (integer / required):
                The ID of the project to associate with the time entry.
            task_id (integer / required):
                The ID of the task to associate with the time entry.
            spent_date (date / required):
                The ISO 8601 formatted date the time entry was spent.
            hours (decimal / optional):
                The current amount of time tracked. If provided, the time entry
                will be created with the specified hours and is_running will be
                set to false. If not provided, hours will be set to 0.0 and
                is_running will be set to true.
            notes (string / optional):
                Any notes to be associated with the time entry.
            external_reference (object / optional):
                An object containing the id, group_id, and permalink of the
                external reference.
    """
