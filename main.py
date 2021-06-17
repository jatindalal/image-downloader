import sys
import requests
import time
import concurrent.futures

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} url-list-file")
    exit()

file_name = sys.argv[1]

img_urls = []

try:
    img_file = open(file_name, "r")
    img_urls.extend([x.strip() for x in img_file.readlines()])
    print(f"Read {len(img_urls)} url(s)")
    img_file.close()
except OSError as err:
    print(f"OS error: {err}")


start_time = time.perf_counter()


def download_image(img_url):
    try:
        img_bytes = requests.get(img_url).content
    except requests.exceptions.RequestException as exp:
        print(f"Requests error: {exp}")
    except:
        print(f"Can't read the url {img_url}")
    img_name = img_url.split('/')[3]
    img_name = f"{img_name}.jpg"
    try:
        with open(img_name, 'xb') as img_file:
            img_file.write(img_bytes)
            print(f"{img_name} was downloaded")
    except OSError as err:
        print(f"OS error: {err}")


# Creating threads and using them
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, img_urls)


end_time = time.perf_counter()

print(f"Finished in {round(end_time - start_time, 2)} seconds")
