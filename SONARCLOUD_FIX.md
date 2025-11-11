# 🔧 Solución Rápida para SonarCloud

## ❌ Error Actual
```
ERROR: Project not found. Please check the 'sonar.projectKey' and 'sonar.organization' properties, 
the 'SONAR_TOKEN' environment variable
```

## ✅ Solución en 3 Pasos

### Paso 1: Crear el Proyecto en SonarCloud (2 minutos)

1. Ve a **https://sonarcloud.io**
2. Inicia sesión con GitHub
3. Click en **"+"** (esquina superior derecha) → **"Analyze new project"**
4. Selecciona tu repositorio: **final-project-ml**
5. Click en **"Set Up"**
6. **IMPORTANTE**: Anota el `projectKey` que aparece (probablemente sea `JuanSNuno_final-project-ml`)

### Paso 2: Obtener el Token de SonarCloud (1 minuto)

1. En SonarCloud, click en tu avatar → **"My Account"** → **"Security"**
2. En la sección **"Generate Tokens"**:
   - Name: `github-actions`
   - Type: `Global Analysis Token`
   - Expires: `90 days` o más
3. Click **"Generate"**
4. **COPIA EL TOKEN** (solo se muestra una vez)

### Paso 3: Agregar el Token a GitHub (1 minuto)

1. Ve a **https://github.com/JuanSNuno/final-project-ml/settings/secrets/actions**
2. Click en **"New repository secret"**
3. Configura:
   - **Name**: `SONAR_TOKEN` (exactamente así, en mayúsculas)
   - **Value**: Pega el token de SonarCloud
4. Click **"Add secret"**

## 🧪 Verificar la Configuración

Ejecuta este script para verificar que todo está correcto:

```powershell
python verify_sonarcloud_config.py
```

## 🚀 Probar

1. Haz un pequeño cambio (por ejemplo, agrega un comentario en algún archivo)
2. Haz commit y push:
   ```powershell
   git add .
   git commit -m "test: Verificar integración con SonarCloud"
   git push origin certification
   ```
3. Ve a **https://github.com/JuanSNuno/final-project-ml/actions**
4. Verifica que el workflow **"SonarCloud Analysis"** se ejecute correctamente

## 📊 Ver Resultados

Una vez que el análisis sea exitoso:
- **Dashboard**: https://sonarcloud.io/dashboard?id=JuanSNuno_final-project-ml

## ⚠️ Notas Importantes

- El `projectKey` **DEBE** coincidir exactamente con el que aparece en SonarCloud
- El formato típico es: `{TuUsuarioGitHub}_{NombreRepositorio}`
- Si ves un `projectKey` diferente en SonarCloud, actualiza estos archivos:
  - `.github/workflows/sonarcloud.yml`
  - `sonar-project.properties`

## 🆘 ¿Problemas?

Consulta la guía detallada: **docs/SONARCLOUD_SETUP.md**

## 📝 Cambios Realizados

He actualizado los siguientes archivos con la configuración correcta:

1. ✅ `.github/workflows/sonarcloud.yml` - Actualizado a la acción v5 y agregada verificación de token
2. ✅ `sonar-project.properties` - Actualizado projectKey al formato correcto
3. ✅ `docs/SONARCLOUD_SETUP.md` - Guía detallada de configuración
4. ✅ `verify_sonarcloud_config.py` - Script de verificación automática

**Ahora solo necesitas completar los 3 pasos arriba para que funcione.** 🎯
