# Guía EnglishAngel (para Felipe, sin tecnicismos)

Todo esto ya está construido y funcionando en tu computador. Esta guía te dice dos cosas: **cómo verlo ahora mismo** y **cómo ponerlo gratis en internet** cuando quieras. No necesitas saber programar.

---

## 1. Verlo ahora (cero pasos técnicos)

Abre el archivo **`index.html`** con doble clic. Es la portada de tu banco. Desde ahí entras a cada tema, haces los ejercicios, le das a "Revisar respuestas" y ves tu puntaje. El botón ▶ del listening usa la voz del navegador (necesitas internet la primera vez para las tipografías).

Así se ve la clase completa: diagnóstico → definición → práctica → listening → reading. Eso es lo que ningún sitio de la competencia te da.

---

## 2. Cómo pedirme más contenido

No tocas archivos. Me escribes con una de estas frases (ya están definidas en tu proyecto):

- **`nuevo tema: A1 | There is / There are | oraciones semilla opcionales`** → genero ese tema, su JSON y su página.
- **`lote: temas/pendientes.txt`** → genero de una todos los temas que están en la lista de pendientes (ya te dejé 15 ahí esperando).
- **`validar contenido/A1/archivo.json`** → reviso que un tema esté bien hecho.
- **`estado`** → te digo qué niveles ya tienen contenido y qué falta.

Cada vez que genero contenido nuevo, corro el build y quedan las páginas listas. Tú solo revisas y, si te gusta, publicas (paso 3).

---

## 3. Ponerlo en internet GRATIS (GitHub Pages)

Esto se hace **una sola vez** para dejarlo montado. Después, actualizar es arrastrar archivos.

### Lo que necesitas
- Una cuenta gratis en **github.com** (crear con tu correo, 2 minutos).
- Nada más. No se paga nada.

### Pasos (te acompaño cuando quieras hacerlo)
1. Entra a github.com y crea una cuenta.
2. Arriba a la derecha, botón **"+" → New repository**.
3. Nombre del repositorio: escribe `englishangel`. Déjalo en **Public**. Clic en **Create repository**.
4. En la página que aparece, busca el enlace **"uploading an existing file"**.
5. Arrastra ahí **todo el contenido de esta carpeta** (index.html, y las carpetas motor, contenido, preview). Clic en **Commit changes**.
6. Ve a la pestaña **Settings** del repositorio → menú lateral **Pages**.
7. En "Branch" elige **main** y carpeta **/ (root)**. Clic en **Save**.
8. Espera 1–2 minutos. GitHub te dará una dirección tipo **`https://tuusuario.github.io/englishangel/`**. ¡Eso ya es tu sitio público!

> Cuando llegues a este punto, avísame y te guío pantalla por pantalla. Es más fácil de lo que suena.

### Para actualizar después
Cada vez que yo genere temas nuevos, subes los archivos igual que en el paso 5 (arrastrar y "Commit"). El sitio se actualiza solo en un minuto.

### Dominio propio (opcional, para después)
Cuando quieras verte pro (ej. `englishangel.com`), se compra un dominio (~$10–15/año) y se conecta a GitHub Pages. Es el único gasto, y es opcional. Con la dirección `.github.io` arrancas perfecto y gratis.

---

## 4. Grabar el video de YouTube (lección en slides)

Cada tema tiene también una **lección en diapositivas**, hecha para grabar en pantalla. Ábrela desde el índice (botón **▶ Lección**) o desde la carpeta `leccion/`.

Cómo se maneja mientras grabas:
- **Flecha derecha → / barra espaciadora / clic** = siguiente slide.
- **Flecha izquierda ←** = atrás.
- **Tecla F** = pantalla completa (ideal antes de empezar a grabar).
- Sale del mismo JSON del tema: portada → el error típico → la regla → vocabulario → ejemplos → cierre. Sin notas en pantalla, tú hablas encima.

Flujo sugerido: abres la lección, tecla **F** para pantalla completa, arrancas tu grabador de pantalla, y vas avanzando con → mientras explicas. Al terminar, ese video va a YouTube y en la descripción pones el link a los ejercicios. Costo: $0.

---

## 5. Cómo está organizado (por si tienes curiosidad)

- **`index.html`** → la portada del banco.
- **`motor/motor-generico.html`** → motor de ejercicios. Renderiza cualquier tema. NO se toca por tema.
- **`motor/lecciones-generico.html`** → motor de lecciones (las slides para video). Tampoco se toca por tema.
- **`contenido/{nivel}/`** → un archivo `.json` por tema. Aquí vive el contenido de verdad.
- **`preview/`** → páginas de ejercicios listas para publicar (una por tema). Se generan solas.
- **`leccion/`** → lecciones en slides para video (una por tema). Se generan solas.
- **`temas/`** → tu backlog (`pendientes.txt`) y lo ya hecho (`hechos.txt`).
- **`build/build.py`** → el script que convierte los JSON en páginas. Lo corro yo.
- **`marketing/`** → tu perfil de Superprof reescrito.

Un tema (un JSON) genera **ejercicios + lección-video** a la vez. Contenido nuevo = un archivo de datos nuevo, no una página nueva. Por eso escala a miles sin volverse un caos.

La idea central: **contenido nuevo = un archivo de datos nuevo, no una página nueva.** Por eso esto escala a miles de ejercicios sin volverse un caos.

## 6. SEO — un paso manual cuando publiques (importante)

El sitio ya trae SEO listo: cada página tiene su título y descripción en inglés (con cola en español), hay un buscador en la portada, y se generan `sitemap.xml` y `robots.txt` para que Google encuentre las páginas.

**Lo único que debes hacer una vez:** en `build/build.py`, línea `BASE_URL`, cambia `USERNAME` por tu usuario de GitHub (ej. si tu usuario es `felipe123`, queda `https://felipe123.github.io/englishangel`). Avísame y lo hago yo. Después de publicar, registra el sitio gratis en **Google Search Console** y envía el `sitemap.xml` — así Google indexa tus 72 páginas más rápido. Te acompaño cuando llegues ahí.

**Estrategia realista:** no vamos a ganarle a los sitios grandes por "present simple exercises" el primer mes. Ganamos el *long-tail*: tus temas híper-específicos (profesiones A–Z con 'a person who', family possessive completions, present simple vs continuous en paralelo). Cada video de YouTube y tu perfil de Superprof enlazando al sitio construyen autoridad con el tiempo.
