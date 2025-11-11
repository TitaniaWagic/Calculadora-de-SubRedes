# 🌐 Calculadora de Subredes

[![Live Demo](https://img.shields.io/badge/demo-online-brightgreen)](https://calculadora-de-subredes.onrender.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Una aplicación web intuitiva y potente para realizar cálculos de subredes IP. Diseñada para facilitar el trabajo con direccionamiento IPv4, segmentación de redes y planificación de infraestructura de red.

**🔗 [Demo en Vivo](https://calculadora-de-subredes.onrender.com/)**

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalación Local](#instalación-local)
- [Uso](#-uso)
  - [Modos de Cálculo](#modos-de-cálculo)
- [Despliegue](#-despliegue)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)
- [Contribuir](#-contribuir)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)

---

## ✨ Características

### 🔢 **Cálculo Completo de Subredes por Conexiones**
- Ingresa una dirección IP base y el número de hosts necesarios por subred
- Calcula automáticamente:
  - Dirección de subred
  - Máscara de subred óptima
  - Primera y última dirección IP utilizable
  - Dirección de broadcast
  - Hosts válidos vs hosts necesarios
  - Total de hosts posibles

### 🎯 **Cálculo de Máscara Mínima**
- Determina la máscara de subred mínima requerida para una cantidad específica de hosts
- Muestra la máscara en formato decimal punteado y en notación CIDR

### 🔍 **Análisis de Subred Existente**
- Ingresa una IP y máscara para analizar una subred existente
- Visualiza todas las subredes disponibles dentro de ese rango

### 📊 **Listado de Hosts Válidos**
- Genera una lista completa de todas las direcciones IP utilizables en una subred
- Distingue entre hosts válidos, dirección de red y broadcast

### 🎨 **Interfaz Intuitiva**
- Diseño limpio y fácil de usar
- Responsive: funciona en desktop, tablet y móvil
- Sin necesidad de conocimientos técnicos avanzados

### ⚡ **Rendimiento Optimizado**
- Cálculos instantáneos incluso para redes grandes
- Backend eficiente con Flask
- Manejo robusto de errores


## 🚀 Instalación

### Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior** - [Descargar Python](https://www.python.org/downloads/)
- **pip** (gestor de paquetes de Python, incluido con Python 3.4+)
- **Git** (opcional, para clonar el repositorio)

### Instalación Local

1. **Clona el repositorio** (o descarga el código fuente):

```bash
git clone https://github.com/TitaniaWagic/Calculadora-de-SubRedes.git
cd calculadora-de-subredes
```

2. **Crea un entorno virtual** (recomendado):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias**:

```bash
pip install -r requirements.txt
```

4. **Ejecuta la aplicación**:

```bash
python backend.py
```

5. **Abre tu navegador** y ve a:

```
http://127.0.0.1:5000
```

¡Listo! La aplicación debería estar corriendo localmente.

---

## 💡 Uso

### Modos de Cálculo

#### 1️⃣ **Cálculo por Conexiones Necesarias**

Ideal para planificar redes cuando conoces la cantidad de dispositivos por segmento.

**Pasos:**
1. Ingresa una **dirección IP base** (ejemplo: `192.168.1.0`)
2. En el campo **"Conexiones"**, ingresa el número de hosts necesarios por subred, separados por comas
   - Ejemplo: `50, 30, 20, 10`
3. Haz clic en **"Calcular"**

**Resultado:** 
- Obtendrás una tabla con cada subred optimizada, mostrando direcciones de red, rangos IP utilizables, broadcasts y máscaras.

---

#### 2️⃣ **Cálculo de Máscara Mínima**

Para determinar qué máscara usar cuando sabes cuántos hosts necesitas.

**Pasos:**
1. Ingresa una **dirección IP base** (ejemplo: `10.0.0.0`)
2. En el campo **"Hosts por subred"**, ingresa el número de hosts
   - Ejemplo: `100`
3. Haz clic en **"Calcular Máscara"**

**Resultado:**
- Máscara en notación CIDR (ejemplo: `/25`)
- Máscara en formato decimal punteado (ejemplo: `255.255.255.128`)

---

#### 3️⃣ **Análisis de Subred por IP/Máscara**

Para analizar una subred existente.

**Pasos:**
1. Ingresa una **dirección IP** (ejemplo: `172.16.0.0`)
2. Ingresa la **máscara de subred**
   - Formato decimal: `255.255.255.0`
   - O formato CIDR: `/24`
3. Haz clic en **"Calcular Subredes"**

**Resultado:**
- Lista de todas las subredes disponibles dentro del rango especificado.

---

#### 4️⃣ **Listado de Hosts Válidos**

Para ver todas las IPs utilizables en una subred.

**Pasos:**
1. Ingresa una **dirección IP** (ejemplo: `192.168.10.0`)
2. Ingresa la **máscara** (ejemplo: `255.255.255.0` o `/24`)
3. Selecciona la opción **"Listar Hosts"**

**Resultado:**
- Lista completa de IPs válidas
- Dirección de red y broadcast
- Total de hosts disponibles

---

## 🌍 Despliegue

### Despliegue en Render

La aplicación está actualmente desplegada en **Render**. Para desplegar tu propia instancia:

1. **Crea una cuenta en [Render](https://render.com/)**

2. **Crea un nuevo "Web Service"**

3. **Conecta tu repositorio de GitHub**

4. **Configura el servicio:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend:app`
   - **Environment:** Python 3

5. **Despliega** y espera a que se complete el proceso

### Despliegue en otras plataformas

- **Heroku:** Usa el `Procfile` incluido
- **Railway:** Funciona out-of-the-box
- **Vercel/Netlify:** Requiere configuración adicional para Flask

---

## 📁 Estructura del Proyecto

```
calculadora-de-subredes/
│
├── backend.py                    # Aplicación Flask principal
├── requirements.txt              # Dependencias de Python
├── runtime.txt                   # Versión de Python para Render
├── start.sh                      # Script de inicio para despliegue
├── README.md                     # Este archivo
├── Notas_para_el_proyecto.txt   # Notas de desarrollo
│
├── templates/                    # Plantillas HTML
│   └── index.html               # Interfaz principal
│
└── static/                       # Archivos estáticos
    ├── style.css                # Estilos CSS
    └── javascript.js            # Lógica del frontend
```

---

## 🛠 Tecnologías

### Backend
- **[Flask](https://flask.palletsprojects.com/)** - Framework web ligero de Python
- **[ipaddress](https://docs.python.org/3/library/ipaddress.html)** - Módulo para manipulación de direcciones IP
- **[Gunicorn](https://gunicorn.org/)** - Servidor WSGI para producción

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos y diseño responsive
- **JavaScript (Vanilla)** - Interactividad

### Herramientas de Desarrollo
- **Python 3.8+**
- **Git** - Control de versiones

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto:

1. **Fork el repositorio**
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Haz commit de tus cambios**:
   ```bash
   git commit -m "Agrega nueva funcionalidad"
   ```
4. **Push a la rama**:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Abre un Pull Request**

### Guías de Contribución
- Mantén el código limpio y comentado
- Sigue las convenciones de estilo PEP 8 para Python
- Añade tests si introduces nuevas funcionalidades
- Actualiza la documentación según sea necesario

---

## 🗺 Roadmap

### Próximas Características

- [ ] **Soporte para IPv6** - Cálculos con direcciones IPv6
- [ ] **Exportar resultados** - Descargar resultados en PDF/CSV
- [ ] **Modo oscuro** - Tema dark para la interfaz
- [ ] **Cálculo de VLSM avanzado** - Variable Length Subnet Masking
- [ ] **Visualización gráfica** - Diagramas de red interactivos
- [ ] **API REST** - Endpoints JSON para integración con otras aplicaciones
- [ ] **Historial de cálculos** - Guardar y recuperar cálculos anteriores
- [ ] **Multi-idioma** - Soporte para inglés, español, portugués

### Mejoras Planificadas

- [ ] Optimización de rendimiento para redes muy grandes
- [ ] Tests unitarios completos
- [ ] Documentación de API
- [ ] Tutorial interactivo para nuevos usuarios

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.


## 🙏 Agradecimientos

- A la comunidad de Python y Flask por sus excelentes herramientas
- A todos los colaboradores que han ayudado a mejorar este proyecto
- A los usuarios que han proporcionado feedback valioso

---

<div align="center">
  
**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**


</div>
