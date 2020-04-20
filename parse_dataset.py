from requests import exceptions
import requests
import cv2
import os


API_KEY = "89b8a8d9bca0466781a864890758c6f3"
MAX_RESULTS = 4000
GROUP_SIZE = 100
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
categories = ['fashion', 'flowers']

EXCEPTIONS = {IOError, FileNotFoundError, exceptions.RequestException,
              exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout}


def create_folder(workspace, name_folder):
    path = os.path.join(workspace, name_folder)
    if not os.path.exists(path):
        os.makedirs(path)
        print("create folder with path {0}".format(path))
    else:
        print("folder exists {0}".format(path))

        return path


for category in categories:
    folder = create_folder(r"dataset", category)


for category in categories:
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": category, "offset": 0, "count": GROUP_SIZE}
    print("[INFO] searching Bing API for '{}'".format(category))
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
    print("[INFO] {} total results for '{}'".format(estNumResults,
                                                    category))

    total = 0

    for offset in range(0, estNumResults, GROUP_SIZE):
        print("[INFO] making request for group {}-{} of {}...".format(
            offset, offset + GROUP_SIZE, estNumResults))
        params["offset"] = offset
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()
        print("[INFO] saving images for group {}-{} of {}...".format(
            offset, offset + GROUP_SIZE, estNumResults))

        for v in results["value"]:
            try:
                print("[INFO] fetching: {}".format(v["contentUrl"]))
                r = requests.get(v["contentUrl"], timeout=30)
                ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                photo = os.path.join('dataset/{}'.format(category),
                                     "{}{}".format('{}'.format(category)+str(total).zfill(8), ext))

                print("[INFO] photo name: {}".format(photo))
                f = open(photo, "wb")
                f.write(r.content)
                f.close()
                image = cv2.imread(photo)
                if image is None:
                    print("[INFO] deleting: {}".format(photo))
                    os.remove(photo)
                    continue
                total += 1

            except Exception as e:
                if type(e) in EXCEPTIONS:
                    print("[INFO] skipping: {}".format(v["contentUrl"]))
                    continue
