from datetime import datetime

from py_moysklad.entities.attached_file import AttachedFile


class Image(AttachedFile):
    updated: datetime
