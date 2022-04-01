from pathlib import Path


class AppConst:
    APP_NAME = "aaqua_sys"
    LOG_FILE = f"{APP_NAME}.log"
    TMP_DIR = "tmp"


Path(AppConst.TMP_DIR).mkdir(parents=True, exist_ok=True)


class RestApiDefinition:
    PING = ""
    GET_INVOCATION_INFO = "get-invocation-info"


class DefaultApiValues:
    GRPC_PORT = 8000
    REST_PORT = 5000
    SERVER_HOST_NAME = "server"
    DB_HOST_NAME = "database"
