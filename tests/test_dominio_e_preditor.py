import json
from pathlib import Path

import pytest

from app.domain.calor import indice_calor_celsius, nivel_do_indice
from app.errors import ModeloIndisponivel
from app.ml.preditor import HeuristicaCalor, ModeloXGBoost, criar_preditor
from app.ml.preparar_variaveis import montar_variaveis
from tests.conftest import dias_para

MODELO_REAL = Path(__file__).resolve().parent.parent / "modelos" / "modelo_refresca.json"


def f(c):
    return c * 9 / 5 + 32


def test_indice_de_calor_bate_com_a_tabela_da_noaa():
    assert f(indice_calor_celsius(32.22, 50)) == pytest.approx(95, abs=1.0)  # 90 °F, 50 %
    assert f(indice_calor_celsius(26.67, 40)) == pytest.approx(80, abs=1.0)  # 80 °F, 40 %


def test_niveis_seguem_as_faixas_do_contrato():
    assert nivel_do_indice(26.9) == "normal"
    assert nivel_do_indice(27.0) == "atencao"
    assert nivel_do_indice(31.9) == "atencao"
    assert nivel_do_indice(32.0) == "perigo"


def test_heuristica_cresce_com_o_indice_de_calor():
    h = HeuristicaCalor()
    p = [h.probabilidade(dias_para("2026-11-20", indice_calor=ic)) for ic in (20, 28, 32, 36)]
    assert p == sorted(p)
    assert 0 <= p[0] < 0.1 and p[-1] > 0.9


def test_variaveis_seguem_o_notebook_de_ml():
    variaveis = montar_variaveis(dias_para("2026-11-20", indice_calor=33.0, temp_max=31.0))
    assert len(variaveis) == 26
    assert variaveis["perigoso_hoje"] == 1.0
    assert variaveis["dias_perigosos_3d"] == 3.0
    assert variaveis["temp_max_media_3d"] == pytest.approx(31.0)


def test_modelo_inexistente_falha_com_mensagem_clara(tmp_path):
    with pytest.raises(ModeloIndisponivel):
        criar_preditor(str(tmp_path / "nao_existe.json"))


def test_carrega_modelo_xgboost_treinado(tmp_path):
    xgboost = pytest.importorskip("xgboost")
    np = pytest.importorskip("numpy")
    nomes = list(montar_variaveis(dias_para("2026-11-20")).keys())
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, len(nomes)))
    y = (X[:, nomes.index("ic_max")] > 0).astype(int)
    booster = xgboost.train({"objective": "binary:logistic"}, xgboost.DMatrix(X, label=y, feature_names=nomes), 20)
    booster.save_model(tmp_path / "modelo.json")
    (tmp_path / "metadados.json").write_text(
        json.dumps({"versao": "2.0", "variaveis": nomes, "limiar_alerta": 0.46, "xgboost": xgboost.__version__})
    )

    preditor = criar_preditor(str(tmp_path / "modelo.json"))
    assert isinstance(preditor, ModeloXGBoost)
    assert preditor.versao == "xgboost-2.0" and preditor.limiar_sugerido == 0.46
    assert 0 <= preditor.probabilidade(dias_para("2026-11-20")) <= 1


@pytest.mark.skipif(not MODELO_REAL.exists(), reason="modelo do repositório de ML não copiado para modelos/")
def test_modelo_real_separa_dia_quente_de_dia_ameno():
    preditor = criar_preditor(str(MODELO_REAL))
    quente = preditor.probabilidade(dias_para("2026-11-20", indice_calor=35.0, temp_max=34.0))
    ameno = preditor.probabilidade(dias_para("2026-11-20", indice_calor=22.0, temp_max=22.0))
    assert quente > preditor.limiar_sugerido > ameno
