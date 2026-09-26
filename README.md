<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=WualterS&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32"/>
</div>

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&weight=800&size=28&duration=3000&pause=1000&color=FF5A1F&center=true&vCenter=true&width=900&lines=⚽+Modelos+estadísticos+de+fútbol;🐍+Python+%2B+Flask+en+producción;📊+Datos+que+se+validan+contra+el+mercado;🤖+Automatización+y+bots" alt="Typing SVG" />
</div>

<p align="center">
  <b>Desarrollador Python · Cusco, Perú 🇵🇪</b><br>
  Construyo productos completos: del modelo estadístico al servidor, la interfaz, las pruebas y el cobro.
</p>

<p align="center">
  <a href="#-proyectos"><img src="https://img.shields.io/badge/Proyectos-FF5A1F?style=for-the-badge&labelColor=0F1420" alt="Proyectos"/></a>
  <a href="#-stack"><img src="https://img.shields.io/badge/Stack-8593AD?style=for-the-badge&labelColor=0F1420" alt="Stack"/></a>
  <a href="#-english"><img src="https://img.shields.io/badge/🇺🇸_English-4CAF50?style=for-the-badge&labelColor=0F1420" alt="English"/></a>
</p>

---

## 👋 Sobre mí

<table>
  <tr>
    <td width="60%" valign="top">

- ⚽ Hoy trabajo en **Instrumento**, una app web que calcula cientos de mercados por partido de fútbol con modelos estadísticos reales y mide si aciertan.
- 📐 Me interesa el **modelado estadístico aplicado**: Dixon-Coles, Binomial Negativa, cópulas, calibración y backtesting.
- 🚀 Me gusta llevar las cosas **a producción**: despliegue en Render, base en Postgres, CI con GitHub Actions y pruebas de interfaz con Playwright.
- 🤖 Empecé automatizando tareas repetitivas con **visión por computadora y OCR** (ver Umapyoi AutoReroll).
- 🎮 Fuera del código: videojuegos y mucha música.

  </td>
    <td width="40%" align="center" valign="top">
      <img src="https://spotify-github-profile.kittinanx.com/api/view.svg?uid=315y23hfxynyj3jvzsaimfrw5poy&cover_image=true&theme=default&show_offline=true&background_color=121212&interchange=false&bar_color=53b14f&bar_color_cover=true" width="320"/>
    </td>
  </tr>
</table>

---

## 🧭 Proyectos

### ⚽ Instrumento — análisis y predicción de fútbol

> *Calcula cientos de mercados por partido, los compara contra la cuota de la casa y registra si acertaste.*

<p>
  <a href="https://app-z8g3.onrender.com/"><img src="https://img.shields.io/badge/▶_Probar_la_app-FF5A1F?style=for-the-badge&labelColor=0F1420" alt="Probar la app"/></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL_(Neon)-4169E1?style=flat-square&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black"/>
  <img src="https://img.shields.io/badge/PWA-5A0FC8?style=flat-square&logo=pwa&logoColor=white"/>
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white"/>
</p>

| | |
|---|---|
| 📈 **Modelos** | Dixon-Coles para goles (con altitud, lesiones y descanso) · Binomial Negativa para 28 estadísticas (córners, tarjetas, tiros…) · cópula gaussiana para combinadas |
| ✅ **Validación** | Backtest contra el mercado, calibración y control de falsos descubrimientos (FDR): cada mercado lleva su sello — *ok*, *ajustado* o *ruido* |
| 🗂️ **Datos** | Ingesta automática de 16 ligas + copas, planteles y mercados de jugador con incertidumbre de minutos |
| 📱 **Producto** | PWA instalable, modo oscuro/claro, en vivo, registro de picks con yield y gráfico de calibración, accesibilidad (contraste AA, objetivos táctiles ≥ 44 px) |
| 💳 **Negocio** | Plan gratis / Pro controlado en el servidor, cobro por Yape o Plin y Libro de Reclamaciones virtual |
| 🛡️ **Calidad** | CI con pytest + Playwright en cada PR, persistencia en Postgres para sobrevivir reinicios, health check y arranque en segundo plano |

<sub>~18 000 líneas de Python · ~4 500 de JavaScript sin frameworks · código privado · 🔗 <a href="https://app-z8g3.onrender.com/">app-z8g3.onrender.com</a></sub>

<br>

### 🏇 Umapyoi AutoReroll — automatización para Umamusume Global

Bot de escritorio que automatiza el reroll del juego: acepta términos, crea el perfil, reclama recompensas, tira el gacha y **detecta las cartas SSR objetivo** con OpenCV + Tesseract OCR. Avisa por webhook de Discord e incluye interfaz en español e inglés.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tesseract_OCR-3C3C3C?style=flat-square"/>
  <img src="https://img.shields.io/badge/Tkinter-FFD43B?style=flat-square&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/Discord_Webhooks-5865F2?style=flat-square&logo=discord&logoColor=white"/>
</p>

---

## 🛠️ Stack

<table>
  <tr>
    <td align="center"><b>Lenguajes</b></td>
    <td><img src="https://skillicons.dev/icons?i=python,js,html,css,sql&theme=dark"/></td>
  </tr>
  <tr>
    <td align="center"><b>Backend y datos</b></td>
    <td><img src="https://skillicons.dev/icons?i=flask,postgres,sqlite&theme=dark"/>&nbsp;
      <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" height="40"/>
      <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" height="40"/>
      <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" height="40"/>
    </td>
  </tr>
  <tr>
    <td align="center"><b>Automatización</b></td>
    <td>
      <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" height="40"/>
      <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" height="40"/>
      <img src="https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white" height="40"/>
    </td>
  </tr>
  <tr>
    <td align="center"><b>Deploy y calidad</b></td>
    <td><img src="https://skillicons.dev/icons?i=git,github,githubactions,vscode&theme=dark"/>&nbsp;
      <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black" height="40"/>
      <img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" height="40"/>
      <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" height="40"/>
    </td>
  </tr>
</table>

---

## 💡 Cómo trabajo

- **Medir antes de creer.** Un modelo sin validación es una opinión: por eso cada mercado de Instrumento pasa por backtest y calibración antes de mostrarse como confiable.
- **Honestidad con el usuario.** La app dice lo que *no* puede hacer y por qué (por ejemplo, no scrapea cuotas para no arriesgar la cuenta del usuario).
- **Cambios pequeños y verificables.** PRs chicos, pruebas automáticas y documentación de cada decisión.

---

<a name="-english"></a>
<details>
<summary><b>🇺🇸 English</b></summary>

<br>

**Python developer from Cusco, Peru.** I build complete products: from the statistical model to the server, the UI, the tests and the billing.

**⚽ Instrumento** — a football analytics web app that prices hundreds of markets per match with real statistical models (Dixon-Coles for goals, Negative Binomial for 28 match stats, a Gaussian copula for accumulators), backtests them against bookmaker odds, and tracks calibration and yield for every saved pick. Built with Flask, pandas and SciPy, persisted in PostgreSQL (Neon), deployed on Render as an installable PWA, with a Free/Pro plan and CI running pytest + Playwright on every PR. **[Try it live →](https://app-z8g3.onrender.com/)**

**🏇 Umapyoi AutoReroll** — a desktop bot that automates rerolling in Umamusume Global using OpenCV and Tesseract OCR to detect target SSR cards, with Discord webhook notifications and an English/Spanish UI.

</details>

---

<div align="center">
  <a href="https://github.com/WualterSDEV">
    <img src="https://img.shields.io/badge/GitHub-WualterSDEV-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
  <br><br>
  <img src="https://komarev.com/ghpvc/?username=WualterSDEV&style=for-the-badge&color=FF5A1F" alt="Visitas al perfil"/>
</div>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer"/>
</div>
