import os
import shutil
import ntpath
import tempfile
import requests

from dataclasses import dataclass

BASE_URL = "http://localhost:8000/"
PATH_TO_LOCAL_STORAGE = "files/"

if not os.path.exists(PATH_TO_LOCAL_STORAGE):
    os.mkdir(PATH_TO_LOCAL_STORAGE)

@dataclass
class Endpoint:
    upload = BASE_URL + "upload"
    update = BASE_URL + "update"
    retrieve = BASE_URL + "retrieve"
    remove = BASE_URL + "remove"

class FileUploader:
    def __init__(self, path: str):
        self.path = path
        self.format = "zip"
        self.filename = self.extract_name()

    def sender(self, url, files=None, stream=False, data=None, json=None):
        if stream:
            with requests.post(url=url, stream=stream, json=json) as response:
                path = PATH_TO_LOCAL_STORAGE + self.filename
                if response.ok:
                    with open(path, "wb") as file:
                        for chunk in response.iter_content():
                            if chunk:
                                file.write(chunk)
                    return
                else:
                    return response.json()

        response = requests.post(
            url=url,
            files=files,
            data=data,
            json=json,
        )
        return response.json()

    def extract_name(self):
        head, tail = ntpath.split(self.path)
        if tail:
            return tail
        return ntpath.basename(head) + ".%s" % self.format

    def get_file(self):
        self.format = "zip"
        if os.path.isdir(self.path):
            head, tail = ntpath.split(self.path)
            directory = ntpath.basename(head)
            with tempfile.TemporaryDirectory() as tmp_directory:
                base_name = os.path.join(tmp_directory, directory)
                shutil.make_archive(
                    base_name=base_name,
                    format=self.format,
                    root_dir=directory
                )
                base_name = base_name + ".%s" % self.format
                return open (base_name, 'rb')
        else:
            return open(self.path, 'rb')

    def upload(self):
        file = self.get_file()
        return self.sender(
            url=Endpoint.upload,
            files=dict(file=file)
        )

    def update(self):
        file = self.get_file()
        return self.sender(
            url=Endpoint.update,
            files=dict(file=file)
        )

    def retrieve(self):
        return self.sender(
            url=Endpoint.retrieve,
            json=dict(filename=self.filename),
            stream=True
        )

    def remove(self):
        return self.sender(
            url=Endpoint.remove,
            json=dict(filename=self.filename)
        )

