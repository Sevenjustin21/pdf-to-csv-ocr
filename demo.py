import fitz                  # PyMuPDF
import pytesseract
from PIL import Image
import io, re, csv, os
import pandas as pd
from datetime import datetime

# 👉 1. PDF 路径
PDF_PATH = r"E:\Desktop\文件夹汇总\upwork\demo.pdf"
# 👉 2. Tesseract 可执行文件路径（Windows 要改）
pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"
# 👉 3. 输出文件
CSV_OUT      = r"E:\Desktop\文件夹汇总\upwork\output_assets.csv"
SUMMARY_OUT  = r"E:\Desktop\文件夹汇总\upwork\summary_report.md"

# --------------------------------------------------
# 工具：把 fitz Pixmap → Pillow Image → OCR 文本
def ocr_pix(pix):
    img = Image.open(io.BytesIO(pix.tobytes("ppm")))
    return pytesseract.image_to_string(img, lang="eng")

# 工具：把一块连贯文字分割成单条资产记录
def parse_assets(text_block):
    lines = [l.strip() for l in text_block.splitlines() if l.strip()]
    assets = []
    i = 0
    while i < len(lines):
        if re.fullmatch(r"\d{7}", lines[i]):          # Asset ID
            asset_id = lines[i]
            desc      = lines[i+1]                    # 描述
            user      = lines[i+2]                    # User
            # Test Instrument 可能三行，也可能两行
            instr  = []
            j = i+3
            while j < len(lines) and not re.match(r"\d{1,2}/\d{2}/\d{4}", lines[j]):
                instr.append(lines[j])
                j += 1
            instr_text = " ".join(instr)

            test_date       = lines[j]                # Date
            retest_period   = lines[j+1]              # Retest Period
            next_test_date  = lines[j+2]              # Next Test
            result          = lines[j+3]              # Pass / Fail

            assets.append([
                asset_id, desc, user, instr_text,
                test_date, retest_period, next_test_date, result
            ])
            # 跳到下一条
            i = j + 4
        else:
            i += 1
    return assets

# --------------------------------------------------
print("📄 读取 PDF 并 OCR...")
doc = fitz.open(PDF_PATH)
all_assets = []

for page in doc:
    text = ocr_pix(page.get_pixmap(dpi=300))
    all_assets.extend(parse_assets(text))

# --------------------------------------------------
print(f"✅ 共解析到 {len(all_assets)} 条资产记录")

# 写 CSV
header = ["Asset ID", "Description", "User",
          "Test Instrument", "Date",
          "Retest Period", "Next Test", "Result"]
pd.DataFrame(all_assets, columns=header).to_csv(CSV_OUT,
                                               index=False,
                                               encoding="utf-8-sig")

# 生成 Markdown 摘要
pass_cnt = sum(1 for a in all_assets if a[-1].lower().startswith("pass"))
fail_cnt = len(all_assets) - pass_cnt
with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
    f.write(f"# Summary Report ({datetime.now():%Y-%m-%d})\n\n")
    f.write(f"- Total Assets: **{len(all_assets)}**\n")
    f.write(f"- ✅ Pass: **{pass_cnt}**\n")
    f.write(f"- ❌ Fail: **{fail_cnt}**\n")

print("🎉 已输出：")
print("   CSV   ->", CSV_OUT)
print("   MD    ->", SUMMARY_OUT)