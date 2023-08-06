import requests
from typing import List
from pydantic import BaseModel

class VersionManifestLatest(BaseModel):
    release: str
    snapshot: str

class VersionManifestVersion(BaseModel):
    id: str
    type: str
    url: str
    time: str
    releaseTime: str

class VersionManifest(BaseModel):
    latest: VersionManifestLatest
    versions: List[VersionManifestVersion]

def get_java_version_manifest() -> VersionManifest:
    timeout = 3
    useragent = 'aoirint/pymcversion'
    headers = {
        'User-Agent': useragent,
    }

    res = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json', headers=headers, timeout=timeout)
    manifest_dict = res.json()

    manifest = VersionManifest.parse_obj(manifest_dict)
    return manifest
