import csv
import json
import logging
import os
from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from typing import List, Text, Optional, Tuple, Dict
import urllib.parse

import requests
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join
from pkg_resources import parse_version

# noinspection PyProtectedMember
from pkg_resources._vendor.packaging.version import Version
from tornado.httputil import HTTPServerRequest

import jupyter_cogram

debug_mode = os.environ.get("DEBUG_MODE", "false") == "true"

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)

logger: logging.Logger = logging.getLogger(__name__)

backend_url = os.environ.get("BACKEND_URL", "https://api.cogram.ai")
completions_enpdoint = os.environ.get("SUGGESTIONS_ENDPOINT", "completions")
package_pypi_url = "https://pypi.org/pypi/jupyter-cogram/json"
demo_mode = os.environ.get("DEMO_MODE", "false") == "true"

check_token_endpoint = "checkToken"

logger.debug(f"Running jupyter-cogram version {jupyter_cogram.__version__}")
logger.debug(f"Backend URL: {backend_url}")
logger.debug(f"Suggestions endpoint: {completions_enpdoint}")
logger.debug(f"PyPI URL: {package_pypi_url}")

config_location = Path().home() / ".ipython/nbextensions/jupyter-cogram"
token_file_name = "cogram_auth_token"
log_file_name = "cogram_access_log"
config_file = "cogram_config.json"

suggestions_timeout = float(os.environ.get("SUGGESTIONS_TIMEOUT", "10.0"))

LATEST_PYPI_VERSION: Optional[Text] = None


def read_csv(
    p: Path = config_location / log_file_name,
) -> Optional[List[Tuple[Text, Text]]]:
    if not p.is_file():
        logger.debug(f"'{p}' is not a file. Cannot read CSV.")
        return None

    out = []
    with p.open() as f:
        reader = csv.reader(f)
        for row in reader:
            k, v = row
            out.append((k, v))

    logger.debug(f"Successfully read CSV with {len(out)} entries.")
    return out


def create_log_file() -> None:
    p = config_location.absolute() / log_file_name
    if not p.is_file():
        logger.info(f"Touching file '{p}'")
        p.touch()


def append_to_log_file() -> None:
    line = f"{datetime.now().isoformat()},{jupyter_cogram.__version__}"

    logger.info(f"Appending to log file '{line}'")
    create_log_file()

    p = config_location.absolute() / log_file_name

    content = p.read_text()

    with p.open("a") as f:
        if not content:
            to_write = line
        else:
            to_write = f"\n{line}"

        f.write(to_write)


def save_token(token: Text, loc: Path = config_location) -> None:
    loc = loc.absolute()

    if not loc.is_dir():
        loc.mkdir(parents=True)

    p = loc / token_file_name

    logger.debug(f"Saving token '{token}' at path '{p}'.")
    p.write_text(token)


def read_config() -> Dict:
    p = config_location / config_file
    if p.is_file():
        with p.open() as f:
            return json.load(f)
    return {}


def save_config(d: Dict, loc: Path = config_location) -> None:
    loc = loc.absolute()

    if not loc.is_dir():
        loc.mkdir(parents=True)

    p = loc / config_file

    logger.debug(f"Saving config '{d}' at path '{p}'.")
    with p.open("w") as f:
        json.dump(d, f, indent=2)


def merge_configs(d: Dict) -> Dict:
    _config = read_config()
    _config.update(**d)
    return _config


def fetch_token(loc: Path = config_location) -> Optional[Text]:
    loc = loc.absolute()
    fname = loc / token_file_name
    logger.debug(f"Checking for token at {fname}")
    if not fname.is_file():
        return None

    return fname.read_text().strip()


def post_auth_token(token: Text, log_launch: bool = False) -> requests.Response:
    url = urllib.parse.urljoin(backend_url, check_token_endpoint)
    logger.debug(f"Posting auth token to {url}. Token: {token}")
    return requests.post(
        url,
        json={
            "auth_token": token,
            "version": jupyter_cogram.__version__,
            "log_launch": log_launch,
        },
    )


def is_installation_up_to_date(
    pypi_url: Text = package_pypi_url,
) -> bool:
    logger.info("Checking if local installation is up to date.")

    try:
        res = requests.get(pypi_url, timeout=2)
    except Exception as e:
        logger.exception(e)
        return True

    if res.status_code != 200:
        # we don't know, so let's return `True`
        return True

    global LATEST_PYPI_VERSION
    LATEST_PYPI_VERSION = res.json().get("info", {}).get("version")
    if not LATEST_PYPI_VERSION:
        # no version returned
        logger.debug("Could not find latest pypi version.")
        return True

    try:
        is_up_to_date = parse_version(jupyter_cogram.__version__) >= parse_version(
            LATEST_PYPI_VERSION
        )
        logger.info(
            f"Have package version {jupyter_cogram.__version__}. "
            f"Latest PyPi version is {LATEST_PYPI_VERSION}. Installed version is up to "
            f"date: {is_up_to_date}."
        )
        return is_up_to_date
    except ValueError as e:
        logger.exception(e)
        return False


def fetch_suggestion_code(
    queries,
    cell_contents: Optional[List[Text]] = None,
    auth_token: Optional[Text] = None,
    temperature: float = 0.2,
    n_suggestions: int = 3,
    prompt_presets: Text = "",
    language: Text = "python",
):
    url = urllib.parse.urljoin(backend_url, completions_enpdoint)

    logger.debug(f"Fetching code for query: {queries}")
    try:
        res = requests.post(
            url,
            json={
                "queries": queries,
                "cell_contents": cell_contents or [],
                "auth_token": auth_token,
                "temperature": temperature,
                "n_suggestions": n_suggestions,
                "prompt_presets": prompt_presets,
                "language": language,
            },
            # retries=1,
        )

        if res.status_code >= 400:
            if res.json() and res.json().get("error") is not None:
                msg = res.json()["error"]
            else:
                msg = res.text

            error_dict = {
                "status": "error",
                "error_msg": msg,
                "status_code": res.status_code,
            }

            raise ValueError(json.dumps(error_dict))

        return res.json()
    except requests.exceptions.Timeout:
        logger.error("Have Timeout")
        error_dict = {
            "status": "error",
            "error_msg": "Request timed out",
            "status_code": HTTPStatus.REQUEST_TIMEOUT,
        }
        logger.debug(f"Submitting error dict {json.dumps(error_dict)}")
        raise ValueError(json.dumps(error_dict))


def bool_arg(request: HTTPServerRequest, name: Text, default: bool = False) -> bool:
    args = request.query_arguments.get(name, [])
    if not args:
        return default

    arg = args[0]

    if isinstance(arg, (bytes, bytearray)):
        arg = arg.decode()

    return arg.lower() == "true"


class JupyterCogramHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramHandler, self).__init__(application, request, **kwargs)

    def post(self):
        data = json.loads(self.request.body)
        queries = data.get("queries", "")
        cell_contents = data.get("cell_contents", [])
        auth_token = data.get("auth_token", "'")
        temperature = float(data.get("temperature", "0.2"))
        n_suggestions = int(data.get("n_suggestions", "3"))
        prompt_presets = data.get("prompt_presets", "")
        language = data.get("language", "python")

        try:
            logger.debug("Submitting to API server")
            suggestions = fetch_suggestion_code(
                queries,
                cell_contents,
                auth_token,
                temperature=temperature,
                n_suggestions=n_suggestions,
                prompt_presets=prompt_presets,
                language=language,
            )

            logger.debug(f"Have suggestions\n{json.dumps(suggestions, indent=2)}")
            if "choices" in suggestions and suggestions["choices"]:
                message = [
                    {"suggestion": c.get("text", ""), "imports": c.get("imports")}
                    for c in suggestions["choices"]
                ]
            else:
                message = None

            status = "success"
            status_code = 200
        except Exception as e:
            logger.exception("Encountered error when submitting to API server.")
            try:
                error_dict = json.loads(str(e))
                status = error_dict["status"]
                message = error_dict["error_msg"]
                status_code = error_dict["status_code"]
            except Exception:
                logger.exception("Unknown error.")
                status_code = 400
                status = "Error"
                message = "Unknown error."

        response = {"status": status, "message": message}
        self.set_status(status_code)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


class JupyterCogramTokenHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramTokenHandler, self).__init__(application, request, **kwargs)

    def post(self):
        logger.debug(f"Receiving token Post!")
        data = json.loads(self.request.body)
        token = data.get("auth_token", "")

        post_token_response = post_auth_token(token)

        if post_token_response.status_code == 200:
            save_token(token)
            status = 200
            response = {"status": status, "message": "Token saved."}
        else:
            status = post_token_response.status_code
            response = post_token_response.json()

        self.set_status(status)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))

    def get(self):
        logger.debug(f"Receiving token fetch request")
        token = fetch_token()
        logger.debug(f"Have fetched token {token}")

        log_launch = bool_arg(self.request, "log_launch")

        response = None
        if token is not None:
            logger.debug(f"Checking if token is valid against API: {token}")
            response = post_auth_token(token, log_launch=log_launch)
            token_valid = response.status_code == 200
        else:
            token_valid = False

        if token_valid:
            status = 200
            response = {
                "status": status,
                "message": "Token found.",
                "auth_token": token,
            }
        else:
            status = response.status_code
            response = {
                "status": response.status_code,
                "error": response.json().get("error", "N/A"),
                "auth_token": None,
            }

        self.set_status(status)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


class JupyterCogramConfigHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramConfigHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.set_status(200)
        response = {"demo_mode": demo_mode, **read_config()}
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))

    def put(self):
        data = json.loads(self.request.body)
        logger.debug(f"Receiving Config update: {data}")
        # noinspection PyBroadException
        try:
            merged_configs = merge_configs(data)
            save_config(merged_configs)
            self.set_status(200)
        except Exception as e:
            self.set_status(404)
            logger.error(f"Encountered error while updating config:{e}")

        self.finish(json.dumps({}))


class JupyterCogramVersionHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramVersionHandler, self).__init__(
            application, request, **kwargs
        )

    def get(self):
        logger.debug(f"Checking package version")
        is_up_to_date = is_installation_up_to_date()
        if is_up_to_date:
            status = 200
            message = (
                f"Installed version ({jupyter_cogram.__version__}) is up "
                f"to date with PyPI"
                f" version ({LATEST_PYPI_VERSION})."
            )
        else:
            status = 400
            message = (
                f"Installed version ({jupyter_cogram.__version__}) is **not** up "
                f"to date with PyPI "
                f"version ({LATEST_PYPI_VERSION})."
            )

        self.set_status(status)
        response = {
            "status": status,
            "message": message,
            "pypi_version": LATEST_PYPI_VERSION,
            "installed_version": jupyter_cogram.__version__,
        }
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


class JupyterUpgradeCogramHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterUpgradeCogramHandler, self).__init__(
            application, request, **kwargs
        )

    def post(self):
        logger.debug(f"Receiving request to upgrade")
        import sys

        previous_version = jupyter_cogram.__version__
        logger.debug(f"Before upgrade, have jupyter-cogram version {previous_version}")
        cmd = f"{sys.executable} -m pip install -U jupyter-cogram"
        logger.debug(f"Running cmd {cmd}")
        status_code = os.system(cmd)

        from importlib import reload

        reload(jupyter_cogram)

        new_version = jupyter_cogram.__version__
        logger.debug(f"After upgrade, have jupyter-cogram version {new_version}")

        if status_code == 0 and parse_version(new_version) >= parse_version(
            previous_version
        ):
            status = 200
            response = {
                "status": "success",
                "message": "Library updated.",
                "new_version": new_version,
            }
        else:
            status = 400
            response = {
                "status": "error",
                "message": "Could not upgrade library. Please check your "
                "Jupyter Notebook server logs. If you keep encountering "
                "the same problem, please reach out at support@cogram.ai",
                "new_version": LATEST_PYPI_VERSION,
            }

        self.set_status(status)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


def get_new_version_message(
    previous_version: Version,
) -> Optional[Text]:
    if previous_version.minor == 7:
        return (
            f"Welcome to your new Cogram version 👋 This version improves how you "
            f"can write code with Cogram: You can now generate code by writing a "
            f"Python "
            f"comment and hitting the Tab key, or by beginning a line of code and "
            f"completing with the Tab key."
        )


class JupyterCogramLaunchHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramLaunchHandler, self).__init__(application, request, **kwargs)

    def get(self):
        logger.debug(f"Receiving launch query.")

        log_content = read_csv()
        is_first_launch = log_content is None

        previous_version = log_content[-1][1] if log_content else None
        is_new_version = (
            parse_version(jupyter_cogram.__version__) > parse_version(previous_version)
            if previous_version
            else False
        )

        msg = None
        if is_first_launch:
            status = "first_launch"
            msg = (
                "Welcome to Cogram 👋 Get started by writing comments or code. You "
                "can trigger completions with the Tab key."
            )
        elif is_new_version:
            status = "new_version"
            msg = get_new_version_message(parse_version(previous_version))
        else:
            status = "ok"

        append_to_log_file()

        self.set_status(200)
        response = {
            "status": status,
            "version": jupyter_cogram.__version__,
            "previous_version": previous_version,
            "msg": msg,
        }

        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")

        self.finish(json.dumps(response))


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication):
        handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    web_app.add_handlers(
        host_pattern,
        [
            (url_path_join(web_app.settings["base_url"], uri), handler)
            for uri, handler in [
                ("/config", JupyterCogramConfigHandler),
                ("/cogram", JupyterCogramHandler),
                ("/token", JupyterCogramTokenHandler),
                ("/checkVersion", JupyterCogramVersionHandler),
                ("/upgrade", JupyterUpgradeCogramHandler),
                ("/launch", JupyterCogramLaunchHandler),
            ]
        ],
    )
    logger.debug("loaded_jupyter_server_extension: jupyter-cogram")
