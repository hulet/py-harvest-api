# Python's Client for Harvest API

## Build

`make build`

## Setup

`pip install harvest_api`

## Usage

### API Endpoints

_Note: that all the api objects will always return an "Response" object from
requests library_

- Getting current authenticated User profile

```
from harvest.credential import PersonalAccessAuthCredential
from harvest.api import UsersMeEndpoint

credential = PersonalAccessAuthCredential(
    personal_token='xyz',
    account_id='123',
)

resp = UsersMeEndpoint(credential).get()

print(resp.status_code)
print(resp.json())
```

- Querying time entries from two days range

```
from harvest.credential import PersonalAccessAuthCredential
from harvest.api import TimeEntryEndpoint

credential = PersonalAccessAuthCredential(
    personal_token='xyz',
    account_id='123',
)

resp = TimeEntryEndpoint(credential).get(params={
    'from': '1972-01-01',
    'to': '1972-01-02',
})

print(resp.status_code)
print(resp.json())
```

### Services (Common Routines)

On services the return is a dictionary

- Querying today's time entries

```
from harvest.credential import PersonalAccessAuthCredential
from harvest.services import TodayTimeEntries

credential = PersonalAccessAuthCredential(
    personal_token='xyz',
    account_id='123',
)

resp = TodayTimeEntries(credential).get()

print(resp)
```

## Credentials

Normally you will use `PersonalAccessAuthCredential` or `OAuth2Credential` for
your project.

But for Personal Access flow two helper classes were added:

- PersonalAccessAuthConfigCredential
- PersonalAccessAuthEnvCredential

They're only here to help on the early stage of the developing process of other
tools using this lib. _(way easier then managing OAuth2 whole flow. Especially
for CLI projects)_

If you pick up `PersonalAccessAuthConfigCredential` then create a `harvest.cfg`
with:

```
[authentication]
token=(\w|\.\-)+
account_id=[0-9]+
```

[This](https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/#personal-access-tokens)
is how you can get the `token` and `account_id`

## Tests

`make tests`

## License

MIT License

Copyright (c) 2019 Ramon Moraes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
