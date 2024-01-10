# Ejecución del Proyecto

Este proyecto requiere un trabajo previo para la creación del conjunto de datos.

Por razones de confidencialidad, no es posible mostrar los conjuntos de datos originales de BSM. No obstante, se pueden examinar los scripts utilizados para su creación.

En caso de disponer de los conjuntos de datos originales, puedes ejecutar el generador del conjunto de datos simplemente ejecutando el siguiente script en Python:

```bash
python3 dataset_generation/dataset_generator.py
```


Este script genera conjuntos de datos auxiliares que se utilizan para construir el conjunto de datos final denominado `dataset.csv`.

Los cuadernos (notebooks) pueden ejecutarse de manera independiente para realizar pruebas en modelos de forma individual y cómoda. El proyecto se compone de 6 cuadernos:

- **`Treball_Previ.ipynb`**: Contiene el código y una breve explicación del preprocesado y la visualización de los datos.
- **`Modelos_Lineales.ipynb`**: Incluye el código de tres modelos lineales (LR, KNN y SVM Poly).
- **`RandomForest.ipynb`**: Contiene el código para el modelo RandomForest.
- **`GradientBoosting.ipynb`**: Contiene el código para el modelo GradientBoosting.
- **`MLP.ipynb`**: Contiene el código para el modelo MLP.

Todo el proyecto se encuentra compilado en un informe detallado llamado `informe.pdf`.