from datetime import date
from decimal import Decimal

import pytest

from checkout import (
    CheckoutError,
    calcular_descuento,
    calcular_envio,
    calcular_subtotal,
    calcular_total,
    validar_item,
    CUPONES
)

HOY_VIGENTE = date(2026, 10, 1)


def item(producto="buzo", talle="M", cantidad=1, **extra):
    return {"producto": producto, "talle": talle, "cantidad": cantidad, **extra}


def codigo_de_error(funcion, *args):
    with pytest.raises(CheckoutError) as error:
        funcion(*args)
    return error.value.code


def test_cantidad_cero_es_invalida():
    assert codigo_de_error(validar_item, item(cantidad=0)) == "CANTIDAD_INVALIDA"

def test_cupones_son_solo_los_esperados():
    assert set(CUPONES) == {"EGRESADOS2026", "BIENVENIDA"}
    assert len(CUPONES) == 2

def test_precio_enviado_por_el_cliente_se_ignora_en_el_subtotal():
    carrito = [item("buzo", cantidad=1, precio=1)]

    subtotal = calcular_subtotal(carrito)

    assert subtotal == Decimal("24999.90")

def test_cupon_porcentual_mayor_que_descuento_por_cantidad_aplica_solo_el_cupon():
    carrito = [item("remera", cantidad=6)]

    resultado = calcular_total(carrito, "RETIRO", "EGRESADOS2026", HOY_VIGENTE)

    assert resultado["descuento"] == Decimal("10799.55")