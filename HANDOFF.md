# HANDOFF — Motor de ejercicios

**Para quien retome este proyecto (humano o Claude). Léelo entero antes de tocar nada.**

Última actualización: 27 julio 2026 · corresponde al release `v1.0`.

Este archivo documenta cómo funciona **de verdad** la plataforma, no cómo parece.
Varias suposiciones razonables sobre este repo son falsas, y una de ellas
destruye audio en producción sin dar ningún error.

---

## 0. Las cinco cosas que tienes que saber antes de editar

1. **No es React.** HTML + JS vanilla, sin bundler, sin `package.json`.
   El build es `build/build.py` (Python 3). Node solo se usa para los tests.

2. **`preview/`, `leccion/` y `evaluacion/` son artefactos generados.** 243 archivos
   que salen de `build.py`. Editarlos a mano funciona hasta el próximo build,
   que los sobrescribe. Se edita `motor/*.html` y se corre `build.py`.

3. **PERO los artefactos ya se editaron a mano en el pasado.** Antes de correr
   `build.py`, verifica que reproduzca lo commiteado (§4). Si no, hay cambios
   vivos que solo existen en los archivos generados y el build los borrará.

4. **El motor está incrustado en 165 archivos** entre los dos repos. No hay un
   único punto de edición. Ver §7.

5. **Hay dos repos.** `EnglishAngel` (sitio público) y `EnglishAngel-Aula`
   (app de aula con Firebase). Aula lee el contenido del sitio por HTTP pero
   tiene **su propia copia** del motor. Un arreglo en uno no llega al otro.

---

## 1. Arquitectura real

```
contenido/{nivel}/{id}.json   81 secuencias — la fuente de verdad del contenido
        │
        └── build/build.py
              ├── preview/{id}.html      81   práctica  (motor/motor-generico.html)
              ├── leccion/{id}.html      81   lección   (motor/lecciones-generico.html)
              ├── evaluacion/{id}.html   81   examen    (motor/evaluacion-generico.html)
              ├── index.html, sitemap.xml, robots.txt
              ├── datos/banco-maestro.json, datos/temas-completos.json
              ├── herramientas/generador-*.html  (datos incrustados)
              └── js/ea-nav.js           desde motor/ea-nav.js + lista de /fluency
```

`build.py` inyecta en cada página: el SEO, el `window.SEQUENCE_DATA` completo,
un bloque de texto plano prerenderizado para bots que no ejecutan JS, y los
`<script src>` de `js/ea-nav.js` y `js/ea-scoring.js`.

**Lo que `build.py` NO genera:** `fluency/` (39 páginas) y `juegos/` (81).
No encontré qué las produce. Podrían tener el mismo desfase que tuvo `preview/`.
**Pendiente de investigar.**

### Repo Aula

```
EnglishAngel-Aula/
  ejercicio.html    copia del motor + Firebase + token de estudiante
  refuerzo.html     otra copia del motor
  comun.js, config.js, catalogo.json
```

`config.js` define `SITE_BASE = "https://pipefleurs87-sudo.github.io/EnglishAngel"`.
Aula hace `fetch(SITE_BASE + '/contenido/{nivel}/{id}.json')` en runtime.
Las páginas requieren `?t={token}&tema={id}`; sin token válido no renderizan.

---

## 2. Schema de contenido

Congelado por decisión de Felipe. **No lo cambies sin preguntar.**

```json
{
  "id": "b1-conditionals-0-1-2-01",
  "nivel": "A1|A2|B1|B2|C1",
  "tema": "...",
  "habilidades": ["grammar","listening","reading","writing"],
  "banco_oraciones": [{"id":"s1","oracion":"..."}],
  "fases": {
    "inicio":    {"interaccion":[],"banner_diagnostico":{},"definicion_pragmatica":"","tabla":{}},
    "practica":  {"ejercicios":[...]},
    "listening": {"guion":["Personaje: línea"],"gaps":["palabra"],"comprension":[]},
    "reading":   {"texto":"...","preguntas":[{"afirmacion":"","respuesta":"true|false"}]},
    "fluency":   {...}
  }
}
```

Gap-fill: la oración se guarda **entera** en `texto`, con `___` marcando el hueco.
No hay campos `prefix`/`suffix`. La pista va entre paréntesis justo después del
hueco: `"If it rains tomorrow, we ___ (stay) at home."`

Tipos válidos: `multiple_choice`, `true_false`, `gap_fill`, `unscramble`,
`correct_mistake`, `transformation`, `write_opposite`, `short_answer_production`,
`reading_comprehension`, y `banked_choice` (nuevo, sin contenido todavía).

Datos útiles a julio 2026: 1368 ejercicios, 233 `gap_fill` (todos con **un solo**
hueco), 79 secuencias con `listening.guion`, 46 de ellas con 3+ personajes.
Ninguna secuencia tiene `fases.fluency` pese a que existen 39 páginas en `/fluency`.

---

## 3. Qué se hizo en v1.0

### Gap-fill inline

El bug era **una regla CSS**: `input[type=text]{ ... width:100% }`. El input ya
estaba dentro del `<p>`, pero ocupaba el ancho completo y partía la oración en
tres líneas. `evaluacion-generico.html` además no aplicaba ninguna clase correctora.

Solución: bloque `.gapfill` + función `construirGapFill()`. Tres detalles que
**no son cosméticos** y no deben "simplificarse":

- `border-bottom` en vez de caja — el estudiante reconoce ese patrón del papel.
- `vertical-align: baseline` — sin esto el input se alinea por su borde inferior
  y la línea de texto salta.
- `white-space: nowrap` en `.gap`, con la pista **dentro** del span — evita que
  el input quede al final de una línea y `(stay)` arranque la siguiente.

Ancho: `7ch` de B1 en adelante; en A1–A2 `max(len(respuesta)+2, 5)`, porque
insinuar la longitud reduce carga cognitiva en niveles bajos.

### N huecos por oración

El código anterior hacía `esc(texto).split('___')` y usaba solo `parts[0]` y
`parts[1]`. Una oración con dos huecos **perdía en silencio** todo el texto
posterior al segundo. `construirGapFill()` recorre N segmentos. Con un hueco el
resultado es idéntico, así que los 233 ejercicios existentes no cambiaron.

### Motor de calificación — `js/ea-scoring.js`

Archivo nuevo, usable en navegador y en node. Cuatro reglas que importan:

1. **La unidad calificable es el ítem, no el ejercicio.** Un gap-fill de 5 huecos
   con 4 aciertos vale 0.8, no 0.
2. **Promedia porcentajes por categoría, ponderados** — nunca ítems crudos.
3. **`unanswered` separado de `incorrect`.** Sin responder suele ser falta de
   tiempo; incorrecto es un error de lengua real. Esa distinción dice si el
   problema fue el examen o el estudiante.
4. **Sin nada calificable devuelve `null`, nunca `0`.** Un 0 es una nota real y
   le pone un cero al estudiante que no hizo nada malo.

Tres estados por categoría: `scored` / `formative` / `skipped`. `formative` es
lo que se quería al pedir "sacar el listening de la nota": el estudiante practica
y el profesor ve el desempeño, sin que penalice.

**`weightMode: 'byItems'` está activo por defecto y es deliberado.** Hace que el
peso de cada categoría sea su número de ítems, lo que reproduce **exactamente**
la nota histórica. Con pesos iguales, reading saltaría de ~17% a 50% de la nota
y reprobaría a estudiantes que hoy aprueban, además de reescribir el umbral de
75% y el progreso guardado en localStorage. Verificado: 0 desviación en las 81
secuencias. **No lo cambies a `'equal'` sin hablarlo con Felipe.**

Para sacar listening de la nota, una línea en la página:

```js
window.EA_SCORING_CONFIG = { modes: { listening: 'formative' } };
```

### Bug de apóstrofos (afectaba a todo el mundo)

`normalize()` aplicaba el mapa de contracciones **antes** de normalizar apóstrofos
tipográficos. Resultado: `it's` → `"it is"` pero `it’s` → `"it's"`, y no coincidían.
Todo estudiante escribiendo desde un teléfono (que inserta `’` automáticamente)
recibía error en cualquier contracción. Se corrigió invirtiendo el orden, en el
sitio y en Aula. **El mapa de contracciones se conservó intacto** — cambiarlo
alteraría notas ya dadas. El de Aula tiene 4 entradas más (`i've`, `you've`,
`we've`, `they've`); también se conservó.

### `banked_choice`

Multiple matching estilo Cambridge (Listening Part 4 / Use of English Part 8):
un banco único de opciones, varias preguntas, cada una elige del mismo banco.
Implementado en los dos motores del sitio. **Sin contenido que lo use.**

Cuatro reglas de comportamiento que no son negociables:

- **El banco nunca se baraja.** Si `A` deja de ser `A` entre renders, el
  estudiante que anotó "1-C" en papel queda perdido.
- **`allowReuse:false` atenúa la opción tomada, no la esconde.** Hay que poder
  cambiar de opinión.
- **Debe poder deseleccionarse.** Un `<input type="radio">` nativo no lo permite;
  por eso son botones con `role="radio"` y toggle.
- **El banco no se repite en cada pregunta.** 6 preguntas × 4 opciones = 24
  bloques de texto y el estudiante deja de leer.

Un grader por pregunta, no por ejercicio.

### `ea-nav.js`

Estaba a medio cablear: `motor/ea-nav.js` es una plantilla con marcador
`{{FLUENCY_IDS}}` que **nada renderizaba**, y el `<script>` estaba puesto a mano
en 24 de 243 páginas. Ahora `build.py` lo genera (derivando la lista de `/fluency`,
porque los JSON de contenido no tienen `fases.fluency`) e inyecta el tag en las 243.

El botón **Games** viene activado en `motor/ea-nav.js` y ahora aparece en todas
las páginas. Fue una decisión heredada del archivo, no pedida. Si sobra, es
borrar esa línea y rebuildear.

---

## 4. El campo minado: `build.py` puede destruir producción

**Antes de correr `build.py` por primera vez en una sesión, haz esto:**

```bash
cp -r preview /tmp/base_preview
cp -r leccion /tmp/base_leccion
cp -r evaluacion /tmp/base_evaluacion
python3 build/build.py
diff -rq /tmp/base_preview preview
diff -rq /tmp/base_leccion leccion
diff -rq /tmp/base_evaluacion evaluacion
```

Si algo difiere y **no** es un cambio que acabas de hacer, para y averigua por qué.

**Esto ya pasó.** En julio 2026 los artefactos tenían un reproductor de mp3 con
fallback a voz sintética que `motor/motor-generico.html` **no tenía** (0 ocurrencias
de `new Audio`). Un rebuild lo habría borrado de las 81 páginas de práctica.
Sin error, sin aviso: solo audio grabado degradado a voz de navegador. Se portó
la versión buena del artefacto a la plantilla antes de seguir.

El desfase iba en **las dos direcciones**: `build.py` a su vez tenía textos SEO
mejorados que nunca se habían desplegado. No asumas que la plantilla siempre está
atrás ni siempre adelante.

---

## 5. Cómo se despliega (importante: no hay git local)

Felipe trabaja por la **interfaz web de GitHub**. La carpeta local
`Documents/EnglishAngel/EnglishAngel-main` es una extracción de zip **sin `.git`**.

- GitHub Pages sirve desde `main`. Una rama no despliega, así que para que
  Felipe pueda probar algo hay que commitear a `main`.
- El uploader web acepta arrastrar carpetas. Límite práctico: ~100 archivos por
  commit, así que las carpetas de 81 van de una en una.
- Los artefactos generados **están commiteados** porque Pages los sirve. No hay
  forma de evitarlo con este hosting.

Sitios en vivo:
- https://pipefleurs87-sudo.github.io/EnglishAngel
- https://pipefleurs87-sudo.github.io/EnglishAngel-Aula

Respaldos locales (fuera del repo): `backup/pre-motor-2026-07-27/` (260 archivos,
estado previo del sitio) y `backup/pre-aula-2026-07-27/` (2 archivos de Aula).

---

## 6. Tests

```bash
node --test "build/test/*.test.js"     # 19 tests, deben pasar todos
```

Las comillas importan: `node --test build/test/` falla con `MODULE_NOT_FOUND`.

Cubren los criterios de aceptación del encargo original. Se verificaron por
**mutación** — introduciendo bugs a propósito para confirmar que los tests los
atrapan:

| Mutante | Tests que fallan |
|---|---|
| `grade` devuelve `0` en vez de `null` | 2 |
| Pondera ítems crudos en vez de porcentajes | 2 |
| Se quita la normalización de apóstrofos | 1 |
| `unanswered` cuenta como `incorrect` | 2 |
| Control inocuo | 0 |

Si tocas `ea-scoring.js`, corre los tests. Si añades lógica, añade el mutante
correspondiente y comprueba que algo falla.

---

## 7. La deuda principal — motor duplicado en 165 archivos

El renderer no está en 4 copias: está **horneado dentro de 165 archivos**, porque
`build.py` estampa la plantilla completa en cada página generada.

Consecuencia medida: cambiar ~60 líneas de JavaScript obligó a regenerar y subir
**247 archivos** por la interfaz web.

### Plan propuesto (no ejecutado)

Extraer el renderer a `js/ea-ejercicios.js`, igual que ya se hizo con
`ea-scoring.js`, y cargarlo con `<script src>` desde los cuatro sitios:

- `motor/motor-generico.html` y `motor/evaluacion-generico.html` → `../js/ea-ejercicios.js`
- Aula `ejercicio.html` y `refuerzo.html` → `SITE_BASE + '/js/ea-ejercicios.js'`

Lo que se mueve: `renderExercise()` y su switch de tipos, `construirGapFill()`,
`gapAncho()`, `construirBanked()`, `normalize()`/`eq()`, y el CSS asociado.

Lo que **se queda** en cada página: el `SEQUENCE_DATA` incrustado (es el contenido
del tema y por eso Google lo indexa) y el prerender de texto plano para bots.

Beneficio: un arreglo de motor pasa de 247 archivos a 1, y deja de necesitar rebuild.

Riesgos a manejar:
- **Caché de GitHub Pages.** Hay que versionar el src (`?v=3`) e incrementarlo
  en `build.py`, o los estudiantes seguirán viendo el motor de ayer.
- **Aula dependería del sitio principal para el motor.** No es un riesgo nuevo
  —ya depende de él para el contenido— pero conviene decirlo.
- **Un error rompe las cuatro páginas a la vez** en vez de una. Hacerlo con
  copia de trabajo, tests, y comparación página por página antes de subir.

---

## 8. Otros pendientes

- **`banked_choice` sin contenido.** El tipo funciona; falta escribir los bancos.
  Las 46 secuencias con 3+ personajes son las que valen la pena; con 2 personajes
  un banco compartido no aporta nada sobre el multiple choice que ya existe.
  Es trabajo pedagógico: los distractores los decide Felipe.
- **`fluency/` y `juegos/` no los genera `build.py`.** Sin averiguar qué los
  produce, podrían tener el mismo desfase que tuvo `preview/`.
- **`prerender_texto()` emite el `___` crudo** en el HTML para bots. No se tocó,
  pero ahora se ve distinto a lo que ve el usuario.
- **La migración de schema a `{{aceptadas|pista}}`** se propuso y se descartó:
  no arreglaba el bug de layout (que era CSS) y habría sido un no-op sobre el
  contenido actual (0 ejercicios con multi-hueco, 0 con variantes). Si algún día
  se quiere multi-respuesta aceptada, ahí está la idea.

---

## 9. Reglas heredadas que siguen vigentes

De `AGENTS.md`, conservadas:

- Tokens de diseño: `--ink:#1B2A41` `--paper:#EFF1EC` `--red:#B23A2E`
  `--gold:#C9962F` `--muted:#6B7079` `--line:#D8DAD1`. Verde de acierto `#2f7d4f`.
  Tipografías: Source Serif 4, IBM Plex Sans, IBM Plex Mono, Caveat.
- El audio se encadena con `utterance.onend`, **nunca** con `setTimeout` fijo.
  Ese bug ya se corrigió una vez.
- No cambiar el schema JSON sin avisar.
- No generar contenido para público infantil todavía.
- No implementar evaluación de pronunciación real ni grabación de voz de
  estudiantes sin aprobación explícita (privacidad de menores, sin resolver).
- El reconocimiento de voz sería transcripción, no evaluación fonética: no
  venderlo como "evaluación de pronunciación".
