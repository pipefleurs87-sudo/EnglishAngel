# -*- coding: utf-8 -*-
import json, glob, re

PRAG = {
 "a1-to-be-nationalities-01":"We use the verb 'to be' (am / is / are) to say who you are, where you are from, and what you are like — your identity in one word.",
 "a1-to-be-neg-questions-01":"To ask a question with 'to be' we put the verb first (Are you...?), and to make it negative we add 'not' after the verb (She is not...).",
 "a1-pronouns-possessives-01":"Subject pronouns (I, you, he...) replace the name; possessive adjectives (my, your, his, her...) say who something belongs to.",
 "a1-demonstratives-01":"We use this/these for what is near and that/those for what is far; this/that are singular and these/those are plural.",
 "a1-present-simple-routines-01":"We use the present simple to talk about routines and things we always do; with he/she/it the verb takes an '-s' at the end.",
 "a1-present-simple-frequency-01":"We use adverbs of frequency (always, usually, sometimes, never) to say how often we do something.",
 "a1-present-simple-neg-questions-01":"To make negatives and questions in the present simple we use do/does + the base verb (no '-s'): the '-s' goes onto 'does'.",
 "a1-present-simple-wh-questions-01":"We use wh- words (what, where, when, why, how) + do/does to ask for information in the present simple: the wh- word comes first, then do/does.",
 "a1-present-simple-likes-01":"We use like/love/hate + a noun or a verb in '-ing' to talk about what we enjoy and our free time.",
 "a1-family-possessive-s-01":"We use 's (apostrophe + s) to say who something belongs to or the relationship between people: 'Sofia's brother' = the brother of Sofia.",
 "a1-relative-clauses-professions-01":"We use 'who' to define a person by what they do: 'a person who + verb' (a person who works, who teaches, who helps).",
 "a1-relative-clauses-places-01":"We use 'where' to define a place by what you do or what happens there: 'a place where + subject + verb'.",
 "a1-relative-clauses-objects-01":"We use 'which' or 'that' (not 'who') to define a thing by its use: 'a thing that you use to + verb'.",
 "a1-object-pronouns-01":"We use object pronouns (me, you, him, her, it, us, them) after the verb or a preposition — they receive the action.",
 "a1-prepositions-place-01":"We use prepositions of place (in, on, under, next to, behind, in front of, between) to say where something is.",
 "a1-prepositions-time-01":"We use 'at' for clock times, 'on' for days and dates, and 'in' for months, years and seasons.",
 "a1-modal-can-ability-01":"We use 'can' to express ability, what we know how to do; can + the base verb, no 'to' (I can swim, not 'I can to swim').",
 "a1-modal-must-duties-01":"We use 'must' for a strong duty or obligation we feel ourselves; must + the base verb. Note: 'mustn't' means it is prohibited.",
 "a1-modal-have-to-01":"We use 'have to / has to' for obligations that come from outside (rules at work or school); with he/she/it we use 'has to'.",
 "a1-modal-would-like-01":"We use 'would like' (I'd like) to express wishes and make polite offers; would like + to + verb, or + a noun.",
 "a1-modal-should-advice-01":"We use 'should' to give advice and suggestions; should + the base verb (no 'to').",
 "a1-present-continuous-01":"We use the present continuous (am/is/are + verb-ing) for actions happening now; the present simple for routines and things that are always true.",
 "a1-wh-questions-bank-01":"Each wh- word asks for different information; in the present simple we use 'do' (you/we/they) and 'does' (he/she/it) + the base verb.",
 "a2-past-simple-narrative-01":"We use the past simple to tell finished actions in the past; after 'did' the verb goes back to its base form (go, not went).",
}

# reemplazos de subcadena, aplicados de mas largo a mas corto (tablas + instrucciones + pistas)
MAP = {
 "La '-s' de tercera persona":"The third-person '-s'",
 "Negativo y contracción":"Negative and contraction",
 "Cerca / Lejos · Singular / Plural":"Near / Far · Singular / Plural",
 "do / does en negativo y pregunta":"do / does in negatives and questions",
 "Relaciones de familia con 's":"Family relationships with 's",
 "a person who + acción":"a person who + action",
 "a place where + acción":"a place where + action",
 "a thing that you use to + acción":"a thing that you use to + action",
 "Present Simple (siempre) vs Present Continuous (ahora)":"Present Simple (always) vs Present Continuous (now)",
 "Present Simple — siempre":"Present Simple — always",
 "Present Continuous — ahora":"Present Continuous — now",
 "Una pregunta con cada wh- (tú / él-ella)":"One question with each wh- (you / he-she)",
 "2ª persona (you)":"2nd person (you)","3ª persona (he/she)":"3rd person (he/she)",
 "¿Dónde va el adverbio?":"Where does the adverb go?",
 "Sujeto + adverbio + verbo":"Subject + adverb + verb","Sujeto + 'to be' + adverbio":"Subject + 'to be' + adverb",
 "Sujeto → Objeto":"Subject -> Object","Pronombre → Posesivo":"Pronoun -> Possessive",
 "can — habilidad":"can — ability","must — obligación":"must — obligation","should — consejo":"should — advice",
 "Palabras wh-":"Wh- words","Gustos y estructura":"Preferences and structure",
 "¿Dónde está?":"Where is it?",
 "Afirmativo (deber)":"Affirmative (duty)","Negativo (prohibición)":"Negative (prohibition)",
 "meses, años, estaciones":"months, years, seasons","horas y night":"clock times & night","días y fechas":"days & dates",
 "Se usa para":"Used for","dentro de":"inside","debajo de":"under","al lado de":"next to","detrás de":"behind",
 "+ to + verbo":"+ to + verb","+ sustantivo":"+ noun",
 "antes del verbo":"before the verb","después del verbo":"after the verb","= tu...":"= your...",
 "Preposición":"Preposition","Significado":"Meaning","Estructura":"Structure","Ejemplo":"Example",
 "Sujeto":"Subject","Verbo":"Verb","Forma":"Form","Negativo":"Negative","Pregunta":"Question",
 "Afirmativo":"Affirmative","Contracción":"Contraction","Relación":"Relationship","Profesión":"Profession",
 "Definición":"Definition","Pronombre":"Pronoun","Posesivo":"Possessive","Gusto":"Preference",
 "Objeto":"Object","Lugar":"Place","qué":"what","dónde":"where","cuándo":"when","por qué":"why","cómo":"how",
 "sobre":"on","dentro":"inside",
 # instrucciones
 "Hazla negativa":"Make it negative","Conviértela en pregunta":"Turn it into a question",
 "Añade 'usually' en el lugar correcto.":"Add 'usually' in the correct place.",
 "Añade obligación con 'must'.":"Add obligation with 'must'.","Añade obligación con 'has to'.":"Add obligation with 'has to'.",
 "Cámbiala usando 'never'.":"Change it using 'never'.","Cámbiala a AHORA (present continuous).":"Change it to NOW (present continuous).",
 "Reemplaza 'Sofía' por un pronombre sujeto.":"Replace 'Sofia' with a subject pronoun.",
 "Reemplaza 'Sofía' por un pronombre objeto.":"Replace 'Sofia' with an object pronoun.",
 "Reemplaza 'Ben' por un pronombre objeto.":"Replace 'Ben' with an object pronoun.",
 "Reescríbelo con 's.":"Rewrite it with 's.","Reescríbela cortésmente con 'would like'.":"Rewrite it politely with 'would like'.",
 "Únelas en una definición con 'who'.":"Join them into a definition with 'who'.",
 "Únelas en una definición con 'where'.":"Join them into a definition with 'where'.",
 "Únelas con 'who' en una definición.":"Join them with 'who' into a definition.",
 "Únelas con 'that'.":"Join them with 'that'.",
 "Ponla en plural (this → these).":"Make it plural (this -> these).",
 "Dale un consejo con 'should'.":"Give advice with 'should'.",
 "Pregunta por el lugar (usa 'Where').":"Ask about the place (use 'Where').",
 "Pregunta por el lugar (Where + does).":"Ask about the place (Where + does).",
 "Pregunta por el modo (How + does).":"Ask about the manner (How + does).","Pregunta por el modo (How).":"Ask about the manner (How).",
 "(usa ":"(use ",
 # pistas entre parentesis
 "(a mí)":"(to me)","(cómo)":"(how)","(dentro)":"(inside)","(al lado)":"(next to)","(sobre)":"(on)",
 "(debajo)":"(under)","(negativo)":"(negative)","(año)":"(year)","(día)":"(day)","(cantidad)":"(quantity)",
 "(¿A qué hora?)":"(at what time?)","(relativo de lugar)":"(place relative)",
}

def tr(s):
    if not isinstance(s,str): return s
    for k in sorted(MAP.keys(), key=len, reverse=True):
        if k in s: s=s.replace(k, MAP[k])
    return s

changed=0
for f in sorted(glob.glob('contenido/*/*.json')):
    d=json.load(open(f,encoding='utf-8'))
    tid=d['id']
    ini=d['fases'].get('inicio',{})
    if tid in PRAG: ini['definicion_pragmatica']=PRAG[tid]
    t=ini.get('tabla')
    if t:
        if 'titulo' in t: t['titulo']=tr(t['titulo'])
        t['encabezados']=[tr(x) for x in t.get('encabezados',[])]
        t['filas']=[[tr(c) for c in row] for row in t.get('filas',[])]
    for ex in d['fases'].get('practica',{}).get('ejercicios',[]):
        if 'instruccion' in ex: ex['instruccion']=tr(ex['instruccion'])
        for k in ('texto','pregunta'):
            if k in ex: ex[k]=tr(ex[k])
    json.dump(d, open(f,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    changed+=1
print("Archivos actualizados:",changed)
