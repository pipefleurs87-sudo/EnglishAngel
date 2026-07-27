#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUILD — EnglishAngel
Un JSON por tema -> 3 paginas (ejercicios, leccion, examen) con SEO por pagina,
+ index.html con buscador instantaneo, + sitemap.xml + robots.txt.
Uso:  python3 build/build.py
"""
import json, pathlib, html, datetime, re, subprocess, shutil, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MOTOR_EJ = ROOT / "motor" / "motor-generico.html"
MOTOR_LE = ROOT / "motor" / "lecciones-generico.html"
MOTOR_EV = ROOT / "motor" / "evaluacion-generico.html"
TEMPLATE = ROOT / "build" / "index_template.html"
MOTOR_LUD = ROOT / "motor" / "ludoteca-generico.html"
LUDOTECA = ROOT / "ludoteca.html"
JUEGOS = ROOT / "juegos"
CONTENIDO = ROOT / "contenido"
PREVIEW = ROOT / "preview"
LECCION = ROOT / "leccion"
EVAL = ROOT / "evaluacion"
INDEX = ROOT / "index.html"
DATOS = ROOT / "datos"
MOTOR_GEN = ROOT / "motor" / "generador-generico.html"
HERRAMIENTAS = ROOT / "herramientas"
MOTOR_CLASE = ROOT / "motor" / "generador-clases.html"

# Repo real en GitHub: pipefleurs87-sudo/EnglishAngel — publicado en /EnglishAngel/ (corregido 2026-07-16: el sufijo .com rompia todos los canonicals).
BASE_URL = "https://pipefleurs87-sudo.github.io/EnglishAngel"

NIVEL_ORDEN = ["A1", "A2", "B1", "B2", "C1", "C2"]
ARQ_GRAMATICALES = {"tiempo_verbal","determinantes","pronombres","comparativos","clausulas_relativas","modales"}
FORMAS_REQUERIDAS = ["afirmativo","negativo","interrogativo","short_answer"]

ETAPAS = {
    "Recognize": ["multiple_choice", "true_false"],
    "Manipulate": ["gap_fill", "unscramble", "correct_mistake"],
    "Transform": ["transformation", "write_opposite", "short_answer_production"],
}

def revisar_etapas(data):
    # Regla (2026-07-10): secuencias A2+ llevan minimo 5 ejercicios por etapa cognitiva.
    if data.get("nivel") == "A1": return
    tipos = [e.get("tipo") for e in data.get("fases", {}).get("practica", {}).get("ejercicios", [])]
    for etapa, tt in ETAPAS.items():
        n = sum(tipos.count(t) for t in tt)
        if n < 5: print("  !  " + data["id"] + " — etapa " + etapa + " con " + str(n) + " ejercicios (minimo 5)")

def revisar_formas(data):
    if data.get("arquetipo") not in ARQ_GRAMATICALES: return
    formas = {o.get("forma") for o in data.get("banco_oraciones", [])}
    faltan = [f for f in FORMAS_REQUERIDAS if f not in formas]
    if faltan: print("  !  " + data["id"] + " — banco SIN formas: " + ", ".join(faltan))

def area_de(data):
    t = data.get("tema","").lower()
    pairs = [("advanced passive","Passive Voice"),
        ("subjunctive","Subjunctive"),("cleft","Cleft Sentences"),("inversion","Inversion"),
        ("gerund clause","Gerund Clauses as Subject"),("participle clause","Participle Clauses"),
        ("emphatic","Emphatic Structures"),("future in the past","Future in the Past"),
        ("ellipsis","Ellipsis & Substitution"),("would rather","Modals"),
        ("register & style","Register & Style"),
        ("reported speech","Reported Speech"),("causative","Causative"),
        ("if only","Wishes & Regrets"),("wish","Wishes & Regrets"),
        ("phrasal verb","Phrasal Verbs"),("linking word","Linkers"),("idiom","Idioms"),
        ("review","Review"),("present simple","Present Simple"),("present continuous","Present Continuous"),
        ("past simple","Past Simple"),("verb to be","Verb To Be"),("would like","Modals"),
        ("have to","Modals"),("modal","Modals"),("relative clause","Relative Clauses"),
        ("preposition","Prepositions"),("object pronoun","Pronouns & Possessives"),
        ("pronoun","Pronouns & Possessives"),("possessive","Possessives"),("family","Possessives"),
        ("this / that","Determiners"),("demonstr","Determiners"),("wh-","Questions"),
        ("question","Questions"),("article","Articles"),("plural","Nouns"),
        ("adjective","Adjectives"),("there is","There is/are"),("comparative","Comparatives"),
        ("superlative","Comparatives"),
        ("present perfect continuous","Present Perfect Continuous"),("present perfect","Present Perfect"),
        ("will vs going to","Will vs Going To"),("going to","Going To"),("have got","Have Got"),
        ("conditional","Conditionals"),("countable","Countable & Uncountable"),
        ("gerund","Gerund vs Infinitive"),("infinitive","Gerund vs Infinitive"),
        ("imperative","Imperatives"),("passive","Passive Voice"),("used to","Used To")]
    for k,v in pairs:
        if k in t: return v
    return data.get("nivel","")

# Titulos hibridos: la data de Trends (jul 2026, MX/CO) muestra que se busca en espanol
# ("ejercicios de ingles" 2:1 sobre "english exercises") pero nombrando el tema en ingles
# o en espanol segun el termino. El titulo captura ambas corrientes: "Past Simple (pasado simple)".
AREA_ES = {"Present Simple":"presente simple","Present Continuous":"presente continuo",
    "Past Simple":"pasado simple","Verb To Be":"verbo to be","Modals":"verbos modales",
    "Relative Clauses":"oraciones relativas","Prepositions":"preposiciones",
    "Pronouns & Possessives":"pronombres en ingles","Possessives":"posesivos",
    "Determiners":"demostrativos","Questions":"preguntas en ingles","Articles":"articulos en ingles",
    "Nouns":"sustantivos y plurales","Adjectives":"adjetivos en ingles",
    "There is/are":"there is y there are","Comparatives":"comparativos y superlativos",
    "Review":"repaso de ingles","Present Perfect":"presente perfecto","Present Perfect Continuous":"presente perfecto continuo",
    "Will vs Going To":"will vs going to","Going To":"futuro con going to","Have Got":"have got",
    "Conditionals":"condicionales en ingles","Countable & Uncountable":"contables e incontables",
    "Gerund vs Infinitive":"gerundio e infinitivo","Imperatives":"imperativos en ingles",
    "Passive Voice":"voz pasiva en ingles","Used To":"used to (habitos pasados)",
    "Reported Speech":"estilo indirecto","Causative":"causativo (mandar a hacer algo)",
    "Wishes & Regrets":"deseos y arrepentimientos","Phrasal Verbs":"phrasal verbs (verbos con particula)",
    "Linkers":"conectores en ingles","Idioms":"modismos en ingles",
    "Subjunctive":"modo subjuntivo en ingles","Cleft Sentences":"oraciones hendidas (cleft sentences)",
    "Inversion":"inversion enfatica","Gerund Clauses as Subject":"gerundio como sujeto",
    "Participle Clauses":"clausulas de participio","Emphatic Structures":"estructuras enfaticas",
    "Future in the Past":"futuro en el pasado","Ellipsis & Substitution":"elipsis y sustitucion",
    "Register & Style":"registro y estilo en ingles"}

def titulo_hibrido(tema, area):
    es = AREA_ES.get(area)
    if es and es.lower() not in tema.lower():
        return tema + " (" + es + ")"
    return tema

def esc(s):
    return html.escape(str(s), quote=True)

def seo_head(title, desc, keywords, jsonld, canonical=""):
    b = "<title>" + esc(title) + "</title>\n"
    b += '<meta name="description" content="' + esc(desc) + '">\n'
    b += '<meta name="keywords" content="' + esc(keywords) + '">\n'
    b += '<meta property="og:title" content="' + esc(title) + '">\n'
    b += '<meta property="og:description" content="' + esc(desc) + '">\n'
    b += '<meta property="og:type" content="article">\n'
    b += '<meta property="og:image" content="' + BASE_URL + '/og-image.png">\n'
    b += '<meta name="twitter:card" content="summary_large_image">\n'
    b += '<meta name="robots" content="index, follow">\n'
    if canonical:
        b += '<link rel="canonical" href="' + esc(canonical) + '">\n'
        b += '<meta property="og:url" content="' + esc(canonical) + '">\n'
    b += '<script type="application/ld+json">' + jsonld + '</script>'
    return b

def prerender_texto(data):
    # Bloque de texto plano con el contenido REAL de la secuencia (sin widgets interactivos).
    # Motivo: hoy el HTML crudo solo trae el JSON embebido -- todo el contenido visible lo arma
    # JavaScript en el navegador. Los bots de IA (GPTBot, ClaudeBot, etc.) no ejecutan JS, y el
    # rastreo normal de Google lo hace en una segunda pasada que puede tardar dias/semanas.
    # Este bloque se inyecta en el contenedor que el JS ya vacia y reconstruye al cargar
    # (app.innerHTML='' / deck.innerHTML=slides.join('')), asi que no cambia NADA para el
    # usuario real -- se reemplaza al instante. Cero cambios al JS existente.
    F = data.get("fases", {})
    inicio = F.get("inicio", {})
    parts = []
    parts.append("<h1>" + esc(data.get("tema", "")) + "</h1>")
    habs = ", ".join(data.get("habilidades", []))
    parts.append("<p><em>" + esc(data.get("nivel", "")) + (" — " + esc(habs) if habs else "") + "</em></p>")

    interaccion = inicio.get("interaccion")
    if isinstance(interaccion, list) and interaccion:
        for linea in interaccion:
            bold = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", esc(linea))
            parts.append("<p>" + bold + "</p>")

    banner = inicio.get("banner_diagnostico")
    if banner:
        a, b, correcta = banner.get("opcion_a", ""), banner.get("opcion_b", ""), banner.get("correcta")
        right = a if correcta == "a" else b
        wrong = b if correcta == "a" else a
        parts.append("<p>Common mistake: \u201c" + esc(wrong) + "\u201d — Correct: \u201c" + esc(right) + "\u201d</p>")

    if inicio.get("definicion_pragmatica"):
        parts.append("<p><em>" + esc(inicio["definicion_pragmatica"]) + "</em></p>")

    tabla = inicio.get("tabla")
    if tabla and isinstance(tabla.get("filas"), list):
        parts.append("<table>")
        if tabla.get("titulo"): parts.append("<caption>" + esc(tabla["titulo"]) + "</caption>")
        heads = tabla.get("encabezados", [])
        if heads: parts.append("<tr>" + "".join("<th>" + esc(h) + "</th>" for h in heads) + "</tr>")
        for fila in tabla["filas"]:
            parts.append("<tr>" + "".join("<td>" + esc(c) + "</td>" for c in fila) + "</tr>")
        parts.append("</table>")

    if inicio.get("vocab_warmup") and isinstance(data.get("vocabulario"), list) and data["vocabulario"]:
        parts.append("<ul>")
        for v in data["vocabulario"]:
            if v.get("pais"):
                parts.append("<li>" + esc(v.get("bandera", "")) + " " + esc(v["pais"]) + " — " + esc(v.get("nacionalidad", "")) + "</li>")
            else:
                parts.append("<li>" + esc(v.get("bandera", "")) + " " + esc(v.get("palabra", "")) + " — " + esc(v.get("traduccion", "")) + "</li>")
        parts.append("</ul>")

    banco = data.get("banco_oraciones")
    if isinstance(banco, list) and banco:
        parts.append("<ul>")
        for o in banco:
            parts.append("<li>" + esc(o.get("oracion", "")) + "</li>")
        parts.append("</ul>")

    ejercicios = F.get("practica", {}).get("ejercicios", [])
    if ejercicios:
        parts.append("<h2>Practice</h2><ol>")
        for ex in ejercicios:
            t = ex.get("tipo")
            if t == "multiple_choice":
                txt = ex.get("pregunta", "") + " (" + ", ".join(ex.get("opciones", [])) + ")"
            elif t == "true_false":
                txt = ex.get("afirmacion", "")
            elif t == "gap_fill":
                txt = ex.get("texto", "")
            elif t == "unscramble":
                txt = "Unscramble: " + ", ".join(ex.get("palabras", []))
            elif t == "correct_mistake":
                txt = "Find the mistake: " + ex.get("texto_con_error", "")
            elif t in ("transformation", "write_opposite"):
                txt = ex.get("oracion_base", "") + " — " + ex.get("instruccion", "")
            elif t == "short_answer_production":
                txt = ex.get("pregunta", "")
            else:
                txt = ""
            parts.append("<li>" + esc(txt) + "</li>")
        parts.append("</ol>")

    listening = F.get("listening", {})
    if isinstance(listening.get("guion"), list) and listening["guion"]:
        parts.append("<h2>Listening</h2>")
        for linea in listening["guion"]:
            parts.append("<p>" + esc(linea) + "</p>")

    reading = F.get("reading", {})
    if reading.get("texto"):
        parts.append("<h2>Reading</h2><p>" + esc(reading["texto"]) + "</p>")
        preguntas = reading.get("preguntas", [])
        if preguntas:
            parts.append("<ul>")
            for pr in preguntas:
                parts.append("<li>" + esc(pr.get("afirmacion", "")) + "</li>")
            parts.append("</ul>")

    return "".join(parts)

def inyectar(motor_txt, data, title, desc, keywords, jsonld, modo="ejercicios", canonical=""):
    ld = json.dumps(jsonld, ensure_ascii=False)
    head = seo_head(title, desc, keywords, ld, canonical)
    page = re.sub(r"<title>.*?</title>", lambda m: head, motor_txt, count=1)
    payload = json.dumps(data, ensure_ascii=False)
    page = page.replace("<body>", "<body>\n<script>window.SEQUENCE_DATA = " + payload + ";</script>", 1)
    pre = prerender_texto(data)
    if modo == "leccion":
        anchor = '<div class="deck" id="deck"></div>'
        assert page.count(anchor) == 1, "deck anchor no encontrado en " + data.get("id", "?")
        page = page.replace(anchor, '<div class="deck" id="deck">' + pre + '</div>', 1)
    else:
        anchor = '<div class="wrap" id="app"><div class="empty">No content loaded.</div></div>'
        assert page.count(anchor) == 1, "app anchor no encontrado en " + data.get("id", "?")
        page = page.replace(anchor, '<div class="wrap" id="app">' + pre + '</div>', 1)
    # navegacion compartida: un solo archivo controla los enlaces de modo de todas las paginas
    if "js/ea-nav.js" not in page:
        assert page.count("</body>") == 1, "body de cierre no encontrado en " + data.get("id", "?")
        page = page.replace("</body>", '<script src="../js/ea-nav.js"></script>\n</body>', 1)
    return page

def jsonld_for(data, area, rtype):
    return {"@context":"https://schema.org","@type":"LearningResource",
        "name":data["tema"],"educationalLevel":data["nivel"],"inLanguage":"en",
        "learningResourceType":rtype,"isAccessibleForFree":True,"teaches":area,
        "provider":{"@type":"Person","name":"Felipe - EnglishAngel"}}

def build_por_tema():
    for d in (PREVIEW, LECCION, EVAL): d.mkdir(exist_ok=True)
    m_ej = MOTOR_EJ.read_text(encoding="utf-8")
    m_le = MOTOR_LE.read_text(encoding="utf-8")
    m_ev = MOTOR_EV.read_text(encoding="utf-8")
    seqs = []
    for jf in sorted(CONTENIDO.rglob("*.json")):
        data = json.loads(jf.read_text(encoding="utf-8"))
        revisar_formas(data)
        revisar_etapas(data)
        tema = data["tema"]; niv = data["nivel"]; area = area_de(data)
        th = titulo_hibrido(tema, area)
        es = AREA_ES.get(area, "")
        kw = tema + " exercises, English grammar, " + area + ", " + niv + " English, ESL, ejercicios de ingles" + ((", ejercicios " + es + ", " + es) if es else "")
        # ejercicios -- titulos/descripciones acortados (Google trunca titulo ~60px/60car, desc ~155car)
        t = th + " — " + niv + " Exercises | EnglishAngel"
        de = tema + " — " + niv + " English exercises: grammar, listening and reading in one sequence. Ejercicios de " + (es if es else "ingles") + " gratis."
        (PREVIEW/(data["id"]+".html")).write_text(inyectar(m_ej,data,t,de,kw,jsonld_for(data,area,"exercise"),"ejercicios",BASE_URL+"/preview/"+data["id"]+".html"),encoding="utf-8")
        # leccion
        t = th + " — " + niv + " Video Lesson | EnglishAngel"
        de = "Video lesson: " + tema + " (" + niv + "). Clear rules, examples and guided practice. Leccion de " + (es if es else "ingles") + " gratis."
        (LECCION/(data["id"]+".html")).write_text(inyectar(m_le,data,t,de,kw,jsonld_for(data,area,"lesson"),"leccion",BASE_URL+"/leccion/"+data["id"]+".html"),encoding="utf-8")
        # examen
        t = th + " — " + niv + " Test | EnglishAngel"
        de = tema + " — " + niv + " test: check your grammar with instant scoring. Examen de " + (es if es else "ingles") + " gratis."
        (EVAL/(data["id"]+".html")).write_text(inyectar(m_ev,data,t,de,kw,jsonld_for(data,area,"quiz"),"examen",BASE_URL+"/evaluacion/"+data["id"]+".html"),encoding="utf-8")
        data["_area"] = area
        seqs.append(data)
        print("  OK  " + data["id"] + "  (3 paginas + SEO)")
    return seqs

def build_ea_nav():
    """Genera js/ea-nav.js desde motor/ea-nav.js.

    La lista de temas con fluidez se deriva de /fluency, no de /contenido: los JSON
    de contenido no tienen bloque fases.fluency (0 de 81), asi que el directorio
    publicado es la unica fuente de verdad disponible.
    """
    plantilla = ROOT / "motor" / "ea-nav.js"
    destino = ROOT / "js" / "ea-nav.js"
    ids = sorted(f.stem for f in (ROOT / "fluency").glob("*.html"))
    txt = plantilla.read_text(encoding="utf-8")
    assert "{{FLUENCY_IDS}}" in txt, "motor/ea-nav.js no tiene el marcador {{FLUENCY_IDS}}"
    txt = txt.replace("{{FLUENCY_IDS}}", json.dumps(ids, ensure_ascii=False))
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(txt, encoding="utf-8")
    print("  OK  js/ea-nav.js (" + str(len(ids)) + " temas con fluidez)")


# ============================================================
# Ludoteca
# ============================================================
# El motor de la ludoteca lee window.EA_POOL, no window.SEQUENCE_DATA, asi que
# necesita su propia inyeccion. slim_pool() es la UNICA funcion que conoce las
# tres formas de "vocabulario" que hay en el contenido; el motor nunca ve esa
# heterogeneidad.

def _vocab_items(data):
    """Normaliza las tres formas de vocabulario a {w, tr, f}."""
    out = []
    for it in (data.get("vocabulario") or []):
        if not isinstance(it, dict):
            continue
        if "palabra" in it:
            w = str(it.get("palabra", "")).strip()
            tr = str(it.get("traduccion", "")).strip()
        elif "nacionalidad" in it:
            # el pais es la cara visible y la nacionalidad la respuesta, no al reves
            w = str(it.get("pais", "")).strip()
            tr = str(it.get("nacionalidad", "")).strip()
        else:
            continue
        if not w or not tr:
            continue
        # "bandera" no siempre es una bandera: en los verbos irregulares lleva el
        # patron vocalico (i-o-en). Se emite siempre, vacia si no hay.
        out.append({"w": w, "tr": tr, "f": it.get("bandera", "") or ""})
    return out


# --- Banco de pistas EN INGLES -------------------------------------------
# Regla dura: si no hay pista en ingles, la palabra NO entra. Nunca se cae de
# vuelta al espanol. Es mejor tener menos cartas que cartas con traduccion.
#
# Dos fuentes, ambas verificadas a mano:
#   1. Los tres temas de clausulas relativas, donde "traduccion" NO es espanol
#      sino la definicion ("Actor" -> "acts in films"), y el banco de oraciones
#      da el molde exacto.
#   2. Cualquier oracion del MISMO tema que contenga la palabra: se tapa y ya
#      es una pista en ingles. Cuando la oracion es definitoria
#      ("My mother's mother is my grandmother") sale justo el formato que
#      queria Felipe, sin escribir nada.

MOLDES_DEF = {
    "a1-relative-clauses-professions-01": "A {w} is a person who {d}.",
    "a1-relative-clauses-objects-01":     "A {w} is a thing that you use to {d}.",
    "a1-relative-clauses-places-01":      "A {w} is a place where you {d}.",
}

def _partir_compuesta(w):
    """'mother / father' -> ['mother','father'];  'drink · drank · drunk' -> ['drink']"""
    w = str(w).strip()
    if "·" in w:
        return [w.split("·")[0].strip()]      # verbos irregulares: solo el infinitivo
    if "/" in w:
        return [x.strip() for x in w.split("/") if x.strip()]
    if "→" in w:
        return [w.split("→")[0].strip()]
    return [w]


def build_pistas(seqs):
    """Devuelve la lista 'd' del pool: pistas en ingles, una por palabra."""
    out = []
    for data in seqs:
        tid, niv = data["id"], data["nivel"]
        frases = [str(o.get("oracion", "")).strip()
                  for o in (data.get("banco_oraciones") or []) if o.get("oracion")]
        molde = MOLDES_DEF.get(tid)
        for it in (data.get("vocabulario") or []):
            if not isinstance(it, dict):
                continue
            bruto = it.get("palabra") or it.get("nacionalidad") or ""
            defin = it.get("traduccion") or ""
            emo = it.get("bandera", "") or ""
            for w in _partir_compuesta(bruto):
                if not w or not re.match(r"^[A-Za-z][A-Za-z' -]*$", w):
                    continue
                pista, clase = None, None
                if molde and defin:
                    pista = molde.format(w="______", d=defin)
                    clase = "def"
                else:
                    rx = re.compile(r"\b" + re.escape(w) + r"\b", re.I)
                    cand = [f for f in frases if rx.search(f)]
                    # se prefiere la oracion definitoria: la que termina en la palabra
                    cand.sort(key=lambda f: (not rx.search(f.rstrip(".?!").split()[-1] if f.split() else ""), len(f)))
                    if cand:
                        pista = rx.sub("______", cand[0], count=1)
                        clase = "sent"
                if not pista:
                    continue
                e = {"n": niv, "t": tid, "w": w, "c": pista, "k": clase}
                if emo and len(emo) <= 4:
                    e["f"] = emo
                out.append(e)

    # Marca de univocidad. Una pista sacada de una oracion suele admitir otras
    # palabras del mismo tema ("They are ______ students" acepta tall, smart,
    # friendly...). Eso la inhabilita para pedir que el estudiante PRODUZCA la
    # palabra, pero sirve perfectamente con opciones o con el emoji al lado.
    # Las definiciones de clausula relativa si son univocas.
    por_tema = {}
    for e in out:
        por_tema.setdefault(e["t"], set()).add(e["w"].lower())
    for e in out:
        if e["k"] == "def":
            e["u"] = 1                       # univoca: vale para producir
        else:
            otras = por_tema[e["t"]] - {e["w"].lower()}
            e["u"] = 0 if otras else 1
    return out


def slim_pool(seqs, solo_id=None):
    fuente = [d for d in seqs if solo_id is None or d["id"] == solo_id]
    q, v, s_, u = [], [], [], []
    for d in fuente:
        tid, niv = d["id"], d["nivel"]
        for ex in ((d.get("fases") or {}).get("practica") or {}).get("ejercicios", []):
            t = ex.get("tipo")
            if t == "multiple_choice" and ex.get("opciones"):
                q.append({"n": niv, "t": tid, "q": ex.get("pregunta", ""),
                          "o": list(ex["opciones"]), "a": ex.get("respuesta", "")})
            elif t == "true_false" and ex.get("afirmacion"):
                # los verdadero/falso son preguntas de dos opciones: sirven igual
                q.append({"n": niv, "t": tid, "q": ex["afirmacion"],
                          "o": ["True", "False"],
                          "a": "True" if str(ex.get("respuesta")).lower() == "true" else "False"})
            elif t == "unscramble" and ex.get("palabras"):
                # los signos sueltos ("?", ".") no son fichas jugables
                ws = [w for w in ex["palabras"] if str(w).strip(" .,;:!?")]
                if len(ws) >= 3:
                    u.append({"n": niv, "t": tid, "w": ws, "a": ex.get("respuesta", "")})
        for e in _vocab_items(d):
            e2 = {"n": niv, "t": tid}; e2.update(e); v.append(e2)
        for o in (d.get("banco_oraciones") or []):
            txt = str(o.get("oracion", "")).strip()
            if txt:
                s_.append({"n": niv, "t": tid, "s": txt})

    if solo_id is None:
        pool = {"modo": "hub",
                "temas": [{"id": d["id"], "nivel": d["nivel"], "tema": d["tema"],
                           "area": d.get("_area", "")} for d in seqs]}
    else:
        d = fuente[0]
        pool = {"modo": "tema", "id": d["id"], "tema": d["tema"], "nivel": d["nivel"],
                "area": d.get("_area", ""),
                "flu": (ROOT / "fluency" / (d["id"] + ".html")).exists()}
    d_ = [x for x in build_pistas(fuente)]
    pool.update({"q": q, "v": v, "s": s_, "u": u, "d": d_})
    return pool


def inyectar_pool(motor_txt, pool, prerender, title, desc, keywords, jsonld, canonical="", css_rel="css/ea-ludoteca.css"):
    """Hermana de inyectar(). Mismo patron, pero con EA_POOL y sin tocar inyectar()."""
    ld = json.dumps(jsonld, ensure_ascii=False)
    head = seo_head(title, desc, keywords, ld, canonical)
    page = re.sub(r"<title>.*?</title>", lambda m: head, motor_txt, count=1)
    payload = json.dumps(pool, ensure_ascii=False, separators=(",", ":"))
    page = page.replace("<body>", "<body>\n<script>window.EA_POOL = " + payload + ";</script>", 1)
    anchor = '<div class="wrap" id="app"><div class="empty">No content loaded.</div></div>'
    assert page.count(anchor) == 1, "ancla de la ludoteca no encontrada"
    page = page.replace(anchor, '<div class="wrap" id="app">' + prerender + "</div>", 1)
    # la hoja compartida cuelga de la raiz, asi que la ruta cambia segun donde viva la pagina
    page = page.replace('href="../css/ea-ludoteca.css"', 'href="' + css_rel + '"', 1)
    return page


def prerender_ludoteca_tema(data, area):
    p = ['<h1>' + esc(data["tema"]) + ' &mdash; juegos</h1>']
    p.append('<p><em>' + esc(data["nivel"]) + ' &middot; ' + esc(area) + '</em></p>')
    p.append('<p>Practica este tema jugando: vocabulario, orden de palabras y gramatica a contrarreloj.</p>')
    p.append('<p><a href="../leccion/' + data["id"] + '.html">Leccion</a> &middot; '
             '<a href="../preview/' + data["id"] + '.html">Ejercicios</a> &middot; '
             '<a href="../evaluacion/' + data["id"] + '.html">Examen</a></p>')
    return "".join(p)


def prerender_ludoteca_hub(seqs):
    p = ['<h1>Ludoteca EnglishAngel</h1>',
         '<p>Juegos de ingles por tema y por nivel: vocabulario, gramatica y orden de palabras. '
         'Todo el material sale de las 81 secuencias del curso.</p>', '<ul>']
    for d in seqs:
        p.append('<li><a href="juegos/' + d["id"] + '.html">' + esc(d["tema"]) +
                 '</a> <em>' + esc(d["nivel"]) + '</em></li>')
    p.append("</ul>")
    return "".join(p)


def build_ludoteca_pool(seqs):
    pool = slim_pool(seqs)
    (DATOS / "ludoteca-pool.json").write_text(
        json.dumps(pool, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  OK  datos/ludoteca-pool.json (" + str(len(pool["q"])) + " q, " +
          str(len(pool["v"])) + " v, " + str(len(pool["s"])) + " s, " +
          str(len(pool["u"])) + " u, " + str(len(pool["d"])) + " pistas EN)")


def build_ludoteca(seqs):
    JUEGOS.mkdir(exist_ok=True)
    motor = MOTOR_LUD.read_text(encoding="utf-8")

    # hub
    t = "Ludoteca — juegos de ingles por nivel | EnglishAngel"
    de = "Juegos de ingles gratis por tema y nivel CEFR: vocabulario, gramatica y orden de palabras. 81 temas, del A1 al C1."
    kw = "juegos de ingles, aprender ingles jugando, vocabulario ingles, gramatica inglesa, ESL games"
    ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Ludoteca EnglishAngel",
          "applicationCategory": "EducationalApplication", "inLanguage": "en", "isAccessibleForFree": True,
          "provider": {"@type": "Person", "name": "Felipe - EnglishAngel"}}
    LUDOTECA.write_text(
        inyectar_pool(motor, slim_pool(seqs), prerender_ludoteca_hub(seqs), t, de, kw, ld,
                      BASE_URL + "/ludoteca.html", css_rel="css/ea-ludoteca.css"),
        encoding="utf-8")
    print("  OK  ludoteca.html (hub)")

    # una pagina por tema
    for d in seqs:
        area = d.get("_area", "")
        th = titulo_hibrido(d["tema"], area)
        t = th + " — " + d["nivel"] + " Games | EnglishAngel"
        de = d["tema"] + " — " + d["nivel"] + " English games: vocabulary, grammar and word order. Juegos de ingles gratis."
        kw = d["tema"] + " games, English games, " + area + ", " + d["nivel"] + " English, juegos de ingles"
        ld = jsonld_for(d, area, "game")
        (JUEGOS / (d["id"] + ".html")).write_text(
            inyectar_pool(motor, slim_pool(seqs, d["id"]), prerender_ludoteca_tema(d, area),
                          t, de, kw, ld, BASE_URL + "/juegos/" + d["id"] + ".html",
                          css_rel="../css/ea-ludoteca.css"),
            encoding="utf-8")
    print("  OK  juegos/ (" + str(len(seqs)) + " paginas)")


def build_index(seqs):
    niveles = [n for n in NIVEL_ORDEN if any(s["nivel"]==n for s in seqs)]
    chips = '<span class="chip-f on" data-level="all">All</span>'
    for n in niveles:
        chips += '<span class="chip-f" data-level="'+n+'">'+n+'</span>'
    # ordenar por nivel y luego por area/tema para lectura agradable
    seqs_sorted = sorted(seqs, key=lambda s:(NIVEL_ORDEN.index(s["nivel"]), s["_area"], s["tema"]))
    cards = []
    for s in seqs_sorted:
        habs = "".join('<span class="chip">'+html.escape(h)+'</span>' for h in s.get("habilidades",[]))
        n_ej = len(s.get("fases",{}).get("practica",{}).get("ejercicios",[]))
        search = " ".join([s["tema"], s["_area"], s.get("arquetipo",""), s["nivel"], "exercises"] + s.get("habilidades",[])).lower()
        cards.append(
            '<div class="card" data-level="'+s["nivel"]+'" data-search="'+html.escape(search)+'">'
            '<div class="card-area">'+html.escape(s["_area"])+' · '+s["nivel"]+'</div>'
            '<div class="card-tema">'+html.escape(s["tema"])+'</div>'
            '<div class="card-meta">'+str(n_ej)+' exercises · sequence + video + test</div>'
            '<div class="chips">'+habs+'</div>'
            '<div class="actions">'
            '<a class="act primary" href="preview/'+s["id"]+'.html">Exercises</a>'
            '<a class="act" href="leccion/'+s["id"]+'.html">&#9654; Lesson</a>'
            '<a class="act" href="evaluacion/'+s["id"]+'.html">&#9998; Test</a>'
            '</div></div>')
    doc = TEMPLATE.read_text(encoding="utf-8")
    doc = doc.replace("{{CHIPS}}", chips).replace("{{CARDS}}", "".join(cards))
    doc = doc.replace("{{TOTAL}}", str(len(seqs))).replace("{{FECHA}}", datetime.date.today().isoformat())
    doc = doc.replace("{{BASE_URL}}", BASE_URL)
    INDEX.write_text(doc, encoding="utf-8")
    print("  OK  index.html (buscador + " + str(len(seqs)) + " temas)")

def build_banco_maestro(seqs):
    # Indice plano de TODOS los ejercicios ya generados, para el generador a la carta
    # (herramientas/generador-ejercicios.html). No genera contenido nuevo -- solo
    # recombina lo que ya existe en /contenido, asi que sigue siendo 100% estatico ($0 hosting).
    items = []
    for s in seqs:
        base = {"nivel": s["nivel"], "tema": s["tema"], "tema_id": s["id"], "area": s.get("_area", ""), "arquetipo": s.get("arquetipo", "")}
        for ex in s.get("fases", {}).get("practica", {}).get("ejercicios", []):
            tipo = ex.get("tipo")
            etapa = None
            for et, tt in ETAPAS.items():
                if tipo in tt: etapa = et
            items.append(dict(base, tipo=tipo, etapa=etapa or "Other",
                combina=ex.get("combina", []), ejercicio=ex))
        rd = s.get("fases", {}).get("reading", {})
        if rd.get("texto"):
            items.append(dict(base, tipo="reading_comprehension", etapa="Reading",
                combina=[], ejercicio={"texto": rd["texto"], "preguntas": rd.get("preguntas", [])}))
    DATOS.mkdir(exist_ok=True)
    payload = json.dumps(items, ensure_ascii=False)
    (DATOS/"banco-maestro.json").write_text(payload, encoding="utf-8")
    print("  OK  datos/banco-maestro.json (" + str(len(items)) + " items)")
    # Inyecta el mismo payload directo en el HTML (igual que window.SEQUENCE_DATA en los otros
    # motores) para que Felipe pueda abrir el archivo con doble clic sin servidor local --
    # fetch() de JSON no funciona bajo file:// en Chrome/Edge, esto lo evita del todo.
    HERRAMIENTAS.mkdir(exist_ok=True)
    gen = MOTOR_GEN.read_text(encoding="utf-8")
    gen = gen.replace("{{BASE_URL}}", BASE_URL)
    gen = gen.replace("<body>", "<body>\n<script>window.BANCO_MAESTRO = " + payload + ";</script>", 1)
    (HERRAMIENTAS/"generador-ejercicios.html").write_text(gen, encoding="utf-8")
    print("  OK  herramientas/generador-ejercicios.html (datos incrustados)")

def build_temas_completos(seqs):
    # Proyeccion liviana de cada tema COMPLETO (no ejercicios sueltos como banco-maestro,
    # sino banco_oraciones + ejercicios de practica juntos) para el class generator
    # (herramientas/generador-clases.html): permite combinar varios temas completos
    # ("moleculas") en una sola clase a la carta. 100% estatico, recombina lo ya generado.
    items = []
    for s in seqs:
        inicio = s.get("fases", {}).get("inicio", {})
        items.append({
            "id": s["id"], "nivel": s["nivel"], "area": s.get("_area", ""),
            "tema": s["tema"], "arquetipo": s.get("arquetipo", ""),
            "habilidades": s.get("habilidades", []),
            "banco_oraciones": s.get("banco_oraciones", []),
            "ejercicios": s.get("fases", {}).get("practica", {}).get("ejercicios", []),
            "banner_diagnostico": inicio.get("banner_diagnostico"),
        })
    DATOS.mkdir(exist_ok=True)
    payload = json.dumps(items, ensure_ascii=False)
    (DATOS/"temas-completos.json").write_text(payload, encoding="utf-8")
    print("  OK  datos/temas-completos.json (" + str(len(items)) + " temas)")
    HERRAMIENTAS.mkdir(exist_ok=True)
    gen = MOTOR_CLASE.read_text(encoding="utf-8")
    gen = gen.replace("{{BASE_URL}}", BASE_URL)
    gen = gen.replace("<body>", "<body>\n<script>window.TEMAS_COMPLETOS = " + payload + ";</script>", 1)
    (HERRAMIENTAS/"generador-clases.html").write_text(gen, encoding="utf-8")
    print("  OK  herramientas/generador-clases.html (datos incrustados)")

def build_sitemap(seqs):
    urls = [BASE_URL + "/", BASE_URL + "/herramientas/generador-ejercicios.html", BASE_URL + "/herramientas/generador-clases.html", BASE_URL + "/herramientas/mapa-3d.html", BASE_URL + "/herramientas/placement.html", BASE_URL + "/herramientas/la-ola.html"]
    for s in seqs:
        for d in ("preview","leccion","evaluacion"):
            urls.append(BASE_URL + "/" + d + "/" + s["id"] + ".html")
    today = datetime.date.today().isoformat()
    x = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        x.append("  <url><loc>"+html.escape(u)+"</loc><lastmod>"+today+"</lastmod></url>")
    x.append("</urlset>")
    (ROOT/"sitemap.xml").write_text("\n".join(x), encoding="utf-8")
    (ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE_URL+"/sitemap.xml\n", encoding="utf-8")
    print("  OK  sitemap.xml ("+str(len(urls))+" urls) + robots.txt")

def verificar_integridad(seqs):
    """
    Chequeo de resiliencia (2026-07-12): valida que cada HTML generado este completo,
    no truncado a medias por un fallo de escritura/sincronizacion. Se agrego despues
    de un bug real donde index.html quedo cortado a mitad del <script> y los filtros
    de nivel dejaron de funcionar sin ningun error visible durante el build.
    Chequea, por archivo: (1) termina en </html>, (2) <script>/</script> balanceados,
    (3) si hay node disponible, sintaxis real de cada bloque <script> inline (se
    saltan los bloques application/ld+json y los <script src=...> externos).
    """
    archivos = [INDEX, HERRAMIENTAS/"generador-ejercicios.html", HERRAMIENTAS/"generador-clases.html", HERRAMIENTAS/"mapa-3d.html", HERRAMIENTAS/"placement.html", HERRAMIENTAS/"la-ola.html"]
    for s in seqs:
        for carpeta in (PREVIEW, LECCION, EVAL):
            archivos.append(carpeta/(s["id"]+".html"))

    tiene_node = shutil.which("node") is not None
    problemas = []
    for f in archivos:
        if not f.exists():
            problemas.append(f.relative_to(ROOT).as_posix() + ": no existe")
            continue
        txt = f.read_text(encoding="utf-8")
        if not txt.rstrip().lower().endswith("</html>"):
            problemas.append(f.relative_to(ROOT).as_posix() + ": no termina en </html> (posible truncado)")
            continue
        if txt.count("<script") != txt.count("</script>"):
            problemas.append(f.relative_to(ROOT).as_posix() + ": <script> y </script> no balanceados")
            continue
        if tiene_node:
            for attrs, bloque in re.findall(r"<script([^>]*)>(.*?)</script>", txt, re.S):
                if "application/ld+json" in attrs or "src=" in attrs:
                    continue
                bloque = bloque.strip()
                if not bloque:
                    continue
                tmp = pathlib.Path(tempfile.gettempdir())/"ea_check.js"
                tmp.write_text(bloque, encoding="utf-8")
                r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
                try:
                    tmp.unlink()
                except OSError:
                    pass
                if r.returncode != 0:
                    ultima = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "desconocido"
                    problemas.append(f.relative_to(ROOT).as_posix() + ": error de sintaxis JS -> " + ultima)

    if problemas:
        print("\n  ADVERTENCIA -- problemas de integridad detectados:")
        for p in problemas:
            print("   x " + p)
        print("  " + str(len(problemas)) + " archivo(s) con problemas. Revisa antes de subir el sitio.\n")
    else:
        print("  OK  integridad (" + str(len(archivos)) + " archivos verificados, todos completos)")
    return problemas

def main():
    print("Construyendo EnglishAngel...")
    build_ea_nav()
    seqs = build_por_tema()
    build_index(seqs)
    build_sitemap(seqs)
    build_banco_maestro(seqs)
    build_temas_completos(seqs)
    build_ludoteca_pool(seqs)
    build_ludoteca(seqs)
    print("Listo. " + str(len(seqs)) + " temas -> " + str(len(seqs)*3) + " paginas + index + sitemap.")
    problemas = verificar_integridad(seqs)
    if problemas:
        sys.exit(1)

if __name__ == "__main__":
    main()
