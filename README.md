# Dauruxü: Detección de estados de ánimo de personas y sus actividades para el apoyo en el diagnóstico de trastornos psicológicos en FRPO

## Indice General

1. Contexto
2. Objetivo General
3. Objetivos Especificos
4. Descripción de carpetas y archivos del proyecto
5. Aplicación
   * Requisitos del sistema
   * Ambiente de desarrollo
   * Ejecución
   * Ambiente de producción
   * Documentación
6. Bibliografía

## Contexto

Existen situaciones en el entorno laboral, que pueden influir sobre la salud de las personas. A estas situaciones, se les conoce como factores de riesgo ocupacional y son definidas como las posibles causas que pueden ser responsables de una enfermedad, lesión o daño, como consecuencia de la actividad que se realiza o el medio en el cual se permanece durante el desempeño de la actividad [1][2]. Dentro del contexto mencionado, se pueden encontrar factores de riesgo de tipo químico[3]; factores de riesgo de tipo biológico [4]; factores de riesgo ambiental [5] y factores de riesgo de tipo psicosocial ocupacional (FRPO). Los FRPO involucran aspectos físicos del entorno laboral como el ruido, la iluminación o la temperatura del entorno [6][7] y aspectos psicológicos en las personas como la monotonía, el estrés y la fatiga laboral causada por la carga de trabajo o el exceso de horas trabajadas [8]. Los aspectos psicológicos de los FRPO serán la motivación principal del presente proyecto. 

Dentro del contexto de los FRPO,  existen investigaciones en las que se demuestra que algunas condiciones laborales, generan efectos relacionados con la salud física como los desórdenes musculo esqueléticos [9] o la conducta de las personas como el sedentarismo [10]. Por otra parte, existen otros estudios que evidencian efectos relacionados con la salud mental como el estrés [11] y trastornos psicológicos como la ansiedad [12] o la depresión [13]. En Colombia, el Ministerio de Salud reportó un total de 9.653 casos de enfermedades de naturaleza laboral durante el 2017, manifestados en diferentes actividades económicas como: comercio, hoteles, restaurantes, servicios domésticos, entre otros [14]. Adicionalmente, se registró un total de 1.078 casos críticos de salud mental por exposición a factores de riesgo psicosocial ocupacional, de los cuales 165 casos ocurrieron en la ciudad de Bogotá. Esta problemática crece año a año, según las estadísticas del Observatorio Nacional de Salud Mental [15]. 

En la actualidad, existen métodos que facilitan la evaluación de FRPO y que se han desarrollado a partir de la integración de modelos, que explican los mecanismos de generación de estrés asociados al trabajo. Blach, Sahagun y Cervantes, exponen un trabajo en el que consolidan los principales cuestionarios para la evaluación de FRPO [16]. Sin embargo, estos procedimientos son susceptibles a la variabilidad e incluso subjetividad en las medidas [17], ya que la evaluación se realiza mediante cuestionarios relacionados a aspectos y/o procesos laborales, que no son observados directamente por los especialistas en Seguridad y Salud en el Trabajo (SST), sino que son referidos por los trabajadores [18].

Existen referentes que han abordado algunos aspectos relacionados con la salud mental de las personas en el entorno laboral [19][20]. Algunos de estos trabajos, han dado como resultado, soluciones tecnológicas para el monitoreo de algunos aspectos específicos de los FRPO que van desde la implementación de controles de carga en las extremidades y otras partes del cuerpo a partir de sensores [21], hasta la evaluación de estrés en personas, empleando imágenes de electroencefalograma [22]. Trabajos como los de Zack Zhu [23] o Raffaele Gravina [24], sugieren perspectivas alternativas, basadas en el reconocimiento de estado de ánimo, a partir de la captura de señales con dispositivos electrónicos portátiles. Si bien estos avances representan un gran potencial para la industria de manufactura, la construcción, entre otros [25], existen estudios como el de Shall Mark [26], en el que se manifiestan como limitaciones para su adopción, las implicaciones de costo; la interrupción de las actividades laborales, el carácter intrusivo representado en  la incomodidad con los dispositivos y la privacidad de las personas. 

Otras aproximaciones, abordan la captura e integración con otras fuentes de datos, dando como resultado arquitecturas multimodales [27][28], en los que se aprovecha el procesamiento de imágenes de video, texto, señales, entre otros, para soportar el diagnóstico de emociones [29]. Trabajos como el de Le Yang [30] y Poria Soujana [31] sugieren la fusión de análisis de la paralingüística, la captura de respuesta de entrevistas, características del rostro que ha sido abordada ampliamente [32]-[35], y el movimiento de los ojos [36]. En estas aproximaciones, se evidencia un aporte significativo en el análisis de patrones de voz, y se abordan algunos aspectos de interés dentro de la evaluación de FRPO. Sin embargo, el modo de video utilizado en las publicaciones mencionadas, se enfocan sólo en el reconocimiento facial, requiriendo la captura de primer plano del rostro de las personas y el uso de sensores, cuya implementación tiene algunas limitaciones como se mencionó anteriormente. Adicionalmente, no se incluyen mecanismos en el que se realice un monitoreo constante. 

Dado al abordaje que se la hado dado a los aspecto psicológicos ocupacionales con la falta de observación directa, la carencia de un seguimiento automático e inteligente y las limitaciones de índole intrusivo, surge la pregunta: ¿Cómo calcular indicadores relacionados con trastornos psicológicos para el monitoreo y evaluación factores de riesgos psicosociales ocupacionales, mediante un seguimiento automático no intrusivo, utilizando técnicas de inteligencia artificial y visión por computadora?

Para calcular los indicadores, el presente proyecto se enfocará en el diseño de mecanismos para la observación de forma continua de un conjunto de estados de ánimo y las actividades de una persona. Dichos mecanismos, extraerán información de características diversas como las emociones y escenarios que se desarrollen durante la jornada laboral, relacionados con FRPO. Adicionalmente se diseñarán mecanismos que integrarán la información extraída y con ello, se conformará una serie de indicadores relacionados con trastornos psicológicos, para asistir al monitoreo y evaluación de FRPO. El reto tecnológico, está representado en tres aspectos principales: El primero, corresponde al procesamiento de imágenes provenientes de cámaras convencionales, que son susceptibles a limitaciones como la posición y los datos que pueden proporcionar. El segundo, implica el seguimiento continuo e inteligente para la extracción de características y el cálculo de indicadores relacionados con estado de ánimo y las actividades. El tercer aspecto, corresponde a la integración de la información mencionada anteriormente, para la conformación de indicadores de hábitos relacionados con trastornos psicológicos y la materialización de riesgos ocupacionales. 

Los aspectos mencionados, se abordarán mediante la investigación y complementación de mecanismos para el reconocimiento de personas, sus posturas, expresiones faciales y corporales [41][42]. Con estos mecanismos, se extraerán indicadores a partir de métricas como la cantidad de veces en las que se ha manifestado tristeza o enojo. Por otra parte, estará el cálculo de indicadores relacionados con actividades desarrolladas durante la jornada laboral. En este caso, se identificará si una persona ha permanecido por más tiempo del normal en las instalaciones, si ha adoptado una conducta sedentaria, o  si ha manifestado episodios constantes de insomnio. Para la concepción de los indicadores, se tomará como referencia cuestionarios o instrumentos manuales como el inventario de Beck [43], la escala PHQ-8 [43], entre otros [44], [45]. Para el aspecto de la captura y el procesamiento de bajo nivel de las imágenes, se emplearán herramientas existentes. Sin embargo, existen escenarios en el que para la captura y seguimiento continuo de una persona, se requerirá el procesamiento de múltiples características de la misma fuente. Adicionalmente, la persona puede ser identificada a través de una cámara en un momento determinado y posteriormente cambiar su posición y ser identificada por otra cámara. Este tipo de problemáticas, han sido abordadas mediante arquitecturas basadas en agentes [46]-[49] en las que se definen tareas para su solución especializada, concurrente mediante la definición de estrategias de cooperación. Estas arquitecturas, brindan otros atributos como la concepción modular y la escalabilidad para desarrollo de sistemas distribuidos [50][51], que son relevantes para el diseño de los mecanismos, dentro de este proyecto.


## Objetivo General
Diseñar una arquitectura para la detección de estados de ánimo de personas y sus actividades, mediante la captura de video convencional no intrusivo y técnicas de inteligencia artificial, con el fin de brindar indicadores que apoyen el diagnóstico de trastornos psicológicos y la materialización factores de riesgo psicosocial ocupacional (FRPO) en ambientes de oficina.
## Objetivos Específicos
1. Analizar las técnicas, modelos y herramientas orientadas al reconocimiento de personas, expresiones faciales, posturas y acciones para la identificación de comportamiento, estados de ánimo y  trastornos psicológicos.
2. Diseñar una arquitectura para el seguimiento continuo de estados de ánimo de personas  y actividades dentro de un contexto laboral, para la obtención de indicadores relacionados con trastornos psicológicos y materialización de factores de riesgo psicosocial ocupacional (FRPO) en ambientes de oficina.
3. Evaluar la precisión y utilidad potencial de la arquitectura propuesta, mediante su implementación parcial y puesta en operación controlada.

## Descripción de carpetas y archivos del proyecto

1. aplicación
2. articulosDelProyecto
3. presentacionesDelProyecto
4. estadoDelArte 
   * primerosPasos
   * mapasMentales
   * proyectosDeReferencia	
5. propuestaDelProyecto

## Aplicación

### Requisitos del sistema
### Ambiente de desarrollo
### Ejecución
### Ambiente de producción

### Documentación

## Bibliografía
[1] Ministerio de la protección social, "Resolución 2646 de 2008," 2008. 
[2] M. Rodríguez, "Factores Psicosociales de Riesgo Laboral: ¿Nuevos tiempos, nuevos riesgos?" Observatorio Laboral Revista Venezolana, vol. 2, (3), pp. 127-141, 2009. Available: http://dialnet.unirioja.es/servlet/oaiart?codigo=2995368.
[3] H. E. Landberg, H. Westberg and H. Tinnerberg, "Evaluation of risk assessment approaches of occupational chemical exposures based on models in comparison with measurements," Safety Science, vol. 109, pp. 412-420, 2018. Available: https://www.sciencedirect.com/science/article/pii/S0925753517315631. DOI: 10.1016/j.ssci.2018.06.006.
[4] C. R. N. CORRAO et al, "Biological Risk and Occupational Health," Industrial Health, vol. 50, (4), pp. 326-337, 2012. Available: https://jlc.jst.go.jp/DN/JALC/10007643537?from=SUMMON. DOI: 10.2486/indhealth.MS1324.
[5] E. G. Marshall et al, "Work-Related Unintentional Injuries Associated With Hurricane Sandy in New Jersey," Disaster Medicine and Public Health Preparedness, vol. 10, (3), pp. 394-404, 2016. Available: https://www-cambridge-org.ezproxy.javeriana.edu.co/core/article/workrelated-unintentional-injuries-associated-with-hurricane-sandy-in-new-jersey/AB0220A1F1E274EA41B0C2A33D0F2DCB. DOI: 10.1017/dmp.2016.47.
[6] P. Nataletti et al, "Occupational Exposure to Mechanical Vibration: The Italian Vibration Database for Risk Assessment," International Journal of Occupational Safety and Ergonomics, vol. 14, (4), pp. 379-386, 2008. Available: http://www.tandfonline.com/doi/abs/10.1080/10803548.2008.11076775. DOI: 10.1080/10803548.2008.11076775.
[7] Raúl Mirza et al, "Occupational Noise-Induced Hearing Loss," Journal of Occupational and Environmental Medicine, vol. 60, (9), pp. e501, 2018. Available: https://www.ncbi.nlm.nih.gov/pubmed/30095587. DOI: 10.1097/JOM.0000000000001423.
[8] V. Forastieri, "Psychosocial risks and work-related stress," Jul, 2013. 
[9] V. Putz-Anderson, B. P. Bernard and National Institute for Occupational Safety and Health, Musculoskeletal Disorders and Workplace Factors : A Critical Review of Epidemiologic Evidence for Work-Related Musculoskeletal Disorders of the Neck, Upper Extremity, and Low Back. 1997Available: http://hdl.handle.net/2027/uc1.31210011098603.
[10] Morales D. Diana, "Trabajo por turnos y presencia de obesidad en los trabajadores: Una revisión sistemática exploratoria," Jan 1, 2014. 
[11] K. Azuma et al, "Prevalence and risk factors associated with nonspecific building‐related symptoms in office employees in Japan: relationships between work environment, Indoor Air Quality, and occupational stress," Indoor Air, vol. 25, (5), pp. 499-511, 2015. Available: https://onlinelibrary.wiley.com/doi/abs/10.1111/ina.12158. DOI: 10.1111/ina.12158.
[12] L. Wiegner et al, "Prevalence of perceived stress and associations to symptoms of exhaustion, depression and anxiety in a working age population seeking primary care - an observational study," BMC Family Practice, vol. 16, (1), pp. 38, 2015. Available: https://www.ncbi.nlm.nih.gov/pubmed/25880219. DOI: 10.1186/s12875-015-0252-7.
[13] M. Luca et al, "Prevalence of depression and its relationship with work characteristics in a sample of public workers," Neuropsychiatric Disease and Treatment, vol. 10, pp. 519-525, 2014. Available: https://www.ncbi.nlm.nih.gov/pubmed/24707177. DOI: 10.2147/NDT.S56989.
[14] Ministerio de salud, "Indicadores de riesgos laborales," Https://Www.Minsalud.Gov.Co, 2018. 
[15] Ministerio de salud, "Observatorio Nacional de Salud Mental," Http://Onsaludmental.Minsalud.Gov.Co, 2019. 
[16] Víctor H. Charria O, O. Felipe Arenas and Kewy V. Sarsosa P, "Factores de riesgo psicosocial laboral: métodos e instrumentos de evaluación," Revista De La Facultad Nacional De Salud Pública, 2011. 
[17] M. Caicoya, "Dilemas en la evaluación de riesgos psicosociales," 2004. 
[18] F. G. Benavides, J. Benach and C. Muntaner, "Psychosocial risk factors at the workplace: Is there enough evidence to establish reference values? Job control and its effect on public health. (Editorial)," Journal of Epidemiology & Community Health, vol. 56, (4), pp. 244, 2002. 
[19] S. Choi et al, "Risk Factor, Job Stress and Quality of Life in Workers With Lower Extremity Pain Who Use Video Display Terminals," Annals of Rehabilitation Medicine, vol. 42, (1), pp. 101-112, 2018. Available: https://www.ncbi.nlm.nih.gov/pubmed/29560330. DOI: 10.5535/arm.2018.42.1.101.
[20] K. Golonka et al, "Occupational burnout and its overlapping effect with depression and anxiety," International Journal of Occupational Medicine and Environmental Health, vol. 32, (2), pp. 229-244, 2019. Available: https://www.ncbi.nlm.nih.gov/pubmed/30855601. DOI: 10.13075/ijomeh.1896.01323.
[21] Yong-Ren Huang and Xu-Feng Ouyang, "Sitting posture detection and recognition using force sensor," in Oct 2012, Available: https://ieeexplore.ieee.org/document/6513203. DOI: 10.1109/BMEI.2012.6513203.
[22] H. Jebelli, S. Hwang and S. Lee, "EEG-based workers' stress recognition at construction sites," Automation in Construction, vol. 93, pp. 315-324, 2018. Available: https://www.sciencedirect.com/science/article/pii/S092658051830013X. DOI: 10.1016/j.autcon.2018.05.027.
[23] Z. Zhu et al, "Naturalistic Recognition of Activities and Mood Using Wearable Electronics," T-Affc, vol. 7, (3), pp. 272-285, 2016. Available: https://ieeexplore.ieee.org/document/7299638. DOI: 10.1109/TAFFC.2015.2491927.
[24] R. Gravina and Q. Li, "Emotion-relevant activity recognition based on smart cushion using multi-sensor fusion," Information Fusion, vol. 48, pp. 1-10, 2019. Available: https://www.sciencedirect.com/science/article/pii/S1566253518301064. DOI: 10.1016/j.inffus.2018.08.001.
[25] C. R. Reid et al, "Wearable Technologies: How Will We Overcome Barriers to Enhance Worker Performance, Health, And Safety?" Proceedings of the Human Factors and Ergonomics Society Annual Meeting, vol. 61, (1), pp. 1026-1030, 2017. Available: https://journals.sagepub.com/doi/full/10.1177/1541931213601740. DOI: 10.1177/1541931213601740.
[26] M. C. Schall, R. F. Sesek and L. A. Cavuoto, "Barriers to the Adoption of Wearable Sensors in the Workplace: A Survey of Occupational Safety and Health Professionals," Human Factors: The Journal of Human Factors and Ergonomics Society, vol. 60, (3), pp. 351-362, 2018. Available: https://journals.sagepub.com/doi/full/10.1177/0018720817753907. DOI: 10.1177/0018720817753907.
[27] M. Magdin, M. Turcani and L. & Hudec, "Evaluating the Emotional State of a User Using a
Webcam," International Journal of Interactive Multimedia and Artificial Intelligence, 2016. . DOI: 10.9781/ijimai.2016.4112.
[28] M. Soleymani et al, "A survey of multimodal sentiment analysis," Image and Vision Computing, vol. 65, pp. 3-14, 2017. Available: https://www.sciencedirect.com/science/article/pii/S0262885617301191. DOI: 10.1016/j.imavis.2017.08.003.
[29] J. M. Harley et al, "A multi-componential analysis of emotions during complex learning with an intelligent multi-agent system," Computers in Human Behavior, vol. 48, pp. 615-625, 2015. Available: https://www.sciencedirect.com/science/article/pii/S0747563215001119. DOI: 10.1016/j.chb.2015.02.013.
[30] L. Yang et al, "Multimodal measurement of depression using deep learning models," in Oct 23, 2017, Available: http://dl.acm.org/citation.cfm?id=3133948. DOI: 10.1145/3133944.3133948.
[31] S. Poria et al, "Ensemble application of convolutional neural networks and multiple kernel learning for multimodal sentiment analysis," Neurocomputing, vol. 261, pp. 217-230, 2017. Available: https://www.sciencedirect.com/science/article/pii/S0925231217302023. DOI: 10.1016/j.neucom.2016.09.117.
[32] V. Campos, B. Jou and X. Giro-i-Nieto, "From Pixels to Sentiment: Fine-tuning CNNs for Visual Sentiment Prediction," 2016. Available: https://arxiv.org/abs/1604.03489.
[33] N. Jain et al, "Hybrid deep neural networks for face emotion recognition," Pattern Recognition Letters, vol. 115, pp. 101-106, 2018. Available: https://www.sciencedirect.com/science/article/pii/S0167865518301302. DOI: 10.1016/j.patrec.2018.04.010.
[34] D. F. Dinges et al, "Optical computer recognition of facial expressions associated with stress induced by performance demands," Aviation, Space, and Environmental Medicine, vol. 76, (6 Suppl), pp. B172, 2005. Available: https://www.ncbi.nlm.nih.gov/pubmed/15943210.
[35] Y. Zhu et al, "Automated Depression Diagnosis Based on Deep Networks to Encode Facial Appearance and Dynamics," T-Affc, vol. 9, (4), pp. 578-584, 2018. Available: https://ieeexplore.ieee.org/document/7812588. DOI: 10.1109/TAFFC.2017.2650899.
[36] S. Alghowinem et al, "Multimodal Depression Detection: Fusion Analysis of Paralinguistic, Head Pose and Eye Gaze Behaviors," T-Affc, vol. 9, (4), pp. 478-490, 2018. Available: https://ieeexplore.ieee.org/document/7763752. DOI: 10.1109/TAFFC.2016.2634527.
[37] S. Acharya and S. Chellappan, IBM CRISP-DM : A Step-by-Step Guide. (1st ed.) Berkeley, CA: Apress L. P, 2016.
[38] Enrique González, "Desarrollo de Aplicaciones basadas en Sistemas MultiAgentes," 2006. 
[39] Ken Schwaber and Jeff Sutherland, "The scrum guide," in Software in 30 DaysAnonymous Hoboken, NJ, USA: John Wiley & Sons, Inc, 2012, pp. 133-152.
[40] V. Venkatesh and H. Bala, "Technology Acceptance Model 3 and a Research Agenda on Interventions," Decision Sciences, vol. 39, (2), pp. 273-315, 2008. Available: https://search.proquest.com/docview/198119893. DOI: 10.1111/j.1540-5915.2008.00192.x.
[41] K. Schindler, L. Van Gool and B. de Gelder, "Recognizing emotions expressed by body pose: A biologically inspired neural model," Neural Networks, vol. 21, (9), pp. 1238-1246, 2008. Available: https://www.sciencedirect.com/science/article/pii/S0893608008000944. DOI: 10.1016/j.neunet.2008.05.003.
[42] B. R. Steunebrink, "The logical structure of emotions," 2010. Available: https://www.openaire.eu/search/publication?articleId=narcis______::72fa20eaf2f70373b9f4223ed8789f52.
[43] SMRC, "Spanish Personal Health Questionnaire Depression Scale (PHQ-8)," 2012. 
[44] Calvo de Mora Martínez, Javier, Evaluación Educativa Y Social. 1991Available: http://catalog.hathitrust.org/Record/006161829.
[45] R. Pekrun et al, "Measuring emotions in students’ learning and performance: The Achievement Emotions Questionnaire (AEQ)," Contemporary Educational Psychology, vol. 36, (1), pp. 36-48, 2011. Available: https://www.sciencedirect.com/science/article/pii/S0361476X10000536. DOI: 10.1016/j.cedpsych.2010.10.002.
[46] C. M. JONKER, J. TREUR and W. C. A. WIJNGAARDS, "An agent-based architecture for multimodal interaction," International Journal of Human-Computer Studies, vol. 54, (3), pp. 351-405, 2001. Available: http://www.sciencedirect.com.ezproxy.javeriana.edu.co:2048/science/article/pii/S1071581900904506. DOI: //doi-org.ezproxy.javeriana.edu.co/10.1006/ijhc.2000.0450.
[47] Eder Mauricio Abello Rodríguez, "Identificación De Actividades Inusuales a Partir Del Uso De CCTV." , Pontificia Universidad Javeriana, 2018.
[48] Daniel Steven Valencia Parada, "Simulador Basado En Agentes Inteligentes Para El Apoyo a La Toma De Decisiones En Los Planes Operacionales De Negocios En Centros Comerciales." , Pontificia Universidad Javeriana, 2015.
[49] Javier Alcalá Vásquez, "Reconocimiento Multimodal Del Estado Emocional De Un Niño En Un Contexto Educativo." , Pontificia Universidad Javeriana, 2017.
[50] S. Manfredi, "Robust scalable stabilisability conditions for large-scale heterogeneous multi-agent systems with uncertain nonlinear interactions: towards a distributed computing architecture," International Journal of Control, vol. 89, (6), pp. 1203-1213, 2016. Available: http://www.tandfonline.com/doi/abs/10.1080/00207179.2015.1125023. DOI: 10.1080/00207179.2015.1125023.
[51] D. Mitrovic, M. Ivanović and Z. Geler, "Agent-Based Distributed Computing for Dynamic Networks," Information Technology and Control, vol. 43, (1), 2014. . DOI: 10.5755/j01.itc.43.1.4588.
