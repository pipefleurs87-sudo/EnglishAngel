## Imported Claude Cowork project instructions

> **LEE `HANDOFF.md` PRIMERO.** Este archivo describe cómo generar *contenido*.
> `HANDOFF.md` describe cómo funciona el *código* — y corrige varias cosas que
> este archivo daba por sentadas. En particular:
>
> - `preview/`, `leccion/` y `evaluacion/` son **artefactos de `build/build.py`**,
>   no archivos que se editen a mano.
> - Correr `build.py` sin verificar antes **puede borrar features vivas** que solo
>   existen en los archivos generados. Ya pasó una vez con el reproductor de mp3.
> - El motor de calificación vive ahora en `js/ea-scoring.js`, con tests en
>   `build/test/`. No está dentro de `motor-generico.html`.
> - Existe un segundo repo, `EnglishAngel-Aula`, con su propia copia del motor.

# CLAUDE.md — Plataforma de apoyo docente (inglés, CEFR)

Este archivo es el contexto persistente del proyecto. Léelo completo antes de generar o modificar nada.

## Qué es esto

Una plataforma de recursos para profesores de inglés, organizada por 3 fases de clase (inicio, práctica, evaluación) × 6 niveles CEFR (A1-C2), con un motor genérico que renderiza cualquier tema desde un JSON — el contenido nuevo no requiere código nuevo.

Diferenciador frente a agendaweb / perfect-english-grammar / liveworksheets: secuencias completas (no ejercicios sueltos), diagnóstico antes de la regla, personajes recurrentes, y un banco de oraciones que alimenta múltiples tipos de ejercicio en vez de contenido repetido.

## Estructura de carpetas (créala si no existe)

```
/motor/motor-generico.html      ← el motor, NO se toca por tema — solo por mejoras de ingeniería
/contenido/{nivel}/{id}.json    ← un archivo por secuencia, ej. /contenido/A1/a1-to-be-nationalities-01.json
/preview/{id}.html              ← copia del motor con el JSON de esa secuencia incrustado, para revisión visual
/temas/pendientes.txt           ← backlog de temas por generar (formato: "nivel | tema | oraciones semilla")
/temas/hechos.txt               ← temas ya generados, para no repetir
```

## Esquema de contenido (obligatorio, no agregar ni quitar campos)

```json
{
  "id": "{nivel}-{tema-slug}-01",
  "nivel": "A1|A2|B1|B2|C1|C2",
  "tema": "...",
  "habilidades": ["grammar","listening","reading","writing","speaking","vocabulary"],
  "vocabulario": [ {"pais":"","bandera":"","nacionalidad":""} ],
  "banco_oraciones": [ {"id":"s1","oracion":"..."} ],
  "fases": {
    "inicio": {
      "banner_diagnostico": {"opcion_a":"...","opcion_b":"...","correcta":"a|b"},
      "definicion_pragmatica": "...",
      "vocab_warmup": true
    },
    "practica": { "ejercicios": [ ... ] },
    "listening": { "guion": ["Personaje: línea"], "gaps": ["palabra"] },
    "reading": { "texto": "...", "preguntas": [ {"afirmacion":"...","respuesta":"true|false"} ] }
  }
}
```

Tipos válidos en `practica.ejercicios` (usa varios por secuencia, no uno solo):
- `multiple_choice` { pregunta (con ___), opciones, respuesta }
- `true_false` { afirmacion, respuesta }
- `gap_fill` { texto (con ___), respuesta } — la oración va **entera** en `texto`; la pista entre paréntesis tras el hueco: `"we ___ (stay) at home."`. Soporta N huecos por oración.
- `unscramble` { palabras, respuesta }
- `correct_mistake` { texto_con_error, respuesta }
- `transformation` { oracion_base, instruccion, respuesta }
- `write_opposite` { oracion_base, instruccion, respuesta }
- `short_answer_production` { pregunta, respuesta }
- `banked_choice` { prompt, options[{id,label}], items[{id,prompt,answer}], allowReuse } — multiple matching estilo Cambridge. Soportado por el motor, **sin contenido todavía**.

## Reglas de generación de contenido

1. **Diagnóstico real, no aleatorio**: `banner_diagnostico` contrasta el error típico de un hispanohablante contra la forma correcta.
2. **Definición pragmática = una oración**: dice para qué se usa la estructura, nunca cómo se conjuga.
3. **Personajes recurrentes** — úsalos en `banco_oraciones` cuando el tema lo permita, no los fuerces:
   - Sofía Reyes: colombiana, diseñadora en Medellín, organizada → simple present, rutinas
   - Ben Whitfield: británico, mochilero en Cartagena, torpe → past simple, narrativa
   - Kenji Sato: japonés, estudiante de intercambio, curioso → preguntas, comparativos
   - Abuela Carmen: abuela de Sofía, sabia → present perfect, modales de consejo
4. **Progresión cognitiva obligatoria**: recognition (`multiple_choice`, `true_false`) → manipulation (`gap_fill`, `unscramble`, `correct_mistake`) → transformation (`transformation`, `write_opposite`, `short_answer_production`).
5. Si el tema no tiene vocabulario propio (ej. do/does), omite `"vocabulario"` y pon `"vocab_warmup": false`.
6. Público objetivo por ahora: **estándar (13+)**. No generar contenido para niños todavía — eso es una fase posterior explícitamente pospuesta.
7. Si un tipo de ejercicio no encaja de forma natural con el tema (pasa más en B2+ con estructuras complejas), no lo fuerces — omítelo de esa secuencia y dilo en el resumen al terminar.

## El motor

Ya no es un solo archivo. Hay **tres plantillas** en `/motor` (`motor-generico.html`
para práctica, `lecciones-generico.html` para lección, `evaluacion-generico.html`
para examen) y `build.py` las estampa en 243 páginas. Además hay dos copias más en
el repo `EnglishAngel-Aula`. Ver `HANDOFF.md` §7 — es deuda técnica conocida.

La calificación y la normalización de respuestas **salieron** del motor: viven en
`js/ea-scoring.js`, con 19 tests en `build/test/scoring.test.js`.

No se reescribe por tema. Solo se modifica cuando:
- Se agrega un tipo de ejercicio nuevo al switch de `renderExercise()`
- Se corrige un bug real (documenta qué corregiste y por qué)
- Se ajusta el motor de calificación (`normalize()`, `gradeAll()`)

Mantén los tokens de diseño ya establecidos al tocar el motor — no los reinventes:
- Colores: `--ink:#1B2A41` `--paper:#EFF1EC` `--red:#B23A2E` `--gold:#C9962F` `--muted:#6B7079` `--line:#D8DAD1`
- Tipografía: Source Serif 4 (títulos), IBM Plex Sans (cuerpo), IBM Plex Mono (etiquetas/tags), Caveat (marcas de corrección estilo lápiz rojo y notas docentes)
- El audio (listening) se encadena con `utterance.onend`, nunca con `setTimeout` fijo — ya se corrigió ese bug una vez, no lo reintroduzcas.

## Límites técnicos conocidos (no son bugs, son decisiones pendientes)

- El reconocimiento de voz (si se implementa) es transcripción, no evaluación fonética real — no lo vendas ni lo documentes como "evaluación de pronunciación".
- La calificación de texto libre normaliza acentos y contracciones, pero sigue siendo comparación textual, no semántica.
- Grabar voz de estudiantes menores de edad tiene implicaciones de privacidad sin resolver — no implementar sin que Felipe lo revise primero.

## Comandos de trabajo

Usa estas frases para que yo sepa qué modo activar:

- **"nuevo tema: [nivel] | [tema] | [oraciones semilla opcional]"** → genero un JSON siguiendo el esquema y las reglas de arriba, lo guardo en `/contenido/{nivel}/`, y creo su preview en `/preview/`.
- **"lote: temas/pendientes.txt"** → proceso todos los temas listados ahí, uno por uno, moviendo cada uno a `temas/hechos.txt` al terminar, y doy un resumen final: cuántos generé, cuáles tuvieron algún tipo de ejercicio omitido y por qué.
- **"validar [archivo]"** → reviso ese JSON contra el esquema y las reglas (no solo estructura, también si el diagnóstico es real, si la progresión cognitiva está en orden), y reporto qué falta o qué está flojo.
- **"motor: [descripción del cambio]"** → modifico `motor-generico.html` respetando los tokens de diseño y sin romper el contenido ya generado.
- **"tests"** → corro `node --test "build/test/*.test.js"` (las comillas importan) y reporto.
- **"estado"** → reporto qué niveles/temas ya tienen contenido, comparado contra el mapa de temas por nivel, para ver qué falta.

## Qué NO hacer sin preguntar primero

- No cambies el esquema JSON sin avisar — todo el contenido ya generado depende de que se mantenga estable.
- No agregues contenido para público "niños" todavía.
- No implementes evaluación de pronunciación real ni grabación de voz de estudiantes sin que Felipe lo apruebe explícitamente (tema de privacidad/menores pendiente).
- No corras `build/build.py` sin verificar antes que reproduce lo commiteado (`HANDOFF.md` §4).
- No cambies `weightMode` de `'byItems'` a `'equal'` en el motor de nota sin hablarlo: cambia la nota de las 81 evaluaciones y el umbral de aprobación.
- No toques el mapa de contracciones de `normalize()`: alteraría notas ya dadas.
- No arregles algo en el sitio sin mirar si `EnglishAngel-Aula` tiene el mismo bug en su copia.
- No inventes el mapa de temas por nivel de cero — pregúntale a Felipe si no está definido para ese nivel todavía.
