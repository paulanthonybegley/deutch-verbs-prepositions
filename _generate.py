#!/usr/bin/env python3
"""
Generate the "Verben mit Präpositionen - B1/C1" interactive course.

Reads data/prepositions.json and produces:
  - index.html                     (landing page)
  - <slug>/index.html  (7 self-contained module apps)

Faithful interactive companion to the YouTube shadowing video
"Deutsch lernen B1-C1: 2.000 Sätze mit Verben + Präpositionen | Shadowing"
by "Einfach deutsch, easy deutsch." (https://www.youtube.com/watch?v=x66O3zCSQp8).

Each module app is fully self-contained (no external assets) and provides
Study / Drill / Fill-in-the-blank (preposition) / Quiz modes with Web Speech
(de-DE) audio and localStorage progress.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "data", "prepositions.json"), encoding="utf-8") as f:
    DATA = json.load(f)

CATS = DATA["categories"]
VERBS = DATA["verbs"]

VIDEO_URL = DATA["source"]["url"]
VIDEO_TITLE = DATA["source"]["title"]
CHANNEL = DATA["source"]["channel"]
CHANNEL_URL = DATA["source"]["channel_url"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def verbs_for(cat):
    start = sum(c["verbs"] for c in CATS[: cat["id"] - 1])
    return VERBS[start : start + cat["verbs"]]


INDEX_CSS = open(os.path.join(HERE, "_work", "index.css"), encoding="utf-8").read()


def render_index():
    cards = []
    for c in CATS:
        cards.append(f"""
<div class="card">
  <div class="card-body">
    <div class="num">Modul {c['id']} · {c['verbs']} Verben</div>
    <h3>{c['emoji']} {esc(c['title'])}</h3>
    <p>{esc(c['description'])}</p>
    <div class="meta"><span>🔊 Audio</span><span>🃏 Karten</span><span>🎯 Quiz</span>
      <div class="bar"><div class="fill" id="bar{c['id']}" style="width:0%"></div></div>
      <span id="pct{c['id']}">0%</span>
    </div>
    <a class="btn" href="{c['slug']}/index.html">Start Modul →</a>
  </div>
</div>""")

    total_verbs = sum(c["verbs"] for c in CATS)
    cats_js = json.dumps([{"id": c["id"], "verbs": c["verbs"]} for c in CATS])

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Verben mit Präpositionen – B1–C1 Shadowing-Training</title>
<style>{INDEX_CSS}</style>
</head>
<body>
<header>
  <h1>🔗 Verben mit Präpositionen – B1–C1</h1>
  <p>Trainiere {total_verbs} der wichtigsten Verben mit Präpositionen in 7 interaktiven Modulen – mit Bedeutung, natürlichen Beispielsätzen, Präposition + Kasus und Audio.</p>
</header>
<div class="container">
  <div class="intro">
    <h2>Über diesen Kurs</h2>
    <p>Eine interaktive Begleitung zur YouTube-Shadowing-Episode
    <a href="{VIDEO_URL}" target="_blank" rel="noopener" style="color:var(--red)"><strong>„{esc(VIDEO_TITLE)}“</strong></a>
    von <strong>{esc(CHANNEL)}</strong>. Das Video trainiert Verben mit Präpositionen über 2.000 Sätze zum Nachsprechen (Shadowing). Dieser Kurs verwandelt das passive Mitsprechen in ein aktives Übungsprogramm: Du lernst jedes Verb zusammen mit seiner festen Präposition, dem richtigen Kasus (Akkusativ oder Dativ), einer deutschen Erklärung und zwei natürlichen Beispielsätzen – und sprichst alles mit der Browser-Stimme nach.</p>
    <p style="margin-top:.5rem">Klicke jedes rot unterlegte deutsche Wort an, um es laut zu hören. Dein Fortschritt wird automatisch gespeichert. Die Module sind nach Präposition und Kasus geordnet: mit + Dativ, auf + Akkusativ, an, für/um/gegen, von/bei/aus, über/unter/vor und zu/nach/in.</p>
  </div>
  <div class="course-grid">{''.join(cards)}</div>
  <div class="stats">
    <div class="stat"><b>{total_verbs}</b> Verben + Präpositionen</div>
    <div class="stat"><b>7</b> Module</div>
    <div class="stat"><b>4</b> Übungsarten</div>
    <div class="stat"><b>🔊</b> Deutsche Aussprache</div>
  </div>
  <div class="intro" style="margin-top:1.4rem">
    <h2>🎥 Zur Video-Episode</h2>
    <p>Hör dir zuerst die Sätze im Video an (idealerweise laut nachsprechend) und arbeite danach die Module aktiv durch. Kanal: <a href="{CHANNEL_URL}" target="_blank" rel="noopener" style="color:var(--red)">{esc(CHANNEL)}</a> · Verben werden mit der Browser-Stimme (Deutsch) ausgesprochen.</p>
  </div>
</div>
<footer>
  <p>Basierend auf <a href="{VIDEO_URL}" target="_blank">„{esc(VIDEO_TITLE)}“</a> von {esc(CHANNEL)}</p>
  <p>Kursübersicht <a href="../index.html">deutch-verbs-prepositions</a> · Audio via Web Speech API (de-DE)</p>
</footer>
<script>
const CATS = {cats_js};
function fmt(){{
  CATS.forEach(c=>{{
    const p = parseInt(localStorage.getItem('dvp-progress-'+c.id)||'0',10);
    document.getElementById('pct'+c.id).textContent = Math.round(p)+'%';
    document.getElementById('bar'+c.id).style.width = Math.round(p)+'%';
  }});
}}
fmt();
window.addEventListener('storage', fmt);
</script>
</body>
</html>
"""
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote index.html")


def render_module(catidx):
    c = CATS[catidx]
    verbs = verbs_for(c)
    verbs_js = json.dumps(
        [
            {"v": v["v"], "verb": v["verb"], "prep": v["prep"], "case": v["case"],
             "en": v["en"], "meaning": v["meaning"],
             "example": v["example"], "natural": v["natural"], "grammar": v["grammar"]}
            for v in verbs
        ],
        ensure_ascii=False,
    )

    with open(os.path.join(HERE, "_work", "module.css"), encoding="utf-8") as f:
        module_css = f.read()

    with open(os.path.join(HERE, "_work", "module.js"), encoding="utf-8") as f:
        module_js = f.read()

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Modul {c['id']}: {esc(c['title'])} – Verben mit Präpositionen</title>
<style>{module_css}</style>
</head>
<body>
<div class="topbar"><a href="../index.html">← Kursübersicht</a><span class="title">{c['emoji']} Modul {c['id']}: {esc(c['title'])}</span><span>🔊 de-DE</span></div>
<header class="hdr"><h1>{c['emoji']} {esc(c['title'])}</h1><p>{esc(c['titleEn'])} · {len(verbs)} Verben · B1–C1</p></header>
<div class="container">
  <div class="progressbox">
    <span>Fortschritt</span>
    <div class="bar"><div class="fill" id="progFill" style="width:0%"></div></div>
    <span id="progPct">0%</span>
    <button class="btn ghost" onclick="resetProg()">Zurücksetzen</button>
  </div>

  <div class="tabs">
    <button class="tabbtn active" data-tab="study">📚 Lernen</button>
    <button class="tabbtn" data-tab="drill">🃏 Karten</button>
    <button class="tabbtn" data-tab="fill">✍️ Lücken</button>
    <button class="tabbtn" data-tab="quiz">🎯 Quiz</button>
  </div>

  <section class="panel active" id="panel-study">
    <h2>Lernen</h2>
    <p class="lede">Arbeite die {len(verbs)} Verben mit Präposition dieser Kategorie durch. Klicke ein deutsches Wort, um es zu hören. Der erste grüne Tag zeigt immer die feste Präposition und den Kasus.</p>
    <div id="studyList"></div>
  </section>

  <section class="panel" id="panel-drill">
    <h2>Karten</h2>
    <p class="lede">Sieh das deutsche Verb und überlege, welche Präposition und welcher Kasus dazugehören. Dreh die Karte um, um die Lösung zu sehen.</p>
    <div class="progressbox"><span>Karte</span><span id="drillPos">1 / {len(verbs)}</span><div class="bar"><div class="fill" id="drillFill" style="width:0%"></div></div></div>
    <div class="flipcard" id="flipcard" onclick="flip()">
      <div class="inner">
        <div class="face front">
          <div class="prompt">Welche Präposition?</div>
          <div class="verb" id="drillVerb"></div>
          <div class="en" id="drillEn"></div>
          <div class="hint">Klicke für die Auflösung</div>
        </div>
        <div class="face back">
          <div class="prep" id="drillPrep"></div>
          <div class="sent" id="drillSent"></div>
        </div>
      </div>
    </div>
    <div class="navbtns">
      <button class="btn ghost" onclick="drillPrev()">← Zurück</button>
      <button class="btn" onclick="drillNext()">Weiter →</button>
    </div>
    <p class="empty-note">Karten durchlaufen die Verben in zufälliger Reihenfolge.</p>
  </section>

  <section class="panel" id="panel-fill">
    <h2>Lücken füllen</h2>
    <p class="lede">Vervollständige den Satz mit der passenden Präposition. Wähle die richtige Präposition und klicke auf „Weiter“.</p>
    <div class="progressbox"><span>Frage</span><span id="fillPos">1 / 10</span><div class="bar"><div class="fill" id="fillFill" style="width:0%"></div></div><span>Punkte</span><span id="fillScore">0 / 0</span></div>
    <div id="fillQ"></div>
    <div class="navbtns"><button class="btn ghost" onclick="fillReset()">Neu mischen</button></div>
    <p class="empty-note">10 zufällige Sätze aus dieser Kategorie. Die richtige Präposition wird automatisch erkannt.</p>
  </section>

  <section class="panel" id="panel-quiz">
    <h2>Quiz</h2>
    <p class="lede">10 gemischte Fragetypen: Präposition, Kasus, Übersetzung und Verbwahl. Jede Frage ist oben beschriftet – antworte und klicke auf „Weiter“.</p>
    <div class="progressbox"><span>Frage</span><span id="quizPos">1 / 10</span><div class="bar"><div class="fill" id="quizFill" style="width:0%"></div></div><span>Punkte</span><span id="quizScore">0 / 0</span></div>
    <div id="quizQ"></div>
    <div class="navbtns"><button class="btn ghost" onclick="quizReset()">Neu mischen</button></div>
    <p class="empty-note">10 Fragen, gemischt aus allen {len(verbs)} Verben mit Präposition dieser Kategorie.</p>
  </section>
</div>
<footer style="text-align:center;padding:1.6rem;color:var(--grey);font-size:.88rem">
  <p>Modul {c['id']} von 7 · Basierend auf „{esc(VIDEO_TITLE)}“ ({esc(CHANNEL)}) · <a href="../index.html" style="color:var(--red)">Kursübersicht</a></p>
</footer>
<script>
const VERBS = {verbs_js};
const CATID = {c['id']};
{module_js}
</script>
</body>
</html>
"""
    with open(os.path.join(HERE, c["slug"], "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {c['slug']}/index.html")


if __name__ == "__main__":
    render_index()
    for i in range(len(CATS)):
        render_module(i)
    print("Done.")
