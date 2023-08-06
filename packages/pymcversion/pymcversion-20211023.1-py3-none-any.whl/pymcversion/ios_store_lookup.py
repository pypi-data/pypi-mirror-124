import requests
from typing import List
from pydantic import BaseModel

class IosStoreLookupEntry(BaseModel):
    screenshotUrls: List[str]
    ipadScreenshotUrls: List[str]
    appletvScreenshotUrls: List[str]
    artworkUrl60: str
    artworkUrl512: str
    artworkUrl100: str
    artistViewUrl: str
    features: List[str]
    supportedDevices: List[str]
    advisories: List[str]
    isGameCenterEnabled: bool
    kind: str
    minimumOsVersion: str
    trackCensoredName: str
    languageCodesISO2A: List[str]
    fileSizeBytes: str
    formattedPrice: str
    contentAdvisoryRating: str
    averageUserRatingForCurrentVersion: float
    userRatingCountForCurrentVersion: int
    averageUserRating: float
    trackViewUrl: str
    trackContentRating: str
    releaseDate: str
    bundleId: str
    trackId: int
    trackName: str
    sellerName: str
    primaryGenreName: str
    genreIds: List[str]
    isVppDeviceBasedLicensingEnabled: bool
    currentVersionReleaseDate: str
    releaseNotes: str
    primaryGenreId: int
    currency: str
    description: str
    artistId: int
    artistName: str
    genres: List[str]
    price: float
    version: str
    wrapperType: str
    userRatingCount: int

class IosStoreLookup(BaseModel):
    resultCount: int
    results: List[IosStoreLookupEntry]


def get_ios_store_lookup() -> IosStoreLookupEntry:
    timeout = 3
    useragent = 'aoirint/pymcversion'
    headers = {
        'User-Agent': useragent,
    }

    res = requests.get('https://itunes.apple.com/lookup?bundleId=com.mojang.minecraftpe', headers=headers, timeout=timeout)
    lookup_dict = res.json()

    lookup = IosStoreLookup.parse_obj(lookup_dict)

    entry = lookup.results[0]

    return entry
