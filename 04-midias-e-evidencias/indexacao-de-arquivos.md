# Indexacao de arquivos

> Status: Em revisao
> Dono: Vitor Ferreira
> Ultima revisao: 2026-09-04
> Tags: `aws-summit-2026`, `midias`, `evidencias`, `privacidade`

Este manifesto registra o volume de midias processadas a partir do ZIP local, sem publicar os arquivos no repositorio.

Por prudencia de privacidade, direitos de imagem, direitos de voz e direitos sobre materiais de terceiros, os assets locais foram removidos da versao publica e do historico Git em 2026-09-04. A reintroducao deve acontecer somente apos revisao humana, autorizacao de uso e validacao editorial.

## Resumo do processamento local

| Tipo | Quantidade | Status publico | Observacao |
| --- | ---: | --- | --- |
| Fotos | 98 | Retiradas temporariamente | Versoes censuradas existem em backup local, mas exigem revisao humana antes de republicacao. |
| Videos | 5 | Retirados temporariamente | Versoes censuradas existem em backup local, mas podem conter pessoas, marcas e falas. |
| Audios | 3 | Retirados temporariamente | Vozes foram preservadas nos arquivos originais; publicacao depende de autorizacao. |
| Transcricoes automaticas | 8 | Retiradas temporariamente | Conteudo derivado de audio/video, sujeito a erro e a direitos de terceiros. |
| Folhas de contato | 11 | Retiradas temporariamente | Resumos visuais das fotos, tambem sujeitos a privacidade. |
| Deteccoes automaticas de rosto | 3454 | Inventario apenas | Numero do pipeline local; nao substitui revisao humana. |
| Tamanho aproximado dos assets saneados | 95,2 MB | Fora do Git publico | Manter em armazenamento privado ate validacao. |

## Criterios para republicar

- Confirmar que nao ha rostos identificaveis sem autorizacao.
- Confirmar que audios, falas e transcricoes podem ser compartilhados no escopo desejado.
- Remover informacoes pessoais, credenciais, QR codes sensiveis, telas internas e dados confidenciais.
- Dar credito aos palestrantes, empresas, AWS e fontes originais.
- Marcar cada item como `Validado` apenas depois de revisao humana.

## Inventario resumido

| ID ou faixa | Tipo | Status | Proxima acao |
| --- | --- | --- | --- |
| FOTO-001 a FOTO-098 | foto | Em revisao, arquivo nao publicado | Revisar privacidade e direitos de imagem. |
| VID-001 a VID-005 | video | Em revisao, arquivo nao publicado | Revisar frames, falas, marcas e contexto. |
| AUD-001 a AUD-003 | audio | Em revisao, arquivo nao publicado | Confirmar autorizacao de voz e conteudo. |
| Transcricoes AUD-001 a AUD-003 | transcricao | Automatico, arquivo nao publicado | Fazer escuta humana e publicar apenas trechos permitidos. |
| Transcricoes VID-001 a VID-005 | transcricao | Automatico, arquivo nao publicado | Revisar utilidade e permissao antes de publicar. |
