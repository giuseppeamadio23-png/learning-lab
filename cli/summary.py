#!/usr/bin/env python3
import sys
from pathlib import Path

def parse_args(argv):
    top = 10
    files = []

    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            print("Uso: python3 summary.py [--top N] <file1.txt> [file2.txt ...]")
            sys.exit(0)
        elif a in ("--top", "-t"):
            if i + 1 >= len(argv):
                print("❌ Errore: manca il numero dopo --top")
                sys.exit(2)
            try:
                top = int(argv[i + 1])
                if top < 0:
                    raise ValueError
            except ValueError:
                print("❌ Errore: --top deve essere un intero >= 0")
                sys.exit(2)
            i += 2
        else:
            files.append(a)
            i += 1

    if not files:
        print("Uso: python3 summary.py [--top N] <file1.txt> [file2.txt ...]")
        sys.exit(1)

    return top, files


def summarize_file(path: Path, top: int) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    words = [w for w in text.split() if w.strip()]

    out = []
    out.append(f"# Summary of {path.name}\n")
    out.append(f"- Lines (non-empty): {len(lines)}")
    out.append(f"- Words: {len(words)}\n")

    out.append(f"## First {top} non-empty lines\n")
    for idx, ln in enumerate(lines[:top], 1):
        out.append(f"{idx}. {ln}")

    return "\n".join(out) + "\n"


def main():
    top, file_args = parse_args(sys.argv[1:])

    exit_code = 0
    for f in file_args:
        p = Path(f).expanduser()
        if not p.exists():
            print(f"⚠️ File non trovato: {p}")
            exit_code = 1
            continue
        if p.is_dir():
            print(f"⚠️ È una cartella, non un file: {p}")
            exit_code = 1
            continue

        md = summarize_file(p, top)
        out_path = p.with_suffix(p.suffix + ".summary.md")  # es: prova.txt -> prova.txt.summary.md
        out_path.write_text(md, encoding="utf-8")
        print(f"✅ Creato: {out_path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
