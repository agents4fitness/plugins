"""Release checks for both plugins. Exit 1 on any failure.

  python plugins/check.py            offline: build, manifests, assets, brand, claude validate (if found)
  python plugins/check.py --online   also: listing URLs resolve; production's OAuth metadata matches each plugin

Set CLAUDE_BIN to the Claude Code binary when `claude` isn't on PATH.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
CLAUDE = ROOT / "claude" / "agents4-coach"
OPENAI = ROOT / "openai" / "agents4-coach"
FAILED = []


def check(ok, what):
    print(("  ok    " if ok else "  FAIL  ") + what)
    if not ok:
        FAILED.append(what)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def bare_brand(text):
    """'Agents4' used as a name without 'Fitness' (identifiers like agents4-coach, AGENTS4_* don't match)."""
    text = re.sub(r"`[^`]*`", "", text)  # code spans hold identifiers and quoted server text
    return re.findall(r"(?<![\w/@.-])Agents4(?![\w-]|\s+Fitness)", text)


def docs_pages():
    """The pages a visitor reads: README, docs/ and the examples (not the generated plugin folders)."""
    paths = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / "examples").rglob("*.md"))]
    return {p: p.read_text(encoding="utf-8") for p in paths}


def anchor(heading):
    """GitHub's anchor for a heading."""
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", text))


def docs(pages, c_market, c_plugin, o_mcp):
    anchors = {p: {anchor(h) for h in re.findall(r"^#{1,6}\s+(.+)$", re.sub(r"```.*?```", "", t, flags=re.S), re.M)}
               for p, t in pages.items()}
    broken = []
    for page, text in pages.items():
        for target in re.findall(r"\]\(([^)\s]+)\)", re.sub(r"```.*?```", "", text, flags=re.S)):
            if re.match(r"[a-z]+:", target):
                continue  # http(s):, mailto:
            path, _, frag = target.partition("#")
            dest = (page.parent / path).resolve() if path else page
            if not dest.exists():
                broken.append(f"{page.name} -> {target}")
            elif frag and dest.suffix == ".md" and frag not in anchors.get(dest, set()):
                broken.append(f"{page.name} -> {target} (no such heading)")
    check(not broken, f"links between the pages resolve ({len(broken)} broken{': ' + '; '.join(broken[:4]) if broken else ''})")

    bad_blocks = []
    for page, text in pages.items():
        for lang, body in re.findall(r"```(\w+)\n(.*?)```", text, flags=re.S):
            try:
                if lang == "json":
                    json.loads(body)
                elif lang == "python":
                    compile(body, f"{page.name} example", "exec")
            except (ValueError, SyntaxError) as exc:
                bad_blocks.append(f"{page.name} {lang}: {exc}")
    check(not bad_blocks, f"json and python examples in the pages parse ({len(bad_blocks)} bad{': ' + '; '.join(bad_blocks[:3]) if bad_blocks else ''})")
    for script in sorted((ROOT / "examples").rglob("*.py")):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
            ok = True
        except SyntaxError:
            ok = False
        check(ok, f"{script.relative_to(ROOT).as_posix()} compiles")

    readme, skills_page = pages[ROOT / "README.md"], pages.get(ROOT / "docs" / "skills.md", "")
    names = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
    missing = [n for n in names if f"`{n}`" not in readme or f"## {n}" not in skills_page]
    check(not missing, f"README and docs/skills.md describe all {len(names)} skills ({'missing: ' + ', '.join(missing) if missing else 'none missing'})")

    everything = "\n".join(pages.values())
    server = o_mcp["oauth_resource"]
    install = f"{c_plugin['name']}@{c_market['name']}"
    check(server in readme and server in pages.get(ROOT / "docs" / "connect.md", ""), f"the pages give the server URL {server}")
    check(f"claude plugin install {install}" in everything and f"codex plugin add {install}" in everything,
          f"the install commands name {install}")
    urls = set(re.findall(r"https://api\.agents4\.com/[\w./?=&-]*", everything))
    known = {server, server + "?profile=coach-compact", "https://api.agents4.com/mcp/claude", "https://api.agents4.com/mcp/oauth",
             "https://api.agents4.com/.well-known/oauth-protected-resource"}
    check(urls <= known, f"no other API address is quoted ({sorted(urls - known) or 'none'})")

    for skill in sorted((ROOT / "examples" / "skills").glob("*/SKILL.md")):
        head = skill.read_text(encoding="utf-8").split("---\n", 2)[1]
        fields = dict(line.split(":", 1) for line in head.splitlines() if ":" in line and not line.startswith(" "))
        check(fields.get("name", "").strip() == skill.parent.name and len(fields.get("description", "").strip()) > 40,
              f"examples/skills/{skill.parent.name}: name matches the folder, description on one line")


def offline():
    print("build")
    check(subprocess.run([sys.executable, str(ROOT / "build.py"), "--check"]).returncode == 0,
          "generated skills match plugins/skills (python plugins/build.py)")

    print("claude code")
    c_plugin, c_market = load(CLAUDE / ".claude-plugin" / "plugin.json"), load(ROOT / ".claude-plugin" / "marketplace.json")
    c_mcp = load(CLAUDE / ".mcp.json")["mcpServers"]["agents4"]
    entry = c_market["plugins"][0]
    check(entry["name"] == c_plugin["name"] and (ROOT / entry["source"]).resolve() == CLAUDE.resolve(),
          f"marketplace '{c_market['name']}' lists {entry['name']} at {entry['source']}")
    check(all(c_plugin.get(k) for k in ("name", "version", "description", "author")), "plugin.json has name/version/description/author")
    check(c_mcp["type"] == "http" and c_mcp["url"].endswith("https://api.agents4.com/mcp/claude}"),
          f"MCP server defaults to the Claude endpoint: {c_mcp['url']}")
    check(c_mcp.get("headers", {}).get("X-Agents4-Key") == "${AGENTS4_API_KEY:-}",
          "optional key header is empty unless AGENTS4_API_KEY is set (OAuth otherwise)")

    print("codex / chatgpt")
    o_plugin, o_market = load(OPENAI / ".codex-plugin" / "plugin.json"), load(ROOT / ".agents" / "plugins" / "marketplace.json")
    o_mcp = load(OPENAI / ".mcp.json")["mcpServers"]["agents4"]
    entry = o_market["plugins"][0]
    check(entry["name"] == o_plugin["name"] and (ROOT / entry["source"]["path"]).resolve() == OPENAI.resolve(),
          f"marketplace '{o_market['name']}' lists {entry['name']} at {entry['source']['path']}")
    check(entry.get("policy", {}).get("authentication") == "ON_INSTALL", "sign-in is requested on install")
    check((OPENAI / o_plugin["skills"]).is_dir() and (OPENAI / o_plugin["mcpServers"]).is_file(),
          "plugin.json skills/ and .mcp.json paths exist")
    ui = o_plugin.get("interface", {})
    required = ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities",
                "websiteURL", "privacyPolicyURL", "termsOfServiceURL", "defaultPrompt", "composerIcon", "logo", "brandColor")
    check(not [k for k in required if not ui.get(k)], f"interface has {', '.join(required)}")
    assets = [ui[k] for k in ("composerIcon", "logo", "logoDark") if ui.get(k)]
    check(all((OPENAI / a).is_file() for a in assets), f"interface assets exist: {assets}")
    check(len(ui.get("shortDescription", "")) <= 80, f"shortDescription is {len(ui.get('shortDescription', ''))} chars")
    check(o_mcp["type"] == "http" and o_mcp["url"] == "https://api.agents4.com/mcp/http?profile=coach-compact",
          f"MCP server uses the compact profile Codex can show in full: {o_mcp['url']}")
    check(o_mcp.get("oauth_resource") == "https://api.agents4.com/mcp/http", "oauth_resource is the /mcp/http resource")

    print("both")
    check(c_plugin["version"] == o_plugin["version"], f"same version ({c_plugin['version']} / {o_plugin['version']})")
    pages = docs_pages()
    copy = [c_plugin["description"], c_plugin.get("displayName", ""), c_market["description"], o_plugin["description"],
            *[str(v) for v in ui.values()], *[p.read_text(encoding="utf-8") for p in (ROOT / "skills").glob("*/SKILL.md")],
            *pages.values(), *[p.read_text(encoding="utf-8") for p in (ROOT / "examples").rglob("*.py")]]
    offenders = [hit for text in copy for hit in bare_brand(text)]
    check(not offenders, f"copy says 'Agents4 Fitness', never bare 'Agents4' ({len(offenders)} bare)")

    print("docs")
    docs(pages, c_market, c_plugin, o_mcp)

    print("files")
    skip = {".git", "__pycache__"}
    texts = [p for p in ROOT.rglob("*") if p.is_file() and not skip & set(p.relative_to(ROOT).parts) and p.suffix != ".png"]
    crlf = [p.relative_to(ROOT).as_posix() for p in texts if b"\r\n" in p.read_bytes()]
    check(not crlf, f"text files use LF line endings ({len(crlf)} with CRLF{': ' + ', '.join(crlf[:4]) if crlf else ''})")
    check((ROOT / ".gitattributes").is_file() and "eol=lf" in (ROOT / ".gitattributes").read_text(encoding="utf-8"),
          ".gitattributes keeps LF on every system")

    claude = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if claude:
        for target in (ROOT, CLAUDE):
            r = subprocess.run([claude, "plugin", "validate", "--strict", str(target)], capture_output=True, text=True)
            check(r.returncode == 0, f"claude plugin validate --strict {target.relative_to(ROOT.parent)}")
    else:
        print("  skip  claude plugin validate (set CLAUDE_BIN)")
    return o_plugin, o_mcp, c_mcp


def get(url, method="GET"):
    req = urllib.request.Request(url, method=method, data=b"{}" if method == "POST" else None,
                                 headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def online(o_plugin, o_mcp, c_mcp):
    print("online")
    ui = o_plugin["interface"]
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        status, _, _ = get(ui[key])
        check(status == 200, f"{key} {ui[key]} -> {status}")
    claude_url = re.search(r":-(https://[^}]+)}", c_mcp["url"]).group(1)
    for name, url, resource in (("codex", o_mcp["url"], o_mcp["oauth_resource"]), ("claude", claude_url, claude_url)):
        status, headers, _ = get(url, "POST")
        challenge = headers.get("WWW-Authenticate", "")
        check(status == 401 and "resource_metadata=" in challenge, f"{name}: {url} asks for sign-in (401 + challenge)")
        meta_url = re.search(r'resource_metadata="([^"]+)"', challenge)
        if meta_url:
            _, _, body = get(meta_url.group(1))
            prm = json.loads(body)
            check(prm.get("resource") == resource, f"{name}: protected resource is {prm.get('resource')}")
            auth = prm["authorization_servers"][0]
            split = urlsplit(auth)
            _, _, body = get(f"{split.scheme}://{split.netloc}/.well-known/oauth-authorization-server{split.path}")
            asm = json.loads(body)
            check(asm.get("registration_endpoint") and "S256" in asm.get("code_challenge_methods_supported", []),
                  f"{name}: authorization server offers client registration and PKCE S256")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    manifests = offline()
    if "--online" in sys.argv:
        online(*manifests)
    print(f"\n{'FAILED: ' + str(len(FAILED)) if FAILED else 'all checks passed'}")
    sys.exit(1 if FAILED else 0)
