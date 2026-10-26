"""Fail early on missing dataset resources; does not validate downloaded ASR models."""
import json
import os
from pathlib import Path
base = Path(os.environ.get("ASR_DATASET_DIR", "/app/dataset"))
files = ["model_comparison.json", "vietnamese_dictionary_clean.json"]
files += [f"{stem}_{key}.json" for stem in ("error_statistics", "sentence_analysis") for key in ("whisper", "phowhisper", "wav2vec2")]
problems = []
for name in files:
    path = base / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if name == "vietnamese_dictionary_clean.json" and (not isinstance(value, dict) or not value):
            problems.append(f"{name}: dictionary must be a non-empty JSON object")
    except (OSError, ValueError) as exc:
        problems.append(f"{name}: {exc}")
if not (base / "audio").is_dir():
    problems.append("audio/: directory is missing")
if problems:
    raise SystemExit("DATASET CHECK FAILED:\n" + "\n".join(problems))
print("Dataset files and dictionary found. ASR models are loaded on first request.")
