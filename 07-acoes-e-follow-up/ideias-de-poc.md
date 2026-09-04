# Ideias de PoC

> Status: Em revisao priorizada
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `poc`, `ideias`

## Ideias

| ID | Ideia | Problema | Servicos ou recursos | Evidencia | Esforco | Impacto |
| --- | --- | --- | --- | --- | --- | --- |
| POC-001 | Modernizar uma aplicacao .NET pequena de SQL Server para Aurora PostgreSQL. | Custo e risco de uma jornada de modernizacao manual. | AWS Transform, AWS Schema Conversion Tool, AWS DMS, Aurora PostgreSQL, S3. | MAM311, AUD-001 e fotos 081-083. | Medio | Alto |
| POC-002 | Publicar um agente interno com identidade e observabilidade desde o primeiro commit. | Agentes funcionais sem rastreabilidade, limites ou controle de acesso. | Amazon Bedrock AgentCore Runtime, Gateway, Identity, Observability e CloudWatch. | AIM202, SEC302, DVT203 e COP401. | Medio | Alto |
| POC-003 | Aplicar AI-DLC a um pequeno servico novo, com spec, testes e checkpoints humanos. | Ambiguidade de requisitos e mudancas geradas por IA sem trilha clara. | Kiro, repositorio Git, pipeline CI/CD e telemetria. | NTA109, DVT203 e fotos 037-038. | Baixo | Medio |
| POC-004 | Criar uma politica FinOps-as-code com simulacao e aprovacao. | Desperdicio recorrente e correcoes tardias de custo. | Cloud Custodian, policy-as-code, AWS Budgets, Cost Explorer e CI/CD. | DEV203 e trilha FinOps. | Baixo | Medio |

## Criterios de selecao

- Valor demonstravel em ate quatro semanas.
- Ambiente e dados nao criticos.
- Metricas de sucesso definidas antes do inicio.
- Revisao de seguranca, custo, licenca e privacidade.
- Resultado documentado para poder ser reutilizado pela comunidade.

