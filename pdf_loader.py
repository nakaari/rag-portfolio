from pypdf import PdfReader
import config

def extract_sections(pdf_path=config.PDF_PATH):
    reader = PdfReader(pdf_path)
    sections = []
    current_label = "cover"
    current_text = ""

    for page in reader.pages:
        text = page.extract_text() or ""

        # Step 1: does a header line exist on this page?
        label = None
        for line in text.split("\n"):
            if "Laws of the Game 2026/27" in line and "|" in line:
                pieces = line.split("|")
                if len(pieces) >= 2:
                    label = pieces[1].strip()
                break  # stop after finding the first header line on this page

        # Step 2: decide what to do based on whether a (new) label was found
        if label and label != current_label:
            if current_text:
                sections.append({"label": current_label, "text": current_text})
            current_label = label
            current_text = text
        else:
            current_text += text

    # Save whatever's left after the loop ends
    if current_text:
        sections.append({"label": current_label, "text": current_text})

    return sections