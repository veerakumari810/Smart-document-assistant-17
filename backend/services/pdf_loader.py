from pypdf import PdfReader

class PDFLoaderService:
    @staticmethod
    def extract_text(file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text