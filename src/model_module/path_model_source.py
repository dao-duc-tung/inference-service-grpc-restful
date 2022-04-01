from .i_model_source import IModelSource


class PathModelSource(IModelSource):
    """
    Path can be URL or local file path.
    URL has format: `http://...` or `https://`
    Local file path has format: `file://...`
    """

    URL = "URL"
    LOCALFILE = "LOCALFILE"
    UNKNOWN = "UNKNOWN"

    @property
    def path_type(self) -> str:
        protocol = self._get_protocol()
        if "http" == protocol or "https" == protocol:
            return PathModelSource.URL
        elif "file" == protocol:
            return PathModelSource.LOCALFILE
        else:
            return PathModelSource.UNKNOWN

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        s = f"path={self.path}"
        return s

    def get_raw_path(self) -> str:
        colon_idx = self._get_colon_idx()
        raw_start_idx = colon_idx + 3  # 3 for '://'
        raw_path = self.path[raw_start_idx:]
        return raw_path

    def _get_colon_idx(self) -> int:
        colon_idx = self.path.find(":")
        return colon_idx

    def _get_protocol(self) -> str:
        colon_idx = self._get_colon_idx()
        if colon_idx == -1:
            return ""

        protocol = self.path[:colon_idx]
        return protocol
