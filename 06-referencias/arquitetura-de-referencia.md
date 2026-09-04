# Arquitetura de referencia

> Status: rascunho
> Dono:
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `arquitetura`, `referencia`

## Agente corporativo governado

```mermaid
flowchart TD
  canal[Canal: app, chat, API] --> auth[Autenticacao e autorizacao]
  auth --> gateway[API Gateway / camada de entrada]
  gateway --> agent[Runtime do agente]
  agent --> model[Foundation model via Amazon Bedrock]
  agent --> tools[Tools: APIs internas, workflows, consultas]
  agent --> kb[Knowledge base / RAG]
  kb --> data[Fontes de dados]
  tools --> systems[Sistemas corporativos]
  agent --> policy[Guardrails e politicas]
  agent --> logs[Logs, traces e auditoria]
  logs --> obs[Observabilidade e avaliacao]
  obs --> backlog[Melhoria continua]
```

## Modernizacao assistida por IA

```mermaid
flowchart LR
  discover[Discover e assessment] --> schema[Schema conversion]
  schema --> database[Database migration]
  database --> code[Transform source code]
  code --> deploy[Deploy em EC2/ECS/EKS/serverless]
  deploy --> operate[Operar, medir e otimizar]
```
