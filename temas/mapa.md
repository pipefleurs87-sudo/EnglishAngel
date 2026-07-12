# Mapa de temas A1-B1 — priorizado por demanda real

Fuente: sesión Google Trends (jul 2026, MX/CO, últimos 12 meses) + contadores de uso ISLCollective + secuenciación agendaweb. Detalle en memoria del proyecto.

## Los 4 datos que ordenan este mapa

1. **Demanda por término (media Trends MX):** past simple 57 > pasado simple 51 > present simple 50 > presente simple 39 > verbo to be 30. El público busca en español pero nombra el tema en inglés → títulos híbridos: "Past Simple (pasado simple)".
2. **Concentración A1-A2:** ISLCollective muestra 5-10x más uso en temas elementales (to be ~496k usos, present simple ~555k) que en B2+ (conditionals 666 worksheets vs 3.675 de present simple). Prioridad: el mejor A1-B1 que existe, no cobertura C1/C2.
3. **Contrastes = categoría propia:** "present perfect or past simple" tiene categoría dedicada (257 worksheets + 185 videos). Los puntos de confusión son unidades de contenido, no extras.
4. **Estacionalidad escolar:** pico sept-oct (índice 100), colapso dic (6-8) y Semana Santa (~15). **Deadline: A2 completo online antes de agosto 2026.**

## Estado (actualizado 2026-07-12, noche — B2 y C1 completos)

- A1, A2 y B1 completos: 53 secuencias.
- B2 completo: 17 temas (Fase 4 gramática + Fase 5 léxico).
- C1 Fase 6 CERRADA: 11 temas, cluster único C1+C2 combinado (ver "Pivote C1/C2" abajo) — subjunctive, cleft sentences, inversion, gerund clauses as subject, participle clauses, emphatic structures, advanced passive, future in the past, ellipsis & substitution, would rather/prefer, y el capstone register & style.
- Total del sitio: 81 secuencias, 243 páginas, build sin advertencias.
- Pendiente: nada priorizado por ahora — Felipe decide próximo paso (subir a GitHub, o seguir con la plataforma privada).

## Pivote C1/C2 — cluster único (2026-07-12)

Decisión de Felipe: en vez de construir C1 y C2 como niveles separados ("menos contenido, pero más especializado"), todo se archiva bajo nivel `C1` en el esquema. El matiz C2 (más registro/precisión que gramática nueva, ver pivote B2/C1/C2 arriba) vive en dos lugares sin necesitar una secuencia aparte: el campo nuevo opcional `tambien_valido` en cualquier ejercicio (muestra una segunda forma válida junto a la respuesta, solo en lección y ejercicios — el examen se mantiene limpio, sin pistas) y las tablas de referencia de cada tema. Se agregó un tema capstone específico sobre control de registro (Register & Style) porque eso es lo que realmente distingue C2 de C1, no gramática adicional. El diagnóstico (`banner_diagnostico`) también se reenfocó para C1/C2: de "error típico vs correcto" a "forma de manual vs forma natural" — la mayoría de alternativas en C1 no son errores, son menos sofisticadas. Ninguno de estos cambios (campo nuevo, reenfoque del diagnóstico) toca los 70 temas A1-B2 ya generados.

## Orden de generación (el detalle vive en pendientes.txt)

**Fase 1 — cerrar A1** (5 temas): articles, adjectives, plurals, have got, imperatives. Articles primero: error fósil del hispanohablante (a apple, the people is, omisión de artículo).

**Fase 2 — A2 núcleo** (la apuesta del pico de agosto): was/were → past simple regular/irregular → past simple neg & questions (regla de formas) → there is/are → countables → comparatives → going to. Past simple es EL término más buscado del nicho; el nivel entero se ancla ahí.

**Fase 3 — B1** (los contrastes estrella): present perfect experiencias → **present perfect vs past simple** (la categoría con demanda propia) → for/since/just/already/yet → past continuous vs past simple → will vs going to → first conditional → second conditional → used to → passive → gerund vs infinitive.

## Transversales derivados de la data (requieren decisión/motor, no son temas)

- **Tabla de referencia imprimible por secuencia** ("tabla del verbo to be" +70% en Trends): asset barato, imán SEO. Los arquetipos tiempo_verbal ya generan tabla de conjugación — falta exportarla como imprimible.
- **Páginas programáticas por verbo irregular** (long tail: "pasado simple de fly", "verbo run en pasado simple y participio"): una página por verbo generada desde JSON. Cambio de motor/build — decidir con Felipe.
- **Vocabulario de juego en metadata** ("wordwall", "kahoot", "games" aparecen en consultas): describir las secuencias también como "juego interactivo" donde aplique.
- Público niños: demanda confirmada en Trends ("exercises for kids" en ascenso) pero **sigue pospuesto** por decisión explícita.

## Pivote 2026-07-12 — B2/C1/C2 sí se construyen

Decisión de Felipe: un sitio que llega hasta B1 no da credibilidad como oferta de un profesor — "yo no confiaría solo hasta B1". Esto NO contradice la data de arriba (la demanda de búsqueda sigue concentrada en A1-B1); es un argumento distinto, de percepción/conversión para su negocio de clases privadas (Superprof), no de tráfico orgánico. Por eso B2/C1/C2 se construyen igual, pero A1-B1 sigue siendo lo que se optimiza para SEO puro — no se le quita prioridad de mantenimiento a lo ya hecho.

B2 sigue el mismo patrón de fases que A1/A2/B1: primero la columna gramatical completa (Fase 4 en pendientes.txt — relative clauses avanzadas, reported speech, modales de deducción presente/pasado, modales de obligación pasado, causativo have/get done, third conditional, mixed conditionals, wish/if only), después una ola léxica (Fase 5 — phrasal verbs agrupados por partícula con "get" introductorio, linkers por función pragmática, idioms por tema narrados por Abuela Carmen). C1 se planea después de cerrar B2 completo (Fases 4+5). C2 queda como exploración sin urgencia de negocio — ver conversación de diseño en memoria del proyecto sobre cómo C1→C2 es más refinamiento de registro/matiz que gramática nueva, y el límite técnico de calificación por comparación literal que eso implica para producción libre.

## Qué NO priorizar (dentro de lo ya decidido)

Evaluación de pronunciación (límite técnico conocido, ver CLAUDE.md). Público niños (pospuesto, decisión explícita de Felipe).
