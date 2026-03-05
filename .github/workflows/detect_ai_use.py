import os, re
PATTERNS = [
  r"\bopenai\b", r"\bazure\s*ai\b", r"\bvertex\s*ai\b", r"\banthropic\b",
  r"\bhuggingface\b", r"\btransformers\b", r"\bllama[-\s]?cpp\b",
  r"\bmlflow\b", r"\bstable[-\s]?diffusion\b", r"\bwhisper\b"
]
RX = re.compile("|".join(PATTERNS), re.IGNORECASE)
hits = []
for root,_,files in os.walk("."):
  if root.startswith("./.git"): continue
  for f in files:
    if f.endswith((".py",".js",".ts",".md",".json",".yml",".yaml",".go",".java",".tf",".sh",".ipynb",".r",".do",".ado")):
      try:
        with open(os.path.join(root,f), "r", encoding="utf-8", errors="ignore") as fh:
          txt = fh.read()
        if RX.search(txt): hits.append(os.path.join(root,f))
      except Exception:
        pass
if hits:
  print("AI usage indicators found in:")
  for h in hits: print(f"- {h}")

