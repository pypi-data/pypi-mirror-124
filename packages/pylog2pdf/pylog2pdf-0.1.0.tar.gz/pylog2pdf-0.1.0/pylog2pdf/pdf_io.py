__all__ = ["write_log", "read_log"]

import ast
import os
from pathlib import Path

from PyPDF2 import PdfFileReader, PdfFileWriter

import pylog2pdf


def write_log(pdf_path: os.PathLike, log: dict = pylog2pdf.LOG) -> Path:
    def make_str_dict(dict_):
        ret = []
        for k, v in dict_.items():
            if v is None:
                continue
            if isinstance(v, dict):
                ret.append((f"/log_{k}", make_str_dict(v)))
            else:
                ret.append((f"/log_{k}", str(v)))
        return dict(ret)

    log = make_str_dict(log)
    log = {k: str(v) for k, v in log.items()}  # Convert nested dict to string

    with Path(pdf_path).open("rb+") as file:
        reader = PdfFileReader(file)
        log.update(dict(reader.getDocumentInfo()))

        writer = PdfFileWriter()
        writer.appendPagesFromReader(reader)
        writer.addMetadata(log)
        writer.write(file)
    return Path(pdf_path)


def read_log(pdf_path: os.PathLike) -> dict:
    pdf_path = Path(pdf_path).with_suffix(".pdf")

    with pdf_path.open("rb") as file:
        reader = PdfFileReader(file)
        log = reader.getDocumentInfo()

    def get_log(dict_):
        ret = []
        for k, v in dict_.items():
            if not k.startswith("/log_"):
                continue  # Not a field this package dumped.

            try:
                value = ast.literal_eval(v)
            except (ValueError, SyntaxError):
                value = v

            if isinstance(value, dict):
                ret.append((k[5:], get_log(value)))
            else:
                ret.append((k[5:], value))
        return dict(ret)

    return get_log(log)
