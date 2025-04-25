import requests as requestsrequests
import json
import io

class ImmichAPI:
    def __init__(self, serverUrl: str, apiKey: str):
        self.baseUrl = serverUrl
        self.apiKey = apiKey

    def requests(self, type:str, url: str, responseType: str = "json", payload: json = {}):
        headers = {'x-api-key': self.apiKey}
        
        if payload:
            headers['Content-Type'] = 'application/json'

        if responseType == "json":
            headers['Accept'] = 'application/json'
        elif responseType == "binary":
            headers['Accept'] = 'application/octet-stream'

        response = requestsrequests.request(type, self.baseUrl + url, headers=headers, data=payload)
        if responseType == "json":
            return json.loads(response.text)
        elif responseType == "binary":
            return io.BytesIO(response.content)
        else:
            return "unknown response type, allowed: json"

    def getAllAlbums(self):
        return(self.requests(type="GET", url="/api/albums"))

    def getAlbumByName(self, name: str):
        albums = self.getAllAlbums()
        for album in albums:
            if album["albumName"] == name:
                return album

    def getAlbumInfo(self, id: int):
        return(self.requests(type="GET", url="/api/albums/" + id))

    def downloadAsset(self, id: int):
        self.requests(type="GET", url="/api/assets/"+id+"/original", responseType="binary")

    def getAllTags(self):
        self.requests(type="GET", url="/api/tags")

    def bulkTagAssets(self, assesIds: tuple[str], tagIds: tuple[str]):
        payload = json.dumps({
            "assetIds": assesIds,
            "tagIds": tagIds
        })
        return(self.requests(type="PUT", url="/api/tags/assets", payload=payload))

# immich = ImmichAPI(serverUrl="http://shuna:2283", apiKey="eyjorY8Z3DYhViEJcutTXLXmUGc0afB9IbG0nf0")
