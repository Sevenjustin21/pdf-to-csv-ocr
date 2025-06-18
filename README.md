# PDF Test Report Extractor

This project provides an automated solution to extract structured data from technician-generated PDF reports. Using PyMuPDF (fitz) and Tesseract OCR, it converts semi-structured scanned documents into clean CSV files and human-readable summaries.

## 🚀 Features

- 📄 PDF to CSV conversion with OCR
- ✏️ Auto-generated summary reports (Markdown format)
- 📌 Adaptive layout handling for variable-length reports
- 🧠 Preprocessing to improve OCR accuracy

## 🛠️ Technologies Used

- Python 3.x
- PyMuPDF (fitz)
- pytesseract (Tesseract OCR)
- pandas

## 📂 Input / Output

- **Input**: Technician-generated PDF reports (1–5 pages, scanned format)
- **Output**:
  - `output_report.csv`: Extracted structured data for further processing (e.g. Airtable)
  - `summary_report.md`: Brief natural language summary for human review

## 📎 Sample Files

- `demo.pdf`: Input test report sample
- `output_report.csv`: Extracted data output
- `summary_report.md`: AI-assisted summary output

## 🧪 Future Improvements

- Auto-validation of extracted fields
- Configurable field-mapping templates
- GUI or web-based interface for non-technical users

## 👋 Contact

For freelance work or project collaboration, feel free to reach me via [[Upwork profile link](https://www.upwork.com/freelancers/~0199ff5f379ffac0a8?mp_source=share)] or open an issue in this repository.
