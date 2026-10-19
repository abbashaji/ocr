# OCR engine comparison on GitHub Actions
1. Create a repo (PRIVATE if the client's sample images must not be public) and upload this folder as-is.
2. Actions tab -> "ocr-bench" -> Run workflow.
3. Open each matrix job's Summary page for the tables; raw JSON is in the run's Artifacts.

Status: the `tesseract` job logic was run locally. The `easyocr` and `paddleocr` jobs are UNTESTED
(dependency versions, PaddleOCR Persian model name, output format). A failed engine does not stop the others;
its error text appears in that job's summary.
Not suitable for: model training (standard runners have no GPU).
