# Proyecto NC Contabilidades — contexto

Sitio informativo + generador de carruseles diarios para NC Contabilidades, la marca de servicios contables de Nicole (contadora). Nace el 20 de agosto de 2026, a partir de una conversación de WhatsApp donde Nicole pidió contenido sobre "noticias actuales, leyes, exigencias, beneficios" del rubro contable en Chile.

**Repositorio:** [github.com/agenciaaimpacto-cyber/nc-contabilidades](https://github.com/agenciaaimpacto-cyber/nc-contabilidades) (público).
**Sitio en vivo:** [nc-contabilidad.netlify.app](https://nc-contabilidad.netlify.app) (Netlify, deploy automático desde `main`).

**Nota de cuenta Netlify:** a diferencia de Radar Comercial y Danny Mera Seguros (que están bajo la cuenta `agenciaaimpacto`), este sitio está en una **cuenta de Netlify distinta**, creada por Danny específicamente para este proyecto (equipo `nelsonmerac1989`), para no compartir créditos/plan con los otros sitios. El repo de GitHub sí sigue bajo `agenciaaimpacto-cyber`, igual que los otros dos — solo Netlify cambia de cuenta.

## Ruta local
`/Users/danny/Contabilidad NC` (fuera de `~/Documents`, mismo criterio que los otros proyectos, por si en algún momento necesita una automatización local con `launchd`).

## Marca y contacto
- **Nombre:** NC Contabilidades.
- **Colores:** navy oscuro `#0B2440` (fondo, header, footer) y naranjo `#F5821F` (acento), sobre fondo papel `#FAFAF8`. Tomados de una pieza gráfica que Nicole ya usa en redes.
- **WhatsApp:** +56 9 3429 1937 (`wa.me/56934291937`).
- **Email:** nicole.edith87@gmail.com.
- Sin cuenta de Instagram propia confirmada todavía — no se inventó ni se puso ninguna en el footer.

## Estructura del sitio
1. `index.html` — Inicio: hook, los 5 servicios, 3 valores de marca, preview de noticias.
2. `servicios.html` — detalle de los 5 servicios: Contabilidad Mensual, Declaraciones IVA y Renta, Formalización de Empresas, Declaraciones Juradas, Término de Giro.
3. `noticias.html` — despachos diarios (normativa, plazos SII, beneficios, cifras), fuentes chilenas verificables.
4. `carruseles.html` — página de descarga, **no listada** (`noindex`, sin link en el menú), mismo patrón que los otros dos proyectos. Se actualiza sola cada día agregando un bloque arriba, sin borrar los días anteriores.

## Carruseles diarios (requisito confirmado el 20 de agosto de 2026)
- **3 carruseles por día**, generados a partir de la investigación de ese día.
- **Carrusel 1 y 2:** sobre el despacho investigado ese día (normativa, exigencias SII, beneficios o cifras — rotando entre los 4 pilares).
- **Carrusel 3 — siempre fijo en este mensaje** (varía el copy/ángulo día a día, no el tema): llamado a la acción sobre que **la contabilidad es tan importante para un negocio como cualquier otra área** (marketing, ventas, operaciones) — evaluar la situación contable o contratar el servicio no es un gasto, es una decisión de negocio. Cierra siempre con CTA a WhatsApp.
- Motor técnico: `carrusel-tools/generate_carousel.py` (Python + Pillow, imágenes 1080x1350, fuentes Archivo Black / Archivo Variable embebidas en `carrusel-tools/fonts/`, copiadas del mismo motor de Radar Comercial / Danny Mera Seguros). Colores de marca: navy `#0B2440` y naranjo `#F5821F`.
- Primer lote (3 carruseles) generado manualmente el 20 de agosto de 2026 para aprobar el estilo: reforma tributaria en tramitación, plazo del F29 de agosto, beneficios de estar al día con el SII — con fuentes reales (France 24, Kame, NSS Legal & Tax, SII, Emol).
- **Estado: montada y corriendo.** Rutina en la nube "NC Contabilidades — despacho + carruseles diarios" (trigger_id `trig_01W953TGSv6jnUq8WNbirWua`, ver en [claude.ai/code/routines/trig_01W953TGSv6jnUq8WNbirWua](https://claude.ai/code/routines/trig_01W953TGSv6jnUq8WNbirWua)), cron `0 12 * * *` (8:00 AM Chile, sin horario de verano — revisar cuando entre el horario de verano en septiembre, puede correrse una hora).
- Nota técnica: la primera corrida de prueba (misma fecha del lote manual, 20 de agosto) se salta sola por la regla de no-duplicar del prompt de la rutina — comportamiento esperado, igual que pasó en Danny Mera Seguros el 12 de agosto. El contenido automático nuevo debería aparecer a partir del 21 de agosto en adelante.

## Reglas de contenido importantes
- **Nunca presentar un proyecto de ley como norma vigente** — si está en tramitación en el Congreso, decirlo explícitamente (aplica directo al despacho de la reforma tributaria de Kast, publicado el 20 de agosto).
- Nunca prometer plazos como compromiso propio del servicio — los plazos legales (SII, etc.) siempre atribuidos a la fuente.
- Español neutro/chileno estándar, sin acentos argentinos (nada de "vos", "tenés").
- Solo fuentes chilenas verificables: SII, Biblioteca del Congreso Nacional, Diario Oficial, Colegio de Contadores de Chile, o medios serios (Emol, La Tercera, BioBioChile, CNN Chile, Diario Financiero).

## Cómo seguir
Al abrir una sesión de Claude Code en esta carpeta, este archivo da el contexto — se puede pedir directamente "seguimos con el sitio de NC Contabilidades" y continuar desde acá.
