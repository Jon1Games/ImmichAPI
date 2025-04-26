import requests as requestsrequests
import json
import io
import random

class ImmichAPI:
    def __init__(self, serverUrl: str, apiKey: str):
        self.baseUrl = serverUrl
        self.apiKey = apiKey

    def requests(self, type:str, url: str, responseType: str = "json", payload: json = {}):
        headers = {'x-api-key': self.apiKey}
        
        if payload or type == "POST":
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
    
    def addAssetsToAlbum(self, albumId:int, assetIds: tuple[int]):
        return(self.requests(type="PUT", url="/api/albums/" + str(albumId) + "/assets", payload=json.dumps({
            "ids": assetIds
        })))
    
    def removeAssetsToAlbum(self, albumId:int, assetIds: tuple[int]):
        return(self.requests(type="DELETE", url="/api/albums/" + str(albumId) + "/assets", payload=json.dumps({
            "ids": assetIds
        })))
    
    def moveToOtherAlbum(self, sourceAlbumId: int, destinationAlbumId: int, assetIds: tuple[int]):
        result = {}
        result["remove"] = self.removeAssetsToAlbum(albumId=sourceAlbumId, assetIds=assetIds)
        result["add"] = self.addAssetsToAlbum(albumId=destinationAlbumId, assetIds=assetIds)
        return result

    def downloadAsset(self, id: int):
        return(self.requests(type="GET", url="/api/assets/"+id+"/original", responseType="binary"))
    
    def downloadRandomAssetFromAlbum(self, albumId: int, count: int = 1):
        assets = self.getAlbumInfo(albumId)["assets"]
        downloaded_assets = []
        for _ in range(count):
            random_asset_id = random.choice(assets)["id"]
            downloaded_assets.append({
                "id": random_asset_id,
                "data": self.downloadAsset(id=random_asset_id)
            })
        return downloaded_assets

    def getAllTags(self):
        return(self.requests(type="GET", url="/api/tags"))
    
    def getTagByName(self, name:str):
        tags = self.getAllTags()
        for tag in tags:
            if tag["name"] == name:
                return tag

    def bulkTagAssets(self, assesIds: tuple[str], tagIds: tuple[str]):
        payload = json.dumps({
            "assetIds": assesIds,
            "tagIds": tagIds
        })
        return(self.requests(type="PUT", url="/api/tags/assets", payload=payload))
    
    def createTag(self, name: str, color: str = "", parent: str = ""):
        data = json.dumps({
            "color": color,
            "name": name
        })
        if parent != "":
            data["parentId"] = parent
        return(self.requests(type="POST", url="/api/tags", payload=data))
