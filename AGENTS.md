## Imported Claude Cowork project instructions

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
- `gap_fill` { texto (con ___), respuesta }
- `unscramble` { palabras, respuesta }
- `correct_mistake` { texto_con_error, respuesta }
- `transformation` { oracion_base, instruccion, respuesta }
- `write_opposite` { oracion_base, instruccion, respuesta }
- `short_answer_production` { pregunta, respuesta }

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

## El motor (`motor-generico.html`)

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
- **"estado"** → reporto qué niveles/temas ya tienen contenido, comparado contra el mapa de temas por nivel, para ver qué falta.

## Qué NO hacer sin preguntar primero

- No cambies el esquema JSON sin avisar — todo el contenido ya generado depende de que se mantenga estable.
- No agregues contenido para público "niños" todavía.
- No implementes evaluación de pronunciación real ni grabación de voz de estudiantes sin que Felipe lo apruebe explícitamente (tema de privacidad/menores pendiente).
- No inventes el mapa de temas por nivel de cero — pregúntale a Felipe si no está definido para ese nivel todavía.
