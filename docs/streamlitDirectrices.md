## Detalle de avance recomendado 2

* Realizar procesos de monitoreo y detección de data drift.
* Desarrollar una aplicación en Streamlit.
* Generar el archivo `README.md` para tu ejercicio, documentando el caso de negocio y los principales hallazgos y proceso.

---

### Componente: `model_monitoring.py`

Crea el trabajo de monitoreo que trae en una tabla los datos junto con los pronósticos entregados y los utiliza, con una periodicidad definida, para muestrear y obtener métricas que permitan detectar cambios en la población que puedan afectar el desempeño del modelo.

**Elementos Clave:**

* **Muestreo:** Muestreo periódico de los datos para análisis estadístico.
* **Medida del Datadrift:** Cálculo de métricas de data drift, como:
    * Kolmogorov-Smirnov (KS test)
    * Population Stability Index (PSI)
    * Jensen-Shannon divergence
    * Chi-cuadrado para variables categóricas
* **Alertas:** Generación de alertas si se detectan desviaciones significativas que puedan comprometer la precisión del modelo.

---

### Componente: Aplicación en Streamlit

Panel de visualización para las métricas de monitoreo.

* **Visualización de métricas**
    * Gráficos de comparación entre distribución histórica vs actual.
    * Tablas con métricas de drift por variable.
    * Indicadores visuales de alerta (semáforo, barras de riesgo).

* **Análisis temporal**
    * Evolución del drift a lo largo del tiempo.
    * Detección de tendencias o cambios abruptos.

* **Recomendaciones**
    * Mensajes automáticos si se supera un umbral crítico.
    * Sugerencias de retraining o revisión de variables.