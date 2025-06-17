from pathlib import Path

from tools.dependencies import doc_convert, pdf2image
from tools.routes import doc_parse


def test_doc2pdf():
    assert (
        doc_convert(Path("uploads/ppt/1.pptx"), Path("uploads/extracted_pdf"))
        is not None
    )


def test_pdf2image():
    assert pdf2image(Path("upload/1.pdf"), Path("upload/extracted_pdf"))


async def test_ppt_parse():
    item = doc_parse.PptParseRequest(ppt_file="upload/1.pptx")
    result = await doc_parse.ppt_parse(item)
    assert result.code == 200
