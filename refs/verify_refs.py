"""Verify reference metadata against Crossref (DOIs) and arXiv. Writes refs/verified.json."""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
DOIS = sys.argv[1].split(",") if len(sys.argv) > 1 else []
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "MM-Book-refcheck/1.0 (mailto:research@example.org)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()
out = {}
for d in DOIS:
    d = d.strip()
    try:
        if d.startswith("arxiv:"):
            x = get("http://export.arxiv.org/api/query?id_list=" + d[6:])
            ns = {"a": "http://www.w3.org/2005/Atom"}
            e = ET.fromstring(x).find("a:entry", ns)
            out[d] = {"title": " ".join(e.find("a:title", ns).text.split()),
                      "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
                      "published": e.find("a:published", ns).text[:10]}
        else:
            m = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(d)))["message"]
            out[d] = {"title": (m.get("title") or [""])[0],
                      "authors": [f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", [])],
                      "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                      "container": (m.get("container-title") or [""])[0], "volume": m.get("volume"),
                      "issue": m.get("issue"), "page": m.get("page"), "article": m.get("article-number"),
                      "publisher": m.get("publisher"), "type": m.get("type")}
    except Exception as ex:
        out[d] = {"ERROR": str(ex)}
    time.sleep(0.3)
prev = {}
try: prev = json.load(open("refs/verified.json"))
except Exception: pass
prev.update(out); json.dump(prev, open("refs/verified.json", "w"), indent=1, ensure_ascii=False)
for d, v in out.items():
    if "ERROR" in v: print("!!", d, v["ERROR"]); continue
    a = v["authors"]; au = "; ".join(a[:3]) + (" et al." if len(a) > 3 else "")
    print(f"{d}\n   {au} ({v.get('year') or v.get('published')}). {v['title']}. {v.get('container','')} {v.get('volume') or ''}({v.get('issue') or ''}) {v.get('page') or v.get('article') or ''}")
