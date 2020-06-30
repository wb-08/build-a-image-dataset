from requests import exceptions
import requests
import cv2
import os


subscription_key = "YOUR_API_KEY"
search_terms = ['girl', 'man']
number_of_images_per_request = 100
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
# search_url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search"

EXCEPTIONS = {IOError, FileNotFoundError, exceptions.RequestException,
              exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout}


def create_folder(name_folder):
    path = os.path.join(name_folder)

    if not os.path.exists(path):
        os.makedirs(path)
        print('------------------------------')
        print("create folder with path {0}".format(path))
        print('------------------------------')

    else:
        print('------------------------------')
        print("folder exists {0}".format(path))
        print('------------------------------')
        return path

# Содержимое ответа сервера в JSON
def get_results():
    search = requests.get(search_url, headers=headers, params=params)
    search.raise_for_status()
    return search.json()

# записываем изображение
def write_image(photo):
    r = requests.get(v["contentUrl"], timeout=25)
    f = open(photo, "wb")
    f.write(r.content)
    f.close()


for category in search_terms:
    folder = create_folder(category)
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": category, "offset": 0, "count": number_of_images_per_request}
    results = get_results()
    total = 0

    for offset in range(0, results["totalEstimatedMatches"], number_of_images_per_request):
        params["offset"] = offset
        results = get_results()

        for v in results["value"]:
            try:
                ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                photo = os.path.join(category, "{}{}".format('{}'.format(category)
                                                             + str(total).zfill(6), ext))

                write_image(photo)
                print("saving: {}".format(photo))
                image = cv2.imread(photo)
                if image is None:
                    print("deleting: {}".format(photo))
                    os.remove(photo)
                    continue

                total += 1

            except Exception as e:
                if type(e) in EXCEPTIONS:
                    continue
