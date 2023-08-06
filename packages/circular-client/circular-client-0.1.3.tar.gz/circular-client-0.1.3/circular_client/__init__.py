__version__ = '0.1.0'

import requests
import json
from datetime import datetime

class CircularApiError(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

class CircularClient:

    def __init__(self, endpoint, key=None):
        self.endpoint = endpoint
        self.key      = key

    # Helpers
    def _proccess_response(self, res):
        ok  = res.status_code == 200
        data = res.json()
        if not ok: raise CircularApiError(data)
        return data

    def _get_headers(self, key_required=False):
        headers = {}
        if key_required and not self.key:
            raise CircularApiError('admin key required')
        if self.key:
            headers.update({'Authorization':'Bearer {0}'.format(self.key)})
        return headers

    # Public interface
    def create_project(self, name, maximum_supply, type_, flags, logo, description, website, email, style, symbol_glyph, enable_signup, signup_needs_approval, signup_model):
        res = requests.post('{0}/v1/project'.format(self.endpoint),
            json={
                'community' : {
                    'name'        : name, 
                    'description' : description,
                    'logo'        : logo,
                    'website'     : website,
                    'email'       : email
                },
                "currency" : {
                    "type"           : type_,
                    "flags"          : flags,
                    "maximum_supply" : maximum_supply
                },
                "users" : {
                    'enabled'        : enable_signup,
                    'schema'         : signup_model,
                    'needs_approval' : signup_needs_approval
                }
            },
            headers=self._get_headers(True)
        )

        return self._proccess_response(res)

    def edit_project(self, symbol, params):
        res = requests.post('{0}/v1/project/{1}'.format(self.endpoint, symbol),
            json=params,
            headers=self._get_headers(True)
        )

        return self._proccess_response(res)

    def get_projects(self):
        res = requests.get(
            '{0}/v1/project'.format(self.endpoint),
            headers=self._get_headers()
        )
        return self._proccess_response(res)

    def get_project(self, symbol):
        res = requests.get(
            '{0}/v1/project/{1}'.format(self.endpoint, symbol),
            headers=self._get_headers()
        )
        return self._proccess_response(res)

    def get_activity(self, symbol, type_='all', limit=10):
        res = requests.get(
            '{0}/v1/project/{1}/activity?type={2}&limit={3}'.format(self.endpoint, symbol, type_, limit),
            headers=self._get_headers()
        )
        return self._proccess_response(res)

    def get_account_activity(self, symbol, account, type_='all', limit=10):
        res = requests.get(
            '{0}/v1/project/{1}/users/{2}/activity?type={3}&limit={4}'.format(self.endpoint, symbol, account, type_, limit),
            headers=self._get_headers()
        )
        return self._proccess_response(res)

    def get_users(self, symbol):
        res = requests.get(
            '{0}/v1/project/{1}/users'.format(self.endpoint, symbol),
            headers=self._get_headers()
        )
        return self._proccess_response(res)

    def set_user_prop(self, symbol, account_name, account_type, prop_name, prop_value):
        res = requests.post(
            '{0}/v1/project/{1}/users/{2}/props?account_type={3}'.format(self.endpoint, symbol, account_name, account_type),
            json={
                'name'     : prop_name,
                'value'    : int(prop_value)
            },
            headers=self._get_headers(True)
        )
        return self._proccess_response(res)

    # Token
    def issue(self, symbol, to, amount, memo, account_type):
        res = requests.post(
            '{0}/v1/project/{1}/issue'.format(self.endpoint, symbol),
            json={
                'to'           : to,
                'amount'       : amount,
                'memo'         : memo,
                'account_type' : account_type
            },
            headers=self._get_headers(True)
        )
        return self._proccess_response(res)

    def burn(self, symbol, amount, memo, from_=None, signature=None):
        res = requests.post(
            '{0}/v1/project/{1}/burn'.format(self.endpoint, symbol),
            json={
                'amount'    : amount,
                'memo'      : memo,
                'from'      : from_,
                'signature' : signature,
            },
            headers=self._get_headers(True)
        )
        return self._proccess_response(res)

    def transfer(self, symbol, from_, to, amount, memo, account_type, signature):
        res = requests.post(
            '{0}/v1/project/{1}/transfer'.format(self.endpoint, symbol),
            json={
                'from'         : from_,
                'to'           : to,
                'amount'       : amount,
                'memo'         : memo,
                'account_type' : account_type,
                'signature'    : signature
            }
        )
        return self._proccess_response(res)

    def changekey(self, symbol, account, pubkey, signature):
        res = requests.post(
            '{0}/v1/project/{1}/users/{2}/changekey'.format(self.endpoint, symbol, account),
            json={
                'account'      : account,
                'pubkey'       : pubkey,
                'signature'    : signature
            },
            headers=self._get_headers()
        )
        return self._proccess_response(res)

    # Users
    def signup(self, symbol, pubkey, account_name, data, client_id, encrypted_json, skip_validation, as_admin=False):
        res = requests.post(
            '{0}/v1/project/{1}/users'.format(self.endpoint, symbol),
            json={
                'pubkey'          : pubkey,
                'account_name'    : account_name,
                'data'            : data,
                'client_id'       : client_id,
                'encrypted_json'  : encrypted_json,
                'skip_validation' : skip_validation
            },
            headers=self._get_headers(as_admin)
        )
        return self._proccess_response(res)

    def confirm(self, symbol, challenge, otp):
        res = requests.post(
            '{0}/v1/project/{1}/users/confirm'.format(self.endpoint, symbol),
            json={
                'challenge' : challenge,
                'otp'       : int(otp)
            }
        )
        return self._proccess_response(res)

    def approve(self, symbol, account_name):
        res = requests.post(
            '{0}/v1/project/{1}/users/approve'.format(self.endpoint, symbol),
            json={
                'account_name' : account_name,
            },
            headers=self._get_headers(True)
        )
        return self._proccess_response(res)


    def retry(self, symbol, challenge):
        res = requests.post(
            '{0}/v1/project/{1}/users/retry'.format(self.endpoint, symbol),
            json={
                'challenge' : challenge
            }
        )
        return self._proccess_response(res)

    def get_user(self, symbol, account_name, sig_generator=None):
        path = '/v1/project/{0}/users/{1}'.format(symbol, account_name)
        headers = self._get_headers()

        if sig_generator is not None:
            ts = datetime.utcnow().strftime('%s')
            sig = sig_generator(path, ts)
            extra_headers = {
                'x-circular-signature' : sig,
                'x-circular-timestamp' : ts
            }
            headers.update(extra_headers)

        res = requests.get(
            '{0}{1}'.format(self.endpoint, path),
            headers=headers
        )
        return self._proccess_response(res)

    def get_wallet(self, wallet_id):
        res = requests.get(
            '{0}/v1/auth/wallet/{1}'.format(self.endpoint, wallet_id),
        )
        return self._proccess_response(res)

