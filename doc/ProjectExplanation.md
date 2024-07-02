# Explicación del Proyecto
Un compilador es un programa, cuya entrada y salida resultan ser también programas. La entrada es un programa con lenguaje de alto nivel, mientras que la salida es un programa con un lenguaje de bajo nivel. 

Para poder hacer un compilador necesitamos pasar por 5 fases fundamentales:
- Análisis Lexicográfico o Lexer
- Análisis Sintáctico o Parser
- Análisis Semántico 
- Optimización 
- Generación

## Lexer
El análisis léxico se ocupa de evaluar las reglas del código fuente, que cada uno de los tokens introducidos sean conocidos. Para ello, cada uno de los tokens es introducido como una expresión regular y convertido a un autómata que detecta si un token coincide con una expresión regular. Al final, devuelve un flujo de tokens que los utiliza el analizador sintáctico o parser. 

Estos tokens no son más que una secuencia de caracteres que cumplen una cierta estructura sintáctica. Estos son símbolos terminales en la gramática que describe al código fuente. 

### Expresiones regulares
Las expresiones regulares son un poderoso instrumento utilizado en programación para describir patrones de texto. Estas patrones pueden ser utilizados para buscar, reemplazar o dividir cadenas de texto basándose en ciertos criterios. Las expresiones regulares se construyen utilizando varios operadores, como la unión, la concatenación (simplemente colocando caracteres uno después del otro), y la clausura de Kleene, que permite repetir un patrón cero o más veces. Cada expresión regular tiene un autómata finito asociado que representa su comportamiento

Las expresiones regulares permiten definir patrones que corresponden a los tokens, facilitando la identificación precisa de cada token en el código fuente. Además, las expresiones regulares son flexibles y potentes, permitiendo describir complejos patrones de texto. 

## Gramática y Parser
### Parser LR(1) 

### Construcción de la tabla 

### Gramática 
La gramática es la responsable de definir la estructura y las reglas de sintaxis del lenguaje de programación que el compilador va a traducir. La gramática es, sencillamente, el conjunto de reglas que definen cómo se pueden combinar las palabras y símbolos de un lenguaje para formar sentencias válidas. Esta estructura es esencial para el análisis sintáctico, una de las fases críticas en el proceso de compilación. 

Durante el análisis sintáctico, el compilador verifica si el código fuente proporcionado sigue las reglas gramaticales establecidas para el lenguaje de programación. Esto incluye verificar la correcta aparición de palabras clave, la estructura de las declaraciones, la coincidencia de paréntesis y corchetes, y otras reglas específicas del lenguaje. Si el código fuente no cumple con estas reglas, el compilador generará un error, indicando que el código no es sintácticamente correcto

La gramática también permite la generación de un árbol sintáctico, que es una representación jerárquica del programa fuente. Este árbol es fundamental para las capas posteriores que posee el compilador, como la optimización de código y la generación de código objetivo. El árbol sintáctico refleja la estructura gramatical del programa, permitiendo al compilador entender y manipular el código fuente de manera eficiente. 

La gramática ayuda a definir el alcance de variables, controlar el flujo de ejecución del programa a través de estructuras de control como bucles y condicionales, y manejar la declaración y uso de funciones. Todas estas características del lenguaje de programación deben ser capturadas y validadas por el compilador a través de su gramática

#### Gramática Libre de Contexto

#### Gramática Atributada

## Semantic Checker o Chequeo Semántico
El chequeo semántico es una etapa crítica en el proceso de compilación o interpretación de programas, enfocada en garantizar la corrección y coherencia de los tipos de datos utilizados dentro del código fuente. Este proceso asegura que todas las operaciones se realicen entre tipos de datos compatibles, que las variables y funciones se utilicen correctamente según sus definiciones, y que los tipos de datos especificados sean apropiados para cada operación o estructura de datos.

Al verificar la correcta aplicación de tipos de datos y la adecuada definición y uso de variables y funciones, este proceso ayuda a prevenir errores de tiempo de ejecución que podrían resultar en fallos del programa o comportamientos inesperados. El chequeo semántico contribuye a mejorar la legibilidad y mantenibilidad del código, al asegurar que las convenciones y restricciones del lenguaje de programación se sigan rigurosamente.

El chequeo semántico se realiza mediante el análisis del Árbol Sintáctico Abstracto (AST) generado durante la fase de análisis sintáctico. A medida que se recorre el AST, se realizan comprobaciones específicas para cada tipo de nodo, incluyendo pero no limitado a:

- *Operadores Binarios*: Verifica que los operandos sean compatibles con el operador aplicado.
- *Bloques de Código*: Asegura que todas las variables y funciones declaradas dentro del bloque estén definidas antes de su uso.
- *Accesos a Miembros de Clases*: Confirma que los objetos accedidos posean los atributos solicitados.
- *Declaraciones Condicionales*: Revisa que las condiciones y los cuerpos de las declaraciones condicionales sean compatibles en términos de tipos de datos.
- *Constantes*: Asegura que los valores asignados a las constantes sean del tipo esperado.
- *Asignaciones Destructivas*: Verifica que los tipos de datos de las variables asignadas sean compatibles con los valores recibidos.
- *Declaraciones de Funciones*: Comprueba que los tipos de parámetros y el valor de retorno sean consistentes con la definición de la función.
- *Invocaciones de Funciones*: Asegura que los argumentos pasados a las funciones sean compatibles con los tipos de parámetros esperados.
- *Declaraciones `let`*: Gestiona el alcance de las variables declaradas y verifica su uso adecuado.
- *Valores Nuevos*: Asegura que los tipos de datos de los nuevos valores sean compatibles con el contexto en el que se utilizan.
- *Parámetros*: Verifica que los tipos de datos de los parámetros sean compatibles con los tipos esperados por las funciones o métodos.
- *Declaraciones de Protocolos*: Asegura que las implementaciones de protocolos cumplan con las especificaciones definidas.
- *Declaraciones de Tipos*: Verifica que los tipos de datos declarados sean utilizados correctamente en el resto del código.
- *Operadores Unarios*: Comprueba que los operandos sean compatibles con el operador unario aplicado.
- *Valores de Variables*: Asegura que los valores asignados a las variables sean compatibles con sus tipos declarados.
### Patron visitor
El patrón Visitor, como una solución innovadora, permite implementar recorridos sobre el Árbol de Sintaxis Abstracta (AST) en el desarrollo de nuestro compilador. Este enfoque propuesto ofrece una alternativa a la práctica común de definir funciones explícitas dentro de la definición de los nodos del AST para tareas como la verificación de su semántica, y su evaluación

La aplicación del patrón Visitor en el desarrollo del compilador presenta múltiples ventajas:
- *Flexibilidad*: Permite la implementación de diferentes visitantes para distintos propósitos, como la generación de código intermedio, la optimización del código, y la verificación de la semántica del programa.
- *Modularidad*: Separa claramente la lógica de recorrido de la estructura del AST, haciendo que el código sea más fácil de entender y mantener.
- *Extensibilidad*: Facilita la adición de nuevos tipos de nodos o visitantes sin afectar el resto del sistema.

El patrón Visitor es particularmente útil en el contexto de fases incrementales de compilación. Al recorrer el AST con diferentes visitantes, el compilador puede acumular información semántica del programa de manera progresiva. Posteriormente, esta información puede ser utilizada para transformar el AST en formas cada vez más similares al lenguaje objetivo, optimizando así el proceso de compilación.
