import json
import threading
import urllib.error
import urllib.request

import pytest

import api

RUTA = "/api/v1/pedidos"


@pytest.fixture
def url(tmp_path):
    servidor = api.crear_servidor(str(tmp_path / "tienda.db"), 0)
    threading.Thread(target=servidor.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
    yield f"http://127.0.0.1:{servidor.server_address[1]}"
    servidor.shutdown()
    servidor.server_close()


def pedir(url, metodo, ruta, cuerpo=None, crudo=None):
    datos = crudo if crudo is not None else (json.dumps(cuerpo).encode() if cuerpo is not None else None)
    req = urllib.request.Request(url + ruta, data=datos, method=metodo,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def compra(**cambios):
    cuerpo = {"email": "ana@mail.com", "zona": "CABA",
              "carrito": [{"producto": "buzo", "talle": "M", "cantidad": 1}]}
    cuerpo.update(cambios)
    return cuerpo


def test_una_ruta_inexistente_devuelve_404(url):
    status, cuerpo = pedir(url, "GET", "/api/v1/otra")
    assert status == 404
    assert cuerpo["error"]["code"] == "RUTA_INEXISTENTE"

# ---------- R11 · CheckoutError -> 422 con el code del error ----------

def test_error_de_negocio_devuelve_422_con_el_code_del_checkout_error(url):
    cuerpo_pedido = compra(carrito=[{"producto": "buzo", "talle": "XXXL", "cantidad": 1}])

    status, cuerpo = pedir(url, "POST", RUTA, cuerpo_pedido)

    assert status == 422
    assert cuerpo["error"]["code"] == "TALLE_INVALIDO"


# ---------- R11 · cuerpo que no es JSON -> 400 JSON_INVALIDO ----------

def test_cuerpo_que_no_es_json_devuelve_400_json_invalido(url):
    status, cuerpo = pedir(url, "POST", RUTA, crudo=b"{esto no es json")

    assert status == 400
    assert cuerpo["error"]["code"] == "JSON_INVALIDO"


# ---------- R11 · fecha con formato incorrecto -> 400 FECHA_INVALIDA ----------

def test_fecha_con_formato_distinto_de_aaaa_mm_dd_devuelve_400_fecha_invalida(url):
    status, cuerpo = pedir(url, "POST", RUTA, compra(fecha="30/11/2026"))

    assert status == 400
    assert cuerpo["error"]["code"] == "FECHA_INVALIDA"


# ---------- R11 · pedido que no existe -> 404 PEDIDO_INEXISTENTE ----------

def test_consultar_un_pedido_que_no_existe_devuelve_404_pedido_inexistente(url):
    status, cuerpo = pedir(url, "GET", RUTA + "/999")

    assert status == 404
    assert cuerpo["error"]["code"] == "PEDIDO_INEXISTENTE"