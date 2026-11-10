# Registro de prompts · Refresca · Serviço de previsão (SOA e Web Services)

O briefing da GS permite IA como copiloto, desde que os prompts fiquem registrados aqui e a equipe saiba explicar cada linha do código.

Os registros abaixo distinguem o desenvolvimento inicial da revisão posterior. Quando o prompt original não está reproduzido literalmente, o conteúdo é identificado como resumo fiel.

## Integrantes

- Italo Caliari Silva - RM554758
- Júlio César Ruiz Zequin - RM554676
- Danilo Gronski Wendler - RM 556602
- Pedro Henrique Muzel Santos - RM 555983
- Vitor Montemor Ismael - RM 556027

---

## 2026-11-09 · Desenvolvimento do serviço de previsão (SOA e Web Services)

- **Ferramenta:** Gemini
- **Integrante:** Italo Caliari Silva
- **Prompt:** resumo fiel do pedido original: desenvolver exclusivamente a entrega da disciplina Arquitetura Orientada a Serviços (SOA) e Web Services da Global Solution 2026.2; analisar o PDF da atividade e os materiais prévios da equipe; implementar um serviço completo em qualquer linguagem adequada, com arquitetura orientada a serviços, endpoints REST, integração com banco, tratamento de erros, validações, documentação, testes, instruções de execução, roteiro de evidências e checklist alinhado à rubrica do professor. O pedido também determinava que os testes locais e a coleta das evidências seriam realizados posteriormente pelo integrante.
- **O que foi aproveitado:** estrutura do projeto em Python/FastAPI, separação em domínio, serviços, repositórios e rotas; persistência com SQLAlchemy/SQLite; migrações Alembic; documentação OpenAPI/Swagger; testes automatizados; roteiro de execução e evidências.
- **O que a equipe ajustou:** o README e os contratos foram organizados para documentar a comunicação com a API principal. A implementação mantém uma heurística identificada como baseline enquanto o arquivo de modelo treinado da disciplina de IA não estiver disponível.
- **Situação da validação local:** o prompt original previa que o integrante executaria os testes e coletaria as evidências posteriormente. Portanto, este registro não afirma que a equipe tenha validado localmente o projeto nessa etapa.

### Verificação posterior do pacote (não confundir com execução local da equipe)

Em uma auditoria posterior, o pacote `gs_soa.zip` foi extraído e executado em ambiente Linux isolado pelo assistente ChatGPT. Nessa execução, `pytest -v` apresentou **14 testes aprovados**; as migrações Alembic também foram aplicadas, revertidas até `base` e reaplicadas com sucesso em um banco SQLite descartável. Essa verificação é um resultado do ambiente de auditoria e não substitui a execução local nem os prints que a equipe deve coletar.

---

## 2026-11-09 · Revisão documental e preparação das evidências

- **Ferramenta:** ChatGPT
- **Integrante:** preencher com o nome do integrante que solicitou e acompanhou esta revisão.
- **Prompt:** resumo fiel do pedido: revisar o repositório `italocaliari/gs_soa` em relação aos critérios da disciplina SOA; ajudar a resolver as evidências 07 (`POST /previsoes` em cenário de calor alto) e 11 (`GET /previsoes/{id}`); corrigir a explicação do estado atual da integração com o modelo de IA; e revisar o registro de prompts para não afirmar uma validação local que não tenha ocorrido.
- **O que foi aproveitado:** identificação das pendências documentais e elaboração de instruções explícitas para coletar as duas evidências a partir da execução real do Swagger.
- **O que a equipe ajustou:** pendente de revisão e confirmação pela equipe após aplicar as alterações propostas e capturar os dois prints.

---

**Importante:** mantenha este arquivo atualizado com novos usos relevantes de IA. Não registre como executado um teste, uma alteração ou uma validação que não tenha sido realizada. Se a equipe tiver feito uma execução local adicional, inclua a data, o integrante, o comando executado e o resultado observado.

---

## 2026-11-09 · Revisão e integração entre as partes

- **Ferramenta:** Claude
- **Integrante:** Danilo Gronski Wendler
- **Prompt:** "Revise os repositórios de C# e SOA do meu colega, confira se seguem a rubrica e os contratos combinados com o app e o modelo de ML, e faça as correções necessárias."
- **O que foi aproveitado:** correção das consultas por data no SQLite (C#), Swagger sempre ativo e API acessível pela rede (C#), DTOs ajustados ao contrato do app (C#), chamada ao serviço de previsão para o alerta do dia (C#), contrato do `POST /previsoes` com os 3 dias usados pelo modelo de ML, integração com o modelo XGBoost treinado e migração `0003` (SOA), testes atualizados e novos.
- **O que a equipe ajustou:** [preencher após rodar `dotnet test`, `pytest`, a API e o serviço localmente]
