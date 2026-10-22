from datetime import date
from decimal import Decimal

import pytest

import pedidos
from checkout import CheckoutError

HOY_VIGENTE = date(2026, 10, 1)


@pytest.fixture
def ruta(tmp_path):
    return str(tmp_path / "tienda.db")


@pytest.fixture
def con(ruta):
    conexion = pedidos.conectar(ruta)
    pedidos.crear_esquema(conexion)
    yield conexion
    conexion.close()


def item(producto="buzo", talle="M", cantidad=1, **extra):
    return {"producto": producto, "talle": talle, "cantidad": cantidad, **extra}


def contar(ruta, tabla):
    assert tabla in ("pedidos", "items")
    otra = pedidos.conectar(ruta)
    try:
        return otra.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
    finally:
        otra.close()


def test_un_id_inexistente_devuelve_none(con):
    assert pedidos.obtener_pedido(con, 999) is None

# ---------- R10 · si calcular_total falla, no queda nada guardado ----------

def test_error_de_checkout_se_propaga_y_no_deja_pedido_ni_items(con, ruta):
    carrito = [item(talle="XXXL")]

    with pytest.raises(CheckoutError) as error:
        pedidos.guardar_pedido(con, "ana@mail.com", carrito, "CABA")

    assert error.value.code == "TALLE_INVALIDO"
    assert contar(ruta, "pedidos") == 0
    assert contar(ruta, "items") == 0


# ---------- R10 · el pedido es definitivo para cualquier otra conexión ----------

def test_otra_conexion_ve_el_pedido_completo_con_sus_items(con, ruta):
    carrito = [item("buzo", cantidad=1), item("remera", cantidad=2)]
    pedido_id = pedidos.guardar_pedido(con, "ana@mail.com", carrito, "CABA")

    otra = pedidos.conectar(ruta)
    try:
        pedido = pedidos.obtener_pedido(otra, pedido_id)
    finally:
        otra.close()

    assert pedido["total"] == Decimal("52499.80")
    assert [i["producto"] for i in pedido["items"]] == ["buzo", "remera"]


# ---------- R10 · los montos guardados son idénticos a los calculados ----------

def test_montos_leidos_son_decimal_identicos_a_los_calculados_por_checkout(con):
    carrito = [item("remera", cantidad=1)]
    pedido_id = pedidos.guardar_pedido(
        con, "ana@mail.com", carrito, "CABA", "EGRESADOS2026", HOY_VIGENTE
    )

    pedido = pedidos.obtener_pedido(con, pedido_id)

    assert pedido["subtotal"] == Decimal("11999.50")
    assert pedido["descuento"] == Decimal("1799.93")
    assert pedido["envio"] == Decimal("2500.00")
    assert pedido["total"] == Decimal("12699.57")


# ---------- R10 · el email es un dato del usuario y no altera la consulta ----------

def test_pedidos_de_con_email_malicioso_no_devuelve_pedidos_ajenos(con):
    pedidos.guardar_pedido(con, "ana@mail.com", [item()], "CABA")

    resultado = pedidos.pedidos_de(con, "' OR '1'='1")

    assert resultado == []