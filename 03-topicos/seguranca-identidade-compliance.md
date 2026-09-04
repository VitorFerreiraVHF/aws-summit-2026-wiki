# Seguranca, Identidade e Compliance

> Status: Em revisao
> Dono: Vitor Ferreira
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `seguranca`, `governanca`, `compliance`

## Insights

- A mensagem de keynote e slides locais foi direta: governanca e seguranca devem acelerar a entrega, nao chegar depois.
- Para agentes, identidade e permissao precisam ser granulares; agentes nao devem operar com privilegios amplos por conveniencia.
- Security by design aparece conectado a pentest, code review, threat modeling, vulnerabilidades de codigo e auditoria.

## Checklist de seguranca para agentes

- Identidade separada por agente, ambiente e finalidade.
- Permissoes minimas para tools e APIs.
- Logs de prompt, contexto, tool calls, decisoes e saidas sensiveis com politica de retencao.
- Avaliacoes e guardrails antes de acao autonoma.
- Revisao de dados usados no RAG: classificacao, origem, frescor e permissao.
- Plano de resposta a incidente para acoes executadas por agentes.

## Evidencias locais

- Fotos 051-055 em [Fotos](../04-midias-e-evidencias/fotos.md#agrupamentos-curados)
- Sessoes relacionadas: [SEC302](../02-agenda-e-sessoes/sessoes/sec302-protegendo-o-acesso-de-agentes-com-o-amazon-bedrock-agentcore-identity.md), [SEC303](../02-agenda-e-sessoes/sessoes/sec303-acelere-a-criacao-de-politicas-com-o-iam-policy-autopilot.md)

