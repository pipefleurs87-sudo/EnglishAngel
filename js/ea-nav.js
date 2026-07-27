/* EnglishAngel — navegacion compartida (2026-07-26)
   UN solo archivo controla los enlaces de modo de TODAS las paginas de tema.
   build.py lo genera desde /contenido (lista de temas con fluidez incrustada abajo),
   igual que hace con los demas artefactos: contenido = datos.

   Por que hace falta la lista: las paginas ya publicadas llevan incrustado el
   window.SEQUENCE_DATA de cuando se generaron, anterior al bloque fases.fluency.
   Por eso no se puede deducir de la propia pagina. Igual se comprueba SEQUENCE_DATA
   para que las paginas nuevas funcionen aunque la lista se quede corta.

   Idempotente: no duplica un enlace que ya exista. Si este archivo faltara,
   la pagina sigue funcionando exactamente igual que antes.

   Para añadir un modo nuevo (ej. Games) en TODO el sitio: se edita SOLO este archivo. */
(function () {
  var CON_FLUIDEZ = ["b1-adverbs-01", "b1-conditionals-0-1-2-01", "b1-gerund-vs-infinitive-01", "b1-passive-voice-01", "b1-present-perfect-bucket-list-01", "b1-present-perfect-continuous-01", "b1-present-perfect-ever-experiences-01", "b1-present-perfect-vs-past-simple-01", "b1-review-grand-01", "b1-used-to-01", "b1-will-vs-going-to-01", "b2-causative-01", "b2-idioms-money-01", "b2-idioms-time-effort-01", "b2-linkers-01", "b2-mixed-conditionals-01", "b2-modals-deduction-past-01", "b2-modals-deduction-present-01", "b2-modals-obligation-past-01", "b2-phrasal-verbs-down-01", "b2-phrasal-verbs-get-01", "b2-phrasal-verbs-on-off-01", "b2-phrasal-verbs-out-01", "b2-phrasal-verbs-up-01", "b2-relative-clauses-01", "b2-reported-speech-01", "b2-third-conditional-01", "b2-wish-if-only-01", "c1-advanced-passive-01", "c1-cleft-sentences-01", "c1-ellipsis-substitution-01", "c1-emphatic-structures-01", "c1-future-in-the-past-01", "c1-gerund-clauses-subject-01", "c1-inversion-01", "c1-participle-clauses-01", "c1-register-style-01", "c1-subjunctive-01", "c1-would-rather-prefer-01"];

  function init() {
    var D = window.SEQUENCE_DATA;
    if (!D || !D.id) return;
    var mb = document.querySelector('.modebar') || document.querySelector('.modebar-fixed');
    if (!mb) return;

    var tieneFluidez = CON_FLUIDEZ.indexOf(D.id) !== -1 || !!(D.fases && D.fases.fluency);
    var modos = [];
    if (tieneFluidez) modos.push(['🗣 Fluency', '../fluency/']);
    modos.push(['🎮 Games', '../juegos/']);   // activado 2026-07-27 (ludoteca publicada)

    modos.forEach(function (m) {
      var destino = m[1] + D.id + '.html';
      if (mb.querySelector('a[href="' + destino + '"]')) return;
      var a = document.createElement('a');
      a.textContent = m[0];
      a.href = destino;
      mb.appendChild(a);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
