from aifactory_alpha.constants import *
from Cryptodome import Random
from Cryptodome.Cipher import AES
from random import random
from hashlib import blake2b
import json
import requests
import http
import time

BLOCK_SIZE=16

class AFAuth():
    refresh_token = None
    auth_token = None
    def __init__(self, user_email, task_id, logger, token=None,
                 password=None, auth_method=AUTH_METHOD.USERINFO, encrypt_mode=True,
                 auth_url=AUTH_DEFAULT_URL, debug=False):
        self.user_email = user_email
        self.task_id = task_id
        self.logger = logger
        self.refresh_token = token
        self.auth_method = auth_method
        self.encrypt_mode = int(encrypt_mode)
        self.auth_url = auth_url
        self.debug = debug
        if auth_method==AUTH_METHOD.TOKEN:
            if debug:
                token = DEBUGGING_PARAMETERS.TOKEN
            self.set_token(token)
            raise(AuthMethodNotAvailableError)
        elif auth_method==AUTH_METHOD.USERINFO:
            pass
        else:
            raise(WrongAuthMethodError)
        if encrypt_mode:
            self.crypt = AFCrypto()

    def set_user_email(self, email: str):
        self.user_email = email

    def set_task_id(self, task_id: int):
        self.task_id = task_id

    def set_token(self, token=None, yes=False):
        token_in_env_var = os.getenv('AF_REFRESH_TOKEN')
        if token_in_env_var is not None:
            if token is not None and (token_in_env_var != token):
                if not yes:
                    print("It will replace your token in the environment variable `AF_REFRESH_TOKEN`.")
                    res = input("Do you want to proceed? [Y/N] - default: Y")
                    if res == 'N':
                        print("Using token from the environment variable `AF_REFRESH_TOKEN`.")
                        token = token_in_env_var
                else:
                    token = token_in_env_var
        self.user_token = user_token

    def _investigate_validation_(self):
        res = []
        if self.auth_method == AUTH_METHOD.TOKEN:
            if self.refresh_token is None:
                res.append(RefreshTokenNotFoundError)
        elif self.auth_method == AUTH_METHOD.USERINFO:
            if self.user_email is None:
                res.append(UserInfoNotDefinedError)
            if self.task_id is None:
                res.append(TaskIDNotDefinedError)
        else:
            res = res.append(WrongAuthMethodError)
        for r in res:
            self.logger.error(r.ment)
        return res

    def _require_password_(self):
        password = None
        if self.debug:
            password = DEBUGGING_PARAMETERS.PASSWORD
        else:
            password = input("Please put your password: ")
        password = self.crypt.encrypt_hash(password)
        for _ in range(AUTH_METHOD.NUM_KEY_STRETCHING):
            password = self.crypt.encrypt_hash(password)
        return password

    def _is_token_valid_(self):
        return False

    def pack_user_info(self, params: dict):
        hashed_password = self._require_password_()
        if self.encrypt_mode:
            hashed_password = self.crypt.encrypt_aes(hashed_password, self.user_email)
        params['password'] = hashed_password
        params['password_encrypted'] = self.encrypt_mode
        return params

    def pack_refresh_token(self, params: dict):
        if self.encrypt_mode:
            refresh_token = self.crypt.encrypt_aes(self.refresh_token, self.user_email)
        params['refresh_token'] = refresh_token
        params['refresh_token_encrypted'] = self.encrypt_mode
        return params

    def get_token(self, num_trial=0, refresh=False):
        if refresh: self.auth_token = None
        if self.auth_token is not None: return self.auth_token

        res = self._investigate_validation_()
        if len(res) != 0:
            return False

        params = {'auth_method': self.auth_method, 'version': VERSION,
                  'task_id': self.task_id, 'user_email': self.user_email}
        if self.auth_method == AUTH_METHOD.USERINFO or self.refresh_token is None:
            params = self.pack_user_info(params)
        elif self.auth_method == AUTH_METHOD.TOKEN and self.refresh_token is not None:
            params = self.pack_refresh_token(params)

        response = requests.get(self.auth_url+'/submit_token', params=params)
        self.logger.info('Response from auth server: {}'.format(response.text))

        if response.text in [AUTH_RESPONSE.TOKEN_EXPIRED, AUTH_RESPONSE.TOKEN_NOT_VALID]:
            self.refresh_token = None
            self.auth_method = AUTH_METHOD.USERINFO
            self.logger.info("Refresh token not valid. We need your password to issue a new one.")
            return self.get_token(num_trial)
        elif response.text == AUTH_RESPONSE.USER_NOT_PARTICIPATING:  # if the user hasn't registered in the task.
            self.logger.error(UserNotRegisteredError.ment)
            raise(UserNotRegisteredError)
        elif response.text == AUTH_RESPONSE.NO_AVAILABLE_LAP:  # if there isn't any lap to submit the result.
            self.logger.error(TaskIDNotAvailableError.ment)
            raise(TaskIDNotAvailableError)
        elif response.text == AUTH_RESPONSE.DB_NOT_AVAILABLE:  # if the system has a problem.
            self.logger.error(AuthServerError.ment)
            raise(AuthServerError)
        elif response.text in [AUTH_RESPONSE.USER_NOT_EXIST, AUTH_RESPONSE.PASSWORD_NOT_VALID]:
            # if the user information was wrong
            if num_trial > AUTH_METHOD.MAX_TRIAL:
                return False
            self.logger.info('Authentification failed. Please check your user info and try again.')
            self.logger.info(self.summary())
            self.logger.info('Please check you have the right password and email that you use to log-in the AI Factory Website.')
            time.sleep(1)
            return self.get_token(num_trial + 1)
        elif response.text == AUTH_RESPONSE.VERSION_NOT_VALID:
            self.logger.info("Authentification failed. \nPlease check if you have the right version.")
            self.logger.info("Try installing the updated version of aifactory-alpha.")
        elif response.status_code == http.HTTPStatus.OK:
            tokens = json.loads(response.text)
            self.auth_token = self.crypt.decrypt_aes(tokens['token'], self.user_email)
            if self.auth_method == AUTH_METHOD.USERINFO:
                self.refresh_token = self.crypt.decrypt_aes(tokens['refresh_token'], self.user_email)
                self.auth_method = AUTH_METHOD.TOKEN
            self.logger.info('Authentification process success.')
            return self.auth_token
        return False

    def summary(self):
        _summary_ = ">>> User Authentification Info <<<\n"
        _summary_ += "Authentification Method:"
        if self.auth_method is AUTH_METHOD.TOKEN:
            _summary_ += "Token \n"
            _summary_ += "    Token: {} \n".format(self.refresh_token)
        elif self.auth_method is AUTH_METHOD.USERINFO:
            _summary_ += "User Information \n"
            _summary_ += "    Task ID: {}\n".format(self.task_id)
            _summary_ += "    User e-mail: {}\n".format(self.user_email)
        return _summary_


class AFCrypto():
    LENGTH_PREFIX = 6
    def __init__(self):
        self.iv = bytes([0x00] * 16) #pycryptodomex 기준

    def encrypt_aes(self, data: str, key: str):
        key += '0'*(16 - (len(key) % 16))
        key = key.encode()
        crypto = AES.new(key, AES.MODE_CBC, self.iv)
        len_data = str(len(data))
        data = len_data.zfill(6) + data
        while len(data) % 16 != 0:
            data += str(int(random()))
        data = data.encode()
        enc = crypto.encrypt(data)
        del crypto
        return enc.hex()

    def decrypt_aes(self, enc: str, key: str):
        key += '0'*(16 - (len(key) % 16))
        key = key.encode()
        crypto = AES.new(key, AES.MODE_CBC, self.iv)
        enc = bytes.fromhex(enc)
        dec = crypto.decrypt(enc).decode()
        len_dec = int(dec[:self.LENGTH_PREFIX])
        dec = dec[self.LENGTH_PREFIX:self.LENGTH_PREFIX+len_dec]
        del crypto
        return dec

    def zero_salting(self, data: str):
        data += '0'*(AUTH_METHOD.SALTED_LENGTH - len(data))
        return data

    def encrypt_hash(self, data: str, zero_salting=True, salt=None):
        if zero_salting:
            data = self.zero_salting(data)
        elif salt is not None:
            data += salt
        return blake2b(data.encode()).hexdigest()


if __name__ == "__main__":
    a = AFCrypto()
    target = "The key is how I think of you."
    sample_key = 'i_love_you_:)'
    print("Target pattern to encrypt: %s" % target)
    print("A key for encryption: %s" % sample_key)
    b = a.encrypt_aes(target, sample_key)
    print("Encrypted Message: %s" % b)
    c = a.decrypt_aes(b, sample_key)
    print("Decrypted Message: %s" % c)
