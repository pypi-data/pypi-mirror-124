# -*- coding: utf-8 -*-
"""
pysciebo implements logic for connecting to the sciebo cloud. For more info check
the official homepage (content in German only, sorry):
    https://www.hochschulcloud.nrw/

Disclaimer: This project is not endorsed officially.
"""
import os
from pathlib import Path
from typing import Optional

import owncloud

__version__ = "1.1.0"


class ScieboClient:
    """
    ScieboClient implements functionality for accessing and uploading data to
    the Sciebo cloud.
    """

    def __init__(self, url, username, password):
        self.client = login(url, username, password)

    def delete(self, remote_file_path: Path) -> bool:
        """Delete a remote file using a remote file path."""
        return self.client.delete(str(remote_file_path))

    def download(
        self,
        remote_file_path: Path,
        local_file_path: Optional[Path] = None,
    ) -> bool:
        """Download a file using a remote and an optional local file path."""
        if local_file_path is None:
            local_file_path = Path(f"{os.getcwd()}/{remote_file_path.name}")
        return self.client.get_file(str(remote_file_path), str(local_file_path))

    def upload(self, remote_file_path: Path, local_file_path: Path) -> bool:
        """Upload a file using a remote and a local file path."""
        return self.client.put_file(str(remote_file_path), str(local_file_path))


def login(url, username, password) -> owncloud.Client:
    """Create an Owncloud client and log in using username and password."""
    oc = owncloud.Client(url)
    oc.login(username, password)

    return oc
