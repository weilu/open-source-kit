import sys, re, os
p = "README.md"
if not os.path.exists(p):
    print("::error::Missing README.md"); sys.exit(1)
t = open(p, "r", encoding="utf-8", errors="ignore").read().lower()
req = {
  "installation": re.search(r"\binstall(ation)?\b", t),
  "usage": re.search(r"\busage|how to run|examples?\b", t),
  "features": re.search(r"\bfeatures?\b", t),
  "contributing": re.search(r"\bcontributing|how to contribute\b", t),
}
missing = [k for k,v in req.items() if not v]
if missing:
    print(f"::warning::README missing sections: {', '.join(missing)}")

