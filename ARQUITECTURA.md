# Arquitectura EnglishAngel — motores, arquetipos y esquema

> Decisiones aprobadas por Felipe (jul 2026). Este archivo complementa el CLAUDE.md.
> Regla de oro intacta: **un motor por artefacto (no por tema). Contenido = datos.**

## Tres artefactos por tema (un JSON → tres páginas)

Cada `contenido/{nivel}/{id}.json` genera automáticamente:

1. **Ejercicios** — `preview/{id}.html` (motor: `motor/motor-generico.html`). Práctica con pistas y reintentos.
2. **Lección** — `leccion/{id}.html` (motor: `motor/lecciones-generico.html`). Slides para video: pragmática → error típico → tabla → vocabulario → ejemplos por forma → práctica con signposting → cierre.
3. **Examen** — `evaluacion/{id}.html` (motor: `motor/evaluacion-generico.html`). Sin pistas, un intento, calificado.

Se construyen con `python3 build/build.py`.

## Arquetipos (recetas de generación, NO motores)

Los tres motores son genéricos. La diferencia pedagógica entre temas vive en el **arquetipo**: una receta de autoría que yo (Claude) sigo al generar el JSON, para que cada categoría lingüística tenga su forma correcta. Campo opcional top-level: `"arquetipo"`.

| arquetipo | para | forma del contenido |
|---|---|---|
| `tiempo_verbal` | to be, present simple, past simple, present continuous | banco por forma (afir/neg/inter/short_answer) + tabla de conjugación |
| `determinantes` | artículos, demostrativos, posesivos | drills de concordancia y contraste (this/these) |
| `pronombres` | sujeto / objeto | sustitución (reemplazar nombre por pronombre) |
| `comparativos` | comparativo / superlativo | tabla de adjetivos (big→bigger→biggest) + "than" |
| `clausulas_relativas` | who / that / where | combinar dos oraciones en una |
| `preposiciones` | lugar / tiempo | selección por contexto, contraste in/on/at |
| `modales` | can, must, should | por función (habilidad/permiso/obligación) |
| `vocabulario` | países, trabajos, comida | sets de palabras con imágenes/banderas |
| `funcional_skills` | listening / reading pesados | centrado en diálogo o texto |
| `joined_exercise` | repasos 100% combinación (fin de bloque/nivel) | todos los ejercicios llevan `combina`; banco sin `forma`; vocab_warmup false |

La velocidad en batch viene de estas recetas, no de multiplicar motores.

## Evolución del esquema (aprobada, retrocompatible)

Campos AÑADIDOS (todos opcionales; el contenido viejo sigue funcionando):

- Top-level `"arquetipo"`: string (ver tabla).
- En `banco_oraciones[]`: `"forma"` = `"afirmativo"|"negativo"|"interrogativo"|"short_answer"`. La lección agrupa los ejemplos por forma cuando está presente.
- En `fases.inicio`: `"tabla"` = `{ "titulo": "...", "encabezados": ["...","..."], "filas": [["...","..."], ...] }`. Se renderiza como tabla de referencia en ejercicios y como slide en la lección.
- En `fases.listening`: `"comprension"` = `[ { "pregunta": "...", "opciones": [...], "respuesta": "..." } ]` (opción múltiple de comprensión, además de `gaps`).

Nada se quitó del esquema original. Todo lo anterior sigue válido.

## Convención de listening (aclarada)

`gaps` = palabras que se OCULTAN en la transcripción (para que completar sea escuchar de verdad). Recomendado 2 por diálogo + 2 de `comprension`. Foco: entender, no copiar.

## Definición de terminado — REGLA DE LAS 4 FORMAS (obligatoria en gramática)

Todo tema con arquetipo gramatical (tiempo_verbal, determinantes, pronombres, comparativos, clausulas_relativas, modales) DEBE tener su `banco_oraciones` con las cuatro formas:
**afirmativo · negativo · interrogativo · short_answer** (yes/no questions and answers).

Incluso demostrativos, posesivos y pronombres lo cumplen usando el verbo 'to be' (Is this...? Yes, it is.).
`build/build.py` verifica esto en cada build y avisa con ⚠ si falta alguna. No dar por terminado un tema con advertencias.

## Joined exercises (ejercicios combinados) — interleaving

Cualquier ejercicio puede llevar un campo opcional `"combina": ["demostrativos","can"]`. El motor de ejercicios muestra un sello **🔗 Combina: ...** que nombra las estructuras que el ejercicio entrelaza. Sirve para spiraling/repaso: practicar estructuras viejas mientras se enseña una nueva. Reutilizable en cualquier tema, no solo modales.

Arquetipo futuro `joined_exercise`: temas de REPASO que son 100% combinación (ej. "A1 Review" mezclando present simple + relativas + modales). Consolidación de fin de nivel y buen material de video.

## Modales (A1, arquetipo modales) — explorados por uso
- can → habilidad (partes del cuerpo)
- must → deberes en casa
- have to → obligaciones trabajo/estudio
- would like → preferencias y ofrecimientos
- should → consejos/sugerencias
Otros modales (could, may, might...) → inicio de A2.

## Herramienta nueva: Banco Maestro + generador de ejercicios a la carta (2026-07-10)

- `build/build.py` → `build_banco_maestro(seqs)`: recorre todas las secuencias ya cargadas y aplana **cada ejercicio individual** de `fases.practica.ejercicios` + cada bloque de `fases.reading` (como pseudo-tipo `reading_comprehension`) en `datos/banco-maestro.json`. Cada item lleva `{nivel, tema, tema_id, area, tipo, etapa, combina, ejercicio}`. `etapa` se deriva del diccionario `ETAPAS` que ya existía para la regla de las 5 por etapa — no hay lógica nueva de clasificación, solo reutilización.
- **No genera contenido nuevo.** Es una recombinación de lo que ya está en `/contenido` — por eso sigue siendo 100% estático, $0 de hosting, sin backend ni IA en vivo. 864 ejercicios indexados a la fecha (A1: 425, A2: 205, B1: 234).
- `motor/generador-generico.html` (4º motor) → `herramientas/generador-ejercicios.html`, generado por build.py igual que los otros 3: arma una hoja a la carta filtrando por nivel, tipo de ejercicio (agrupados por etapa cognitiva Recognize/Manipulate/Transform/Reading) y búsqueda de tema opcional. Reutiliza literalmente `renderExercise()`, `normalize()`/`eq()` y el patrón de `graders[]`/Check answers de `motor-generico.html` — mismo motor de calificación, sin reescribirlo.
- CORRECCIÓN 2026-07-10 (mismo día): la primera versión usaba `fetch('../datos/banco-maestro.json')`, que falla bajo `file://` (Chrome/Edge bloquean fetch de archivos locales sin servidor) — Felipe lo abrió con doble clic y vio "Could not load the exercise bank." Se corrigió incrustando el JSON directo en el HTML en build time (`window.BANCO_MAESTRO = [...]`, mismo patrón que `window.SEQUENCE_DATA` en los otros 3 motores). Ya no depende de fetch ni de servidor local. `datos/banco-maestro.json` se sigue escribiendo también como artefacto independiente (por si sirve para el class generator después), pero la página ya no lo necesita.
- Enlazada desde `index.html` (vía `build/index_template.html`) y agregada a `sitemap.xml`.
- Pendiente / decisión futura con Felipe: si el pool de una combinación muy específica (nivel+tema+tipo) da pocos resultados, la opción NO es generar con IA en el momento (rompería el modelo $0) — la solución es seguir ampliando el banco de contenido curado, igual que siempre.
- Concepto hermano pendiente: **class generator** (plan de clase imprimible + modo profesor en vivo, como 4º motor `clase-generico.html`, seleccionando 1+ secuencias) — decidido con Felipe pero no construido todavía.

### Iteraciones del generador (mismo día, 2026-07-11)

- **Menús en vez de texto libre**: se reemplazó el input de búsqueda de tema por un `<select>` con las áreas reales + chips de **Category** (Grammar/Vocabulary/Skills/Review, derivadas de `arquetipo`). Motivo: escribir "simple past" no encontraba "Past Simple" (búsqueda literal). De paso se extendió `area_de()` en build.py — 11 temas que caían al fallback de nivel (Conditionals, Countable & Uncountable, Gerund vs Infinitive, Going To, Have Got, Imperatives, Passive Voice, Present Perfect, Present Perfect Continuous, Used To, Will vs Going To) ahora tienen área propia, con sus entradas en `AREA_ES` para el título híbrido.
- **Conteo en vivo**: el texto de estado ya no dice solo "864 exercises available" fijo — se recalcula (`updateCount()`) en cada click de chip o cambio de `<select>`, mostrando "N of 864 match this combination" (rojo si N=0). Antes había que darle a Generate para descubrir que una combinación (ej. Category=Grammar apagado + Topic=Past Simple, que se cancelan entre sí) no tenía resultados.
- **Links pre-filtrados + Copy link**: la página lee `?nivel=&tipo=&categoria=&tema=&cantidad=&auto=1` al cargar y pre-marca los filtros (útil para mandarle a un estudiante un link ya armado antes de clase). Botón "🔗 Copy link to this" arma esa URL desde el estado actual de los filtros y la copia al portapapeles (con fallback visible si el navegador bloquea `clipboard.writeText`, común en `file://`).
- BUG propio corregido en el camino: `applyUrlParams()` intentaba hacer click en `#generar` ANTES de que `document.getElementById('generar').onclick=...` se hubiera asignado (orden de ejecución del script) — `auto=1` no generaba nada. Se movió la llamada al final del script, después de conectar todos los handlers. Verificado con jsdom (`/tmp` fuera del repo), no con navegador real, cada vez que se tocó este archivo.

### INCIDENTE 2026-07-11: la herramienta Edit truncó `motor/generador-generico.html`

Al agregar `og:image`/`canonical` al head de este motor use la herramienta `Edit` directamente (no el patrón `python3 <<'PYEOF' ... src.replace(...) + assert count==1` que ya era la regla). El archivo quedó cortado a mitad del `<script>` final (sobrevivió el 96% del JS, se perdieron los últimos ~580 bytes: el cierre de `check.onclick`, `reset.onclick`, `printBtn.onclick` y `applyUrlParams()` + `})();`). CLAUDE.md ya advertía esto para los 3 motores originales — **ahora sabemos que aplica igual al 4to motor** (`generador-generico.html`) y probablemente a cualquier archivo de tamaño similar (~20KB+), sin importar si es "motor" en el sentido original. Recuperado reconstruyendo desde un `<script>` extraído previamente y verificado con `node --check` (`/tmp/gen_fixed8.js`, guardado durante una verificación anterior en la misma sesión) — sin esa copia de respaldo habría sido mucho más difícil. Lección reforzada: **NUNCA Edit/Write en NINGÚN archivo HTML grande del proyecto**, no solo los 3 motores originales — todo cambio en `motor/*.html` (los 4) va por shell heredoc o `python3` con `assert count==1`, sin excepción. Además: guardar copias de los `<script>` extraídos en `/tmp` durante las verificaciones de sesión es, en la práctica, la única red de seguridad que existe (no hay `.git` en la carpeta montada).
- **Menú de Topic dinámico (que nunca dé 0)**: el `<select>` de tema se repuebla en cada cambio de Level/Type/Category (`onFilterChange()` → `refreshTemaOptions()` + `updateCount()`), mostrando el conteo real junto a cada área ("Prepositions (0)") y deshabilitando (`option.disabled`) las que están en cero para el resto de filtros activos. Si el tema elegido deja de tener resultados por un cambio en otro filtro, se resetea solo a "Any topic" en vez de dejar al usuario parado en una combinación imposible (ej. Level=A2+B1 con Topic=Prepositions, que solo existe en A1). Motivado por: Felipe encontró justo ese caso. Limpieza de paso: `applyUrlParams()` se estaba llamando DOS veces (un residuo del fix anterior) — quedó en una sola, al final del script, y ahora llama `refreshTemaOptions()` antes de fijar el `tema` de la URL para que la opción exista/esté habilitada.

## Changelog motores — 2026-07-09 (sesión data de demanda)

- **Calificación de lo resuelto** (motor-generico): `Check answers` califica solo ítems respondidos (`answered()` por grader); score "X/Y answered · Z total". Lo no tocado ya no cuenta como error → el docente puede asignar subsecciones. El examen (evaluacion-generico) sigue calificando todo a propósito.
- **Barra de modos** en las 3 páginas (Lesson · Practice · Test), derivada de `D.id` con rutas relativas `../{leccion|preview|evaluacion}/`. En la lección es overlay discreto arriba a la derecha + link real en el slide final.
- **Duración estimada** en el masthead de ejercicios (≈ min class), calculada del contenido — promesa zero-prep.
- **Print de tabla de referencia** (botón 🖨 + CSS @media print, clase body.print-tabla) — captura demanda "tabla del verbo to be" (Trends +70%).
- **Títulos híbridos** en build.py: dict AREA_ES → "<Tema> (término español)" en title/og/meta/keywords. Justificación: Trends jul 2026.
- **Regla de generación nueva**: 2-3 ejercicios por tipo en secuencias nuevas (las 24 previas quedan como están, backfill pendiente). Arquetipo `joined_exercise` formalizado (4 repasos A1 generados).
- RECORDATORIO del bug: Edit/Write truncan los motores — volvió a pasar hoy. Heredoc siempre + node --check.

## 2026-07-11 (noche) — Class Generator

Quinto artefacto estatico: `herramientas/generador-clases.html` (motor fuente `motor/generador-clases.html`),
enlazado como "🧩 Class Generator" junto al Exercise Generator en las 159 paginas de contenido y en el home.

Que hace: Felipe elige 2+ temas ya existentes (checklist agrupado por nivel) y un titulo de clase.
El JS combina banco_oraciones + practica.ejercicios de los temas elegidos en UNA sesion nueva
(misma forma que un JSON normal de /contenido: banner_diagnostico reutilizado del primer tema
seleccionado que tenga uno, definicion_pragmatica auto-generada de una linea, tabla auto-armada
"Topic | Key example"), la renderiza en vivo con los mismos widgets/calificacion del Exercise
Generator, y ofrece "Download JSON" para registrarla de forma permanente despues (Felipe la manda
y se integra a /contenido con el flujo normal de build.py si quiere que tenga su propia pagina).

"Registro" sin backend: localStorage (`ea_mis_clases`) guarda cada clase generada (titulo, nivel,
ids de temas, fecha) en el navegador de Felipe para recargarla despues -- explicitamente NO es
persistencia entre dispositivos ni multiusuario; eso queda para la fase de plataforma con backend
(Firebase, decidida como candidata pero pospuesta hasta confirmar que el sitio estatico funciona).

Datos: nueva proyeccion `datos/temas-completos.json` (build_temas_completos() en build.py) --
a diferencia de banco-maestro.json (ejercicios sueltos indexados), esta guarda cada tema COMPLETO
(banco_oraciones + ejercicios + banner_diagnostico) para poder combinar "moleculas" enteras.
v1 omite listening/reading en las clases combinadas (mezclar guiones/lecturas narrativas de temas
distintos no tiene sentido sin autoria; se deja para una iteracion futura si Felipe lo pide).

Decision explicita de Felipe: la futura "plataforma" (login, progreso, calificaciones, comentarios
con captura de correo) es un proyecto SEPARADO del repo publico de GitHub Pages, con acceso
controlado solo a los estudiantes que el elija -- no se construye todavia. Antes de decidir backend,
confirmar que la app estatica funciona (build limpio + generador de ejercicios + generador de clases
verificados con jsdom).

Protocolo anti-truncado respetado: los 3 motores de contenido + generador-clases.html se tocaron
solo por shell+Python (`src.replace` + `assert count==1`), verificados con `node --check` sobre el
script extraido y `tail -c` confirmando el cierre `</html>`. build.py igual, verificado con py_compile.
