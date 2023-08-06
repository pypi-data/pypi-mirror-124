import aiohttp, aiofiles, asyncio

async def asyncDownloadGif(name, gif_url, download_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(gif_url) as resp:
            f = await aiofiles.open(download_path + name + ".gif", mode="wb")
            await f.write(await resp.read())
            await f.close()

async def asyncSearchGif(search:str, limit:int=8, download:bool=False, download_path: str=""):
    default_apiKey = "LIVDSRZULELA"

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://g.tenor.com/v1/search?q={search}&key={default_apiKey}&limit={limit}") as resp:
            response = await resp.json()
            result = []
            if download==False:
                for i in range(len(response["results"])):
                    find_data = response["results"][i]
                    result.append({"id":find_data["id"], "name": find_data["content_description"], "gif":find_data["media"][0]["gif"]["url"], "preview":find_data["media"][0]["gif"]["preview"]})
            else:
                for i in range(len(response["results"])):
                    find_data = response["results"][i]
                    await asyncDownloadGif(find_data["content_description"], find_data["media"][0]["gif"]["url"], download_path)
                    result.append({"id":find_data["id"], "name": find_data["content_description"], "gif":find_data["media"][0]["gif"]["url"], "preview":find_data["media"][0]["gif"]["preview"]})
            
            return result

def searchGif(search:str, limit:int=8, download:bool=False, download_path:str="", loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncSearchGif(search, limit, download, download_path))