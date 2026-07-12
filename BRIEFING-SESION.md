# BRIEFING TÉCNICO — EnglishAngel (para la próxima sesión)

Actualizado: 2026-07-10, cierre de la sesión nocturna A2+B1+A1. Lee esto junto con `CLAUDE.md` y `ARQUITECTURA.md`. Este archivo tiene prioridad donde haya conflicto, porque es lo más reciente.

## Estado actual

- **51 temas → 153 páginas** (preview/ + leccion/ + evaluacion/ por tema) + index + sitemap (154 URLs). Build **sin advertencias**.
- **A1: 32 temas (completo). A2: 10 (completo). B1: 10 (completo).**
- `temas/pendientes.txt` tiene UNA sola línea: "A2 | Past Simple — Negatives & Questions". Felipe debe decidir si se genera como refuerzo o se tacha (ya está cubierto en gran parte por regulares+irregulares).
- **El push a GitHub Pages está PENDIENTE** — la carpeta montada en Cowork no expone `.git`; Felipe hace commit+push desde su máquina. Tras el push: reenviar sitemap en Search Console.

## Protocolo anti-truncado (CRÍTICO — ha fallado ~6 veces)

- **NUNCA** usar las herramientas Write/Edit sobre los motores (`motor/*.html`), `build/build.py`, ni JSONs largos. Se truncan silenciosamente.
- Archivos nuevos: `cat > archivo <<'JSONEOF' ... JSONEOF` por shell.
- Modificaciones a motores/build.py: script Python por shell con `src.replace(anchor, ...)` + `assert src.count(anchor)==1`.
- Verificar después: `python3 -m py_compile build/build.py`, `tail -c 12 motor/*.html` debe terminar en `</html>`, y `json.load()` para cada JSON.
- Compilar siempre: `python3 build/build.py` y revisar que no haya líneas `  !`.

## Reglas de generación (todas obligatorias en temas nuevos)

1. **Esquema**: el de CLAUDE.md + campos opcionales ya aprobados: `arquetipo` (top), `banco_oraciones[].forma`, `fases.inicio.tabla`, `fases.inicio.interaccion` (NUEVO de esta sesión), `fases.listening.comprension`, `ejercicios[].combina`.
2. **Regla de formas**: banco etiquetado con afirmativo / negativo / interrogativo / short_answer. Chequeo `revisar_formas` en build.py. En temas sin formas naturales (ej. imperativos) se cubre con equivalentes ("Can you..., please?").
3. **Regla 5 por etapa (A2+)**: mínimo 5 ejercicios por etapa cognitiva — Recognize (multiple_choice, true_false), Manipulate (gap_fill, unscramble, correct_mistake), Transform (transformation, write_opposite, short_answer_production). Chequeo `revisar_etapas`. El patrón usado: 5-6 / 8 / 7 ≈ 20 ejercicios. A1 exento del chequeo, pero las 5 A1 nuevas ya lo cumplen.
4. **`interaccion`** (opcional, muy usado): 3-4 líneas "Personaje: texto" que abren la fase inicio ANTES del diagnóstico; `**negritas**` resaltan la estructura meta (se renderizan con fondo dorado). La página de **lección aún NO la renderiza** — mejora pendiente.
5. **Diagnóstico**: siempre error fósil real de hispanohablante vs forma correcta (ej. "the players was", "I visit her last week", "no touch the oven").
6. **Vocabulario**: tarjetas `{bandera, palabra, traduccion}`. `bandera` es un slot flexible: emoji, sonido (/t/ /d/ /ɪd/), patrón de irregulares (i-a-u, i-o-en, -ought, -ept, =, ew/own, ★, modal, -ed, 2 forms, irreg), o etiqueta (since/for, past/perfect, +ing/+to, -ly/-ily). **Verbos y adjetivos siempre con sus 3 formas** en `palabra` ("drink · drank · drunk", "good · better · the best"). Si el tema no tiene vocab propio: omitir `vocabulario` y `vocab_warmup: false`.
7. **MC de completar** (estilo condicionales): "If I study for the exam..." + 3 continuaciones, solo una válida, y **la correcta varía de posición** (a, b, c) entre ejercicios.
8. **Personajes**: Sofía (planes, presente, organización), Ben (pasado, desastres, have got británico), Kenji (preguntas, comparación, curiosidad), Abuela Carmen (present perfect, used to, consejos, sabiduría + humor). Continuidad ya establecida: la ola destruyó el teléfono de Ben, el cliente del "more blue but less blue" de Sofía, la abuela conoció a su esposo en un café de Miami y le vendió mangos a García Márquez en 1982, ganó un concurso de cumbia en 1975.
9. **Público 13+**. Nada de contenido infantil (pospuesto). Evitar alcohol (se sustituyó "drinking" por karaoke) y figuras públicas en ejercicios.
10. Si algo no encaja naturalmente, se omite y se reporta (ej.: pasiva del present perfect continuous — omitida por antinaturalidad).

## Cambios de motor de esta sesión (ya hechos, no repetir)

- `motor-generico.html`: render de `inicio.interaccion` (mini-diálogo con clases .mini-dialog/.mini-who/.mini-txt) + shuffle Fisher-Yates del unscramble.
- `evaluacion-generico.html`: mismo shuffle.
- `lecciones-generico.html`: fix de tarjetas vocab (bandera + palabra + traduccion) y grid por columnas calculadas (8→4×2, 12→4×3, sin tarjetas huérfanas).
- `build.py`: `revisar_etapas` (≥5 por etapa, solo A2+).

## Flujo por tema (el ritmo que funcionó: ~20 temas en una noche)

1. Felipe da la guía del tema (o del cluster) — propósito, ejemplos semilla, tipo de ejercicios. Si no la da, se le pregunta solo lo decisivo (AskUserQuestion con opciones concretas); las últimas 5 de B1 las diseñó Claude solo con visto bueno general.
2. Generar el JSON completo por heredoc → `json.load` → `python3 build/build.py` → verificar 0 advertencias.
3. Actualizar `temas/pendientes.txt` (quitar línea) y `temas/hechos.txt` (agregar con notas).
4. Avisar a Felipe qué preview revisar. No avanzar 2+ temas sin checkpoint salvo que él lo pida.

## Próximos pasos sugeridos (en orden)

1. Felipe: commit + push + reenviar sitemap en Search Console (pico de demanda escolar es sept-oct; agosto es la ventana).
2. Decidir la línea pendiente de A2 (Negatives & Questions: ¿refuerzo o tachar?).
3. Renderizar `interaccion` también en la lección (video/slides).
4. Reviews tipo `joined_exercise` para A2 y B1 (como los 4 de A1) — espiral de repaso.
5. Definir mapa B2 con Felipe (NO inventarlo — regla de CLAUDE.md). Los adverbios comparativos ya quedaron en B1.
6. Marketing/SEO: títulos híbridos ya activos; considerar páginas programáticas de conjugación por verbo (long tail de Trends).
