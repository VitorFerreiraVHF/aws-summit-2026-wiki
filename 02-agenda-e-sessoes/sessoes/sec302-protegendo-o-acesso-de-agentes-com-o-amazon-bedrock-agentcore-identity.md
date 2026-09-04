# Protegendo o acesso de agentes com o Amazon Bedrock AgentCore Identity | SEC302

> Status: Oficial; Em revisao
> Dono: Vitor Ferreira
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `sessao`, `sec302`

## Creditos

- Palestrante(s)/organizacao(oes): Nomes individuais nao informados no catalogo oficial; confirmar em materiais publicados.
- Fonte: [Agenda oficial AWS Summit Sao Paulo 2026](https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/)

## Metadados oficiais

| Campo | Valor |
| --- | --- |
| Codigo | SEC302 |
| Horario | 16:00 BRT |
| Local | Pavilhão 4 \| Sessão Interativa 2 |
| Tipo | Sessão Interativa |
| Nivel | 300 – Advanced |
| Topicos AWS | Seguranca e compliance |
| Areas de interesse | Generative AI, IAM |
| Publico indicado | Engenharia, Profissionais de TI, Arquitetura de sistemas |
| Industrias |  |
| Servicos AWS detectados | Amazon Bedrock, Amazon Bedrock AgentCore |
| Formato/recursos | Chalk talk, Discussao |

## Descricao oficial

Aprenda a implementar controles de acesso robustos para agentes de IA em aplicações modernas usando serviços da AWS. Esta sessão aborda padrões essenciais para autenticação e autorização de agentes de IA usando o Amazon Bedrock AgentCore Identity. Demonstraremos arquiteturas práticas que ajudam a garantir que os agentes de IA operem com segurança dentro de limites definidos, mantendo total visibilidade em todo o seu ambiente AWS.

## Topicos relacionados na wiki

[Seguranca, Identidade e Compliance](../../03-topicos/seguranca-identidade-compliance.md)

## Referencias oficiais relacionadas

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AgentCore Identity - AWS Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started.html)

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
| Agentes precisam operar com identidade, permissao e limite claros, como qualquer workload critico. | Descricao oficial AWS e inventario FOTO-051 a FOTO-056 | Reduz risco de agentes acessarem dados, ferramentas ou sistemas fora do escopo. | Definir matriz de permissoes por tipo de agente e ferramenta. |
| Autenticacao e autorizacao devem cobrir tanto acesso do usuario ao agente quanto acesso do agente a sistemas externos. | Documentacao AgentCore Identity | Fecha lacunas comuns de seguranca em fluxos agenticos. | Desenhar fluxo de inbound auth, outbound auth e auditoria para uma POC. |
| Visibilidade de identidade e credenciais e requisito de producao, nao detalhe final. | Descricao oficial AWS | Facilita investigacao, compliance e resposta a incidente. | Conectar com [DVT203](dvt203-debug-mais-rapido-governe-melhor-ai-dlc-e-observabilidade.md) e [COP401](cop401-instrumente-visualize-e-resolva-problemas-em-sua-aplicacao-de-ia.md). |

## Agradecimento

Agradecimento aos palestrantes e organizacoes por compartilhar conhecimento com a comunidade AWS.


