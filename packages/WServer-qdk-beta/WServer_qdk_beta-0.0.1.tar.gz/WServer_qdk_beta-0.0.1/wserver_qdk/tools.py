""" Разный инструментарий, полезный при взаимодействии с WServer """
import base64


def encode_photo(photo_path):
    """ Кодирует фото в base64

    :param photo_path: Абсолютный путь до фото.
    :return: Последовательность в кодировке base64."""
    with open(photo_path, 'rb') as fobj:
        photo_data = base64.b64encode(fobj.read())
    return photo_data
