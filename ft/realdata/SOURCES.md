# Source table (TASK F research, 2026-10-27/28)

Discovery ran on GitHub Actions (run 40570635989, artifact `discovery`, 30 days). fa.wikisource has 11,374 pages at quality 3
("proofread") and 16,342 at quality 4 ("validated"); 397 works have >= 1 such page, 103 have >= 50, 39 have >= 200.

| source | licence | size / what ground truth is | decision | why |
|---|---|---|---|---|
| fa.wikisource ProofreadPage + Wikimedia Commons scans (21 works used, see ATTRIBUTION.md) | scan: per-work Commons tag (PD / CC0 / CC BY 4.0 / CC BY-SA 4.0); transcription: CC BY-SA 4.0 | ~27.7k proofread/validated pages in total; we sampled 60-200 pages per work. Ground truth = human proofread page text (levels 3-4) | USED (only source) | real scans, page-aligned human text, licence per work, diverse eras (1851-2022) and print styles |
| same, w05 TarikhMashrouteh, w15 Sarq magazine 1924 | PD | w05: no usable proofread pages; w15: every sampled page flagged complex (columns/ads) | in works.json, produced 0 lines | layout too complex for line-level labelling |
| Hugging Face: SeyedAli/Persian-OCR (MIT), ordaktaktak/Persian-OCR-230k (MIT), AliShafiee2003/persian-ocr-garshasp-70c (CC BY 4.0), WeightedAI/Persian_OCR_synth_sentences_100k (Apache-2.0) | permissive per metadata | not inspected (huggingface.co is unreachable from the sandbox and was not examined on Actions); names/size suggest synthetic text lines | NOT USED | "real" means scanned/rendered by real software; provenance and label quality unverified. Follow-up candidate: audit garshasp-70c |
| Hugging Face: MR3z4/persian-handwriting-ocr | CC BY-NC-SA 4.0 | handwriting | REJECTED | non-commercial; also handwriting is out of scope |
| Hugging Face: Reza2kn/* (printed-ocr-3.5m, community-dataset ...), mshojaei77/persian-ocr-bench, PersianML/persian-ocr-benchmark | none / other / openrail | unknown provenance | REJECTED | licence unclear or non-standard |
| Zenodo | - | query returned no Persian OCR datasets | none | - |
| archive.org / other digital libraries | - | not searched in depth: OCR text there is not human-verified, and bulk access is not available from the sandbox | NOT USED | OCR text alone is not ground truth |

## Legal risks to read before commercial use
1. Transcriptions are CC BY-SA 4.0: the dataset (labels) must be redistributed under CC BY-SA 4.0 with attribution. Whether a model
   trained on it is a "derivative" is legally unsettled; ask a lawyer before shipping.
2. Most scans are tagged "Public domain" on Commons by the uploader (several are Iranian works from 1933-1977, e.g. w08/w09
   Al-e-Ahmad, w10 Hedayat, w14 Behrangi, w06 Feuvrier translation). Iranian public-domain status and US status can differ; the tag
   was NOT independently verified per work. Works with an explicit open licence: w11, w19 (CC BY-SA 4.0), w12, w21 (CC BY 4.0), w13 (CC0).
3. Page images contain only book pages; no personal data was seen in the 60-line visual check, but no automatic PII scan was run.
