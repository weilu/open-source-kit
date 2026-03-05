import os
BAD_EXT = {".csv",".tsv",".parquet",".xlsx",".zip",".gz",".jsonl",".feather",".sav",".dta",".rds"}
MAX_INLINE_BYTES = 512 * 1024
violations = []
for root,_,files in os.walk("."):
    if root.startswith("./.git"): continue
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in BAD_EXT:
            path = os.path.join(root,f)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > MAX_INLINE_BYTES:
                violations.append((path,size))
if violations:
    for p,s in violations:
        print(f"::warning::{p} is {s} bytes; consider Git LFS/external storage")
