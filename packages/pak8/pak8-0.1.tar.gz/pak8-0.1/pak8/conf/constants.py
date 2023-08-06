from pathlib import Path

PAK8_DIR: Path = Path(__file__).resolve().parent
EXAMPLES_DIR: Path = PAK8_DIR.joinpath("../examples")
PHIDATA_COM_CLI_JSON_KEY_PATH: str = str(
    Path.home().joinpath("phidata", "keys", "phidata-com-cli.json")
)
NAMESPACE_RESOURCE_GROUP_KEY = "ns"
DEFAULT_K8S_NAMESPACE = "default"
RBAC_RESOURCE_GROUP_KEY = "rbac"
DEFAULT_K8S_SERVICE_ACCOUNT = "default"
