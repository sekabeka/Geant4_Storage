import os
import aiofiles

PATH_TO_STORAGE = "storage/"
if not os.path.exists(PATH_TO_STORAGE):
    os.mkdir(PATH_TO_STORAGE)


class Storage:
    def __init__(
            self,
            filename: str,
            content: bytes = b'',
    ):
        self.filename = filename
        self.content = content
        self.filepath = PATH_TO_STORAGE + self.filename

    async def upload(self):
        if not self.exists():
            async with aiofiles.open(self.filepath, mode="wb") as file:
                await file.write(self.content)
            return True

    async def update(self):
        if self.exists():
            async with aiofiles.open(self.filepath, mode="wb") as file:
                await file.write(self.content)
            return True

    async def remove(self):
        if self.exists():
            os.remove(self.filepath)
            return True

    async def retrieve(self):
        if self.exists():
            return self.filepath

    def exists(self):
        return os.path.exists(self.filepath)
