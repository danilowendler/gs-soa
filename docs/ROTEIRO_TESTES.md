# Roteiro de testes e evidências · Serviço de previsão

Execute na raiz do projeto, com o ambiente virtual ativo (Python 3.12+), `pip install -r requirements-dev.txt` feito e o `.env` copiado do `.env.example` (ele já aponta para o modelo treinado em `modelos/`).
Salve os prints em `docs/evidencias/` com os nomes sugeridos.

> **Refazer os prints 01, 02, 03, 06 a 11, 13 a 16, 18 e 19.** O contrato do `POST /previsoes` mudou para o formato do modelo de ML (3 dias de clima) e entrou a migração `0003`; os prints antigos mostram o formato anterior.

| # | O que fazer | Resultado esperado | Evidência (arquivo sugerido) |
| --- | --- | --- | --- |
| 1 | `alembic upgrade head` | Mensagens `-> 0001`, `0001 -> 0002` e `0002 -> 0003`; arquivo `refresca_previsao.db` criado | `01_migracao_upgrade.png` |
| 2 | `alembic current` e `alembic history` | `0003 (head)` e as três revisões listadas | `02_migracao_historico.png` |
| 3 | `sqlite3 refresca_previsao.db ".schema previsoes"` | Tabela `previsoes` com a coluna `dias_json` e o índice `ix_previsoes_data` | `03_schema_banco.png` |
| 4 | `uvicorn app.main:app --port 8000` | `Uvicorn running on http://127.0.0.1:8000` | `04_servidor_no_ar.png` |
| 5 | Abrir http://localhost:8000/docs | Swagger com `/previsoes` (POST, GET), `/previsoes/{id}`, `/previsoes/data/{data}`, `/health` | `05_swagger.png` |
| 6 | No Swagger, `POST /previsoes` com o exemplo pronto do Swagger (ou o `curl` do README) | `201`; corpo com `id`, `dataPrevista`, `probabilidade`, `perigoso`, `versaoModelo: "xgboost-1.0"` | `06_post_201.png` |
| 7 | `POST /previsoes` com o JSON de dia quente abaixo | `201` e `perigoso: true` | `07_post_dia_quente.png` |
| 8 | `POST /previsoes` com o JSON de dia ameno abaixo | `201` e `perigoso: false` | `08_post_dia_ameno.png` |
| 9 | `POST /previsoes` com `umidMedia: 150` em um dos dias | `422` com o campo inválido apontado | `09_post_422.png` |
| 10 | `POST /previsoes` com `tempMin` maior que `tempMax` em um dos dias | `422` | `10_post_422_min_max.png` |
| 11 | `GET /previsoes/{id}` com o `id` do passo 6 | `200` com os 3 dias de entrada, o resultado e `criadoEm` | `11_get_id.png` |
| 12 | `GET /previsoes/9999` | `404` com `{"erro":"nao_encontrada",...}` | `12_get_404.png` |
| 13 | `GET /previsoes?data=2026-11-20&limite=10` | `200` com lista só do dia filtrado | `13_get_lista.png` |
| 14 | `GET /previsoes/data/2026-11-20` | `200` com a última previsão do dia | `14_get_por_data.png` |
| 15 | `GET /health` | `200` com `{"status":"ok","banco":"ok","versaoModelo":"xgboost-1.0"}` | `15_health.png` |
| 16 | `sqlite3 refresca_previsao.db "select id,data,probabilidade,perigoso,versao_modelo from previsoes;"` | Linhas gravadas pelos passos 6 a 8 | `16_dados_no_banco.png` |
| 17 | Reiniciar o servidor e repetir o passo 11 | A previsão continua lá (persistência) | `17_persistencia.png` |
| 18 | `pytest -v` | Todos os testes `PASSED` (são 18); `0 failed` | `18_pytest.png` |
| 19 | `alembic downgrade base` e depois `alembic upgrade head` | Reverte as três migrações e reaplica sem erro | `19_migracao_downgrade.png` |

### JSON para a evidência 07 (dia quente)

```json
{
  "dataPrevista": "2026-11-20",
  "dias": [
    { "dia": "2026-11-17", "tempMax": 32.0, "tempMin": 20.0, "tempMedia": 26.0, "umidMedia": 50.0, "umidMin": 30.0, "indiceCalorMax": 33.0, "pressaoMedia": 923.0, "radiacaoTotal": 24000, "precipTotal": 0.0, "ventoMedio": 2.0 },
    { "dia": "2026-11-18", "tempMax": 33.0, "tempMin": 20.5, "tempMedia": 26.5, "umidMedia": 50.0, "umidMin": 30.0, "indiceCalorMax": 34.0, "pressaoMedia": 923.0, "radiacaoTotal": 24000, "precipTotal": 0.0, "ventoMedio": 2.0 },
    { "dia": "2026-11-19", "tempMax": 34.0, "tempMin": 21.0, "tempMedia": 27.0, "umidMedia": 50.0, "umidMin": 30.0, "indiceCalorMax": 35.2, "pressaoMedia": 923.0, "radiacaoTotal": 24000, "precipTotal": 0.0, "ventoMedio": 2.0 }
  ]
}
```

### JSON para a evidência 08 (dia ameno)

```json
{
  "dataPrevista": "2026-11-20",
  "dias": [
    { "dia": "2026-11-17", "tempMax": 22.0, "tempMin": 14.0, "tempMedia": 18.0, "umidMedia": 75.0, "umidMin": 55.0, "indiceCalorMax": 22.0, "pressaoMedia": 926.0, "radiacaoTotal": 15000, "precipTotal": 3.0, "ventoMedio": 2.5 },
    { "dia": "2026-11-18", "tempMax": 21.0, "tempMin": 14.0, "tempMedia": 17.5, "umidMedia": 78.0, "umidMin": 58.0, "indiceCalorMax": 21.0, "pressaoMedia": 927.0, "radiacaoTotal": 14000, "precipTotal": 5.0, "ventoMedio": 2.5 },
    { "dia": "2026-11-19", "tempMax": 22.0, "tempMin": 15.0, "tempMedia": 18.0, "umidMedia": 75.0, "umidMin": 55.0, "indiceCalorMax": 22.0, "pressaoMedia": 926.0, "radiacaoTotal": 15000, "precipTotal": 1.0, "ventoMedio": 2.0 }
  ]
}
```

**Importante:** não crie ou edite imagens manualmente para simular respostas. Os prints devem ser capturados da execução real do Swagger na sua máquina.

Observações:

- Se o `pytest` apontar falha, **não ajuste o teste para passar**: leia a mensagem, corrija o código e rode de novo.
- Se o servidor não subir com "O modelo foi treinado com xgboost 3.4.1, mas está instalado o ...", reinstale com `pip install -r requirements.txt` (precisa de Python 3.12+).
