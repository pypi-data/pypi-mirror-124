from tqdm import tqdm
import requests
import os


class Datasets:
    """
    Generic class for data operations to download and extract datasets
    from a URL
    """

    @staticmethod
    def download_from_url(url: str = None, dst: str = None) -> int:
        """
        download dataset from a url

        :param url: url to download file
        :type url: str
        :param dst: destination path to save the file
        :type dst: str
        :returns: file size and saved datasets

        """
        if url is None or dst is None:
            raise TypeError("Missing the required arguments")

        req = requests.get(url, stream=True, verify=False)
        file_size = int(req.headers["Content-length"])
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)
        else:
            first_byte = 0
        pbar = tqdm(
            total=file_size,
            initial=first_byte,
            unit="B",
            unit_scale=True,
            desc=url.split("/")[-1],
        )

        with (open(dst, "wb")) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)

        pbar.close()
        return file_size
