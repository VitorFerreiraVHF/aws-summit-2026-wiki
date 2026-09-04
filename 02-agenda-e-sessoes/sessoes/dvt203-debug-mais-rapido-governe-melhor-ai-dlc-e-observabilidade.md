# Debug mais rápido, governe melhor: AI-DLC e observabilidade | DVT203

> Status: Oficial; Em revisao
> Dono: Vitor Ferreira
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `sessao`, `dvt203`

## Creditos

- Palestrante(s)/organizacao(oes): Nomes individuais nao informados no catalogo oficial; confirmar em materiais publicados.
- Fonte: [Agenda oficial AWS Summit Sao Paulo 2026](https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/)

## Metadados oficiais

| Campo | Valor |
| --- | --- |
| Codigo | DVT203 |
| Horario | 12:30 BRT |
| Local | Pavilhão 4 \| Sessão Interativa 1 |
| Tipo | Sessão Interativa |
| Nivel | 200 – Intermediate |
| Topicos AWS | Inteligencia artificial |
| Areas de interesse |  |
| Publico indicado | Ciencia de dados, Engenharia, Profissionais de TI |
| Industrias |  |
| Servicos AWS detectados | Amazon Bedrock, Amazon Bedrock AgentCore |
| Formato/recursos | Chalk talk, Discussao |

## Descricao oficial

Seu agente funciona em dev e alucina em produção — e ninguém sabe explicar por quê. Em geral a causa está a montante: o agente foi construído sem governança. Neste chalk talk desenhamos uma abordagem em duas camadas. Primeiro, o AI-DLC (AI-Driven Development Life Cycle): metodologia open-source e AI-native, com checkpoints validados por humanos e trilhas de auditoria que barram erros antes do deploy. Depois, a observabilidade do Amazon Bedrock AgentCore: traces OpenTelemetry de cada chamada de modelo e ferramenta, avaliação contínua e rollouts seguros. Quando um trace revela uma decisão ruim, os artefatos do AI-DLC explicam por quê.

## Topicos relacionados na wiki

[Generative AI e Machine Learning](../../03-topicos/generative-ai-machine-learning.md)

## Referencias oficiais relacionadas

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AgentCore Observability - AWS Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html)

## Evidencias locais

Associacao automatica por conteudo visual, agenda e temas. Os arquivos locais foram retirados da versao publica; validar manualmente antes de citar como evidencia final da sessao.

| Evidencia | Tipo | Observacao |
| --- | --- | --- |
| FOTO-037 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |
| FOTO-038 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |
| FOTO-044 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |
| FOTO-046 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |
| FOTO-049 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |
| FOTO-050 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |
| FOTO-053 (asset local em revisao) | foto | AgentCore, contexto, RAG e observabilidade: Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala. |

## Insights

| Insight | Evidencia | Impacto | Proxima acao |
| --- | --- | --- | --- |
| Observabilidade de agente precisa explicar a cadeia completa: prompt, ferramenta, chamada de modelo, decisao e resultado. | Descricao oficial AWS e inventario FOTO-037 a FOTO-053 | Facilita diagnostico de alucinacao, latencia, custo e falhas antes que cheguem ao usuario final. | Definir padrao minimo de traces e spans para agentes internos. |
| AI-DLC coloca checkpoints humanos e trilhas de auditoria antes do deploy, nao apenas depois do incidente. | Descricao oficial AWS | Reduz risco de deploy de agentes sem requisitos, criterios de aceite ou evidencia de revisao. | Criar checklist de governanca para PoCs de IA generativa. |
| Quando um trace mostra decisao ruim, os artefatos de desenvolvimento devem explicar a causa. | Descricao oficial AWS | Aproxima engenharia, seguranca e operacao em uma mesma linha de investigacao. | Conectar esta sessao com [COP401](cop401-instrumente-visualize-e-resolva-problemas-em-sua-aplicacao-de-ia.md) para instrumentacao pratica. |

## Agradecimento

Agradecimento aos palestrantes e organizacoes por compartilhar conhecimento com a comunidade AWS.


