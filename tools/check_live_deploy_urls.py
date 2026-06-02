from urllib.request import Request, urlopen
import sys

URLS = [
    "https://between-potential-and-ideal.onrender.com/",
    "https://between-potential-and-ideal.onrender.com/en.html",
    "https://between-potential-and-ideal.onrender.com/robots.txt",
    "https://between-potential-and-ideal.onrender.com/sitemap.xml",
    "https://between-potential-and-ideal.onrender.com/pages/he/files.html",
    "https://between-potential-and-ideal.onrender.com/pages/en/files-en.html",
    "https://between-potential-and-ideal.onrender.com/pages/he/glossary.html",
    "https://between-potential-and-ideal.onrender.com/pages/en/glossary-en.html",
    "https://between-potential-and-ideal.onrender.com/pages/he/potential-ideal-optimal.html",
    "https://between-potential-and-ideal.onrender.com/pages/en/potential-ideal-optimal-en.html",
    "https://between-potential-and-ideal.onrender.com/pages/he/ai-as-witness.html",
    "https://between-potential-and-ideal.onrender.com/pages/en/ai-as-witness-en.html",
    "https://between-potential-and-ideal.onrender.com/files/appendices/stories-before-thought-hebrew-rtl.html",
    "https://between-potential-and-ideal.onrender.com/files/appendices/stories-before-thought-english.html",
    "https://between-potential-and-ideal.onrender.com/files/ai-believes/what-ai-believes-en.html",
    "https://between-potential-and-ideal.onrender.com/files/ai-believes/what-ai-believes-he.html",
]

def main() -> int:
    errors = []
    for url in URLS:
        try:
            req = Request(url, headers={"User-Agent": "BPI live deploy QA"})
            with urlopen(req, timeout=30) as response:
                status = response.status
                final_url = response.geturl()
                print(status, final_url)
                if status < 200 or status >= 400:
                    errors.append(f"{url}: bad status {status}")
        except Exception as exc:
            errors.append(f"{url}: {exc}")

    if errors:
        print("\nFAIL: live deploy URL check found issues")
        for error in errors:
            print("-", error)
        return 1

    print("\nOK: live deploy URLs are reachable.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
