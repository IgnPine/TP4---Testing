# Auditoria

## Sección 1

| Test | Clasificación | Justificación |
|---|---|---|
| `test_subtotal` | **Tautológico** | Realiza el mismo cálculo que la función que testea, tomando los valores del CATALOGO, lo que deja pasar un precio mal cargado en el catálogo. |
| `test_total_funciona` | **Inútil** | Solo verifica que `calcular_total` devuelve algo distinto de `None`, lo que deja pasar cualquier error de cálculo |
| `test_total_positivo` | **Débil** | Verifica que el total de una campera a GBA es `> 0`, lo que deja pasar cualquier tipo de error de cálculo. |
| `test_cupon_egresados` | **Débil** | Verifica que se aplique el descuento del cupón, pero no contempla la fecha actual y la fecha de vencimiento del cupón. |
| `test_envio_caba` | **Débil** | Verifica que se calcula correctamente el envío desde CABA, pero no contempla el subtotal que determina si tendrá costo de envío. |
| `test_descuento_por_cantidad` | **Débil** | Verifica que se aplique el descuento por cantidad, pero no emplea ningún caso extremo. |
| `test_talle_valido` | **Débil** | Utiliza la función validar_item(), pero si la función no funciona correctamente, el test tampoco. |
| `test_no_explota_con_varios_productos` | **Inútil** | No valida nada útil, nunca se rompe, y no hay un manejo correcto de los errores. |

### Mutar

Mutantes generados : 29
Muertos            : 17
Sobrevivientes     : 12
Puntaje de mutación: 58.6%

Esta suite cubre casi el 80% del código, pero aún así no detecta ninguna falla porque los test no están bien implementados con los casos extremos apropiados, por lo que no detectan ningún error, aún habiendo fallas que provoquen que el código con siga los requerimientos establecidos. 

## Sección 2

### Resultado de `ruff check checkout.py`

## H-01 · Cupón oculto `DEBUG100` con 100% de descuento

- **Ubicación:** checkout.py, línea 23
- **Categoría:** seguridad
- **Regla violada:** R6 ("Estos son los únicos dos cupones que existen")
- **Qué pasa:** el diccionario `CUPONES` incluye `DEBUG100`, un cupón de 100% válido hasta 2099. Cualquiera que lo escriba paga solo el envío, o nada si la compra supera $ 60.000.
- **Cómo la encontré:** lectura de la spec (R6 lista solo dos cupones) contra el diccionario `CUPONES`

## H-02 · Inyección SQL en `pedidos_de`

- **Ubicación:** pedidos.py, líneas 106–108
- **Categoría:** seguridad
- **Regla violada:** R10 ("ningún valor puede alterar la consulta a la base")
- **Qué pasa:** el email se interpola con un f-string dentro del SQL. `pedidos_de(con, "' OR '1'='1")` devuelve los pedidos de todos los clientes. Un email con una comilla simple rompe la consulta con `OperationalError`.
- **Cómo la encontré:** lectura del código (f-string en `con.execute`) contra el último punto de R10

## H-03 · `calcular_subtotal` acepta el precio que manda el cliente

- **Ubicación:** checkout.py, línea 49
- **Categoría:** seguridad
- **Regla violada:** R1 ("El precio sale siempre del catálogo. Si el ítem trae un precio propio, se ignora")
- **Qué pasa:** `item.get("precio", CATALOGO[...])` usa el `precio` del ítem si existe. `{"producto": "buzo", "talle": "M", "cantidad": 1, "precio": 1}` da subtotal 1 en vez de 24.999,90.
- **Cómo la encontré:** lectura de la spec (R1) contra el `item.get("precio", …)`

## H-04 · `guardar_pedido` guarda como `precio_unitario` el precio del cliente

- **Ubicación:** pedidos.py, línea 64
- **Categoría:** seguridad
- **Regla violada:** R10 ("`precio_unitario` es el precio del catálogo, nunca uno enviado por el cliente") y R1
- **Qué pasa:** es el mismo patrón que H-03. Un ítem con `"precio": 1` queda guardado con `precio_unitario = 1` y el detalle del pedido no coincide con el catálogo.
- **Cómo la encontré:** lectura de R10 contra el `item.get("precio", …)`

## H-05 · El pedido se confirma en la base antes de calcular el total

- **Ubicación:** pedidos.py, líneas 39–50
- **Categoría:** manejo de errores
- **Regla violada:** R10 ("Si `calcular_total` lanza `CheckoutError`, el error se propaga y no queda nada guardado")
- **Qué pasa:** `guardar_pedido` hace el `INSERT` y el `commit()` (línea 48) antes de llamar a `calcular_total` (línea 50). Si el carrito es inválido (talle, cupón, zona…), el error se propaga pero la fila ya está confirmada en `pedidos`, con importes en 0 y sin ítems.
- **Cómo la encontré:** lectura del orden de las operaciones en `guardar_pedido` contra R10

## H-06 · Importes e ítems nunca se confirman (falta el `commit` final)

- **Ubicación:** pedidos.py, líneas 52–71 (el único `commit` está en la línea 48)
- **Categoría:** lógica y límites
- **Regla violada:** R10 ("Cuando `guardar_pedido` termina, el pedido es definitivo: cualquier otra conexión lo ve completo, con todos sus ítems")
- **Qué pasa:** el `UPDATE` de los importes y los `INSERT` de `items` quedan en una transacción abierta. Al hacer `con.close()` sin `commit`, SQLite los descarta. Por la API, el `POST` responde 201 con los totales (se leen desde la misma conexión), pero un `GET` posterior devuelve importes en 0 y `items: []`.
- **Cómo la encontré:** lectura de `guardar_pedido` (un solo `commit`, antes de los cambios) contra R10

## H-07 · Los errores de negocio devuelven 500, con un formato que no es el de la spec

- **Ubicación:** api.py, líneas 53–54 (y 67–68 en `do_GET`)
- **Categoría:** manejo de errores
- **Regla violada:** R11 (cualquier `CheckoutError` → 422 con su `code`; "Todos los errores tienen el mismo formato"; "Un error nunca puede devolver 500")
- **Qué pasa:** `except Exception` captura todo, incluso `CheckoutError`, y responde 500 con `{"error": str(e)}`. Un talle inválido, un cupón vencido o una zona inexistente nunca llegan al frontend como 422 con su `code`. Además el cuerpo no tiene `code` ni `message`, y `str(e)` expone textos internos.
- **Cómo la encontré:** lectura de la tabla de errores de R11 contra el único `except` del `do_POST`

## H-08 · La fecha viaja como texto y nunca se convierte a `date`

- **Ubicación:** api.py, línea 41
- **Categoría:** fechas
- **Regla violada:** R11 (la fecha viaja como texto `AAAA-MM-DD`; formato inválido → 400 `FECHA_INVALIDA`) y firma de `calcular_total` (`fecha: date | None`)
- **Qué pasa:** `datos.get("fecha")` pasa el string tal cual a `checkout`, que compara `fecha < date(...)`. Con `EGRESADOS2026` y `"fecha": "2026-11-30"` ocurre un `TypeError` y la API responde 500. `FECHA_INVALIDA` nunca se genera.
- **Cómo la encontré:** lectura de R11 contra el flujo `api.py` → `pedidos.py` → `checkout.py`. Es una falla en el paso de información entre capas: la API no convierte el tipo que `checkout` espera.

## H-09 · Un producto inexistente se ignora en silencio

- **Ubicación:** checkout.py, líneas 34–41 (`validar_item` no valida el producto) y 48–51 (`except:` con `continue`)
- **Categoría:** manejo de errores
- **Regla violada:** R1 (producto inexistente → `PRODUCTO_INEXISTENTE`) y sección 3 (orden producto → talle → cantidad)
- **Qué pasa:** `calcular_subtotal([{"producto": "gorra", "talle": "M", "cantidad": 1}])` no falla: el `KeyError` lo traga el `except:` y el ítem se saltea, con subtotal 0. Además, un ítem con producto y talle inválidos informa `TALLE_INVALIDO` en vez de `PRODUCTO_INEXISTENTE`.
- **Cómo la encontré:** ruff E722 (línea 50) y lectura de R1 y de la sección 3

## H-10 · El cupón se acumula con el descuento por cantidad

- **Ubicación:** checkout.py, líneas 61, 74 y 82 (`descuento +=` en los tres casos)
- **Categoría:** lógica y límites
- **Regla violada:** R6 ("El cupón no se acumula con el descuento por cantidad (R5). Se calculan los dos y se aplica el mayor")
- **Qué pasa:** el código suma ambos descuentos. Con 6 prendas y `EGRESADOS2026` aplica 10% + 15% = 25%, y debería aplicar solo 15%. Con `BIENVENIDA` suma $ 3.000 al 10%, en vez de elegir el mayor de los dos.
- **Cómo la encontré:** lectura de R6 contra el uso de `+=`

## H-11 · El envío gratis se evalúa sobre el subtotal sin descuento

- **Ubicación:** checkout.py, línea 110 (se pasa `subtotal` a `calcular_envio`) y línea 96 (comparación `>= 60000`)
- **Categoría:** lógica y límites
- **Regla violada:** R8 ("El envío es gratis si el subtotal ya con el descuento aplicado es de $ 60.000 o más") y firma `calcular_envio(subtotal_con_descuento, zona)`
- **Qué pasa:** con 2 buzos y 1 remera el subtotal es $ 61.999,30. Con `EGRESADOS2026` el descuento es $ 9.299,90 y el subtotal con descuento queda en $ 52.699,40. El envío a CABA debería costar $ 2.500, pero el código lo da gratis porque recibe el subtotal sin descuento.
- **Cómo la encontré:** lectura de R8 contra el argumento que pasa `calcular_total`

## H-12 · Los importes de `checkout.py` son `float` o `int`, no `Decimal`

- **Ubicación:** checkout.py, líneas 12–16 (catálogo), 20–24 (cupones), 26–31 (envíos), 54, 84 y 117 (`round`)
- **Categoría:** numéricos
- **Regla violada:** R7 ("Todos los importes se manejan como `Decimal`. Nunca `float`") y contrato de la sección 1 (devuelven `Decimal`)
- **Qué pasa:** `calcular_subtotal([buzo M ×1])` devuelve `24999.9`, un `float` cuyo valor real es `24999.900000000001455…`. El resultado mezcla tipos: `subtotal` y `total` son `float`, y `envio` es `int` (`2500` o `0`). El ejemplo de la sección 5 da `{"subtotal": 49999.8, "envio": 2500, …}`.
- **Cómo la encontré:** lectura de la spec (R7 dice "nunca float") contra los literales del catálogo

## H-13 · Los montos se guardan como `REAL` y pierden exactitud

- **Ubicación:** pedidos.py, líneas 12–15 y 23 (esquema `REAL`), 55–58 y 68 (`float(...)`), 88–91 y 97 (`Decimal(float)`)
- **Categoría:** numéricos
- **Regla violada:** R10 ("Los montos que devuelve `obtener_pedido` son idénticos a los que calculó `checkout`: `Decimal`, mismo valor, sin ninguna pérdida")
- **Qué pasa:** se convierte a `float` al guardar y se vuelve a `Decimal` desde un `float` al leer. `Decimal(24999.9)` da `24999.900000000001455…` y no `Decimal("24999.90")`, así que los importes leídos no son iguales a los calculados.
- **Cómo la encontré:** lectura de R10 contra el tipo de columna y las conversiones

## H-14 · Los montos viajan como números JSON y no como texto

- **Ubicación:** api.py, línea 18 (`json.dumps(cuerpo, default=float)`)
- **Categoría:** numéricos
- **Regla violada:** R11 ("Los montos viajan siempre como texto (`"1799.93"`), nunca como número JSON")
- **Qué pasa:** `default=float` convierte cada `Decimal` en número. La respuesta trae `"total": 12699.57` en lugar de `"12699.57"`, y `49999.80` se serializa como `49999.8`. Afecta al `POST` y al `GET`.
- **Cómo la encontré:** lectura del ejemplo de respuesta de R11 contra `_responder`

## H-15 · El redondeo no es comercial

- **Ubicación:** checkout.py, líneas 54, 84 y 117
- **Categoría:** numéricos
- **Regla violada:** R7 ("el medio centavo redondea hacia arriba")
- **Qué pasa:** `round()` sobre `float` redondea según el valor binario y, en empates exactos, al par más cercano. No es `ROUND_HALF_UP`. El ejemplo de la spec (15% de $ 11.999,50 = $ 1.799,925 → $ 1.799,93) puede dar $ 1.799,92.
- **Cómo la encontré:** lectura de R7 y de su ejemplo contra el uso de `round(x, 2)`

## H-16 · `fecha=None` rompe con `TypeError` al usar `EGRESADOS2026`

- **Ubicación:** checkout.py, línea 72 (llamada desde pedidos.py línea 50 y api.py línea 41)
- **Categoría:** fechas
- **Regla violada:** R6 (sin fecha se usa el día de hoy), firma (`fecha: date | None`) y sección 1 ("Nunca otro tipo de excepción")
- **Qué pasa:** `guardar_pedido` y la API pasan `fecha=None` explícito cuando no hay fecha, y eso pisa el valor por defecto. `None < date(...)` lanza `TypeError`. Todo pedido con `EGRESADOS2026` y sin fecha falla.
- **Cómo la encontré:** seguimiento del valor de `fecha` a través de las tres capas

## H-17 · `date.today()` como valor por defecto, evaluado una sola vez al importar

- **Ubicación:** checkout.py, líneas 57 y 102
- **Categoría:** fechas
- **Regla violada:** R6 ("Si no se recibe `fecha`, se usa la fecha del día en que se hace la llamada")
- **Qué pasa:** el valor por defecto se calcula al importar el módulo. En un servidor que lleva días corriendo, "hoy" queda congelado en la fecha de arranque, y `EGRESADOS2026` seguiría aceptándose después del 30/11 si el servidor arrancó antes.
- **Cómo la encontré:** ruff B008 (líneas 57 y 102)

## H-18 · Método inexistente en el mensaje de zona inválida

- **Ubicación:** checkout.py, línea 93
- **Categoría:** alucinación
- **Regla violada:** R8 (zona que no existe → `ZONA_INVALIDA`) y sección 1 ("Nunca otro tipo de excepción")
- **Qué pasa:** `ENVIOS.keys().join(', ')` no existe en Python: `join` es un método de `str`, no de `dict_keys`. Toda zona inválida lanza `AttributeError` y nunca `ZONA_INVALIDA`.
- **Cómo la encontré:** lectura de la ruta de error de `calcular_envio`

## H-19 · `EGRESADOS2026` vence un día antes: el 30/11/2026 ya figura vencido

- **Ubicación:** checkout.py, línea 72
- **Categoría:** fechas
- **Regla violada:** R6 ("Válido hasta el 30/11/2026 inclusive")
- **Qué pasa:** `if not fecha < datos["vence"]` lanza `CUPON_VENCIDO` cuando `fecha >= vence`. El 30/11/2026 debería ser válido y recién el 01/12 el cupón está vencido.
- **Cómo la encontré:** análisis de valores límite de R6 (29/11, 30/11, 01/12)

## H-20 · La cantidad 10 se rechaza

- **Ubicación:** checkout.py, línea 40
- **Categoría:** lógica y límites
- **Regla violada:** R3 (entero entre 1 y 10, ambos inclusive)
- **Qué pasa:** la condición `1 <= item["cantidad"] < 10` deja afuera el 10. `cantidad = 10` lanza `CANTIDAD_INVALIDA` y debería ser válida.
- **Cómo la encontré:** análisis de valores límite de R3 contra el operador `<`

## H-21 · El descuento por cantidad empieza en 6 prendas, no en 5

- **Ubicación:** checkout.py, línea 60
- **Categoría:** lógica y límites
- **Regla violada:** R5 ("5 o más")
- **Qué pasa:** `cantidad_prendas > 5` deja sin descuento a un carrito de exactamente 5 prendas. Con 5 remeras ($ 59.997,50) debería descontarse $ 5.999,75.
- **Cómo la encontré:** análisis de valores límite de R5 contra el operador `>`

## H-22 · No se valida el carrito vacío

- **Ubicación:** checkout.py, líneas 44–54 (`calcular_subtotal`) y 102–111 (`calcular_total`)
- **Categoría:** lógica y límites
- **Regla violada:** R4 (carrito sin ítems → `CARRITO_VACIO`) y sección 3 (primer chequeo)
- **Qué pasa:** `calcular_total([], "CABA")` devuelve subtotal 0 y total 2500 (solo el envío) en lugar de lanzar `CARRITO_VACIO`. Ese `code` no existe en ningún punto del código.
- **Cómo la encontré:** búsqueda en el código de cada código de error de la sección 4 de la spec

## H-23 · `validar_item` modifica el carrito que recibe

- **Ubicación:** checkout.py, línea 35
- **Categoría:** efectos laterales
- **Regla violada:** R4 ("Ninguna función modifica el carrito que recibe")
- **Qué pasa:** `item["talle"] = item["talle"].upper()` escribe sobre el diccionario del llamador. Tras `calcular_total(carrito, …)`, un `"m"` pasó a `"M"` en el carrito del frontend.
- **Cómo la encontré:** lectura de R4 contra la asignación a `item[...]`

## H-24 · La cantidad acepta decimales y booleanos

- **Ubicación:** checkout.py, línea 40
- **Categoría:** tipos
- **Regla violada:** R3 ("Cualquier otro valor, incluidos los no enteros → `CANTIDAD_INVALIDA`")
- **Qué pasa:** `1 <= 2.5 < 10` es verdadero, así que `cantidad = 2.5` pasa la validación y llega al subtotal. `True` también pasa, porque `bool` es subclase de `int`. Un string como `"2"` lanza `TypeError` en lugar de `CANTIDAD_INVALIDA`.
- **Cómo la encontré:** análisis de particiones inválidas de R3 (decimal, bool, texto)

## H-25 · El talle no ignora espacios al principio y al final

- **Ubicación:** checkout.py, línea 35
- **Categoría:** strings
- **Regla violada:** R2 ("`"  M "` es válido")
- **Qué pasa:** solo se aplica `.upper()`, sin `.strip()`. `"  M "` no está en `TALLES` y lanza `TALLE_INVALIDO`.
- **Cómo la encontré:** lectura de R2 y su ejemplo contra la normalización del talle

## H-26 · El cupón distingue mayúsculas de minúsculas

- **Ubicación:** checkout.py, líneas 64–66
- **Categoría:** strings
- **Regla violada:** R6 ("No se distingue mayúscula de minúscula y se ignoran los espacios alrededor")
- **Qué pasa:** se hace `strip()` pero no `upper()`. `"egresados2026"` o `"Bienvenida"` lanzan `CUPON_INVALIDO`.
- **Cómo la encontré:** lectura de R6 contra la normalización del código

## H-27 · Un cupón vacío o con solo espacios se trata como cupón inválido

- **Ubicación:** checkout.py, líneas 63–66
- **Categoría:** strings
- **Regla violada:** R6 (`None`, `""` o solo espacios equivalen a no usar cupón, no es un error)
- **Qué pasa:** solo `None` se trata como "sin cupón". `""` y `"   "` entran al bloque, quedan como `""`, no están en `CUPONES` y lanzan `CUPON_INVALIDO`.
- **Cómo la encontré:** partición de entradas de cupón (`None`, `""`, `"  "`) contra la condición `cupon != None`

## H-28 · Un JSON inválido devuelve 500 en lugar de 400 `JSON_INVALIDO`

- **Ubicación:** api.py, líneas 31–32
- **Categoría:** manejo de errores
- **Regla violada:** R11 (cuerpo que no es JSON válido → 400 `JSON_INVALIDO`)
- **Qué pasa:** `json.loads(...)` lanza `JSONDecodeError` con un cuerpo roto, y el `except Exception` lo convierte en 500.
- **Cómo la encontré:** lectura de la tabla de errores de R11 contra el flujo de `do_POST`

## H-29 · Faltan campos o tienen tipo incorrecto: 500 en lugar de 400 `DATOS_INCOMPLETOS`

- **Ubicación:** api.py, líneas 37–39
- **Categoría:** manejo de errores
- **Regla violada:** R11 (falta email, zona o carrito, o tienen otro tipo → 400 `DATOS_INCOMPLETOS`)
- **Qué pasa:** `datos["email"]`, `datos["carrito"]` y `datos["zona"]` lanzan `KeyError` si faltan. Si el email o la zona no son string, `.strip()` lanza `AttributeError` en `pedidos.py`. Todo termina en 500.
- **Cómo la encontré:** lectura de R11 y de los accesos directos `datos[...]`

## H-30 · `GET` de un pedido inexistente devuelve 200 con `null`

- **Ubicación:** api.py, líneas 64–66
- **Categoría:** lógica y límites
- **Regla violada:** R11 (el pedido no existe → 404 `PEDIDO_INEXISTENTE`)
- **Qué pasa:** `obtener_pedido` devuelve `None` (R10) y el código lo responde con `_responder(200, None)`, es decir, `200 null`. Nunca se genera el 404 `PEDIDO_INEXISTENTE`.
- **Cómo la encontré:** lectura de R10 (`None` si no existe) contra R11 (404)

## H-31 · Code smell: import sin usar y comparación con `None`

- **Ubicación:** checkout.py, línea 1 (`import json`) y línea 63 (`!= None`)
- **Categoría:** code smell
- **Regla violada:** ninguna regla de negocio (mantenibilidad)
- **Qué pasa:** `json` no se usa en ningún punto del módulo. `!= None` debería ser `is not None`.
- **Cómo la encontré:** ruff F401 (línea 1) y E711 (línea 63)

---

## Tabla resumen (de la más grave a la menos grave)

| ID | Archivo y línea | Categoría | Regla incumplida | Severidad |
| --- | --- | --- | --- | --- |
| H-01 | checkout.py:23 | seguridad | R6 | Alta |
| H-02 | pedidos.py:106–108 | seguridad | R10 | Alta |
| H-03 | checkout.py:49 | seguridad | R1 | Alta |
| H-04 | pedidos.py:64 | seguridad | R10, R1 | Alta |
| H-05 | pedidos.py:39–50 | manejo de errores | R10 | Alta |
| H-06 | pedidos.py:52–71 | lógica y límites | R10 | Alta |
| H-07 | api.py:53–54, 67–68 | manejo de errores | R11 | Alta |
| H-08 | api.py:41 | fechas | R11 | Alta |
| H-09 | checkout.py:34–41, 48–51 | manejo de errores | R1, sección 3 | Alta |
| H-10 | checkout.py:61, 74, 82 | lógica y límites | R6 | Alta |
| H-11 | checkout.py:96, 110 | lógica y límites | R8 | Alta |
| H-12 | checkout.py:12–31, 54, 84, 117 | numéricos | R7, sección 1 | Alta |
| H-13 | pedidos.py:12–23, 55–68, 88–97 | numéricos | R10 | Alta |
| H-14 | api.py:18 | numéricos | R11 | Alta |
| H-15 | checkout.py:54, 84, 117 | numéricos | R7 | Alta |
| H-16 | checkout.py:72 | fechas | R6, sección 1 | Alta |
| H-17 | checkout.py:57, 102 | fechas | R6 | Alta |
| H-18 | checkout.py:93 | alucinación | R8, sección 1 | Alta |
| H-19 | checkout.py:72 | fechas | R6 | Media |
| H-20 | checkout.py:40 | lógica y límites | R3 | Media |
| H-21 | checkout.py:60 | lógica y límites | R5 | Media |
| H-22 | checkout.py:44–54, 102–111 | lógica y límites | R4 | Media |
| H-23 | checkout.py:35 | efectos laterales | R4 | Media |
| H-24 | checkout.py:40 | tipos | R3 | Media |
| H-25 | checkout.py:35 | strings | R2 | Media |
| H-26 | checkout.py:64–66 | strings | R6 | Media |
| H-27 | checkout.py:63–66 | strings | R6 | Media |
| H-28 | api.py:31–32 | manejo de errores | R11 | Media |
| H-29 | api.py:37–39 | manejo de errores | R11 | Media |
| H-30 | api.py:64–66 | lógica y límites | R11 | Media |
| H-31 | checkout.py:1, 63 | code smell | (ninguna) | Baja |