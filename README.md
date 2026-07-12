# ✨ EnglishAngel

**Material docente interactivo para inglés, del A1 al C1**

Secuencias de diagnóstico + práctica + evaluación, organizadas por nivel CEFR. Publicado en GitHub Pages con hosting $0.

---

## ¿Qué es esto?

Una biblioteca de **ejercicios reales y estructurados** que funciona simultáneamente como:
- 📚 Material para tus clases privadas
- 🌐 Páginas SEO públicas (compite con Agendaweb, Perfect English Grammar)
- 🎬 Guiones listos para vídeos tutoriales

Nada de ejercicios sueltos. Cada tema es una **secuencia completa** con diagnóstico real, práctica cognitiva estructurada (recognition → manipulation → production) y examen sin pistas.

---

## 🎯 Niveles y cobertura

- **A1** ✅ Completo (15 temas + 4 reviews)
- **A2** ✅ Completo (10 temas + 1 review)
- **B1** ✅ Completo (12 temas + 1 review)
- **B2** ✅ Completo (17 temas)
- **C1** ✅ Completo (11 temas + "Register & Style" capstone)

**Total:** 81 secuencias, 243 páginas interactivas.

---

## 🚀 Cómo funciona

### Para estudiantes
1. Abren la página de un tema (ej. "A1 — To Be & Nationalities")
2. Ven una **lección** con ejemplos narrativos y personajes recurrentes
3. Hacen **práctica** con 8–12 ejercicios variados (opción múltiple, huecos, unscramble, etc.)
4. Pueden tomar un **examen** (versión sin pistas, un intento, calificado)
5. Generan **hojas de práctica personalizadas** con el Exercise Generator

### Para ti (profesor)
- Copiar/pegar ejercicios a WhatsApp o Classroom
- Usar los temas como script para grabaciones
- Armar clases combinando 2+ temas con el Class Generator
- Insertar en tu perfil Superprof como prueba social

---

## 📂 Estructura (sin jerga técnica)

```
EnglishAngel/
├── motor/
│   ├── motor-generico.html         ← motor de ejercicios (NO tocar)
│   ├── lecciones-generico.html     ← motor de lecciones (NO tocar)
│   ├── evaluacion-generico.html    ← motor de exámenes (NO tocar)
│   └── generador-generico.html     ← motor del generador (NO tocar)
│
├── contenido/
│   ├── A1/
│   │   ├── a1-to-be-nationalities-01.json
│   │   ├── a1-have-got-01.json
│   │   └── ... (cada tema es un archivo JSON)
│   ├── A2/, B1/, B2/, C1/
│   └── ... (mismo patrón por nivel)
│
├── build/
│   └── build.py                    ← genera todas las 243 páginas
│
├── herramientas/
│   ├── generador-ejercicios.html   ← filtra y arma hojas personalizadas
│   └── generador-clases.html       ← arma clases combinando temas
│
├── datos/
│   ├── banco-maestro.json          ← todos los 864 ejercicios indexados
│   └── temas-completos.json        ← resumen de cada tema
│
├── preview/                         ← vista previa de cada tema (para revisar)
│
└── index.html                      ← página de inicio
```

---

## 🛠️ Tareas comunes

### Generar contenido nuevo (nuevo tema)

```bash
# Abre CLAUDE.md en el workspace y di:
# "nuevo tema: A1 | Present Simple — Affirmative | I am, you are, he is..."
```

El motor genera automáticamente:
- Archivo JSON en `contenido/A1/`
- Página de lección
- Página de práctica
- Página de examen
- Una vista previa para revisar

### Procesar un lote de temas pendientes

```bash
# Abre CLAUDE.md y di:
# "lote: temas/pendientes.txt"
```

Procesa todos los temas del backlog en order, uno por uno.

### Reconstruir todas las páginas tras editar un tema

```bash
python3 build/build.py
```

(Solo necesitas correr esto si editas JSON directamente — Felipe no es técnico, así que normalmente no lo harás.)

### Validar un tema antes de publicar

```bash
# Abre CLAUDE.md y di:
# "validar a1-present-simple-01.json"
```

Chequea que el diagnóstico sea real, la progresión cognitiva esté en orden, y el esquema sea válido.

---

## 🎨 Características clave

✅ **Diagnóstico real**, no aleatorio  
Cada tema contrasta el error típico de un hispanohablante contra la forma correcta.

✅ **Progresión cognitiva obligatoria**  
Recognition → Manipulation → Transformation. El motor valida esto automáticamente.

✅ **Personajes recurrentes**  
- **Sofía Reyes** (colombiana, diseñadora en Medellín)
- **Ben Whitfield** (británico, mochilero en Cartagena)
- **Kenji Sato** (japonés, estudiante de intercambio)
- **Abuela Carmen** (sabia, narradora de modales y phrasal verbs)

Reutilización narrativa: el teléfono perdido de Ben aparece en reported speech, deducción y conditional — mismo incidente, 3 ángulos gramaticales.

✅ **Ejercicios variados**  
8 tipos: Multiple Choice, True/False, Gap Fill, Unscramble, Correct Mistake, Transformation, Write Opposite, Short Answer Production.

✅ **Banco de ejercicios doble uso**  
Cada ejercicio aparece en: lección + práctica + generador de hojas personalizadas + generador de clases.

---

## 🌐 Publicación en GitHub Pages

El sitio vive en: **https://pipefleurs87-sudo.github.io/EnglishAngel.com/**

Para actualizar tras crear contenido:
1. Abre GitHub Desktop
2. Sincroniza la carpeta `EnglishAngel` al repo
3. Abre Search Console para validar nuevas URLs

(Felipe se encarga del push — aquí solo está el contenido.)

---

## 🔧 Reglas técnicas (para referencia)

**Nunca edites:**
- `motor/*.html` (salvo por bugs reales, y solo vía shell heredoc)
- `build/build.py` (salvo por bugs reales)

**Siempre usa shell `cat > archivo <<'EOF'`** para archivos grandes — las herramientas Edit/Write los truncan.

**El esquema JSON es obligatorio:**
Cada tema tiene un `id`, `nivel`, `tema`, `habilidades`, `banco_oraciones`, y `fases` (inicio, práctica, listening, reading). No agregar ni quitar campos sin avisar.

---

## 📋 Checklist de lanzamiento

- [x] A1 completo y publicado
- [x] A2 completo y publicado
- [x] B1 completo y publicado
- [x] B2 completo y publicado
- [x] C1 completo y publicado
- [x] Sitemap y robots.txt actualizados
- [x] SEO: títulos, descripciones, og:image
- [x] Exercise Generator listo
- [x] Class Generator listo
- [ ] Google Search Console validado
- [ ] Segunda URL en Superprof (la primera tiene antigüedad, no borrar)

---

## 💬 Preguntas frecuentes

**¿Puedo editar un tema que ya existe?**  
Sí. Edita el JSON en `contenido/{nivel}/` y reconstruye: `python3 build/build.py`.

**¿Dónde veo las vistas previas de los temas?**  
Abre `preview/{id}.html` en tu navegador. Es una página local sin conexión a internet.

**¿Cuántos ejercicios debería tener un tema?**  
A1: 8–10 por tipo  
A2+: 10–12 por tipo  
8 tipos = 64–96 ejercicios por tema (reconocimiento + manipulación + transformación)

**¿Qué hago si algo se ve roto?**  
Mándame la URL y una captura. Probablemente sea:
- JSON mal formado (chequealo con un editor JSON)
- Motor que necesita un update
- URL de GitHub Pages mal (reconstruir tras push)

---

## 📞 Contacto y soporte

**Tu email:** pipefleurs87@gmail.com  
**Tu perfil Superprof:** [[Enlace](https://www.superprof.es)](https://www.superprof.co/ingles-real-para-hablar-sin-miedo-conversacion-confianza-clases-disfrutan.html)

Para crear contenido nuevo o reportar bugs, usa la interfaz CLAUDE.md del repo.

---

**Última actualización:** Julio 2026  
**Estado:** Sitio vivo con 81 secuencias, 243 páginas, 864 ejercicios.  
**Siguiente:** Esperar validación de Google Search Console + decidir plataforma privada (login, progreso, calificaciones).
