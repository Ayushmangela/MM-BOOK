"""Cross-check in-text citations against the reference list in chapter.md (APA author-date)."""
import re, sys, unicodedata
s = open(sys.argv[1] if len(sys.argv) > 1 else "chapter.md", encoding="utf-8").read()
body = s[:s.index("# REFERENCES")]
refs_block = s[s.index("# REFERENCES"):s.index("# ADDITIONAL READING")]
refs = [l[5:] for l in refs_block.splitlines() if l.startswith("@REF ")]
def key_of_ref(r):
    year = re.search(r"\((\d{4}[a-z]?)", r).group(1)
    authors = r[:r.index(" (" + year)]
    if authors.startswith(("European Parliament", "Central Consumer", "Ministry of", "News On AIR", "OpenAI")):
        first = authors.split(".")[0] if not authors.startswith("European") else "European Parliament & Council of the European Union"
        return (first.rstrip("."), year)
    surnames = re.findall(r"(?:^|, |& )([A-ZÄÖÜŻÉ][^\s,]*(?: [a-z]{1,3} [A-Z][^\s,]*)?(?:-[A-Z][^\s,]*)?), [A-Z]\.", authors)
    n = len(re.findall(r", [A-Z]\.", authors))
    if n == 1: k = surnames[0]
    elif n == 2: k = f"{surnames[0]} & {surnames[1]}"
    else: k = f"{surnames[0]} et al."
    return (k, year)
ref_keys = {key_of_ref(r): r for r in refs}
# in-text: parenthetical "(X, 2020; Y & Z, 2021)" and narrative "X (2020)" / "X and Y (2020)"
cites = set()
for grp in re.findall(r"\(([^()]*\d{4}[a-z]?[^()]*)\)", body):
    for part in grp.split(";"):
        m = re.match(r"\s*(?:e\.g\., )?(.+?),\s*(\d{4}[a-z]?)(?:,\s*(\d{4}[a-z]?))*\s*$", part.strip())
        if m:
            name = m.group(1).replace(" and ", " & ")
            for y in re.findall(r"\d{4}[a-z]?", part):
                cites.add((name, y))
for m in re.finditer(r"([A-ZÄÖÜŻ][\w'’\-ıé]+(?: (?:and|&) [A-ZÄÖÜŻ][\w'’\-ıé]+| et al\.)?)(?:'s|’s)? \((\d{4}[a-z]?)(?:, (\d{4}[a-z]?))?\)", body):
    name = m.group(1).replace(" and ", " & ")
    for y in (m.group(2), m.group(3)):
        if y: cites.add((name, y))
cites = {c for c in cites if not re.match(r"^(Figure|Table|Appendix|RQ|P\d)", c[0])}
missing = sorted(c for c in cites if c not in ref_keys)
uncited = sorted(k for k in ref_keys if k not in cites)
print("references:", len(refs), "| distinct in-text citations:", len(cites))
print("CITED BUT NOT IN REFERENCES:", missing)
print("IN REFERENCES BUT NOT CITED:", uncited)
