import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 summary.py <file.txt>")
        sys.exit(1)

    p = Path(sys.argv[1])
    text = p.read_text(encoding="utf-8", errors="ignore")

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    words = [w for w in text.split() if w.strip()]

    out = []
    out.append(f"# Summary of {p.name}\n")
    out.append(f"- Lines (non-empty): {len(lines)}")
    out.append(f"- Words: {len(words)}\n")
    out.append("## First 10 non-empty lines\n")
    for i, ln in enumerate(lines[:10], 1):
        out.append(f"{i}. {ln}")

    md = "\n".join(out) + "\n"
    out_path = p.with_suffix(".summary.md")
    out_path.write_text(md, encoding="utf-8")
    print(f"✅ Creato: {out_path}")

if __name__ == "__main__":
    main()
