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

Some snippets are provided in the snippets folder, you will need *some* of the requirements in the `snippet-requirements.txt`.
Also the config is loaded form the `.env` file, which could look like this:
```env
IMMICH_SERVER_URL=http://localhost:2283
IMMICH_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
IMAGE_COUNT=1
SOURCE_ALBUM_NAME=myAlbum
DESTINATION_ALBUM_NAME=myNewAlbum
DESTINATION_FOLDER=download
```
