### Detalle de avance recomendado 1

* Realizar el proceso de ingeniería de características.
* Empezar a entrenar los primeros modelos.
* Realizar la evaluación de los modelos supervisados, seleccionando el de mejor performance.

---

### Componente: `ft_engineering.py`

Crea la primera componente de nuestro flujo de creación de modelos operativos, del cual se generan los *features* y se retorna el dataset con el cuál se entrenarán los modelos.

* **Resultado:** Genera los conjuntos de datos de entrenamiento y evaluación.
* **Requisito:** Se solicita crear *pipelines* como los siguientes.


Lo que muestra tu diagrama es un ColumnTransformer de scikit-learn. Este es el método estándar de la industria para aplicar diferentes transformaciones a diferentes columnas de tu dataset, todo dentro de un solo paso de pipeline.

Tu pipeline está diseñado para manejar tres tipos de características:

Numeric (Numéricas):

SimpleImputer: Rellena valores faltantes (probablemente con la media o mediana).

Categoric (Categóricas Nominales):

SimpleImputer: Rellena valores faltantes (probablemente con la moda, el valor más frecuente).

OneHotEncoder: Convierte las categorías (ej: "Rojo", "Verde") en columnas binarias (0s y 1s).

Categoric Ordinales (Categóricas Ordinales):

SimpleImputer: Rellena valores faltantes.

OrdinalEncoder: Convierte las categorías que tienen un orden (ej: "Bajo", "Medio", "Alto") en números (ej: 0, 1, 2).

Este ColumnTransformer es el núcleo de tu "ingeniería de características".

¿Te gustaría que te genere el código de Python con scikit-learn para crear exactamente ese ColumnTransformer que se ve en tu imagen?Lo que muestra tu diagrama es un ColumnTransformer de scikit-learn. Este es el método estándar de la industria para aplicar diferentes transformaciones a diferentes columnas de tu dataset, todo dentro de un solo paso de pipeline.

Tu pipeline está diseñado para manejar tres tipos de características:

Numeric (Numéricas):

SimpleImputer: Rellena valores faltantes (probablemente con la media o mediana).

Categoric (Categóricas Nominales):

SimpleImputer: Rellena valores faltantes (probablemente con la moda, el valor más frecuente).

OneHotEncoder: Convierte las categorías (ej: "Rojo", "Verde") en columnas binarias (0s y 1s).

Categoric Ordinales (Categóricas Ordinales):

SimpleImputer: Rellena valores faltantes.

OrdinalEncoder: Convierte las categorías que tienen un orden (ej: "Bajo", "Medio", "Alto") en números (ej: 0, 1, 2).

Este ColumnTransformer es el núcleo de tu "ingeniería de características".

¿Te gustaría que te genere el código de Python con scikit-learn para crear exactamente ese ColumnTransformer que se ve en tu imagen?