import os
import requests
import random
from urllib.parse import urljoin, urlparse
from halo import Halo
from termcolor import colored

spinner = Halo(text="Downloading...", spinner="dots", text_color="yellow")
instagram_url = input("Paste Instagram Url: ")
print(instagram_url)

response = requests.get(f"{instagram_url}?__a=1")
response_json = response.json()


def findKeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findKeys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findKeys(j, kv):
                yield x


def getFileType(url):
    url = urljoin(url, urlparse(url).path)
    file_type = url.split(".")[-1]
    file_ext = f".{file_type}"
    return file_ext


def downloadFile(fileUrl):
    while True:
        spinner.start()
        filename = f"instagram-{random.randint(1, 100000)}{getFileType(fileUrl)}"

        with open(filename, 'wb+') as handle:
            responseFile = requests.get(fileUrl, stream=True)
            responseFileSize = responseFile.headers["Content-length"]
            if not responseFile.ok:
                print(responseFile)
            for block in responseFile.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        break
    print(f"\nsize: {responseFileSize} kb")
    print(colored("✨Download completed", "green"))
    spinner.stop()


# get images and videos
images = list(findKeys(response_json, 'display_url'))
videos = list(findKeys(response_json, 'video_url'))

# remove duplicates
videos = list(dict.fromkeys(videos))
images = list(dict.fromkeys(images))


# download files
if len(images) > 0:
    for i in range(len(images)):
        downloadFile(images[i])

if len(videos) > 0:
    for i in range(len(videos)):
        downloadFile(videos[i])
