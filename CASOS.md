# Casos
# R1 — Catálogo y precios

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Productos existentes en el catálogo: `"buzo"`, `"remera"` y `"campera"`. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Productos inexistentes o con el nombre mal escrito: `"gorra"`, `"BUZO"`, `"CAMpera"`, `"REmeRA"`, `""`, `None`. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Los tres productos existentes y sus precios exactos. |
| 2 | Productos inexistentes, cadenas vacías y valores nulos. |
| 3 | Precio enviado por el cliente diferente del precio del catálogo. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Producto existente. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 1}])`` | `Decimal("24999.90")` |
| Caso 2 | Producto existente. | ``calcular_subtotal([{"producto": "remera", "talle": "M", "cantidad": 1}])`` | `Decimal("11999.50")` |
| Caso 3 | Producto existente. | ``calcular_subtotal([{"producto": "campera", "talle": "M", "cantidad": 1}])`` | `Decimal("47999.99")` |
| Caso 4 | Producto inexistente. | ``calcular_subtotal([{"producto": "gorra", "talle": "M", "cantidad": 1}])`` | `CheckoutError` con código `PRODUCTO_INEXISTENTE`. |
| Caso 5 | Nombre de producto con mayúsculas. | ``calcular_subtotal([{"producto": "BUZO", "talle": "M", "cantidad": 1}])`` | `CheckoutError` con código `PRODUCTO_INEXISTENTE`. |
| Caso 6 | Precio propio enviado por el cliente. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 1, "precio": 1}])`` | `Decimal("24999.90")`. |

# R2 — Talles

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Talles admitidos: `"XS"`, `"S"`, `"M"`, `"L"`, `"XL"` y `"XXL"`. |
| 2 | Talles escritos con mayúsculas o minúsculas. |
| 3 | Talles con espacios al principio o al final. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Talles inexistentes: `"XXS"`, `"XXXL"`, `"talle"`. |
| 2 | Cadena vacía, valor `None` u otros valores que no representen un talle válido. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Todos los talles admitidos, incluidos los extremos `"XS"` y `"XXL"`. |
| 2 | Variantes de mayúsculas y minúsculas. |
| 3 | Talles con espacios exteriores. |
| 4 | Talles inmediatamente ajenos al conjunto permitido. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Talle válido. | ``calcular_subtotal([{"producto": "buzo", "talle": "XS", "cantidad": 1}])`` | `Decimal("24999.90")`. |
| Caso 2 | Talle válido con minúsculas y espacios. | ``calcular_subtotal([{"producto": "buzo", "talle": "  m ", "cantidad": 1}])`` | `Decimal("24999.90")`. |
| Caso 3 | Talle inválido. | ``calcular_subtotal([{"producto": "buzo", "talle": "XXS", "cantidad": 1}])`` | `CheckoutError` con código `TALLE_INVALIDO`. |
| Caso 4 | Talle vacío. | ``calcular_subtotal([{"producto": "buzo", "talle": "", "cantidad": 1}])`` | `CheckoutError` con código `TALLE_INVALIDO`. |

# R3 — Cantidad

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Números enteros comprendidos entre 1 y 10, ambos inclusive. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Enteros menores que 1 o mayores que 10. |
| 2 | Números con decimales, incluso si están dentro del intervalo permitido. |
| 3 | Valores que no sean enteros, como cadenas de texto o `None`. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Límites válidos: 1 y 10. |
| 2 | Límites inválidos cercanos: 0 y 11. |
| 3 | Cantidades no enteras próximas a los límites: 1.5 y 9.5. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Cantidad mínima válida. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 1}])`` | `Decimal("24999.90")`. |
| Caso 2 | Cantidad máxima válida. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 10}])`` | `Decimal("249999.00")`. |
| Caso 3 | Cantidad inferior al límite permitido. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 0}])`` | `CheckoutError` con código `CANTIDAD_INVALIDA`. |
| Caso 4 | Cantidad superior al límite permitido. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 11}])`` | `CheckoutError` con código `CANTIDAD_INVALIDA`. |
| Caso 5 | Cantidad decimal. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": 1.5}])`` | `CheckoutError` con código `CANTIDAD_INVALIDA`. |
| Caso 6 | Cantidad con tipo de dato incorrecto. | ``calcular_subtotal([{"producto": "buzo", "talle": "M", "cantidad": None}])`` | `CheckoutError` con código `CANTIDAD_INVALIDA`. |

# R4 — Carrito

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Carritos con uno o más ítems válidos. |
| 2 | Carritos con varios ítems válidos. |
| 3 | Ítems que contienen claves adicionales, que deben ignorarse. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Carrito vacío. |
| 2 | Carrito sin ítems. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Carrito con cero ítems. |
| 2 | Carrito con un solo ítem. |
| 3 | Carrito con varios ítems. |
| 4 | El carrito debe conservar su contenido después de ejecutar las funciones que lo reciben. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Carrito vacío. | ``calcular_subtotal([])`` | `CheckoutError` con código `CARRITO_VACIO`. |
| Caso 2 | Carrito con un ítem válido. | ``calcular_subtotal([{"producto": "remera", "talle": "M", "cantidad": 1}])`` | `Decimal("11999.50")`. |
| Caso 3 | Carrito con varios ítems válidos. | ``calcular_subtotal([{"producto": "remera", "talle": "M", "cantidad": 1}, {"producto": "buzo", "talle": "L", "cantidad": 1}])`` | `Decimal("36999.40")`. |
| Caso 4 | Ítem con una clave adicional. | ``calcular_subtotal([{"producto": "remera", "talle": "M", "cantidad": 1, "color": "azul"}])`` | `Decimal("11999.50")`. |

# R5 — Descuento por cantidad

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Carritos con menos de 5 prendas: no corresponde descuento por cantidad. |
| 2 | Carritos con 5 o más prendas: corresponde un descuento del 10% sobre el subtotal. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | No hay particiones inválidas específicas para esta regla, siempre que el carrito y sus ítems sean válidos. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | 4 prendas: no se aplica descuento. |
| 2 | 5 prendas: se aplica descuento del 10%. |
| 3 | 6 o más prendas: se aplica descuento del 10%. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Menos de 5 prendas. | ``calcular_descuento(Decimal("47999.80"), 4)`` | `Decimal("0.00")`. |
| Caso 2 | Exactamente 5 prendas. | ``calcular_descuento(Decimal("50000.00"), 5)`` | `Decimal("5000.00")`. |
| Caso 3 | Más de 5 prendas. | ``calcular_descuento(Decimal("60000.00"), 6)`` | `Decimal("6000.00")`. |

# R6 — Cupones

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Cupón `EGRESADOS2026` utilizado hasta el 30/11/2026 inclusive. |
| 2 | Cupón `BIENVENIDA` con un subtotal igual o superior a $20.000. |
| 3 | Cupones escritos con mayúsculas o minúsculas y espacios exteriores. |
| 4 | Ausencia de cupón mediante `None`, cadena vacía o texto formado únicamente por espacios. |
| 5 | Cupones válidos combinados con descuento por cantidad: se aplica el mayor de los dos descuentos, sin acumularlos. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Cupón inexistente. |
| 2 | Cupón `EGRESADOS2026` después del 30/11/2026. |
| 3 | Cupón `BIENVENIDA` con subtotal inferior a $20.000`. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Fecha de vigencia de `EGRESADOS2026`: 30/11/2026 y 01/12/2026. |
| 2 | Subtotal de `BIENVENIDA`: $19.999,99, $20.000,00, $20.000,01. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Cupón `EGRESADOS2026` vigente. | ``calcular_descuento(Decimal("11999.50"), 1, "EGRESADOS2026", date(2026, 11, 30))`` | `Decimal("1799.93")`. |
| Caso 2 | Cupón `EGRESADOS2026` vencido. | ``calcular_descuento(Decimal("11999.50"), 1, "EGRESADOS2026", date(2026, 12, 1))`` | `CheckoutError` con código `CUPON_VENCIDO`. |
| Caso 3 | Cupón `BIENVENIDA` con el mínimo alcanzado. | ``calcular_descuento(Decimal("20000.00"), 1, "BIENVENIDA", date(2026, 11, 20))`` | `Decimal("3000.00")`. |
| Caso 4 | Cupón `BIENVENIDA` por debajo del mínimo. | ``calcular_descuento(Decimal("19999.99"), 1, "BIENVENIDA", date(2026, 11, 20))`` | `CheckoutError` con código `CUPON_MINIMO_NO_ALCANZADO`. |
| Caso 5 | Cupón inexistente. | ``calcular_descuento(Decimal("25000.00"), 1, "DESCUENTO2026", date(2026, 11, 20))`` | `CheckoutError` con código `CUPON_INVALIDO`. |
| Caso 6 | Cupón con minúsculas y espacios. | ``calcular_descuento(Decimal("20000.00"), 1, "  bienvenida ", date(2026, 11, 20))`` | `Decimal("3000.00")`. |
| Caso 7 | Ausencia de cupón. | ``calcular_descuento(Decimal("25000.00"), 1, "   ", date(2026, 11, 20))`` | `Decimal("0.00")`. |
| Caso 8 | Comparación entre descuento por cantidad y cupón. | ``calcular_descuento(Decimal("100000.00"), 5, "BIENVENIDA", date(2026, 11, 20))`` | `Decimal("10000.00")`, porque el 10% por cantidad supera los $3.000 del cupón. |
| Caso 9 | Descuento limitado al subtotal. | ``calcular_descuento(Decimal("1000.00"), 1, None, date(2026, 11, 20))`` | `Decimal("0.00")`. El descuento no puede superar el subtotal. |

# R7 — Dinero y redondeo

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Importes representados mediante `Decimal`. |
| 2 | Descuentos porcentuales que producen importes con dos decimales exactos. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Utilizar `float` para manejar importes contradice el contrato de la especificación. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Resultados que terminan exactamente en medio centavo. |
| 2 | Resultados con más de dos decimales. |
| 3 | Conservación del valor monetario con dos decimales. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Descuento porcentual con redondeo. | ``calcular_descuento(Decimal("11999.50"), 1, "EGRESADOS2026", date(2026, 11, 30))`` | `Decimal("1799.93")` |
| Caso 2 | Descuento porcentual con resultado exacto. | ``calcular_descuento(Decimal("20000.00"), 5, None, date(2026, 11, 20))`` | `Decimal("2000.00")`. |
| Caso 3 | Importe decimal exacto. | ``calcular_subtotal([{"producto": "remera", "talle": "M", "cantidad": 1}])`` | `Decimal("11999.50")` |

# R8 — Envío

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Zonas admitidas: `CABA`, `GBA`, `INTERIOR` y `RETIRO`. |
| 2 | Zonas escritas con mayúsculas o minúsculas y espacios exteriores. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Zonas inexistentes, como `"LA PLATA"`, `""`, `None` o `"OTRA"`: `ZONA_INVALIDA`. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Subtotal con descuento de $59.999,99. |
| 2 | Subtotal con descuento de $60.000,00. |
| 3 | Subtotal con descuento superior a $60.000. |
| 4 | Costos de envío de las cuatro zonas. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Zona `CABA`, subtotal límite con costo de envío. | ``calcular_envio(Decimal("59999.99"), "CABA")`` | `Decimal("2500.00")`. |
| Caso 4 | Zona `RETIRO`subtotal sin costo de envío. | ``calcular_envio(Decimal("50000.00"), "RETIRO")`` | `Decimal("0.00")`. |
| Caso 5 | Zona `CABA`, subtotal límite sin costo de envío. | ``calcular_envio(Decimal("60000.00"), "CABA")`` | `Decimal("0.00")`. |
| Caso 6 | Zona `CABA`, subtotal con costo de envío. | ``calcular_envio(Decimal("65000.00"), "GBA")`` | `Decimal("0.00")`. |
| Caso 7 | Zona normalizada. | ``calcular_envio(Decimal("50000.00"), "  gba ")`` | `Decimal("4000.00")`. |
| Caso 8 | Zona inválida. | ``calcular_envio(Decimal("50000.00"), "LA PLATA")`` | `CheckoutError` con código `ZONA_INVALIDA`. |

# R9 — Total

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Compras con total calculado como subtotal − descuento + envío |
| 2 | Compras con descuento igual a cero. |
| 3 | Compras con descuento por cantidad. |
| 4 | Compras con descuento por cupón. |
| 5 | Compras con envío con costo. |
| 6 | Compras con envío gratis. |
| 7 | Compras con retiro en el colegio. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Compras con total calculado de menera diferente |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Descuento igual a cero. |
| 2 | Subtotal después del descuento igual a $60.000, que hace gratuito el envío. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Compra sin descuento y con envío pago. | ``calcular_total([{"producto": "buzo", "talle": "M", "cantidad": 2}], "CABA")`` | <br>`subtotal`: `Decimal("49999.80")`<br>`descuento`: `Decimal("0.00")`<br>`envio`: `Decimal("2500.00")`<br>`total`: `Decimal("52499.80")` |
| Caso 2 | Compra con descuento por cupón. | ``calcular_total([{"producto": "remera", "talle": "M", "cantidad": 1}], "CABA", "EGRESADOS2026", date(2026, 11, 30))`` | <br>`subtotal`: `Decimal("11999.50")`<br>`descuento`: `Decimal("1799.93")`<br>`envio`: `Decimal("2500.00")`<br>`total`: `Decimal("12699.57")` |
| Caso 3 | Compra con envío gratis. | ``calcular_total([{"producto": "buzo", "talle": "M", "cantidad": 3}], "CABA")`` | <br>`subtotal`: `Decimal("74999.70")`<br>`descuento`: `Decimal("7499.97")`<br>`envio`: `Decimal("0.00")`<br>`total`: `Decimal("67499.73")` |
| Caso 4 | Compra con error de zona. | ``calcular_total([{"producto": "buzo", "talle": "M", "cantidad": 1}], "LA PLATA")`` | `CheckoutError` con código `ZONA_INVALIDA`. |

# R10 — Persistencia

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | Guardar un pedido válido y recuperar sus datos. |
| 2 | Guardar un pedido y consultarlo desde otra conexión a la misma base de datos. |
| 3 | Recuperar importes idénticos a los calculados por checkout, conservando el tipo `Decimal`. |
| 4 | Guardar el precio unitario obtenido del catálogo. |
| 5 | Normalizar el email a minúsculas y sin espacios exteriores. |
| 6 | Normalizar zona, talle y cupón a mayúsculas y sin espacios exteriores. |
| 7 | Guardar un cupón vacío como `None`. |
| 8 | Consultar los pedidos de un email sin distinguir mayúsculas ni espacios y en orden del más reciente al más antiguo. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Guardar un pedido cuyo carrito o cuyos datos produzcan un `CheckoutError`. |
| 2 | Consultar un identificador de pedido inexistente: debe devolver `None`. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Pedido válido frente a pedido inválido. |
| 2 | Pedido visible desde una conexión diferente. |
| 3 | Identificador existente frente a identificador inexistente. |
| 4 | Email con mayúsculas y espacios exteriores. |
| 5 | Cupón vacío frente a cupón informado. |
| 6 | Dos o más pedidos para verificar el orden cronológico inverso. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Guardado y recuperación de un pedido válido. | `Guardar un pedido con email `"ana@mail.com"`, zona `"CABA"` y carrito `[{"producto": "remera", "talle": "M", "cantidad": 1}]`, sin cupón.` | Se obtiene un identificador y `obtener_pedido(con, id)` devuelve el pedido con subtotal `Decimal("11999.50")`, descuento `Decimal("0.00")`, envío `Decimal("2500.00")` y total `Decimal("14499.50")`. |
| Caso 2 | Persistencia entre conexiones. | `Guardar un pedido en una conexión y consultarlo mediante otra conexión a la misma base de datos.` | La segunda conexión recupera el pedido completo, incluidos todos sus ítems. |
| Caso 3 | Pedido con datos inválidos. | `Intentar guardar un pedido cuyo carrito contiene un producto inexistente.` | Se propaga `CheckoutError` con código `PRODUCTO_INEXISTENTE` y no queda guardado ni el pedido ni ninguno de sus ítems. |
| Caso 4 | Normalización de datos. | `Guardar un pedido con email `" Ana@Mail.com "`, zona `" caba "`, talle `" m "` y cupón `" egresados2026 "`, utilizando una fecha válida.` | El pedido recuperado contiene email `"ana@mail.com"`, zona `"CABA"`, talle `"M"` y cupón `"EGRESADOS2026"`. |
| Caso 5 | Cupón vacío. | `Guardar un pedido con cupón `"   "`.` | El pedido recuperado tiene el campo `cupon` igual a `None`. |
| Caso 6 | Precio unitario del catálogo. | `Guardar un pedido con un buzo cuyo ítem enviado incluye además `"precio": 1`.` | El `precio_unitario` recuperado es `Decimal("24999.90")`, no el precio enviado por el cliente. |
| Caso 7 | Identificador inexistente. | ``obtener_pedido(con, 999999)`, suponiendo que ese identificador no existe.` | `None`. |
| Caso 8 | Orden de los pedidos. | `Guardar dos pedidos para `"ana@mail.com"` y ejecutar `pedidos_de(con, " ANA@MAIL.COM ")`.` | Se devuelven ambos pedidos, primero el más reciente y después el más antiguo. |

# R11 — API HTTP

## Particiones válidas

| Elemento | Descripción |
|---|---|
| 1 | `POST /api/v1/pedidos` con JSON válido y todos los datos obligatorios. |
| 2 | `POST /api/v1/pedidos` con cupón y fecha opcionales omitidos. |
| 3 | `GET /api/v1/pedidos/{id}` con un identificador existente. |
| 4 | Respuestas exitosas con los importes representados como texto en JSON. |

## Particiones inválidas

| Elemento | Descripción |
|---|---|
| 1 | Cuerpo que no es JSON válido. |
| 2 | Falta email, zona o carrito, o alguno tiene un tipo incorrecto. |
| 3 | Fecha con formato incorrecto. |
| 4 | Error de negocio producido por `CheckoutError`. |
| 5 | Identificador de pedido inexistente. |
| 6 | Ruta inexistente. |
| 7 | Respuestas con estado `500`. |

## Valores límite

| Elemento | Descripción |
|---|---|
| 1 | Fecha válida en formato `AAAA-MM-DD` frente a fecha con formato incorrecto. |
| 2 | Campos obligatorios presentes frente a ausentes. |
| 3 | Identificador de pedido existente frente a inexistente. |
| 4 | Importes representados como cadenas frente a números JSON. |
| 5 | Puerto automático al crear el servidor con `puerto=0`. |
| 6 | La base de datos debe utilizar un archivo, no `":memory:"`. |

## Casos

| Caso | Partición | Entrada | Salida esperada |
|---|---|---|---|
| Caso 1 | Creación de pedido válida. | `Enviar un `POST /api/v1/pedidos` con el cuerpo:` | Estado `201 Created` y respuesta con `id` y los importes como texto:<br>`"subtotal": "11999.50"`<br>`"descuento": "1799.93"`<br>`"envio": "2500.00"`<br>`"total": "12699.57"` |
| Caso 2 | Creación de pedido sin campos opcionales. | `Enviar un `POST /api/v1/pedidos` con el cuerpo:` | Estado `201 Created`, con los importes calculados sin cupón y la fecha determinada por el comportamiento predeterminado de checkout. |
| Caso 3 | Cuerpo JSON inválido. | `Enviar un `POST /api/v1/pedidos` con un cuerpo que no sea JSON válido, por ejemplo `{"email":`.` | Estado `400` y respuesta con código `JSON_INVALIDO`. |
| Caso 4 | Falta un campo obligatorio. | `Enviar un `POST /api/v1/pedidos` con el cuerpo:` | Estado `400` y respuesta con código `DATOS_INCOMPLETOS`. |
| Caso 5 | Fecha con formato incorrecto. | `Enviar un `POST /api/v1/pedidos` con todos los campos obligatorios válidos y `"fecha":"30-11-2026"`.` | Estado `400` y respuesta con código `FECHA_INVALIDA`. |
| Caso 6 | Error de negocio. | `Enviar un `POST /api/v1/pedidos` con un carrito que contenga `{"producto":"gorra","talle":"M","cantidad":1}` y el resto de los datos obligatorios válidos.` | Estado `422` y respuesta con código `PRODUCTO_INEXISTENTE`. |
| Caso 7 | Recuperación de pedido existente. | `Enviar un `GET /api/v1/pedidos/{id}` con el identificador de un pedido existente.` | El pedido completo con sus ítems y los importes representados como texto en JSON. |
| Caso 8 | Recuperación de pedido inexistente. | `Enviar un `GET /api/v1/pedidos/999999`, suponiendo que ese pedido no existe.` | Estado `404` y respuesta con código `PEDIDO_INEXISTENTE`. |
| Caso 9 | Ruta inexistente. | `Enviar una solicitud a una ruta no definida, por ejemplo `GET /ruta-inexistente`.` | Estado `404` y respuesta con código `RUTA_INEXISTENTE`. |
| Caso 10 | Creación del servidor con puerto automático. | ``crear_servidor("pedidos_test.db", puerto=0)`.` | Se obtiene un servidor sin arrancar, con un puerto libre consultable mediante `servidor.server_address[1]`. |
| Caso 11 | Base de datos en memoria. | ``crear_servidor(":memory:")`.` | Esta configuración no cumple el contrato de la especificación. El sistema de API y los tests que necesitan conexiones independientes deben utilizar una ruta de archivo. |
| Caso 12 | Ausencia de errores HTTP 500. | `Ejecutar solicitudes que produzcan los errores contemplados en las particiones inválidas anteriores.` | Cada solicitud devuelve el estado y el código de error que le corresponden; ninguna devuelve `500`. |
