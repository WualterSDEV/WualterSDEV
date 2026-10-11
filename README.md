<img src="img/banner.png" alt="WualterS · Desarrollador Python · Modelos estadísticos llevados a producción · Cusco, Perú" width="100%"/>

Desarrollo productos de datos de punta a punta: el modelo estadístico, el servidor, la interfaz, las pruebas y el despliegue. Hoy construyo **Instrumento**, una app web de pronósticos de fútbol que publica cuánto acierta.

<p>
  <a href="https://instrumentoapp.com"><img src="img/btn-app.png" height="44" alt="Abrir Instrumento"/></a>
  <a href="mailto:wualters.dev@gmail.com"><img src="img/btn-correo.png" height="44" alt="Escribir a wualters.dev@gmail.com"/></a>
</p>

---

## Proyecto destacado

### Instrumento · pronósticos de fútbol con un modelo real

**El problema:** casi todos los pronósticos de fútbol que circulan son opiniones, y nadie lleva la cuenta de cuántos aciertan.

**Qué hace:** calcula la probabilidad de cientos de resultados por partido con modelos estadísticos, la compara con la cuota de la casa, guarda cada pick antes de que empiece el partido y publica sus aciertos, incluidos los que fallaron. Es gratis y funciona en PC y en el celular.

<a href="https://instrumentoapp.com"><img src="img/hero.jpg" alt="Instrumento en PC y en el celular" width="100%"/></a>

<p>
  <a href="https://instrumentoapp.com"><img src="img/btn-app.png" height="40" alt="Abrir la app"/></a>
  <a href="https://instrumentoapp.com/aciertos"><img src="img/btn-aciertos.png" height="40" alt="Aciertos públicos"/></a>
  <a href="https://instrumentoapp.com/como-funciona"><img src="img/btn-como.png" height="40" alt="Cómo funciona"/></a>
</p>

**Funciones principales**

- **Hoy:** los picks más seguros del día, cada uno con su probabilidad y el nivel de datos que lo respalda.
- **Análisis por partido:** quién gana, goles, córners, tarjetas y tiros, con una combinada sugerida y el contexto (árbitro, descanso, historial).
- **En vivo:** gráfico de presión que se actualiza durante el partido y avisos push con goles y picks.
- **Combinar:** junta líneas de varios partidos y calcula la probabilidad de que salgan todas, sin multiplicar a ciegas las del mismo partido.
- **Registro:** tus picks con acierto, ganancia en unidades y «¿Cuánto meter?» según tu bank (Kelly fraccionado).
- **Se mejora solo:** reentrena cada día y cada semana prueba ajustes contra partidos ya jugados; aplica solo los que ganan.

**Tecnología:** Python 3.11 · Flask · pandas · SciPy · PostgreSQL (Neon) · JavaScript sin frameworks (PWA) · pytest · Playwright · GitHub Actions · Render

**Estado:** en producción en [instrumentoapp.com](https://instrumentoapp.com) · ~770 pruebas automáticas en cada cambio · 28 competiciones · código privado.

#### Aciertos en vivo

<a href="https://instrumentoapp.com/aciertos"><img src="https://raw.githubusercontent.com/WualterSDEV/WualterSDEV/datos/aciertos.svg" alt="Porcentaje de acierto de los picks de Instrumento, actualizado cada 6 horas" width="100%"/></a>

<sub>Datos reales de la app, actualizados solos cada 6 horas. El % aparece recién con 20 picks medidos.</sub>

#### Pantallas

<img src="img/pantallas.jpg" alt="Pantallas de Instrumento: Hoy, Partidos, Análisis, En vivo, Combinar y Registro" width="100%"/>

<sub>Interfaz real de la app, mostrada con datos de ejemplo.</sub>

<details>
<summary><b>Cómo funciona por dentro</b></summary>

<br>

1. **Datos:** ingesta automática de API-Football: partidos, estadísticas, planteles y alineaciones de 28 competiciones.
2. **Goles:** modelo Dixon-Coles (con xG, altitud, lesiones y descanso). De una sola matriz de marcadores salen quién gana, goles y ambos marcan, así nunca se contradicen.
3. **Estadísticas:** Binomial Negativa para córners, tarjetas, tiros y faltas; cópula gaussiana para las combinadas.
4. **Validación:** backtest walk-forward, calibración y control de falsos descubrimientos. Un mercado que no lo supera se marca como *ruido*.
5. **Medición:** cada pick se guarda antes del partido y se cierra con el resultado. También se mide el CLV contra la cuota de cierre.
6. **Mejora:** cada semana compara 7 ajustes del modelo con partidos que no vio y aplica solo los que ganan claro.

</details>

<details>
<summary><b>Lo que la app hace sola cada día</b> (hora de Lima)</summary>

<br>

- **1:00, cada 7 días:** auto-mejora del modelo.
- **4:00:** respaldo de cuentas, picks e historial.
- **5:00:** reentreno con los resultados nuevos.
- **Mañana:** combinadas del día y picks en el canal de Telegram.
- **Durante cada partido:** seguimiento en vivo y avisos push.
- **Al terminar cada partido:** cierre de los picks con el marcador y las estadísticas finales.
- **Lunes 10:00:** resumen «Tu semana» para cada usuario.

Cada tarea de fondo reporta su estado; si una se cae, llega un aviso por Telegram.

</details>

---

## Otros proyectos

### Umapyoi AutoReroll · automatización para Umamusume Global

Bot de escritorio que hace solo el reroll del juego: acepta términos, crea el perfil, reclama recompensas, tira el gacha y detecta las cartas SSR objetivo con visión por computadora. Avisa por Discord y tiene interfaz en español e inglés.

**Tecnología:** Python · OpenCV · Tesseract OCR · Tkinter · webhooks de Discord

**Estado:** repositorio privado.

---

## Tecnologías

- **Lenguajes:** Python · JavaScript · HTML y CSS · SQL
- **Backend y datos:** Flask · PostgreSQL · SQLite · pandas · NumPy · SciPy
- **Modelado:** Dixon-Coles · Binomial Negativa · cópulas · calibración · backtesting · criterio de Kelly
- **Automatización:** OpenCV · Tesseract OCR · Selenium · Discord
- **Calidad y despliegue:** pytest · Playwright · ruff · GitHub Actions · Render · PWA

---

## Cómo trabajo

- **Medir antes de creer.** Un modelo sin validación es una opinión: cada mercado pasa por backtest y calibración antes de mostrarse.
- **Honestidad con el usuario.** La app dice lo que no puede hacer y por qué, y no oculta los picks que fallan.
- **Cambios pequeños y verificables.** Pull requests chicos, pruebas automáticas en cada uno y cada decisión documentada.

---

## Contacto

¿Un proyecto con datos, un modelo que hay que llevar a producción o una automatización? Escríbeme.

<p>
  <a href="mailto:wualters.dev@gmail.com"><img src="img/btn-correo.png" height="44" alt="wualters.dev@gmail.com"/></a>
  <a href="https://instrumentoapp.com"><img src="img/btn-web.png" height="44" alt="instrumentoapp.com"/></a>
</p>

<details>
<summary><b>English</b></summary>

<br>

**Python developer from Cusco, Peru.** I build data products end to end: the statistical model, the server, the UI, the tests and the deployment. Contact: [wualters.dev@gmail.com](mailto:wualters.dev@gmail.com).

**Instrumento** ([instrumentoapp.com](https://instrumentoapp.com)) is a free football analytics web app. It prices hundreds of markets per match with statistical models (Dixon-Coles for goals, Negative Binomial for match stats, a Gaussian copula for accumulators), compares them with bookmaker odds, saves every pick before kick-off and publishes its track record, misses included. It retrains daily and runs a weekly self-improvement loop that only ships changes that beat the current model on unseen matches. Built with Flask, pandas, SciPy and PostgreSQL, deployed on Render as an installable PWA, with ~770 automated tests (pytest + Playwright) on every change. Source code is private.

**Umapyoi AutoReroll** is a desktop bot that automates rerolling in Umamusume Global, using OpenCV and Tesseract OCR to detect target SSR cards, with Discord notifications and an English/Spanish UI. Private repository.

</details>
