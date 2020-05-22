# Este es un archivo de configuración configuracionPaquetesYEntorno.R
# Se establecerán los trozos de código para la configuración del entorno
# y carga de librerías

## @knitr cargaLibrerias

# Librería de manipulación de datos en R
library(dplyr)
# Librería de generación de gráficos
library(ggplot2)
# Libreria de procedimientos psicométricos 
library(psych)
# Librería para estilo de tablas
library(kableExtra)
# Librería para estilo grillas de gráficas
library(gridExtra)
# Habilita el uso de python en el presente documento
library(reticulate) 
# Utiliza el interprete del entorno virtual
use_condaenv("Proy1MAAII", conda = "/software/anaconda3/bin/conda")