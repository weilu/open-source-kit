import json, os, tomllib

stack = {}
def exists(*names): return any(os.path.exists(n) for n in names)

if exists("package.json"): stack["javascript"] = "node"
if exists("requirements.txt","pyproject.toml","setup.cfg"): stack["python"] = "pip/pyproject"
if exists("pom.xml","build.gradle","build.gradle.kts"): stack["java"] = "maven/gradle"
if exists("go.mod"): stack["go"] = "go modules"
if exists("Cargo.toml"): stack["rust"] = "cargo"
if exists("composer.json"): stack["php"] = "composer"
if exists("Gemfile"): stack["ruby"] = "bundler"
if exists("DESCRIPTION"): stack["r"] = "r (package)"
if any(n.endswith(".do") or n.endswith(".ado") for n in os.listdir(".")): stack["stata"] = "stata"

# extra framework hints
frameworks = []
if os.path.exists("package.json"):
    import json as _json
    try:
        pj = _json.load(open("package.json"))
        deps = (pj.get("dependencies") or {}) | (pj.get("devDependencies") or {})
        for k in deps:
            if k in ("react","next","vue","svelte","vite","angular"): frameworks.append(k)
            if k in ("express","fastify","koa","nest"): frameworks.append(k)
    except Exception: pass

if os.path.exists("pyproject.toml"):
    try:
        py = tomllib.load(open("pyproject.toml","rb"))
        if "tool" in py and "poetry" in py["tool"]: frameworks.append("poetry")
        if "project" in py and "dependencies" in py["project"]:
            for d in py["project"]["dependencies"]:
                if isinstance(d,str) and any(x in d.lower() for x in ("django","fastapi","flask","pydantic")):
                    frameworks.append(d.split()[0])
    except Exception: pass

print(json.dumps({"stack":stack, "framework_hints":sorted(set(frameworks))}, indent=2))

