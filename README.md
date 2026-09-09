# VideoClip Desktop

<p align="center">
 <img width="256" height="256" alt="videoclip-desktop-256" src="https://github.com/user-attachments/assets/7a34a77f-9a48-4234-9e4d-2e9952d7f196" 
 width="160" alt="VideoClip Desktop">
</p>

<h1 align="center">VideoClip Desktop</h1>

<p align="center">
  Descarga videos, extrae audio y crea clips desde una aplicación de escritorio simple y moderna.
</p>

<p align="center">
  <strong>Tu contenido, tu manera.</strong>
</p>

---

## Sobre VideoClip Desktop

**VideoClip Desktop** es una aplicación de escritorio desarrollada en Python y PySide6 que permite trabajar con contenido multimedia desde una interfaz gráfica, sin necesidad de utilizar comandos de terminal.

La aplicación utiliza **yt-dlp** para la obtención de contenido y **FFmpeg** para el procesamiento de audio y video.

Actualmente la versión pública está orientada a **Linux x86-64**, con soporte para Ubuntu y distribuciones basadas en Debian.

---

## Características

* Descargar videos completos.
* Seleccionar calidad de video.
* Crear clips indicando tiempo de inicio y fin.
* Realizar cortes precisos mediante FFmpeg.
* Extraer audio en formato MP3.
* Analizar videos antes de descargarlos.
* Mostrar título, canal, duración y miniatura.
* Asignar nombres personalizados a los archivos.
* Seleccionar carpeta de destino.
* Guardar carpetas favoritas.
* Abrir directamente la carpeta de descarga.
* Abrir el archivo descargado.
* Barra de progreso.
* Cancelación de descargas.
* Historial persistente de descargas.
* Notificaciones del sistema.
* Integración opcional con cookies de Brave.
* Interfaz oscura.
* yt-dlp incluido.
* FFmpeg y ffprobe incluidos en las distribuciones Linux.

---

## Capturas

### Interfaz principal

<p align="center">
  <img
    src="assets/screenshots/01-main-window.png"
    width="900"
    alt="Interfaz principal de VideoClip Desktop"
  >
</p>

### Creación de clips

<p align="center">
  <img
    src="assets/screenshots/02-clip-mode.png"
    width="900"
    alt="Modo de creación de clips de VideoClip Desktop"
  >
</p>

### Historial de descargas

<p align="center">
  <img
    src="assets/screenshots/03-history.png"
    width="900"
    alt="Historial de descargas de VideoClip Desktop"
  >
</p>

## Descargar

Las versiones publicadas de VideoClip Desktop están disponibles en:

**GitHub Releases**

https://github.com/DeivyJose/video-clip-desktop/releases

Para Linux se ofrecen actualmente dos formatos:

| Formato     | Uso recomendado                                           |
| ----------- | --------------------------------------------------------- |
| `.AppImage` | Ejecutar la aplicación sin instalarla                     |
| `.deb`      | Instalarla en Ubuntu, Debian y distribuciones compatibles |

---

# Linux

## Opción 1 — AppImage

Descarga:

```text
VideoClip-Desktop-1.0.0-x86_64.AppImage
```

Dale permiso de ejecución:

```bash
chmod +x VideoClip-Desktop-1.0.0-x86_64.AppImage
```

Ejecuta:

```bash
./VideoClip-Desktop-1.0.0-x86_64.AppImage
```

No necesitas instalar Python, yt-dlp, FFmpeg ni ffprobe por separado.

---

## Opción 2 — Ubuntu / Debian

Descarga:

```text
VideoClip-Desktop-1.0.0-amd64.deb
```

Instálalo con:

```bash
sudo apt install ./VideoClip-Desktop-1.0.0-amd64.deb
```

Después podrás buscar:

```text
VideoClip Desktop
```

en el menú de aplicaciones.

También puedes ejecutarlo desde terminal:

```bash
videoclip-desktop
```

### Desinstalar

```bash
sudo apt remove videoclip-desktop
```

---

# Uso

## Descargar un video

1. Pega la URL.
2. Presiona **Analizar**.
3. Selecciona **Video**.
4. Elige la calidad.
5. Selecciona la carpeta de destino.
6. Presiona **Descargar**.

---

## Crear un clip

Selecciona:

```text
Modo: Recorte
```

Indica:

```text
Inicio: 00:00:10
Final:  00:00:25
```

VideoClip Desktop descargará y procesará únicamente la sección seleccionada.

También puedes activar el corte preciso para obtener una delimitación más exacta.

---

## Extraer MP3

Selecciona:

```text
Modo: MP3
```

y presiona:

```text
Descargar
```

VideoClip Desktop utilizará FFmpeg para generar el archivo de audio.

---

# Historial

VideoClip Desktop mantiene un historial local de las descargas realizadas.

El historial permite:

* localizar archivos recientes;
* abrir archivos;
* abrir la carpeta que los contiene;
* conservar registros después de cerrar la aplicación.

Los datos de configuración se almacenan localmente en:

```text
~/.config/video-clip-desktop/
```

Eliminar el historial desde la aplicación no elimina los archivos descargados.

---

# Compatibilidad

## Linux

Versión actual:

```text
Linux x86-64
```

Principalmente probada en:

```text
Ubuntu 24.04 LTS
```

También puede funcionar en otras distribuciones Linux compatibles.

## Windows

La distribución para Windows está prevista para una etapa posterior del proyecto.

---

# Privacidad

VideoClip Desktop funciona localmente.

La aplicación no requiere crear una cuenta propia de VideoClip Desktop y no almacena tus descargas en servidores administrados por este proyecto.

El contenido descargado se guarda en la carpeta seleccionada por el usuario.

---

# Uso responsable

VideoClip Desktop es una herramienta para gestionar contenido multimedia.

El usuario es responsable de utilizar la aplicación respetando:

* los derechos de autor;
* las licencias del contenido;
* los términos de los servicios utilizados;
* las leyes aplicables en su jurisdicción.

---

# Autor

**Deivy Jose**

GitHub:

https://github.com/DeivyJose

LinkedIn:

https://www.linkedin.com/in/deivy-jose-ure%C3%B1a-namias-6058a9237/

---

<p align="center">
  <strong>VideoClip Desktop</strong><br>
  Tu contenido, tu manera.
</p>
