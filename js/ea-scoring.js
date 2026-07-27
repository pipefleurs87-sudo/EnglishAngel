/* EnglishAngel — motor de calificacion (2026-07-27)

   UN solo archivo con la logica de normalizacion y nota. Lo usan las paginas de
   evaluacion en el navegador y los tests en node (node --test build/test/).

   Tres decisiones que NO son cosmeticas:

   1. La unidad calificable es el ITEM, no el ejercicio. Un gap-fill de 5 huecos
      con 4 aciertos vale 0.8, no 0.
   2. La nota promedia PORCENTAJES por categoria, ponderados — nunca items crudos.
      Sumando items, una seccion de 30 huecos de grammar ahoga una de 5 de reading.
   3. Sin nada calificable la nota es null, NUNCA 0. Un 0 es una nota real y le
      pone un cero al estudiante que no hizo nada malo.

   Tres estados por categoria, no un booleano:
     scored     el estudiante lo hace, sale en el reporte, suma a la nota
     formative  el estudiante lo hace, sale en el reporte, NO suma
     skipped    no se hace, no sale, no suma
   'formative' es lo que de verdad se queria al pedir "sacar el listening de la
   nota": el estudiante practica y el profesor ve el desempeno, sin penalizar.
*/
(function (root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.EAScoring = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var APOSTROFOS = /[‘’ʼ´`]/g;
  var INVISIBLES = /[​-‍﻿]/g;
  var ESPACIOS_RAROS = /[    ]/g;

  // Se conserva tal cual estaba en el motor: cambiarlo alteraria notas ya dadas.
  var CONTRACCIONES = {
    "i'm": "i am", "you're": "you are", "he's": "he is", "she's": "she is",
    "it's": "it is", "we're": "we are", "they're": "they are",
    "isn't": "is not", "aren't": "are not", "don't": "do not",
    "doesn't": "does not", "didn't": "did not", "can't": "cannot",
    "won't": "will not", "that's": "that is", "what's": "what is"
  };

  function normalize(valor, opts) {
    opts = opts || {};
    if (valor == null) return '';
    var s = String(valor)
      .replace(INVISIBLES, '')
      .replace(ESPACIOS_RAROS, ' ')
      .replace(APOSTROFOS, "'")   // ANTES del mapa: el motor viejo lo hacia despues
      .toLowerCase()
      .replace(/\s+'/g, "'")      // "I 'd" -> "i'd"
      .trim();

    for (var k in CONTRACCIONES) {
      if (!Object.prototype.hasOwnProperty.call(CONTRACCIONES, k)) continue;
      s = s.replace(new RegExp('\\b' + k.replace("'", "'?") + '\\b', 'g'), CONTRACCIONES[k]);
    }

    s = s.normalize('NFD').replace(/[̀-ͯ]/g, '');
    s = opts.stripFinalPunctuation
      ? s.replace(/[.,;:!?]+$/, '')
      : s.replace(/[.,;:!?]/g, '');
    return s.replace(/\s+/g, ' ').trim();
  }

  function matchesAny(aceptadas, dada, opts) {
    var lista = Array.isArray(aceptadas) ? aceptadas : [aceptadas];
    var g = normalize(dada, opts);
    if (g === '') return false;
    for (var i = 0; i < lista.length; i++) {
      if (normalize(lista[i], opts) === g) return true;
    }
    return false;
  }

  function isAnswered(g) {
    if (g == null) return false;
    if (Array.isArray(g)) return g.length > 0;
    return String(g).trim() !== '';
  }

  // Categoria por tipo de ejercicio. El schema de contenido no la trae, y no se
  // toca: se deriva. Se puede sobreescribir por item con item.category.
  var CATEGORIA_POR_TIPO = {
    multiple_choice: 'grammar', true_false: 'grammar', gap_fill: 'grammar',
    unscramble: 'grammar', correct_mistake: 'grammar',
    transformation: 'grammar', write_opposite: 'grammar',
    short_answer_production: 'writing',
    reading_comprehension: 'reading',
    banked_choice: 'listening'
  };

  function categoriaDe(item) {
    return item.category || CATEGORIA_POR_TIPO[item.tipo] || 'grammar';
  }

  function checkItem(item) {
    var dada = item.given;
    switch (item.tipo) {
      case 'banked_choice':
      case 'multiple_choice':
      case 'true_false':
        return String(dada) === String(item.answers);
      default:
        return matchesAny(item.answers, dada, { stripFinalPunctuation: true });
    }
  }

  /* items: [{ id, tipo, category?, answers, given }]
     config: { modes, weights, defaultMode, scale } */
  function scoreAssessment(items, config) {
    config = config || {};
    var modes = config.modes || {};
    var weights = config.weights || {};
    var defaultMode = config.defaultMode || 'scored';
    var scale = config.scale == null ? 100 : config.scale;
    // 'byItems': el peso de cada categoria es su numero de items. Con eso el promedio
    // ponderado de porcentajes ES aciertos_totales/items_totales — o sea, la nota
    // historica de EnglishAngel. Cambiar a 'equal' redistribuye el peso a partes iguales.
    var weightMode = config.weightMode || 'equal';

    var byCategory = {};
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      var cat = categoriaDe(it);
      var mode = Object.prototype.hasOwnProperty.call(modes, cat) ? modes[cat] : defaultMode;
      if (mode === 'skipped') continue;

      if (!byCategory[cat]) {
        byCategory[cat] = {
          mode: mode, weight: Object.prototype.hasOwnProperty.call(weights, cat) ? weights[cat] : 1,
          correct: 0, incorrect: 0, unanswered: 0, possible: 0, percent: null, items: []
        };
      }
      var b = byCategory[cat];
      var respondido = isAnswered(it.given);
      var ok = respondido && checkItem(it);

      b.possible += 1;
      if (!respondido) b.unanswered += 1;
      else if (ok) b.correct += 1;
      else b.incorrect += 1;

      b.items.push({
        id: it.id, tipo: it.tipo, given: it.given == null ? null : it.given,
        expected: it.answers, ok: ok, answered: respondido
      });
    }

    var num = 0, den = 0;
    for (var cat2 in byCategory) {
      if (!Object.prototype.hasOwnProperty.call(byCategory, cat2)) continue;
      var bb = byCategory[cat2];
      bb.percent = bb.possible ? bb.correct / bb.possible : null;
      if (weightMode === 'byItems' && !Object.prototype.hasOwnProperty.call(weights, cat2)) {
        bb.weight = bb.possible;
      }
      if (bb.mode !== 'scored' || !bb.possible) continue;
      num += bb.percent * bb.weight;
      den += bb.weight;
    }

    var ratio = den ? num / den : null;
    var cats = Object.keys(byCategory);
    return {
      ratio: ratio,
      grade: ratio == null ? null : ratio * scale,
      byCategory: byCategory,
      counted: cats.filter(function (c) { return byCategory[c].mode === 'scored'; }),
      reported: cats.filter(function (c) { return byCategory[c].mode === 'formative'; })
    };
  }

  return {
    normalize: normalize,
    matchesAny: matchesAny,
    isAnswered: isAnswered,
    categoriaDe: categoriaDe,
    scoreAssessment: scoreAssessment,
    CATEGORIA_POR_TIPO: CATEGORIA_POR_TIPO
  };
});
