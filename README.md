# AWS Summit 2026 - Wiki de Conhecimento

Esta wiki foi criada para organizar anotacoes, fotos, gravacoes, transcricoes, referencias e insights do AWS Summit 2026 em Markdown simples, legivel no GitHub e no Azure DevOps.

O projeto tem finalidade exclusivamente comunitaria e sem fins lucrativos: registrar aprendizados, melhorar a experiencia de consulta e compartilhar conhecimento com a comunidade AWS e interessados. Veja a [licenca de uso comunitario](LICENSE.md).

Use a [Home](Home.md) como ponto de entrada principal. O repositorio foi publicado para facilitar a consulta e o compartilhamento gratuito de conhecimento.

## Status publico

Base em construcao: o catalogo oficial esta completo, enquanto insights, evidencias e creditos passam por curadoria progressiva.

Por prudencia de privacidade e direitos autorais, os arquivos locais de audio, foto, video, folhas de contato e transcricoes automaticas foram retirados da versao publica e do historico Git. A wiki preserva o inventario, as contagens e os IDs de evidencias para reintroducao futura somente apos revisao humana, autorizacao de uso e validacao editorial.

## Autoria e citacao

Projeto mantido e curado por [Vitor Ferreira](https://github.com/VitorFerreiraVHF). Ao reutilizar esta base, preserve os creditos e aponte para este repositorio. Um registro estruturado para citacao esta em [CITATION.cff](CITATION.cff).

Contribuicoes seguem o [guia de contribuicao](CONTRIBUTING.md).

## Transparencia da publicacao

- O catalogo e os metadados de sessoes vem da [agenda oficial da AWS](https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/).
- Insights, organizacao, transcricoes e associacoes com fotos sao curadoria comunitaria de Vitor Ferreira e nao representam a AWS.
- Fotos e videos locais nao estao publicados nesta versao publica; eles exigem revisao humana antes de qualquer reintroducao.
- Audios locais e transcricoes automaticas derivadas nao estao publicados nesta versao publica; confirme autorizacao e revise trechos antes de divulgar como citacao.
- Materiais de terceiros continuam sujeitos aos direitos de seus titulares. Consulte a [licenca](LICENSE.md) e os creditos de cada fonte.

## Legenda editorial

| Status | Significado |
| --- | --- |
| `Oficial` | Informacao vinda de fonte oficial AWS ou documentacao do servico. |
| `Automatico` | Conteudo gerado por automacao, transcricao ou associacao inicial; requer revisao humana. |
| `Em revisao` | Conteudo em curadoria, com pendencias de credito, privacidade, autorizacao ou validacao tecnica. |
| `Validado` | Conteudo conferido manualmente e adequado para divulgacao no escopo indicado. |

## Status da base

- [Catalogo oficial AWS](02-agenda-e-sessoes/catalogo-oficial-aws.md) com 182 sessoes importadas.
- [Paginas por sessao](02-agenda-e-sessoes/sessoes.md) geradas para receber evidencias, insights e agradecimentos.
- [Inventario de midias locais](04-midias-e-evidencias/indexacao-de-arquivos.md): 98 fotos, 5 videos, 3 audios e 8 transcricoes foram processados localmente, mas os arquivos nao estao publicados.
- [Principais insights](01-resumo-executivo/principais-insights.md), [glossario](06-referencias/glossario.md), [links oficiais](06-referencias/links-oficiais.md) e fluxos Mermaid incluidos.
- [Gravacoes publicas e minutagens](06-referencias/bibliografia-e-leituras.md#gravacoes-publicas-e-youtube) verificadas no canal oficial AWS Events.

## Entrada rapida

- [Home](Home.md)
- [Como usar a wiki](00-como-usar.md)
- [Resumo executivo](01-resumo-executivo.md)
- [Agenda e sessoes](02-agenda-e-sessoes.md)
- [Topicos](03-topicos.md)
- [Midias e evidencias](04-midias-e-evidencias.md)
- [Conhecimento compartilhado](05-conhecimento-compartilhado.md)
- [Referencias](06-referencias.md)
- [Acoes e follow-up](07-acoes-e-follow-up.md)
- [Templates](templates.md)

## Objetivo

Transformar o material coletado no evento em uma base consultavel de conhecimento:

- separar conteudo por trilha, sessao, topico e impacto;
- conectar referencias oficiais, anotacoes e evidencias validadas aos insights extraidos;
- registrar recomendacoes, riscos, oportunidades e proximas acoes;
- facilitar compartilhamento com lideranca, times tecnicos e comunidades internas.

## Compatibilidade

- GitHub: `README.md` funciona como pagina inicial do repositorio. Se usar GitHub Wiki, `Home.md` e `_Sidebar.md` tambem serao reconhecidos.
- Azure DevOps Wiki: `Home.md` pode ser usado como entrada e os arquivos `.order` ajudam a definir a ordem das paginas.
- Links: todos os links usam caminhos relativos, evitando dependencias de uma plataforma especifica.
- Markdown: a estrutura evita recursos proprietarios para manter a leitura simples em ambos os ambientes.

## Fluxo recomendado

1. Cadastre cada palestra em [catalogo de sessoes](02-agenda-e-sessoes/catalogo-de-sessoes.md).
2. Registre fotos, videos e transcricoes no indice de [midias e evidencias](04-midias-e-evidencias/indexacao-de-arquivos.md), mantendo os arquivos fora do Git publico ate a revisao.
3. Extraia insights usando o [template de insight](templates/insight.md).
4. Consolide aprendizados nos [topicos](03-topicos.md).
5. Leve recomendacoes e iniciativas para [acoes e follow-up](07-acoes-e-follow-up.md).
