# ImmichAPI
some python funktions to talk with the immich api

## Usage

Just clone to your directory (and put folder in .gitignore).
Then import the ImmichAPI class.

```python
from ImmichAPI.main import ImmichAPI
```

## Requirements
if you have yout own requirements.txt you can add this:
```
-r immichAPI/requirements.txt
```

## Snippets

### download random image(s) from album and move those to other album

```python
serverURL = ""
apiKey = ""
image_count = 1
source_album_name = ""
destination_album_name = ""

immich = ImmichAPI(serverURL, apiKey)

source_album = immich.getAlbumByName(source_album_name)
destination_album = immich.getAlbumByName(destination_album_name)
assets = immich.downloadRandomAssetFromAlbum(source_album["id"], count=image_count)

count = 0
for asset in assets:
    count = count + 1
    with open("asset-" + str(count) + ".png", "wb") as file:
        file.write(asset["data"].read())

immich.moveToOtherAlbum(sourceAlbumId=source_album["id"], destinationAlbumId=destination_album["id"], assetIds=[asset["id"] for asset in assets])
```
