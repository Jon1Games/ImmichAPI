import os
import sys
sys.path.append("..")
from main import ImmichAPI
from dotenv import load_dotenv

load_dotenv()
# CONFIG
serverURL = os.getenv("IMMICH_SERVER_URL")
apiKey = os.getenv("IMMICH_API_KEY")
source_album_name = os.getenv("MAAOA-SOURCE_ALBUM_NAME")
destination_album_name = os.getenv("MAAOA-DESTINATION_ALBUM_NAME")

def run(
        serverURL: str,
        apiKey: str,
        source_album_name: str,
        destination_album_name: str,
        ):
    immich = ImmichAPI(serverURL, apiKey)

    source_album = immich.getAlbumByName(source_album_name)
    destination_album = immich.getAlbumByName(destination_album_name)
    assets = immich.getAlbumInfo(source_album["id"])["assets"]

    immich.moveToOtherAlbum(sourceAlbumId=source_album["id"], destinationAlbumId=destination_album["id"], assetIds=[asset["id"] for asset in assets])

run(
    serverURL=serverURL,
    apiKey=apiKey,
    source_album_name=source_album_name,
    destination_album_name=destination_album_name
)