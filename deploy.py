"""Deploy the ./vercel folder to Vercel (production) without the Vercel CLI.

Usage:  VERCEL_TOKEN=your_token python3 deploy.py
Create the token at https://vercel.com/account/tokens
"""
import hashlib, json, os, pathlib, sys, urllib.request, urllib.error

PROJECT = "assel-saginayeva-eportfolio"
ROOT = pathlib.Path(__file__).parent / "vercel"
TOKEN = os.environ.get("VERCEL_TOKEN", "").strip()
if not TOKEN:
    import getpass
    TOKEN = getpass.getpass("Paste your Vercel token (it stays hidden) and press Enter: ").strip()
if not TOKEN:
    sys.exit("No token given.")

def call(method, url, data=None, headers=None):
    h = {"Authorization": f"Bearer {TOKEN}"}
    h.update(headers or {})
    req = urllib.request.Request("https://api.vercel.com" + url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            body = r.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"Vercel API error {e.code} on {url}: {e.read().decode()[:500]}")

files = []
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and p.name != ".DS_Store":
        raw = p.read_bytes()
        sha = hashlib.sha1(raw).hexdigest()
        rel = p.relative_to(ROOT).as_posix()
        print(f"uploading {rel} ({len(raw)//1024} KB)")
        call("POST", "/v2/files", raw, {"Content-Type": "application/octet-stream",
             "x-vercel-digest": sha, "Content-Length": str(len(raw))})
        files.append({"file": rel, "sha": sha, "size": len(raw)})

dep = call("POST", "/v13/deployments?skipAutoDetectionConfirmation=1", json.dumps({
    "name": PROJECT, "files": files, "target": "production",
    "projectSettings": {"framework": None, "buildCommand": None, "outputDirectory": None, "installCommand": None},
}).encode(), {"Content-Type": "application/json"})

print("\nDeployment:", "https://" + dep.get("url", "?"))
print("Site (after ~1 min):", f"https://{PROJECT}.vercel.app")
