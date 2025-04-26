import os
import sys
sys.path.append("..")
from main import ImmichAPI
from dotenv import load_dotenv

load_dotenv()
# CONFIG
serverURL = os.getenv("IMMICH_SERVER_URL")
apiKey = os.getenv("IMMICH_API_KEY")
image_count = int(os.getenv("DCA-IMAGE_COUNT"))
source_album_name = os.getenv("DCA-SOURCE_ALBUM_NAME")
destination_album_name = os.getenv("DCA-DESTINATION_ALBUM_NAME")
destination_folder = os.getenv("DCA-DESTINATION_FOLDER")

def run(
        serverURL: str,
        apiKey: str,
        image_count: int,
        source_album_name: str,
        destination_album_name: str,
        destination_folder: str
        ):
    immich = ImmichAPI(serverURL, apiKey)

    source_album = immich.getAlbumByName(source_album_name)
    destination_album = immich.getAlbumByName(destination_album_name)
    assets = immich.downloadRandomAssetFromAlbum(source_album["id"], count=image_count)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    if destination_folder != "" or destination_folder is None:
        destination_folder = destination_folder + "/"

    count = 0
    for asset in assets:
        while True:
            count = count + 1
            image_path = destination_folder + "asset-" + str(count) + ".jpg"
            if not os.path.exists(image_path):
                break

        with open(image_path, "wb") as file:
            file.write(asset["data"].read())

    immich.moveToOtherAlbum(sourceAlbumId=source_album["id"], destinationAlbumId=destination_album["id"], assetIds=[asset["id"] for asset in assets])

run(
    serverURL=serverURL,
    apiKey=apiKey,
    image_count=image_count,
    source_album_name=source_album_name,
    destination_album_name=destination_album_name,
    destination_folder=destination_folder
)