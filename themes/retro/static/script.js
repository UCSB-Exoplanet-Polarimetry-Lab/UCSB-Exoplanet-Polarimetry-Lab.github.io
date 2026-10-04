/* Millar-Blanchaer Research Group — GeoCities Edition
   All the "dynamic" bits: calm-mode toggle, visitor counter,
   slideshow, guestbook (stored in your own browser only), web ring. */
(function () {
  function store(key, val) { try { if (val === undefined) return localStorage.getItem(key); localStorage.setItem(key, val); } catch (e) { return null; } }

  /* CALM DOWN: turns off every blinking thing. Remembered per browser. */
  var site = document.getElementById('site');
  /* Inside the frames edition, the banner and nav live in their own frames, so hide this page's copies. */
  if (window.top !== window.self && !document.body.classList.contains('is-frame')) site.classList.add('framed');
  var calmBtn = document.getElementById('calmBtn');
  function setCalm(on) {
    site.classList.toggle('calm', on);
    if (calmBtn) { calmBtn.textContent = on ? 'LIVE A LITTLE' : 'CALM DOWN'; calmBtn.classList.toggle('party', on); calmBtn.setAttribute('aria-pressed', on); }
    store('mmb-calm', on ? '1' : '0');
  }
  if (store('mmb-calm') === '1') setCalm(true);
  if (calmBtn) calmBtn.addEventListener('click', function () { setCalm(!site.classList.contains('calm')); });

  /* Visitor counter: counts *your* visits, in your browser. Honest, like a hit counter never was. */
  var digits = document.getElementById('visitorDigits');
  if (digits) {
    var n = parseInt(store('mmb-visits') || '0', 10) + 1;
    store('mmb-visits', n);
    var seed = 1998 + n * 7; // every site started at some suspiciously large number
    var s = String(seed).padStart(6, '0');
    digits.innerHTML = '';
    for (var i = 0; i < s.length; i++) { var d = document.createElement('span'); d.textContent = s[i]; digits.appendChild(d); }
  }

  /* Slideshow (the old carousel, now with buttons that go clunk) */
  var show = document.querySelector('.show');
  if (show) {
    var imgs = show.querySelectorAll('.stage img');
    var cap = show.querySelector('.cap');
    var dots = show.querySelector('.dots');
    var cur = 0, timer = null;
    for (var k = 0; k < imgs.length; k++) {
      (function (idx) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = idx + 1; b.setAttribute('aria-label', 'Photo ' + (idx + 1));
        b.addEventListener('click', function () { go(idx); start(); });
        dots.appendChild(b);
      })(k);
    }
    function go(i) {
      cur = (i + imgs.length) % imgs.length;
      for (var j = 0; j < imgs.length; j++) { imgs[j].classList.toggle('on', j === cur); dots.children[j].classList.toggle('on', j === cur); }
      cap.textContent = imgs[cur].getAttribute('alt') || '';
    }
    function start() { stop(); if (!site.classList.contains('calm')) timer = setInterval(function () { go(cur + 1); }, 6000); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    show.querySelector('.prev').addEventListener('click', function () { go(cur - 1); start(); });
    show.querySelector('.next').addEventListener('click', function () { go(cur + 1); start(); });
    show.addEventListener('mouseenter', stop); show.addEventListener('mouseleave', start);
    go(0); start();
  }

  /* Guestbook: entries live in localStorage, so only you see what you wrote. */
  var gbForm = document.getElementById('gbForm');
  if (gbForm) {
    var list = document.getElementById('gbList');
    var seedEntries = [
      { who: 'Beta Pictoris b', from: '19.4 parsecs away', msg: 'Nice site. Would appreciate it if you stopped watching me orbit.', when: '1995-03-14' },
      { who: 'Luhman 16A', from: 'the third-closest system to the Sun', msg: 'Banded clouds? Rude. Also true.', when: '2020-05-01' }
    ];
    function load() { try { return JSON.parse(store('mmb-guestbook') || 'null') || seedEntries; } catch (e) { return seedEntries; } }
    function render() {
      var entries = load(); list.innerHTML = '';
      entries.slice().reverse().forEach(function (e) {
        var div = document.createElement('div'); div.className = 'gb-entry';
        var who = document.createElement('div'); who.className = 'who'; who.textContent = e.who;
        if (e.from) { var fr = document.createElement('span'); fr.textContent = ' from ' + e.from; who.appendChild(fr); }
        var msg = document.createElement('div'); msg.textContent = e.msg;
        var when = document.createElement('div'); when.className = 'when'; when.textContent = e.when;
        div.appendChild(who); div.appendChild(msg); div.appendChild(when); list.appendChild(div);
      });
    }
    gbForm.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var who = document.getElementById('gb-name').value.trim() || 'Anonymous Coward';
      var from = document.getElementById('gb-from').value.trim();
      var msg = document.getElementById('gb-msg').value.trim();
      if (!msg) return;
      var entries = load(); entries.push({ who: who, from: from, msg: msg, when: new Date().toISOString().slice(0, 10) });
      store('mmb-guestbook', JSON.stringify(entries)); render(); gbForm.reset();
      document.getElementById('signedMsg').hidden = false;
    });
    render();
  }

  /* Publications filter pills */
  var pills = document.querySelectorAll('.pill'), pubRows = document.querySelectorAll('tr.pub'), yrRows = document.querySelectorAll('tr.yr');
  if (pills.length) {
    pills.forEach(function (p) { p.addEventListener('click', function () {
      var k = p.dataset.kind, n = 0;
      pills.forEach(function (q) { var a = q === p; q.classList.toggle('active', a); q.setAttribute('aria-pressed', a); });
      pubRows.forEach(function (r) { var show = k === 'all' || r.dataset.kind === k; r.hidden = !show; if (show) n++; });
      yrRows.forEach(function (y) { var nxt = y.nextElementSibling, any = false; while (nxt && !nxt.classList.contains('yr')) { if (!nxt.hidden) any = true; nxt = nxt.nextElementSibling; } y.hidden = !any; });
      var c = document.getElementById('pubCount'); if (c) c.textContent = n;
    }); });
  }

  /* Star-trail cursor: sparkles follow the mouse. Not on touch screens, not in calm mode, not with reduced motion. */
  if (window.matchMedia('(pointer:fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var trailColors = ['#FFF23B', '#FFFFFF', '#BFD3FF', '#FF3BE4', '#7CFF9B', '#FFB13B'], lastTrail = 0;
    document.addEventListener('mousemove', function (e) {
      if (site.classList.contains('calm')) return;
      var now = performance.now(); if (now - lastTrail < 14) return; lastTrail = now;
      for (var k = 0; k < 3; k++) {
        var s = document.createElement('span'); s.className = 'trail'; s.textContent = k === 1 ? '\u2727' : '\u2726';
        s.style.left = (e.clientX + (Math.random() * 28 - 14)) + 'px'; s.style.top = (e.clientY + (Math.random() * 28 - 14)) + 'px';
        s.style.color = trailColors[Math.floor(Math.random() * trailColors.length)];
        s.style.fontSize = (7 + Math.random() * 13) + 'px';
        s.style.setProperty('--dx', (Math.random() * 50 - 25) + 'px');
        s.style.animationDuration = (0.8 + Math.random() * 0.7) + 's';
        document.body.appendChild(s); (function (el) { setTimeout(function () { el.remove(); }, 1600); })(s);
      }
    });
  }


  /* Soundtrack: an ORIGINAL loop in the style of 1994 shareware FM soundtracks (driving bass, square arps,
     detuned saw lead, synth drums). Composed here, not sampled or transcribed from any game. Click to play. */
  var npBtn = document.getElementById('soundBtn');
  if (npBtn && (window.AudioContext || window.webkitAudioContext)) {
    var AC = window.AudioContext || window.webkitAudioContext, ctx = null, master = null, timer = null;
    var BPM = 150, STEP = 60 / BPM / 4, BAR = 16, BARS = 8;
    // E minor: i VI VII i | i VI iv V
    var roots = [40, 36, 38, 40, 40, 36, 45, 47];
    var chords = [[64,67,71],[60,64,67],[62,66,69],[64,67,71],[64,67,71],[60,64,67],[57,60,64],[59,63,66]];
    // lead melody: [step, midi, lengthInSteps]
    var lead = [
      [0,76,3],[4,79,2],[6,78,2],[8,76,4],[12,71,4],
      [16,72,3],[20,76,2],[22,74,2],[24,72,4],[28,67,4],
      [32,74,3],[36,78,2],[38,76,2],[40,74,2],[42,69,2],[44,74,4],
      [48,76,6],[54,71,2],[56,67,2],[58,69,2],[60,71,4],
      [64,76,2],[66,76,2],[68,79,4],[72,81,2],[74,79,2],[76,78,4],
      [80,79,3],[84,76,1],[86,72,2],[88,76,4],[92,79,4],
      [96,81,3],[100,84,2],[102,83,2],[104,81,4],[108,76,4],
      [112,75,4],[116,78,2],[118,71,2],[120,75,4],[124,71,4]
    ];
    var leadAt = {}; lead.forEach(function (n) { leadAt[n[0]] = n; });
    var arpPat = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 3, 2, 1, 0, 1];
    var noiseBuf = null, step = 0, nextTime = 0;
    function hz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
    function noise() {
      if (noiseBuf) return noiseBuf;
      noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
      var d = noiseBuf.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      return noiseBuf;
    }
    function env(g, t, peak, a, d, sus, len, r) {
      g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(peak, t + a);
      g.gain.exponentialRampToValueAtTime(Math.max(peak * sus, 0.0001), t + a + d);
      g.gain.setValueAtTime(Math.max(peak * sus, 0.0001), t + len); g.gain.exponentialRampToValueAtTime(0.0001, t + len + r);
    }
    function voice(type, midi, t, len, vol, cutoff, detune) {
      var g = ctx.createGain(), f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.Q.value = 4;
      f.frequency.setValueAtTime(cutoff, t); f.frequency.exponentialRampToValueAtTime(Math.max(cutoff * 0.3, 200), t + len);
      env(g, t, vol, 0.008, 0.08, 0.6, len, 0.06);
      [-(detune || 0), (detune || 0)].forEach(function (c) {
        var o = ctx.createOscillator(); o.type = type; o.frequency.value = hz(midi); o.detune.value = c;
        o.connect(f); o.start(t); o.stop(t + len + 0.1);
      });
      f.connect(g); g.connect(master);
    }
    function kick(t) {
      var o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine';
      o.frequency.setValueAtTime(160, t); o.frequency.exponentialRampToValueAtTime(42, t + 0.12);
      g.gain.setValueAtTime(0.9, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
      o.connect(g); g.connect(master); o.start(t); o.stop(t + 0.25);
    }
    function snare(t) {
      var n = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
      n.buffer = noise(); f.type = 'bandpass'; f.frequency.value = 1900; f.Q.value = 0.8;
      g.gain.setValueAtTime(0.5, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.16);
      n.connect(f); f.connect(g); g.connect(master); n.start(t); n.stop(t + 0.2);
      var o = ctx.createOscillator(), g2 = ctx.createGain(); o.type = 'triangle'; o.frequency.value = 190;
      g2.gain.setValueAtTime(0.35, t); g2.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
      o.connect(g2); g2.connect(master); o.start(t); o.stop(t + 0.1);
    }
    function hat(t, open) {
      var n = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
      n.buffer = noise(); f.type = 'highpass'; f.frequency.value = 7500;
      g.gain.setValueAtTime(open ? 0.22 : 0.14, t); g.gain.exponentialRampToValueAtTime(0.001, t + (open ? 0.14 : 0.035));
      n.connect(f); f.connect(g); g.connect(master); n.start(t); n.stop(t + 0.2);
    }
    function playStep(i, t) {
      var bar = Math.floor(i / BAR) % BARS, s = i % BAR, root = roots[bar], ch = chords[bar];
      // bass: driving eighths, octave pops on 6 and 14, leading note into the next bar
      if (s % 2 === 0) voice('sawtooth', root + ((s === 6 || s === 14) ? 12 : 0), t, STEP * 0.9, 0.22, 420, 0);
      if (s === 15) voice('sawtooth', roots[(bar + 1) % BARS] - 1, t, STEP * 0.8, 0.16, 420, 0);
      // arpeggio: square 16ths over the chord
      var ai = arpPat[s], an = ai === 3 ? ch[0] + 12 : ch[ai];
      voice('square', an + 12, t, STEP * 0.5, 0.045, 2600, 0);
      // lead: detuned saws
      var L = leadAt[i % (BAR * BARS)];
      if (L) voice('sawtooth', L[1], t, STEP * L[2] * 0.92, 0.11, 3200, 9);
      // pad: soft chord on the downbeat
      if (s === 0) ch.forEach(function (m) { voice('triangle', m - 12, t, STEP * BAR * 0.95, 0.035, 900, 5); });
      // drums
      if (s === 0 || s === 4 || s === 8 || s === 12 || (bar % 2 === 1 && s === 14)) kick(t);
      if (s === 4 || s === 12 || (bar === 7 && s >= 13)) snare(t);
      if (s % 2 === 0) hat(t, s === 2 || s === 10);
    }
    function tick() {
      while (nextTime < ctx.currentTime + 0.12) { playStep(step, nextTime); step++; nextTime += STEP; }
    }
    function start() {
      if (!ctx) {
        ctx = new AC(); master = ctx.createGain(); master.gain.value = 0.5;
        var comp = ctx.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 4;
        master.connect(comp); comp.connect(ctx.destination);
      }
      ctx.resume(); step = 0; nextTime = ctx.currentTime + 0.05; timer = setInterval(tick, 25);
      site.classList.add('sound-on'); npBtn.setAttribute('aria-pressed', 'true'); npBtn.innerHTML = '&#9835; SOUND ON'; playing = true;
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; } if (ctx) ctx.suspend();
      site.classList.remove('sound-on'); npBtn.setAttribute('aria-pressed', 'false'); npBtn.innerHTML = '&#9835; SOUND OFF';
    }
    /* Preferred: the real thing, Jan125's FM space-shooter tracks (OGA-BY 3.0, see audio/CREDITS.txt).
       Falls back to the robot-composed loop above if the files can't be loaded (e.g. the one-file preview). */
    var tracks = ['level1', 'level2', 'level3', 'level4', 'level5'], ti = 0, audio = null, useSynth = false, playing = false;
    var npLabel = document.getElementById('npLabel');
    function setLabel(t) { if (npLabel) npLabel.textContent = t; }
    function playTrack() {
      if (!audio) {
        audio = new Audio(); audio.volume = 0.6; audio.preload = 'auto';
        audio.addEventListener('ended', function () { ti = (ti + 1) % tracks.length; playTrack(); });
        audio.addEventListener('error', function () { if (!useSynth) { useSynth = true; audio = null; start(); setLabel('NOW PLAYING: shadow_run.fm (robot-composed fallback)'); } });
      }
      audio.src = 'audio/' + tracks[ti] + '.ogg';
      var p = audio.play(); if (p && p.catch) p.catch(function () {});
      setLabel('NOW PLAYING: ' + tracks[ti] + '.ogg by Jan125 (OGA-BY 3.0)');
    }
    function soundOn() {
      playing = true; site.classList.add('sound-on'); npBtn.setAttribute('aria-pressed', 'true'); npBtn.innerHTML = '&#9835; SOUND ON';
      if (useSynth) start(); else playTrack();
    }
    function soundOff() {
      playing = false; if (audio) { audio.pause(); } stop();
      setLabel('SOUNDTRACK: Jan125, "Stereotypical 90\'s space shooter music" (toggle up top)');
    }
    npBtn.addEventListener('click', function () { playing ? soundOff() : soundOn(); });
    /* |<< and >>| : skip within Jan125's tracks (starts playback if it was off) */
    function skip(d) {
      if (useSynth) { soundOn(); return; }
      ti = (ti + d + tracks.length) % tracks.length;
      if (playing) playTrack(); else soundOn();
    }
    var prevB = document.getElementById('prevTrack'), nextB = document.getElementById('nextTrack');
    if (prevB) prevB.addEventListener('click', function () { skip(-1); });
    if (nextB) nextB.addEventListener('click', function () { skip(1); });
  }

  /* Web ring: RANDOM really is random. */
  var rnd = document.getElementById('ringRandom');
  if (rnd) {
    var ringEl = document.getElementById('webring'), ring = [];
    try { ring = JSON.parse(ringEl.getAttribute('data-ring')) || []; } catch (e) { ring = []; }
    if (!ring.length) ring = ['https://exoplanetarchive.ipac.caltech.edu/'];
    rnd.addEventListener('click', function (ev) { ev.preventDefault(); window.open(ring[Math.floor(Math.random() * ring.length)], '_blank', 'noopener'); });
  }
})();
