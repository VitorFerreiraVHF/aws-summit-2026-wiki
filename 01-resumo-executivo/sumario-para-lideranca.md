# Sumario para lideranca

> Status: rascunho informado por evidencias
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `lideranca`, `resumo-executivo`

## Mensagem principal

O AWS Summit Sao Paulo 2026 reforcou uma mudanca de foco: IA agentica precisa sair da demonstracao e entrar em operacao com governanca, observabilidade, identidade e capacidade de evolucao. A modernizacao tambem apareceu como jornada orientada por evidencias, com assessment, conversao assistida, migracao de dados, alteracao de codigo e deploy. O material coletado sugere que pessoas, processo e medicao sao tao importantes quanto a escolha da ferramenta. Para a comunidade, o melhor proximo passo e transformar os aprendizados em pequenas provas de valor documentadas, com criterios de seguranca e custo desde o inicio.

## Sinais observados

| Tema | Sinal observado | Impacto esperado | Recomendacao |
| --- | --- | --- | --- |
| IA agentica | AgentCore aparece associado a runtime, gateway, memoria, identidade, observabilidade e harness de avaliacao. | Mais viabilidade para operar agentes em escala, mas com nova superficie de risco. | Comecar por um caso de uso limitado, com telemetria e least privilege obrigatorios. |
| Modernizacao | O fluxo observado combina discovery, assessment, schema conversion, DMS, transformacao de codigo e deploy. | Reducao do trabalho manual em jornadas .NET, SQL Server e mainframe. | Validar uma carga nao critica com plano de rollback e revisao humana de cada sugestao. |
| Engenharia | AI-DLC e desenvolvimento orientado a especificacoes colocam checkpoints antes do codigo e do deploy. | Menos ambiguidade, mais rastreabilidade e melhor qualidade de mudancas geradas por IA. | Criar um playbook interno de especificacao, testes, revisao e auditoria. |
| Seguranca | A mensagem recorrente foi combinar seguranca, conformidade e velocidade, sem trata-las como escolhas excludentes. | Governanca passa a ser parte do caminho de entrega, nao uma etapa final. | Definir guardrails, identidade, dados sensiveis e evidencias de auditoria como criterios de pronto. |
| Pessoas | A gravacao AUD-002 enfatiza mudanca cultural, pessoas e processo. | A adocao pode falhar mesmo com tecnologia adequada. | Nomear donos, capacitar os times e medir o processo de transformacao. |

## Implicacoes

- A estrategia de IA deve ser acompanhada por estrategia de dados, identidade, observabilidade e custos.
- A modernizacao assistida por IA acelera o trabalho, mas nao elimina a responsabilidade tecnica sobre schema, codigo, dados e deploy.
- A base de conhecimento pode servir como memoria de decisoes, material de onboarding e fonte para novas PoCs.

## Proximos passos sugeridos

1. Revisar manualmente as tres transcricoes de audio e atribuir cada uma a uma sessao.
2. Escolher duas PoCs: modernizacao SQL Server com AWS Transform e agente governado com AgentCore.
3. Definir indicadores de sucesso antes de implementar: tempo, custo, qualidade, risco e experiencia.
4. Fazer revisao humana das imagens censuradas antes de qualquer compartilhamento publico.
5. Atualizar a wiki quando a AWS publicar gravações oficiais ou novos materiais do Summit.

## Referencias de contexto

- [Pagina oficial do AWS Summit Sao Paulo 2026](https://aws.amazon.com/pt/events/summits/sao-paulo/)
- [Agenda oficial](https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/)
- [AWS Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AWS Transform](https://aws.amazon.com/transform/)
