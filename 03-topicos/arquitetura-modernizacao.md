# Arquitetura e Modernizacao

> Status: Em revisao
> Dono: Vitor Ferreira
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `modernizacao`, `aws-transform`, `kiro`

## Insights

- Modernizacao com IA precisa comecar por objetivo, maturidade, portfolio, target stacks e criterios de decisao.
- O material local reforca EBA e Working Backwards como mecanismos para alinhar negocio, engenharia e arquitetura.
- Inventario sozinho nao e plano: faltam dependencias, contexto de negocio, decisao de dados e cronograma de ondas.
- AWS Transform e ferramentas de ISV aparecem como aceleradores complementares para discovery, assessment, migracao, modernizacao e orquestracao.

## Fluxo recomendado

```mermaid
flowchart LR
  objetivo[Objetivo de negocio] --> maturidade[Maturidade e portfolio]
  maturidade --> decisao[Decisao de modernizar primeiro]
  decisao --> arquitetura[Fundamentos de arquitetura moderna]
  arquitetura --> ferramentas[AWS Transform + Kiro + ISVs]
  ferramentas --> poc[POC com criterios de sucesso]
  poc --> ondas[Roadmap em ondas]
  ondas --> producao[Operacao e melhoria continua]
```

## Evidencias locais

- [Grupo Mod-AI/EBA](../04-midias-e-evidencias/fotos.md#agrupamentos-curados)
- [Workshop SQL Server com AWS Transform](../04-midias-e-evidencias/fotos.md#agrupamentos-curados)
- Sessao relacionada: [MAM311](../02-agenda-e-sessoes/sessoes/mam311-acelerando-a-modernizacao-de-net-e-sql-server-com-ia-agentica.md)

## Referencias oficiais

- [AWS Transform](https://aws.amazon.com/transform/)
- [AWS Database Migration Service](https://aws.amazon.com/dms/)
- [AWS Schema Conversion Tool](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html)
- [AWS Application Migration Service](https://aws.amazon.com/application-migration-service/)

