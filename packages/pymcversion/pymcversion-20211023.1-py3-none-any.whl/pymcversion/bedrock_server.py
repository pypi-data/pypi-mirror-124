import re
import requests

from pydantic import BaseModel

class VersionInfoOS(BaseModel):
    os_type: str
    url: str
    version: str

class VersionInfo(BaseModel):
    linux: VersionInfoOS
    win: VersionInfoOS

# https://www.minecraft.net/en-us/download/server/bedrock
def get_bedrock_server_latest_version() -> VersionInfo:
    timeout = 3
    useragent = 'aoirint/pymcversion'
    headers = {
        'User-Agent': useragent,
    }

    res = requests.get('https://www.minecraft.net/en-us/download/server/bedrock', headers=headers, timeout=timeout)
    html = res.text

    info_dict = {}

    # https://minecraft.azureedge.net/bin-linux/bedrock-server-1.17.40.06.zip
    for os_type in ['linux', 'win']:
        m = re.search(rf'"https://minecraft\.azureedge\.net/bin-{os_type}/bedrock-server-(.+?)\.zip"', html)
        if m is None:
            raise Exception('No match found. URL or filename changed?')

        url = m.group(0)[1:-1]
        version = m.group(1)

        info_dict[os_type] = VersionInfoOS(
            os_type=os_type,
            url=url,
            version=version,
        )

    info = VersionInfo.parse_obj(info_dict)

    return info
