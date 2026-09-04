# Riscos e alertas

> Status: rascunho
> Dono:
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `riscos`

| Risco | Sinal de alerta | Mitigacao |
| --- | --- | --- |
| Agente com permissao ampla | Uso de credenciais compartilhadas ou `AdministratorAccess` | IAM granular, ambientes separados, aprovacao humana para acoes sensiveis |
| RAG sem governanca | Fontes duplicadas, antigas ou sem dono | Catalogo, classificacao, freshness e controles de acesso |
| Modernizacao por inventario | Lista grande de servidores sem criterio de negocio | Priorizacao por valor, dependencia, risco e dados |
| POC sem caminho para producao | Demo funciona, mas nao ha observabilidade/custo/seguranca | Definir landing zone, SLOs, guardrails e ownership desde o inicio |
| IA como substituta de processo | Medicao apenas de codigo gerado | Medir fluxo completo e qualidade operacional |
