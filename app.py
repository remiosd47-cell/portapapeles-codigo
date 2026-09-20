import json
import os
import streamlit as st

# Nombre del archivo donde se guardarán tus códigos de forma persistente
DB_FILE = "snippets.json"


def cargar_datos():
  """Carga los códigos guardados desde el archivo JSON."""
  if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}


def guardar_datos(datos):
  """Guarda los cambios en el archivo JSON."""
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)


# Configuración inicial de la página web
st.set_page_config(
    page_title="Mi Portapapeles de Código", page_icon="💻", layout="centered"
)
st.title("📂 Mi Librería de Código Personal")

# Cargamos los datos actuales
snippets = cargar_datos()

# Creamos dos pestañas: una optimizada para copiar rápido (PC) y otra para gestionar (Celular)
tab_pc, tab_movil = st.tabs(
    ["📋 Copiar Rápido (PC)", "✏️ Crear / Editar Entradas (Celular)"]
)

# --- VISTA DE LA PC ---
with tab_pc:
  st.subheader("Tus fragmentos listos para usar")
  if not snippets:
    st.info(
        "Aún no hay códigos guardados. Usa la pestaña de celular para crear el"
        " primero."
    )

  for titulo, codigo in snippets.items():
    # Creamos una tarjeta visual limpia para cada código
    with st.container(border=True):
      st.markdown(f"**📌 {titulo}**")
      # st.code muestra el código con formato y trae su propio botón de copiado
      st.code(codigo, language="python")

# --- VISTA DEL CELULAR / ADMINISTRACIÓN ---
with tab_movil:
  st.subheader("Administrar Fragmentos")

  # Elegimos si queremos crear uno nuevo o editar uno viejo
  accion = st.radio(
      "¿Qué deseas hacer?", ["Crear nuevo código", "Editar código existente"]
  )

  if accion == "Crear nuevo código":
    with st.form("form_nuevo"):
      nuevo_titulo = st.text_input("Título descriptivo (ej. Leer archivo CSV)")
      nuevo_codigo = st.text_area("Pega tu bloque de código aquí")
      boton_guardar = st.form_submit_button("Guardar en la nube")

      if boton_guardar:
        if nuevo_titulo and nuevo_codigo:
          snippets[nuevo_titulo] = nuevo_codigo
          guardar_datos(snippets)
          st.success(f"¡'{nuevo_titulo}' guardado con éxito!")
          st.rerun()  # Recarga la app para reflejar los cambios
        else:
          st.error("Por favor completa ambos campos.")

  else:  # Editar existente
    if snippets:
      # Seleccionamos cuál queremos modificar
      a_editar = st.selectbox(
          "Selecciona el código que quieres actualizar", list(snippets.keys())
      )
      codigo_viejo = snippets[a_editar]

      with st.form("form_editar"):
        edit_titulo = st.text_input("Modificar título", value=a_editar)
        edit_codigo = st.text_area("Modificar código", value=codigo_viejo)
        boton_actualizar = st.form_submit_button("Guardar cambios")

        if boton_actualizar:
          # Si cambió el título, borramos la llave vieja para que no se duplique
          if edit_titulo != a_editar:
            del snippets[a_editar]
          snippets[edit_titulo] = edit_codigo
          guardar_datos(snippets)
          st.success("¡Entrada actualizada correctamente sin crear duplicados!")
          st.rerun()
    else:
      st.info("No hay códigos disponibles para editar.")

