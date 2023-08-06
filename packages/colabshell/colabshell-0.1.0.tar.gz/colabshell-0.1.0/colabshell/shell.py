import os
import subprocess
from pyngrok import ngrok
from pgrok import pgrok
import sys
import platform
from urllib.request import urlopen
from http import HTTPStatus
import socket
import time
import tempfile
import secrets
import logging
from kafka_logger import init_kafka_logger, OutputLogger
import gdrivefs.config
from gdrivefs import oauth_authorize, gdfuse

logger = logging.getLogger(__name__)

TTYD_VERSION = "1.6.3"
CDN_URL_PREFIX = f"https://github.com/tsl0922/ttyd/releases/download/{TTYD_VERSION}/"

PLATFORMS = {
    "linux_x86_64_aarch64": CDN_URL_PREFIX + "ttyd.aarch64",
    "linux_x86_64_arm": CDN_URL_PREFIX + "ttyd.arm",
    "linux_i386": CDN_URL_PREFIX + "ttyd_linux.i686",
    "linux_x86_64": CDN_URL_PREFIX + "ttyd.x86_64"
}
DEFAULT_DOWNLOAD_TIMEOUT = 6
DEFAULT_RETRY_COUNT = 0
_print_progress_enabled = True


_BINARY_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'bin'))
_TTYD_BINARY = None
os.makedirs(_BINARY_DIR, exist_ok=True)


class TTydInstallError(Exception):
    """ TTYD Installer Exception """
    pass


class ColabShell:
    """Interactive shell env for google-colab/kaggle-notebook
    """

    def __init__(
        self,
        port=10001,
        subdomain=None,
        username=None,
        password=None,
        mount_drive=None,
        interactive=False,
        tunnel_backend='pgrok',
        logger_name="kafka.logger",
        settings_ini=None,

    ) -> None:
        global logger

        self.option_string = 'allow_other'
        self.tunnel_backend = tunnel_backend
        self.port = port
        self.username = username
        self.password = password
        self.mount_drive = mount_drive
        self.auth_storage_filepath = gdrivefs.config.DEFAULT_CREDENTIALS_FILEPATH
        self.subdomain = subdomain if subdomain else secrets.token_hex(4)

        # Set Kafka-Logger to redirect output to topic
        if settings_ini:
            logger = init_kafka_logger(logger_name, settings_ini)
        else:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.INFO)
            stdout_handler.setFormatter(logging.Formatter(
                "%(asctime)s %(name)-12s %(levelname)-8s %(message)s", "%Y-%m-%dT%H:%M:%S"
            ))
            logger.addHandler(stdout_handler)

        self.redirector = OutputLogger(logger)

        # Auth Google drive, interactive mode in notebook/shell env
        if self.mount_drive and interactive and platform.system().lower() == 'linux':
            self._handle_auth_url()
            authcode = input("Enter Auth code from your browser\n")

            self._auth_write(authcode)

        # Install TTYD Shell interface
        self._install_ttyd()

    def mount_gdrive(self):

        gdfuse.mount(
            auth_storage_filepath=self.auth_storage_filepath,
            mountpoint=self.mount_drive,
            debug=gdrivefs.config.IS_DEBUG,
            nothreads=gdrivefs.config.IS_DEBUG,
            option_string=self.option_string
        )

    def _get_url(self):
        # This won't actually be needed so set it to the default.
        gdfuse.set_auth_cache_filepath(self.auth_storage_filepath)

        oa = oauth_authorize.get_auth()
        return oa.step1_get_auth_url()

    def _handle_auth_url(self):
        url = self._get_url()

        with self.redirector:
            print(
                "To authorize FUSE to use your Google Drive account, visit the "
                "following URL to produce an authorization code:\n\n%s\n" % (url,)
            )

    def _auth_write(self, authcode):
        gdfuse.set_auth_cache_filepath(self.auth_storage_filepath)
        oa = oauth_authorize.get_auth()

        oa.step2_doexchange(authcode)
        with self.redirector:
            print("Authorization code recorded.")

    def _install_ttyd(self):
        """ Download and install ttyd in current directory

        Raises:
            TTydInstallError: Raise TTyd installer error incase unable to sucessfully install a binaries
        """
        assert platform.system().lower() not in ["windows", "cygwin"], "Windows platform not supported"
        global _TTYD_BINARY
        _paths = os.environ['PATH'].split(":")
        _paths.append(_BINARY_DIR)
        for path in _paths:
            if os.path.exists(path + os.sep + 'ttyd') and \
                    os.access(path + os.sep + 'ttyd', os.X_OK):
                _TTYD_BINARY = path + os.sep + 'ttyd'
                with self.redirector:
                    print(">>> ttyd binary already available >>> ")
                    return

        arch = "x86_64" if sys.maxsize > 2 ** 32 else "i386"
        if platform.uname()[4].startswith("arm") or \
                platform.uname()[4].startswith("aarch64"):
            arch += "_arm"
        system = platform.system().lower()

        if system == 'darwin':
            _cmd = "brew install ttyd"
            with subprocess.Popen(
                [_cmd], shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True,
            ) as proc, self.redirector:
                for line in proc.stdout:
                    print(line, end="")

            _TTYD_BINARY = "/usr/local/bin/ttyd"
            return

        plat = system + "_" + arch
        try:
            url = PLATFORMS[plat]
            with self.redirector:
                print("Platform to download: {}".format(plat))
        except KeyError:
            raise TTydInstallError("\"{}\" is not a supported platform".format(plat))

        try:
            download_path = self._download_ttyd(url)
            _TTYD_BINARY = os.path.realpath(_BINARY_DIR + os.sep + "ttyd")
            os.rename(download_path, _TTYD_BINARY)
            os.chmod(_TTYD_BINARY, int("777", 8))
        except Exception as e:
            raise TTydInstallError("An error occurred while installing ttyd from {}: {}".format(url, e))

    def _download_ttyd(self, url, retries=0, **kwargs):
        """
        Given the url download the ttyd binaries for the specific platform
        Args:
            url ([type]): [description]
            retries ([type], optional): [description]. Defaults to 0.

        Raises:
            e: [description]

        Returns:
            [type]: [description]
        """
        kwargs["timeout"] = kwargs.get("timeout", DEFAULT_DOWNLOAD_TIMEOUT)

        try:
            with self.redirector:
                self._print_progress("Downloading ttyd ...")
                print("Downloading ttyd from {} ...".format(url))

            local_filename = url.split("/")[-1]
            response = urlopen(url)

            status_code = response.getcode()

            if status_code != HTTPStatus.OK:
                with self.redirector:
                    print("Response status code: {}".format(status_code))
                    return None

            length = response.getheader("Content-Length")
            if length:
                length = int(length)
                chunk_size = max(4096, length // 100)
            else:
                chunk_size = 64 * 1024

            download_path = os.path.join(tempfile.gettempdir(), local_filename)
            with open(download_path, "wb") as f:
                size = 0
                while True:
                    buffer = response.read(chunk_size)
                    if not buffer:
                        break

                    f.write(buffer)
                    size += len(buffer)

                    if length:
                        percent_done = int((float(size) / float(length)) * 100)
                        self._print_progress("Downloading ttyd: {}%".format(percent_done))

            self._clear_progress()

            return download_path
        except socket.timeout as e:
            if retries < DEFAULT_RETRY_COUNT:
                time.sleep(0.5)
                return self._download_file(url, retries + 1, **kwargs)
            else:
                raise e

    def _print_progress(self, line):
        if _print_progress_enabled:
            sys.stdout.write("{}\r".format(line))
            sys.stdout.flush()

    def _clear_progress(self, spaces=100):
        if _print_progress_enabled:
            sys.stdout.write((" " * spaces) + "\r")
            sys.stdout.flush()

    def _start_ngrok_server(self):
        if self.authtoken:
            ngrok.set_auth_token(self.authtoken)
        active_tunnels = ngrok.get_tunnels()
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            ngrok.disconnect(public_url)
        url = ngrok.connect(addr=self.port, options={"bind_tls": True})
        return url

    def _start_pgrok_server(self):
        active_tunnels = pgrok.get_tunnels()
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            pgrok.disconnect(public_url)
        tunnel = pgrok.connect(addr=self.port, name=self.subdomain)
        return tunnel.public_url

    def run(self):
        with self.redirector:
            print(">>> Starting Tunnelling Sever >>>")
            if self.tunnel_backend == 'pgrok':
                url = self._start_pgrok_server()
            else:
                url = self._start_ngrok_server()
            print(f"Code Server can be accessed on: {url}")
        
        # TODO: GdriveFS only works for Linux now. Support for Mac will be added later
        if self.mount_drive and platform.system().lower() == 'linux':
            self.mount_gdrive()

        if self.username and self.password:
            _cmd = f"{_TTYD_BINARY} --credential {self.username}:{self.password} --port {self.port} /bin/bash"
        else:
            _cmd = f"{_TTYD_BINARY} --port {self.port} /bin/bash"

        with subprocess.Popen([_cmd],
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True,
                              ) as proc, self.redirector:
            for line in proc.stdout:
                print(line, end="")
