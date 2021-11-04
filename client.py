import requests
import argparse

def main(api):
    
    addr = 'http://127.0.0.1:8000'
    url = addr + api
    file_path = 'ankle_boot.jpeg'

    files = {'file': (file_path, open(file_path, 'rb'), "image/jpeg")}
    response = requests.post(url, files=files)

    print(response)

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-api','--api_route', help='/kafka-predict or /pubsub-predict')
    args = parser.parse_args()
    main(args.api_route)
