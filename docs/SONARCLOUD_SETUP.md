# Guía de Configuración de SonarCloud

## Problema Actual
El análisis de SonarCloud falla con el error:
```
Project not found. Please check the 'sonar.projectKey' and 'sonar.organization' properties, 
the 'SONAR_TOKEN' environment variable
```

## Pasos para Solucionar

### 1. Crear/Verificar el Proyecto en SonarCloud

1. Ve a [SonarCloud](https://sonarcloud.io)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en el botón **"+"** en la esquina superior derecha
4. Selecciona **"Analyze new project"**
5. Selecciona tu organización: **juansnuno**
6. Busca y selecciona el repositorio: **final-project-ml**
7. Haz clic en **"Set Up"**

### 2. Configurar el Token de SonarCloud

#### Opción A: Crear un Nuevo Token

1. En SonarCloud, ve a tu perfil (esquina superior derecha)
2. Click en **"My Account"** > **"Security"**
3. En la sección **"Tokens"**, genera un nuevo token:
   - **Name**: `github-actions-final-project-ml`
   - **Type**: `Global Analysis Token` o `Project Analysis Token`
   - **Expires in**: Selecciona una duración apropiada (recomendado: 90 días o más)
4. Copia el token generado (¡solo se muestra una vez!)

#### Opción B: Usar un Token Existente

Si ya tienes un token, verifica que:
- No haya expirado
- Tenga permisos suficientes para analizar proyectos
- Sea de tipo "Analysis" token

### 3. Agregar el Token a GitHub Secrets

1. Ve a tu repositorio en GitHub: `https://github.com/JuanSNuno/final-project-ml`
2. Click en **"Settings"** (pestaña del repositorio)
3. En el menú lateral izquierdo, click en **"Secrets and variables"** > **"Actions"**
4. Click en **"New repository secret"**
5. Configura el secret:
   - **Name**: `SONAR_TOKEN`
   - **Value**: Pega el token copiado de SonarCloud
6. Click en **"Add secret"**

### 4. Verificar la Configuración del Proyecto en SonarCloud

1. En SonarCloud, ve a tu proyecto: **final-project-ml**
2. Click en **"Administration"** > **"Analysis Method"**
3. Selecciona **"GitHub Actions"**
4. Verifica que la configuración muestre:
   ```
   sonar.projectKey=JuanSNuno_final-project-ml
   sonar.organization=juansnuno
   ```
   
   **⚠️ IMPORTANTE**: El `projectKey` en SonarCloud suele ser `{organization}_{repository-name}`

### 5. Actualizar la Configuración del Proyecto

El `projectKey` correcto debería ser probablemente uno de estos:
- `JuanSNuno_final-project-ml` (formato típico de SonarCloud)
- `final-project-ml` (nombre simple del repositorio)

**Verifica en SonarCloud cuál es el projectKey exacto de tu proyecto.**

### 6. Probar la Configuración

Una vez configurado todo:

1. Haz un commit pequeño a la rama `certification`
2. Haz push al repositorio
3. Ve a la pestaña **"Actions"** en GitHub
4. Verifica que el workflow **"SonarCloud Analysis"** se ejecute exitosamente

## Comandos Útiles para Diagnóstico

### Verificar el proyecto localmente (opcional)
```bash
# Instalar sonar-scanner localmente
# Ver: https://docs.sonarcloud.io/advanced-setup/ci-based-analysis/sonarscanner-cli/

# Ejecutar análisis local (requiere SONAR_TOKEN configurado)
sonar-scanner \
  -Dsonar.projectKey=JuanSNuno_final-project-ml \
  -Dsonar.organization=juansnuno \
  -Dsonar.sources=mlops_pipeline/src \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=YOUR_SONAR_TOKEN
```

## Checklist de Verificación

- [ ] Proyecto creado en SonarCloud
- [ ] Token de SonarCloud generado
- [ ] Secret `SONAR_TOKEN` agregado en GitHub
- [ ] `projectKey` correcto identificado en SonarCloud
- [ ] Archivos de configuración actualizados con el `projectKey` correcto
- [ ] Push realizado para probar el workflow
- [ ] Workflow ejecutado exitosamente

## Solución de Problemas Comunes

### Error: "Project not found"
- Verifica que el proyecto existe en SonarCloud
- Confirma que el `projectKey` es exactamente el mismo que en SonarCloud
- Asegúrate de que el token tenga permisos para el proyecto

### Error: "SONAR_TOKEN is not recommended"
- Esto es solo un warning si el token no está configurado
- Asegúrate de que el secret `SONAR_TOKEN` existe en GitHub

### Error: "Could not find a default branch"
- El proyecto fue creado recientemente en SonarCloud
- Espera unos minutos y vuelve a intentar
- Ejecuta un análisis manual desde SonarCloud primero

## Referencias

- [Documentación de SonarCloud](https://docs.sonarcloud.io/)
- [GitHub Actions para SonarCloud](https://github.com/SonarSource/sonarcloud-github-action)
- [Análisis de Python con SonarCloud](https://docs.sonarcloud.io/enriching-results/languages/python/)
