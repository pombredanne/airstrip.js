from keyring.backend import KeyringBackend
from keyring.errors import PasswordSetError
from keyring.errors import PasswordDeleteError

import sys
import subprocess
import re
import binascii


class OSXPatchedKeyring(KeyringBackend):
    """Mac OS X extended Keychain"""

    # regex for extracting password from security call
    password_regex = re.compile("""password:\s*(?:0x(?P<hex>[0-9A-F]+)\s*)?"""
                                """(?:"(?P<pw>.*)")?""")

    def supported(self):
        """Recommended for all OSX environment.
        """
        return sys.platform == 'darwin' or -1

    @staticmethod
    def set_password(service, username, password):
        if username is None:
            username = ''
        try:
            # set up the call for security.
            call = subprocess.Popen([
                    'security',
                    'add-generic-password',
                    '-a',
                    username,
                    '-s',
                    service,
                    '-w',
                    password,
                    '-U'
                ],
                stderr = subprocess.PIPE,
                stdout = subprocess.PIPE,
            )
            stdoutdata, stderrdata = call.communicate()
            code = call.returncode
            # check return code.
            if code is not 0:
                raise PasswordSetError('Can\'t store password in keychain')
        except:
            raise PasswordSetError("Can't store password in keychain")

    @staticmethod
    def get_password(service, username):
        if username is None:
            username = ''

        try:
            call = subprocess.Popen([
                    'security',
                    'find-internet-password',
                    '-g',
                    '-a',
                    'dmp42',
                    '-s',
                    'github.com'
                ],
                stderr = subprocess.PIPE,
                stdout = subprocess.PIPE,
            )
            stdoutdata, stderrdata = call.communicate()
            code = call.returncode

            if code is not 0:
                raise OSError("Can't fetch internet password from system")
            output = stderrdata.decode()

            if output == 'password: \n':
                return ''
            # search for special password pattern.
            matches = OSXPatchedKeyring.password_regex.search(output)
            if matches:
                group_dict = matches.groupdict()
                hex = group_dict.get('hex')
                pw = group_dict.get('pw')
                if hex:
                    # it's a weird hex password, decode it.
                    return unicode(binascii.unhexlify(hex), 'utf-8')
                else:
                    # it's a normal password, send it back.
                    return pw
            # nothing was found, it doesn't exist.
            return None
        except:
            return None
        # finally:
        #     call.kill()

    @staticmethod
    def delete_password(service, username):
        if username is None:
            username = ''
        try:
            # set up the call for security.
            call = subprocess.Popen([
                    'security',
                    'delete-generic-password',
                    '-a',
                    username,
                    '-s',
                    service
                ],
                stderr = subprocess.PIPE,
                stdout = subprocess.PIPE
            )
            stdoutdata, stderrdata = call.communicate()
            code = call.returncode
            # check return code.
            if code is not 0:
                raise PasswordDeleteError('Can\'t delete password in keychain')
        except:
            raise PasswordDeleteError("Can't delete password in keychain")

