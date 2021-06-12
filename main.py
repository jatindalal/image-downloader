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
    with open(file_name, "r") as img_file:
        urls = img_file.readlines()
        urls = [x.strip() for x in urls]
        print(f"Read {len(urls)} urls...")
        img_urls.extend(urls)
        img_file.close()
except:
    print("Cannot read urls from file!")
    exit()


start_time = time.perf_counter()


def download_image(img_url):
    try:
        img_bytes = requests.get(img_url).content
    except:
        print(f"Can't read the url {img_url}")
    img_name = img_url.split('/')[3]
    img_name = f"{img_name}.jpg"
    try:
        with open(img_name, 'xb') as img_file:
            img_file.write(img_bytes)
            print(f"{img_name} was downloaded...")
    except:
        print(f"Cannot create the file {img_name}")


# Creating threads and using them
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, img_urls)


end_time = time.perf_counter()

print(f"Finished in {end_time - start_time} seconds")
