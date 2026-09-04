# Instrumente, visualize e resolva problemas em sua aplicação de IA | COP401

> Status: Oficial; Em revisao
> Dono: Vitor Ferreira
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `sessao`, `cop401`

## Creditos

- Palestrante(s)/organizacao(oes): Nomes individuais nao informados no catalogo oficial; confirmar em materiais publicados.
- Fonte: [Agenda oficial AWS Summit Sao Paulo 2026](https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/)

## Metadados oficiais

| Campo | Valor |
| --- | --- |
| Codigo | COP401 |
| Horario | 15:00 BRT |
| Local | Sala 206 BC \| Sessão sobre Programação |
| Tipo | Sessão sobre Programação |
| Nivel | 400 – Expert |
| Topicos AWS | Inteligencia artificial, Cloud operations |
| Areas de interesse | agentic-ai, Monitoramento e observabilidade |
| Publico indicado | Engenharia DevOps, Engenharia, Arquitetura de sistemas |
| Industrias |  |
| Servicos AWS detectados | Amazon Bedrock, Amazon Bedrock AgentCore, Amazon CloudWatch |
| Formato/recursos | Code talk, Discussao |

## Descricao oficial

Construa uma aplicação de IA agêntica usando o Amazon Bedrock AgentCore e o Strands Agent SDK, e depois instrumente-a para ter observabilidade completa com o AWS Distro for OpenTelemetry. Nesta sessão prática de live coding, acompanhe toda a telemetria de agentes e modelos de fundação fluindo em tempo real para o dashboard de IA generativa do Amazon CloudWatch. Aprenda a diagnosticar picos de latência, throttling, erros e consumo excessivo de tokens nos fluxos de trabalho dos seus agentes. Saia desta sessão pronto para observar, diagnosticar e corrigir problemas nas suas próprias aplicações de IA generativa antes que seus clientes percebam.

## Topicos relacionados na wiki

[Generative AI e Machine Learning](../../03-topicos/generative-ai-machine-learning.md), [Observabilidade e Operacoes](../../03-topicos/observabilidade-operacoes.md)

## Referencias oficiais relacionadas

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AgentCore Observability - AWS Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html)
- [Strands Agents SDK](https://strandsagents.com/)

## Evidencias locais

Associacao automatica por conteudo visual, agenda e temas. Os arquivos locais foram retirados da versao publica; validar manualmente antes de citar como evidencia final da sessao.

| Evidencia | Tipo | Observacao |
| --- | --- | --- |
| FOTO-051 (asset local em revisao) | foto | Governanca, seguranca e AWS Continuum: Evidencias visuais reforcando que governanca e seguranca aceleram a entrega quando entram no ciclo de desenvolvimento. |
| FOTO-052 (asset local em revisao) | foto | Governanca, seguranca e AWS Continuum: Evidencias visuais reforcando que governanca e seguranca aceleram a entrega quando entram no ciclo de desenvolvimento. |
| FOTO-054 (asset local em revisao) | foto | Governanca, seguranca e AWS Continuum: Evidencias visuais reforcando que governanca e seguranca aceleram a entrega quando entram no ciclo de desenvolvimento. |
| FOTO-055 (asset local em revisao) | foto | Governanca, seguranca e AWS Continuum: Evidencias visuais reforcando que governanca e seguranca aceleram a entrega quando entram no ciclo de desenvolvimento. |
| FOTO-056 (asset local em revisao) | foto | Governanca, seguranca e AWS Continuum: Evidencias visuais reforcando que governanca e seguranca aceleram a entrega quando entram no ciclo de desenvolvimento. |

## Insights

| Insight | Evidencia | Impacto | Proxima acao |
| --- | --- | --- | --- |
| Instrumentar agentes desde o inicio evita que diagnostico dependa de reproduzir erro em producao. | Descricao oficial AWS e documentacao AgentCore Observability | Reduz tempo de investigacao para latencia, throttling, erro e consumo excessivo de tokens. | Criar baseline de telemetria para agentes com CloudWatch e OpenTelemetry. |
| Dashboards de IA generativa devem expor qualidade operacional e custo, nao apenas disponibilidade tecnica. | Descricao oficial AWS | Ajuda engenharia, operacao e lideranca a enxergar impacto real dos agentes. | Definir paineis com latencia, erro, tokens, chamadas de ferramentas e traces. |
| A combinacao Bedrock AgentCore, Strands Agent SDK, ADOT e CloudWatch sugere um caminho pratico para agentes observaveis. | Referencias oficiais relacionadas | Facilita transformar demo em aplicacao operavel. | Preparar uma POC curta baseada em agente instrumentado com traces e metricas. |

## Agradecimento

Agradecimento aos palestrantes e organizacoes por compartilhar conhecimento com a comunidade AWS.


