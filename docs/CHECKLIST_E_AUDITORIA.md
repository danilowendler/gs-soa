# Checklist de requisitos e auditoria do material existente

## 1. Requisitos do PDF (slide 27, SOA e Web Services) × implementação

| Requisito | Peso | Onde está | Como comprovar |
| --- | --- | --- | --- |
| Estruturação do domínio | 3,0 | Camadas `domain/`, `services/`, `repositories/`, `routers/`, `schemas.py`, `errors.py`; entidade `Previsao` com regra `e_perigosa`; índice de calor NOAA em `domain/calor.py`; preditor atrás de interface (`ml/preditor.py`) | README (estrutura), código, testes de domínio |
| Conexão com banco de dados | 3,0 | `database.py` (engine, sessão por requisição), `PrevisaoRepository`, SQLAlchemy 2.0, URL por variável de ambiente | Roteiro 3, 16, 17 |
| Migrações | 1,5 | Alembic: `migrations/versions/0001` (tabela), `0002` (índice) e `0003` (3 dias de entrada do modelo de ML) | Roteiro 1, 2, 19 |
| Documentação automática | 1,5 | OpenAPI/Swagger do FastAPI, com exemplos, descrições e respostas de erro | Roteiro 5 |
| Testes automatizados | 1,0 | `tests/` (18 testes) | `docs/evidencias/18_pytest.png` e nova execução local pela equipe |
| Chamadas de APIs REST (objetivo) | n/d | `POST/GET /previsoes`, consumido pela API em C# | Roteiro 6 a 15 |
| Repositório GitHub | entregável | Este repositório | Link no Teams |
| README com execução, descrição e integrantes | entregável | `README.md` (preencher integrantes e links) | Revisão |
| Documentação dos endpoints | entregável | `/docs`, `/redoc` | Roteiro 5 |
| Evidências | entregável | `docs/evidencias/` | Roteiro inteiro |

## 2. Auditoria do que o colega deixou pronto

**Aproveitado sem mudar:** Ficha, Persona, ODS, tabela de contratos, níveis do índice de calor, exemplos de requisição e resposta de `POST /previsoes`, modelo do `prompts.md`.

**Correto e alinhado ao PDF:** o README segue a sugestão de ficha do slide 20; registra dados simulados vs. públicos; a arquitetura coloca o serviço de previsão em Python/FastAPI (o PDF permite qualquer linguagem).

**Completado durante a preparação:** descrição desta parte, estrutura do projeto, passos de execução, tabela de entregáveis com a rubrica de SOA, entrada de prompt referente ao desenvolvimento do serviço e destaque do serviço de previsão no diagrama Mermaid. Os testes e as migrações também foram executados posteriormente em ambiente Linux isolado durante a auditoria; isso não deve ser descrito como execução local feita por integrante da equipe.

**Pontos que a equipe precisa decidir ou revisar:**

1. **Campos de entrada do modelo.** Resolvido: o `POST` recebe os 3 dias de clima no formato do modelo de ML, e `app/ml/preparar_variaveis.py` (cópia do repositório de ML) monta as 26 variáveis.
2. **Modelo treinado.** Resolvido: `modelos/modelo_refresca.json` e `metadados.json` vêm do repositório de ML, com `xgboost==3.4.1` fixo. A heurística continua disponível como linha de base quando `REFRESCA_MODELO_PATH` está vazio.
3. **Resposta `201`.** O README só mostra o corpo da resposta, não o status. Usei `201 Created`. Avise quem faz a API em C# para aceitar 2xx.
4. **Campos extras.** O `POST` responde exatamente os cinco campos do contrato. Os `GET` devolvem mais campos (entrada e `criadoEm`); a API em C# deve ignorar o que não usar.
5. **Mesmo dia com várias previsões.** Cada `POST` cria um registro novo; `GET /previsoes/data/{data}` devolve o mais recente. Se preferirem uma previsão única por dia, é uma mudança pequena (migração nova + `409` ou atualização).
6. **Professor da disciplina:** o PDF não traz o nome. Não inventei nenhum.
7. **Links:** falta só o link das outras partes e os responsáveis na tabela de repositórios.
8. **Evidências:** refazer os prints indicados no topo do roteiro, porque o contrato do `POST` mudou.
9. **Combinado da GS:** cada integrante deve saber explicar cada linha. Leia o código antes de entregar.
