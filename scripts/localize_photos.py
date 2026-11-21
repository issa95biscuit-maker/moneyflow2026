"""Télécharge les photos Unsplash référencées dans les pages et les sert depuis assets/photos/."""
import re, glob, os, urllib.request
os.makedirs("assets/photos", exist_ok=True)
URL = re.compile(r'https://images\.unsplash\.com/photo-([0-9a-f-]+)\?w=(\d+)[^"\']*')
cache = {}
for page in glob.glob("*.html"):
    src = open(page, encoding="utf-8").read()
    def repl(m):
        pid, w = m.group(1), m.group(2)
        name = f"assets/photos/{pid}-{w}.jpg"
        if name not in cache:
            if not os.path.exists(name):
                try:
                    req = urllib.request.Request(f"https://images.unsplash.com/photo-{pid}?w={w}&q=72&fm=jpg&fit=crop",
                                                 headers={"User-Agent": "Mozilla/5.0"})
                    data = urllib.request.urlopen(req, timeout=30).read()
                    if len(data) < 2000: raise ValueError("fichier trop petit")
                    open(name, "wb").write(data)
                    print("OK", name, len(data))
                except Exception as e:
                    print("ECHEC", pid, e); cache[name] = None
                    return m.group(0)
            cache[name] = name
        return cache[name] or m.group(0)
    new = URL.sub(repl, src)
    if new != src:
        open(page, "w", encoding="utf-8").write(new)
