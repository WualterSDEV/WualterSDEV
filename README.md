<div align="center">
  <img width="100%" src="img/banner.gif" alt="WualterS · Desarrollador Python · Cusco, Perú"/>
</div>

<p align="center">
  Construyo productos completos: del modelo estadístico al servidor, la interfaz, las pruebas y el cobro.
</p>

<p align="center">
  <a href="#-proyectos"><img src="https://img.shields.io/badge/Proyectos-FF5A1F?style=for-the-badge&labelColor=0F1420" alt="Proyectos"/></a>
  <a href="#-stack"><img src="https://img.shields.io/badge/Stack-8593AD?style=for-the-badge&labelColor=0F1420" alt="Stack"/></a>
  <a href="#-english"><img src="https://img.shields.io/badge/🇺🇸_English-4CAF50?style=for-the-badge&labelColor=0F1420" alt="English"/></a>
</p>

---

## 👋 Sobre mí

- ⚽ Hoy trabajo en **Instrumento**, una app web que calcula cientos de mercados por partido de fútbol con modelos estadísticos reales y mide si aciertan.
- 📐 Me interesa el **modelado estadístico aplicado**: Dixon-Coles, Binomial Negativa, cópulas, calibración y backtesting.
- 🚀 Me gusta llevar las cosas **a producción**: despliegue en Render, base en Postgres, CI con GitHub Actions y pruebas de interfaz con Playwright.
- 🤖 Empecé automatizando tareas repetitivas con **visión por computadora y OCR** (ver Umapyoi AutoReroll).
- 🔭 Ahora mismo: midiendo con datos reales si el xG, el CLV y las bajas de titulares mejoran los pronósticos.
- 🎮 Fuera del código: videojuegos y mucha música.

<img src="img/codigo.png" alt="class WualterS(Desarrollador)" width="100%"/>

---

## 🧭 Proyectos

### ⚽ Instrumento — análisis y predicción de fútbol

> *Calcula cientos de mercados por partido, los compara contra la cuota de la casa y registra si acertaste.*

<a href="https://instrumentoapp.com"><img src="img/hero.png" alt="Instrumento: pronósticos de fútbol con un modelo real" width="100%"/></a>

<p>
  <a href="https://instrumentoapp.com"><img src="https://img.shields.io/badge/▶_Probar_la_app-FF5A1F?style=for-the-badge&labelColor=0F1420" alt="Probar la app"/></a>
  <a href="https://instrumentoapp.com/aciertos"><img src="https://img.shields.io/badge/✅_Aciertos_públicos-C6F432?style=for-the-badge&labelColor=0F1420" alt="Aciertos públicos"/></a>
</p>

<a href="https://instrumentoapp.com/aciertos"><img src="https://raw.githubusercontent.com/WualterSDEV/WualterSDEV/datos/aciertos.svg" alt="Aciertos de Instrumento en vivo" width="100%"/></a>

<sub>☝️ Datos reales de la app, se actualizan solos cada 6 horas. Cada pick se guarda antes del partido y cuentan también los que fallaron.</sub>

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
| 🧠 **Contra el mercado** | Aprende del xG (goles esperados), mide el CLV de cada pick contra la cuota de cierre y si las bajas de titulares pesan más de lo que el modelo ya espera |
| 📱 **Producto** | PWA instalable, picks del día, en vivo con gráfico de presión, combinadas, «¿Cuánto meter?» con el bank del usuario (Kelly fraccionado), registro con yield y calibración, notificaciones push propias (Web Push + VAPID) y referidos |
| 💳 **Negocio** | Plan gratis / Pro controlado en el servidor, cobro por Yape o Plin y Libro de Reclamaciones virtual |
| 🛡️ **Calidad** | ~600 pruebas (pytest + Playwright con pantallas reales) en cada PR, ruff, arquitectura por capas vigilada por una prueba, hilos de fondo con semáforo de salud y avisos por Telegram |

<img src="img/pantallas.png" alt="Pantallas: Hoy, Partidos, Análisis, En vivo, Combinar y Registro" width="100%"/>

<table>
  <tr>
    <td align="center" width="25%"><h3>~600</h3><sub>pruebas automáticas en cada cambio</sub></td>
    <td align="center" width="25%"><h3>16 + copas</h3><sub>ligas con datos propios</sub></td>
    <td align="center" width="25%"><h3>28</h3><sub>estadísticas por partido modeladas</sub></td>
    <td align="center" width="25%"><h3>100%</h3><sub>de los picks guardados antes del partido</sub></td>
  </tr>
</table>

<details>
<summary><b>🧠 Cómo funciona por dentro</b></summary>

<br>

```mermaid
flowchart LR
    A[(API-Football)] --> B[Base de partidos]
    B --> C[Dixon-Coles<br>goles + xG]
    B --> D[Binomial Negativa<br>28 estadísticas]
    C --> E[Matriz de marcadores]
    E --> F[Mercados coherentes]
    D --> F
    F --> G[Backtest y<br>calibración]
    G --> H[Pick guardado<br>ANTES del partido]
    H --> I["/aciertos y CLV<br>contra el cierre"]
```

- Todo sale de una sola matriz de marcadores: quién gana, goles y ambos marcan nunca se contradicen.
- Walk-forward: entrena con el pasado, predice lo siguiente y avanza; un mercado que no supera el control de falsos descubrimientos se marca como *ruido*.
- El historial público no se recalcula: lo que se ve es lo que el modelo dijo antes de cada partido.

</details>

<sub>~26 000 líneas de Python · ~9 000 de JavaScript sin frameworks · código privado · 🔗 <a href="https://instrumentoapp.com">instrumentoapp.com</a></sub>

<br>

### 🏇 Umapyoi AutoReroll — automatización para Umamusume Global

<img src="img/umapyoi.png" alt="Umapyoi AutoReroll" width="100%"/>

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

**Lenguajes**<br>
<img src="https://skillicons.dev/icons?i=python,js,html,css,sql&theme=dark"/>

**Backend y datos**<br>
<img src="https://skillicons.dev/icons?i=flask,postgres,sqlite&theme=dark"/><br>
<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white"/>

**Automatización**<br>
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
<img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white"/>

**Deploy y calidad**<br>
<img src="https://skillicons.dev/icons?i=git,github,githubactions,vscode&theme=dark"/><br>
<img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black"/>
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white"/>
<img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white"/>

---

## 🐍 Actividad

<div align="center">
  <img src="https://raw.githubusercontent.com/WualterSDEV/WualterSDEV/output/snake.svg" alt="La serpiente se come mis contribuciones" width="100%"/>
  <br>
  <sub>La serpiente se come mis contribuciones del año (se actualiza sola cada día).</sub>
</div>

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

**⚽ Instrumento** — a football analytics web app that prices hundreds of markets per match with real statistical models (Dixon-Coles for goals, Negative Binomial for 28 match stats, a Gaussian copula for accumulators), backtests them against bookmaker odds, measures closing-line value, and tracks calibration and yield for every saved pick — with a public, verifiable track record. Built with Flask, pandas and SciPy, persisted in PostgreSQL (Neon), deployed on Render as an installable PWA, with a Free/Pro plan and CI running pytest + Playwright on every PR. **[Try it live →](https://instrumentoapp.com)**

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
