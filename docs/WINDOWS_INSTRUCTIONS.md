# 🪟 INSTRUCCIONES PARA WINDOWS - Sistema Completo

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener:

- ✅ Python 3.11+ instalado
- ✅ Git (opcional)
- ✅ Docker Desktop (solo si usas Docker)

### Verificar Instalación

Abre **PowerShell** y ejecuta:

```powershell
# Verificar Python
python --version

# Debe mostrar: Python 3.11.x o superior

# Verificar pip
pip --version

# Si Docker:
docker --version
```

---

## ⚡ OPCIÓN 1: Un Solo Comando (Recomendado)

### Paso 1: Abre PowerShell

1. Presiona `Win + R`
2. Escribe `powershell`
3. Presiona `ENTER`

### Paso 2: Navega al Proyecto

```powershell
cd "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml"
```

### Paso 3: Instala Dependencias (Primera Vez)

```powershell
pip install -r requirements.txt
```

### Paso 4: Inicia el Sistema

```powershell
python run_full_system.py
```

### Paso 5: Espera y Disfruta

- Verá mensajes de inicialización
- Se abrirá una ventana de API
- Se abrirá navegador automáticamente
- UI disponible en **http://localhost:8501**

---

## 🐳 OPCIÓN 2: Docker (Producción)

### Paso 1: Instala Docker Desktop

Descarga desde: https://www.docker.com/products/docker-desktop

### Paso 2: Inicia Docker Desktop

1. Abre "Docker Desktop" desde Start Menu
2. Espera a que el icono esté verde

### Paso 3: Abre PowerShell

```powershell
cd "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml"
```

### Paso 4: Construye la Imagen (Primera Vez)

```powershell
docker-compose build
```

Espera 2-3 minutos.

### Paso 5: Inicia los Servicios

```powershell
docker-compose up
```

Verás logs de inicio. Cuando veas:
```
✓ API en http://localhost:8000
✓ UI en http://localhost:8501
```

### Paso 6: Abre Navegador

Ve a: **http://localhost:8501**

### Para Detener:

Presiona `CTRL + C` en PowerShell

---

## 👨‍💻 OPCIÓN 3: Manual (Control Total)

### Paso 1: Abre 2 PowerShells

Abre dos ventanas de PowerShell.

**En ambas:**
```powershell
cd "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml"
pip install -r requirements.txt
```

### Paso 2: Terminal 1 - API

En la **primera PowerShell:**

```powershell
cd mlops_pipeline\src\scripts
python model_deploy.py
```

Verás:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**NO CIERRES ESTA VENTANA.**

### Paso 3: Terminal 2 - UI

En la **segunda PowerShell:**

```powershell
streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

Verás:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Se abrirá navegador automáticamente.

---

## 🌐 Acceso a la Interfaz

Después de cualquier opción anterior, tu navegador abrirá:

```
http://localhost:8501
```

Si no se abre automáticamente, copia manualmente esa URL en tu navegador.

### URLs Principales

| Servicio | URL |
|----------|-----|
| **UI Principal** | http://localhost:8501 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

---

## 🎯 Primer Uso - Guía Rápida

### Predicción Individual (2 minutos)

1. Abre http://localhost:8501
2. Ve a pestaña **"📋 Predicción Individual"**
3. Deja valores por defecto
4. Haz clic en **"🔮 Realizar Predicción"**
5. Espera resultado (~2 segundos)
6. Verás probabilidad y recomendaciones

### Predicción por Lote (5 minutos)

1. Ve a pestaña **"📊 Predicción por Lote"**
2. Haz clic en **"📄 Descargar Plantilla CSV"**
3. Abre en Excel
4. Completa múltiples pacientes (u usa valores)
5. Guarda como CSV
6. Sube archivo en UI
7. Haz clic **"🔮 Predecir Lote"**
8. Descarga resultados

---

## ❌ Solución de Problemas (Windows)

### Problema: "Python no reconocido"

```powershell
# Solución: Usa python.exe
python.exe --version

# O agrega a PATH manualmente
# Win + X → Settings → System → About → 
# Advanced system settings → Environment Variables
```

### Problema: "Puerto 8501 en uso"

```powershell
# Buscar proceso
netstat -ano | findstr :8501

# Matar proceso (si PID es 1234)
taskkill /PID 1234 /F

# O usar otro puerto
streamlit run mlops_pipeline/src/scripts/prediction_ui.py --server.port 8502
```

### Problema: "API no disponible"

```powershell
# Verificar que está ejecutándose
curl http://localhost:8000/health

# Si no responde, iniciar en otra terminal
python mlops_pipeline\src\scripts\model_deploy.py
```

### Problema: "ModuleNotFoundError"

```powershell
# Instalar dependencias nuevamente
pip install -r requirements.txt --upgrade
```

### Problema: "FileNotFoundError: best_model.joblib"

```powershell
# Entrenar modelo
python run_pipeline.py --full

# Espera 5-10 minutos según tu computadora
```

### Problema: Streamlit se congela

```powershell
# Presiona CTRL + C
# Espera 5 segundos
# Reinicia

streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

### Problema: Docker no inicia

```powershell
# Opción 1: Reconstruir
docker-compose down
docker-compose build --no-cache

# Opción 2: Limpiar todo
docker system prune
docker-compose up
```

---

## 🔧 Configuración Avanzada (Windows)

### Cambiar Puerto Streamlit

```powershell
# En lugar de 8501, usar 8502
streamlit run mlops_pipeline/src/scripts/prediction_ui.py --server.port 8502
```

### Cambiar URL de API

Abre: `mlops_pipeline/src/scripts/prediction_ui.py`

Busca línea 28:
```python
API_URL = "http://localhost:8000"
```

Cambia a tu servidor:
```python
API_URL = "http://tu-servidor.com:8000"
```

Guarda y reinicia Streamlit.

### Acceso desde Otra Computadora

```powershell
# Obtén tu IP local
ipconfig

# Busca "IPv4 Address: 192.168.x.x" o similar

# Inicia UI en 0.0.0.0
streamlit run mlops_pipeline/src/scripts/prediction_ui.py ^
  --server.address 0.0.0.0 ^
  --server.port 8501
```

Luego accede desde otra PC:
```
http://192.168.x.x:8501
```

---

## 🐛 Testing & Validación

### Verificar que todo funciona

```powershell
python test_prediction_ui.py
```

Ejecuta todos los checks:
- ✓ Python version
- ✓ Dependencias instaladas
- ✓ Artefactos presentes
- ✓ Script UI existe
- ✓ API disponible
- ✓ Predicción funciona

---

## 📊 Comandos Útiles de Windows

### Ver qué procesos usan puertos

```powershell
# Ver puerto 8000
netstat -ano | findstr :8000

# Ver puerto 8501
netstat -ano | findstr :8501
```

### Matar proceso por ID

```powershell
taskkill /PID 5432 /F
```

### Ver ambiente Python

```powershell
python -m venv --help
pip list
pip show streamlit
```

### Instalar paquete específico

```powershell
pip install plotly==5.18.0
pip install --upgrade pandas
```

### Limpiar cache pip

```powershell
pip cache purge
```

---

## 🔄 Ciclo Desarrollo (Iterativo)

### Primera Vez

1. `pip install -r requirements.txt`
2. `python run_pipeline.py --full` (entrena modelo)
3. `python run_full_system.py` (inicia todo)

### Siguientes Veces

1. `python run_full_system.py` (ya tiene artefactos)

### Modificar Interfaz

1. Edita `prediction_ui.py`
2. Streamlit se recarga automáticamente (F5 en navegador)
3. No es necesario reiniciar

### Reentrenar Modelo

```powershell
python run_pipeline.py --full --skip-training
# O
python run_pipeline.py --full
```

---

## 🚀 Ciclos de Uso Diario

### Mañana
```powershell
python run_full_system.py
# Listo en ~30 segundos
```

### Hacer predicción
```
1. http://localhost:8501
2. Completa formulario
3. Obtén resultado
```

### Cerrar
```powershell
# Presiona CTRL + C en PowerShell
# Ambas ventanas cierran
```

### Luego (Siguiente día)
```powershell
python run_full_system.py
# Repite
```

---

## 📈 Monitoreo (Opcional)

### Ver dashboard de monitoreo

```powershell
python mlops_pipeline/src/scripts/model_monitoring.py

# Luego
streamlit run mlops_pipeline/src/scripts/streamlit_app.py
```

---

## 💾 Backup de Resultados

### Guardar predicciones

1. Ve a "📊 Predicción por Lote"
2. Sube CSV
3. Predice
4. Descarga resultados
5. Guarda en carpeta segura

### Backup de artefactos

```powershell
# Copiar carpeta artifacts
Copy-Item -Path mlops_pipeline/artifacts -Destination backup_artifacts -Recurse
```

---

## ⏱️ Tiempo Estimado por Tarea

| Tarea | Tiempo |
|-------|--------|
| Instalación (primera vez) | 5 min |
| Instalar dependencias | 3 min |
| Entrenar modelo | 5-10 min |
| Iniciar sistema | 30 seg |
| Primera predicción | 2 min |
| Predicción por lote | 5 min |
| Configurar Docker | 10 min |

---

## ✅ Checklist Pre-Producción

Antes de usar en ambiente real:

- [ ] ✓ Ejecutar `test_prediction_ui.py` (todos pasan)
- [ ] ✓ Predicción individual funciona
- [ ] ✓ Predicción por lote funciona
- [ ] ✓ Descargas funcionan
- [ ] ✓ API responde (`curl localhost:8000/health`)
- [ ] ✓ UI se ve profesional
- [ ] ✓ Recomendaciones claras
- [ ] ✓ Leer disclaimer médico
- [ ] ✓ ✅ Sistema listo

---

## 🎓 Recursos Adicionales

**Documentación:**
- QUICK_START_UI.md - Inicio rápido (5 min)
- PREDICTION_UI_GUIDE.md - Manual completo (45 min)
- README_UI.md - Documentación total (60 min)
- DOCUMENTATION_INDEX.md - Índice maestro

**Código:**
- `prediction_ui.py` - Interfaz (700+ líneas comentadas)
- `model_deploy.py` - API FastAPI
- `run_full_system.py` - Orquestación

---

## 🆘 Ayuda de Última Hora

**Algo no funciona?**

1. Abre PowerShell
2. Ejecuta: `python test_prediction_ui.py`
3. Mira qué falla
4. Abre PREDICTION_UI_GUIDE.md → Troubleshooting
5. Sigue la solución

---

## 🎉 ¡Listo!

Si llegaste aquí, estás 100% listo para:

✅ Usar la interfaz  
✅ Hacer predicciones  
✅ Exportar resultados  
✅ Desplegar en producción  

**¡Que disfrutes el sistema!** 🚀

---

**Versión:** 1.0 para Windows  
**Última actualización:** Noviembre 2025  
**Compatibilidad:** Windows 10/11
