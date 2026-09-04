from __future__ import annotations

import json
import textwrap
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "_work" / "reports"
SESSIONS_JSON = REPORTS / "aws_summit_sp_2026_sessions.json"
MEDIA_JSON = REPORTS / "media_manifest.json"
TRANSCRIPTS_JSON = REPORTS / "transcript_manifest.json"


EVENT_LINKS = {
    "AWS Summit Sao Paulo 2026": "https://aws.amazon.com/pt/events/summits/sao-paulo/",
    "Agenda oficial": "https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/",
    "FAQ oficial": "https://aws.amazon.com/pt/events/summits/sao-paulo/faqs/",
    "Patrocinadores oficiais": "https://aws.amazon.com/pt/events/summits/sao-paulo/sponsors/",
    "Aplicativo do evento": "https://aws.amazon.com/pt/events/summits/mobile-app/",
    "Canal oficial AWS Events no YouTube": "https://www.youtube.com/@AWSEventsChannel",
    "Pesquisa do Summit Sao Paulo 2026 no canal AWS Events": "https://www.youtube.com/@AWSEventsChannel/search?query=AWS%20Summit%20S%C3%A3o%20Paulo%202026",
}


SERVICE_LINKS = {
    "Amazon API Gateway": "https://aws.amazon.com/api-gateway/",
    "Amazon Bedrock": "https://aws.amazon.com/bedrock/",
    "Amazon Bedrock AgentCore": "https://aws.amazon.com/bedrock/agentcore/",
    "Amazon CloudWatch": "https://aws.amazon.com/cloudwatch/",
    "Amazon Connect": "https://aws.amazon.com/connect/",
    "Amazon DocumentDB": "https://aws.amazon.com/documentdb/",
    "Amazon DynamoDB": "https://aws.amazon.com/dynamodb/",
    "Amazon EC2": "https://aws.amazon.com/ec2/",
    "Amazon ECS": "https://aws.amazon.com/ecs/",
    "Amazon EKS": "https://aws.amazon.com/eks/",
    "Amazon EventBridge": "https://aws.amazon.com/eventbridge/",
    "Amazon Kendra": "https://aws.amazon.com/kendra/",
    "Amazon OpenSearch Service": "https://aws.amazon.com/opensearch-service/",
    "Amazon Q Business": "https://aws.amazon.com/q/business/",
    "Amazon Q Developer": "https://aws.amazon.com/q/developer/",
    "Amazon RDS": "https://aws.amazon.com/rds/",
    "Amazon S3": "https://aws.amazon.com/s3/",
    "Amazon SageMaker": "https://aws.amazon.com/sagemaker/",
    "AWS Application Migration Service": "https://aws.amazon.com/application-migration-service/",
    "AWS CloudFormation": "https://aws.amazon.com/cloudformation/",
    "AWS Database Migration Service": "https://aws.amazon.com/dms/",
    "AWS Glue": "https://aws.amazon.com/glue/",
    "AWS Lambda": "https://aws.amazon.com/lambda/",
    "AWS Schema Conversion Tool": "https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html",
    "AWS Step Functions": "https://aws.amazon.com/step-functions/",
    "AWS Transform": "https://aws.amazon.com/transform/",
    "Kiro": "https://kiro.dev/",
    "OpenSearch": "https://aws.amazon.com/opensearch-service/",
}


TAG_LABELS = {
    "ai": "Inteligencia artificial",
    "analytics": "Dados e Analytics",
    "app-integration": "Integracao de aplicacoes",
    "architecture": "Arquitetura",
    "biz-app": "Aplicacoes de negocio",
    "cloud-ops": "Cloud operations",
    "compute": "Computacao",
    "databases": "Bancos de dados",
    "euc-bus-app": "End-user computing",
    "industry": "Industria",
    "migrations": "Migracoes",
    "network-cont-delivery": "Networking e entrega de conteudo",
    "open-source": "Open source",
    "security-compliance": "Seguranca e compliance",
    "serverless": "Serverless",
    "storage": "Storage",
}


LOCAL_EVIDENCE_GROUPS = [
    {
        "title": "Mod-AI, EBA e Working Backwards",
        "photos": ["FOTO-005", "FOTO-006", "FOTO-008", "FOTO-009", "FOTO-019", "FOTO-026", "FOTO-028", "FOTO-036"],
        "sessions": ["MAM311", "MAM310-R", "MAM310-R1", "MAM307", "MAM210"],
        "topics": ["Modernizacao", "AWS Transform", "Kiro", "EBA", "Working Backwards"],
        "note": "Evidencias visuais de jornada de modernizacao com IA: avaliacao, fundamentos, servicos cloud-native, AI-DLC, legado e POC.",
    },
    {
        "title": "AgentCore, contexto, RAG e observabilidade",
        "photos": ["FOTO-037", "FOTO-038", "FOTO-044", "FOTO-046", "FOTO-049", "FOTO-050", "FOTO-053"],
        "sessions": ["AIM202", "AIM206", "AIM312", "DVT202", "DVT203", "AIM309-R", "DVT304-R"],
        "topics": ["Agentic AI", "Amazon Bedrock AgentCore", "RAG", "Observabilidade", "AWS Context"],
        "note": "Evidencias visuais sobre agentes em producao, harness, conhecimento, dados e lacunas de deploy/auditoria/escala.",
    },
    {
        "title": "Governanca, seguranca e AWS Continuum",
        "photos": ["FOTO-051", "FOTO-052", "FOTO-054", "FOTO-055", "FOTO-056"],
        "sessions": ["KEYNOTE", "SEC302", "SEC303", "DVT203", "COP401"],
        "topics": ["Governanca", "Seguranca", "Threat modeling", "Code review", "Code vulnerabilities"],
        "note": "Evidencias visuais reforcando que governanca e seguranca aceleram a entrega quando entram no ciclo de desenvolvimento.",
    },
    {
        "title": "Keynote e mensagens executivas",
        "photos": ["FOTO-055", "FOTO-056", "FOTO-057", "FOTO-060", "FOTO-063", "FOTO-064"],
        "sessions": ["KEYNOTE"],
        "topics": ["Estrategia", "Pessoas", "Processo", "Escala"],
        "note": "Mensagens de keynote: planejar e governar antes de escalar, medir processo alem do codigo e investir em pessoas antes de ferramentas.",
    },
    {
        "title": "Workshop SQL Server com AWS Transform",
        "photos": ["FOTO-081", "FOTO-082", "FOTO-083"],
        "sessions": ["MAM311"],
        "topics": ["SQL Server", "AWS Transform", "Schema conversion", "Database migration", "Amazon ECS", "Amazon EC2"],
        "note": "Evidencias visuais do fluxo de modernizacao: descoberta/assessment, conversao de schema, migracao de banco, transformacao de codigo e deploy.",
    },
    {
        "title": "Ambiente, agenda e sinalizacao do evento",
        "photos": ["FOTO-001", "FOTO-002", "FOTO-073", "FOTO-075", "FOTO-076", "FOTO-077", "FOTO-084", "FOTO-088"],
        "sessions": [],
        "topics": ["Evento", "Agenda", "Networking"],
        "note": "Fotos de contexto para memoria do evento, orientacao de salas e validacao de horarios.",
    },
]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def md_cell(value: Any) -> str:
    return str(value or "").replace("\n", " ").replace("|", "\\|")


def fmt_duration(seconds: Any) -> str:
    if seconds in (None, ""):
        return ""
    seconds = int(float(seconds))
    return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"


def session_by_code(sessions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {session["code"]: session for session in sessions}


def session_link(session: dict[str, Any], from_agenda: bool = False) -> str:
    prefix = "" if from_agenda else "../02-agenda-e-sessoes/"
    rel = session["page_path"].replace("02-agenda-e-sessoes/", "")
    return f"[{md_cell(session['code'])}]({prefix}{rel})"


def media_by_id(media: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in media}


def media_link(item: dict[str, Any], from_page: str = "04") -> str:
    path = item["relative_output_path"].replace("\\", "/")
    if from_page == "04":
        path = path.replace("04-midias-e-evidencias/", "")
    elif from_page == "root":
        path = path
    else:
        path = "../" + path
    return f"[{item['id']}]({path})"


def make_contact_sheets(media: list[dict[str, Any]]) -> list[str]:
    photos = [item for item in media if item.get("type") == "foto"]
    output_dir = ROOT / "04-midias-e-evidencias" / "assets" / "contact-sheets"
    output_dir.mkdir(parents=True, exist_ok=True)
    for old in output_dir.glob("*.jpg"):
        old.unlink()
    if not photos:
        return []

    thumb_w, thumb_h = 420, 300
    label_h = 44
    cols, rows = 3, 3
    sheet_paths: list[str] = []
    for sheet_index in range(0, len(photos), cols * rows):
        chunk = photos[sheet_index : sheet_index + cols * rows]
        canvas = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
        draw = ImageDraw.Draw(canvas)
        for offset, item in enumerate(chunk):
            source = ROOT / item["relative_output_path"]
            if not source.exists():
                continue
            with Image.open(source) as img:
                img = ImageOps.exif_transpose(img).convert("RGB")
                img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                x = (offset % cols) * thumb_w + (thumb_w - img.width) // 2
                y = (offset // cols) * (thumb_h + label_h) + label_h
                canvas.paste(img, (x, y))
            label = f"{item['id']} | faces {item.get('faces_detected', 0)}"
            lx = (offset % cols) * thumb_w + 10
            ly = (offset // cols) * (thumb_h + label_h) + 12
            draw.text((lx, ly), label, fill="black")
        out = output_dir / f"contact-sheet-{len(sheet_paths) + 1:02d}.jpg"
        canvas.save(out, quality=88)
        sheet_paths.append(str(out.relative_to(ROOT)).replace("\\", "/"))
    return sheet_paths


def build_palestrantes(sessions: list[dict[str, Any]]) -> None:
    org_sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    missing = []
    for session in sessions:
        speaker = session.get("speakers", "").strip()
        if not speaker:
            missing.append(session)
            continue
        org_sessions[speaker].append(session)

    lines = [
        "# Palestrantes e contatos",
        "",
        "> Status: revisao comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `creditos`, `palestrantes`",
        "",
        "Esta pagina registra creditos com base no catalogo oficial da AWS. Em muitos itens, o catalogo informa a organizacao responsavel e nao o nome individual do palestrante; por isso, a coluna abaixo usa `Palestrante(s)/organizacao(oes)`.",
        "",
        f"- Sessoes com credito informado no catalogo: {len(sessions) - len(missing)}",
        f"- Sessoes sem credito nominal no catalogo: {len(missing)}",
        "",
        "## Creditos oficiais disponiveis",
        "",
        "| Palestrante/organizacao | Sessoes |",
        "| --- | --- |",
    ]
    for speaker, related in sorted(org_sessions.items(), key=lambda item: (-len(item[1]), item[0].lower())):
        links = ", ".join(session_link(session, from_agenda=True) for session in related)
        lines.append(f"| {md_cell(speaker)} | {links} |")
    lines.extend(
        [
            "",
            "## A complementar",
            "",
            "Quando nomes individuais forem confirmados em slides, LinkedIn, videos oficiais ou materiais publicados pelos palestrantes, adicionar uma linha no formato:",
            "",
            "| Nome | Organizacao | Sessao | Link publico | Observacao |",
            "| --- | --- | --- | --- | --- |",
            "|  |  |  |  |  |",
            "",
            "## Agradecimento",
            "",
            "Obrigado a todos os palestrantes, clientes, parceiros, comunidades e equipes da AWS por compartilhar conhecimento no AWS Summit Sao Paulo 2026.",
        ]
    )
    write("02-agenda-e-sessoes/palestrantes-e-contatos.md", "\n".join(lines))


def build_trilhas(sessions: list[dict[str, Any]]) -> None:
    topic_counts = Counter(topic for session in sessions for topic in session.get("event_topics", []))
    area_counts = Counter(area for session in sessions for area in session.get("areas_of_interest", []))
    location_counts = Counter(session.get("location") or "Nao informado" for session in sessions)
    type_counts = Counter(session.get("session_type") or "Nao informado" for session in sessions)
    level_counts = Counter(session.get("level") or "Nao informado" for session in sessions)

    def table(counter: Counter, labeler=lambda value: value, limit: int | None = None) -> str:
        lines = ["| Item | Sessoes |", "| --- | ---: |"]
        for key, count in counter.most_common(limit):
            lines.append(f"| {md_cell(labeler(key))} | {count} |")
        return "\n".join(lines)

    content = f"""
    # Trilhas e palcos

    > Status: revisao comunitaria
    > Dono: Vitor Ferreira
    > Ultima revisao: 2026-09-04
    > Tags: `aws-summit-2026`, `agenda`, `trilhas`

    Visao consolidada do catalogo oficial da AWS para ajudar consultas por tema, nivel, formato e local.

    ## Por topico oficial

    {table(topic_counts, lambda value: TAG_LABELS.get(value, value))}

    ## Por area de interesse

    {table(area_counts, lambda value: value.replace("-", " ").title(), 20)}

    ## Por nivel

    {table(level_counts)}

    ## Por formato

    {table(type_counts)}

    ## Por palco/local

    {table(location_counts, limit=40)}
    """
    content = textwrap.dedent(content)
    content = "\n".join(line[4:] if line.startswith("    ") else line for line in content.splitlines())
    write("02-agenda-e-sessoes/trilhas-e-palcos.md", content)


def build_media_pages(media: list[dict[str, Any]], transcripts: list[dict[str, Any]]) -> None:
    contact_sheets = make_contact_sheets(media)
    counts = Counter(item.get("type") for item in media)
    total_bytes = sum(int(item.get("size_bytes") or 0) for item in media)
    total_faces = sum(int(item.get("faces_detected") or 0) for item in media)

    lines = [
        "# Indexacao de arquivos",
        "",
        "> Status: revisao comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `midias`, `evidencias`",
        "",
        "Manifesto das midias processadas a partir do ZIP local. Rostos em fotos e videos foram censurados automaticamente antes de entrar nos assets publicaveis.",
        "",
        f"- Total de arquivos processados: {len(media)}",
        f"- Fotos: {counts.get('foto', 0)}",
        f"- Videos: {counts.get('video', 0)}",
        f"- Audios: {counts.get('audio', 0)}",
        f"- Tamanho aproximado dos assets saneados: {total_bytes / 1024 / 1024:.1f} MB",
        f"- Deteccoes automaticas de rosto aplicadas: {total_faces}",
        "",
        "## Aviso de privacidade",
        "",
        "A censura foi feita por deteccao automatica e pode falhar em rostos muito pequenos, virados ou parcialmente ocultos. Antes de tornar o repositorio publico ou reutilizar imagens fora do contexto privado, faca uma revisao humana das fotos e videos.",
        "",
        "## Manifesto",
        "",
        "| ID | Tipo | Arquivo original | Asset saneado | Dimensao/duracao | Rostos detectados | Observacao |",
        "| --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for item in media:
        dims = ""
        if item.get("width") and item.get("height"):
            dims = f"{item['width']}x{item['height']}"
        if item.get("duration_seconds"):
            dims = f"{dims} / {fmt_duration(item['duration_seconds'])}".strip(" /")
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item["id"]),
                    md_cell(item["type"]),
                    md_cell(item.get("original_name")),
                    media_link(item),
                    md_cell(dims),
                    md_cell(item.get("faces_detected", 0)),
                    md_cell(item.get("notes")),
                ]
            )
            + " |"
        )
    write("04-midias-e-evidencias/indexacao-de-arquivos.md", "\n".join(lines))

    photo_lines = [
        "# Fotos",
        "",
        "> Status: revisao comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `fotos`, `evidencias`",
        "",
        "Fotos saneadas e agrupamentos curados para consulta. As folhas de contato abaixo usam as imagens ja censuradas.",
        "",
        "## Folhas de contato",
        "",
    ]
    for sheet in contact_sheets:
        name = Path(sheet).name
        photo_lines.append(f"- [{name}]({sheet.replace('04-midias-e-evidencias/', '')})")
    photo_lines.extend(["", "## Agrupamentos curados", "", "| Grupo | Fotos | Sessoes relacionadas | Observacao |", "| --- | --- | --- | --- |"])
    by_id = media_by_id(media)
    sessions = session_by_code(load_json(SESSIONS_JSON, []))
    for group in LOCAL_EVIDENCE_GROUPS:
        photo_links = ", ".join(media_link(by_id[photo_id]) for photo_id in group["photos"] if photo_id in by_id)
        related_links = ", ".join(session_link(sessions[code]) for code in group["sessions"] if code in sessions)
        photo_lines.append(f"| {md_cell(group['title'])} | {photo_links} | {related_links or 'Contexto geral'} | {md_cell(group['note'])} |")
    write("04-midias-e-evidencias/fotos.md", "\n".join(photo_lines))

    av_lines = [
        "# Videos e gravacoes",
        "",
        "> Status: revisao comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `videos`, `audios`, `gravacoes`",
        "",
        "Videos saneados e audios preservados para apoio as transcricoes. Use o material como evidencia interna e revise qualquer trecho antes de citar publicamente.",
        "",
        "## Videos",
        "",
        "| ID | Arquivo | Duracao | Rostos detectados | Observacao |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for item in media:
        if item.get("type") == "video":
            av_lines.append(f"| {item['id']} | {media_link(item)} | {fmt_duration(item.get('duration_seconds'))} | {item.get('faces_detected', 0)} | {md_cell(item.get('notes'))} |")
    av_lines.extend(["", "## Audios", "", "| ID | Arquivo | Duracao | Observacao |", "| --- | --- | --- | --- |"])
    for item in media:
        if item.get("type") == "audio":
            av_lines.append(f"| {item['id']} | {media_link(item)} | {fmt_duration(item.get('duration_seconds'))} | {md_cell(item.get('notes'))} |")
    av_lines.extend(
        [
            "",
            "## Gravacoes publicas",
            "",
            "- [Canal oficial AWS Events no YouTube](https://www.youtube.com/@AWSEventsChannel)",
            "- [Pesquisa por AWS Summit Sao Paulo 2026 no canal oficial](https://www.youtube.com/@AWSEventsChannel/search?query=AWS%20Summit%20S%C3%A3o%20Paulo%202026)",
            "- [Tabela de videos, creditos e minutagens](../06-referencias/bibliografia-e-leituras.md#gravacoes-publicas-e-youtube)",
            "",
            "Verificacao realizada em 2026-09-04: ainda nao foi localizada gravacao oficial do evento de Sao Paulo. Os videos oficiais de outros Summits devem ser tratados apenas como contexto, nunca como substitutos das gravacoes locais. Nao foram encontrados comentarios oficiais com minutagens para o evento de Sao Paulo nessa data.",
            "",
            "As minutagens das transcricoes locais estao nos arquivos de [transcricao automatica](transcricoes.md) e precisam de revisao por escuta manual.",
        ]
    )
    write("04-midias-e-evidencias/videos-e-gravacoes.md", "\n".join(av_lines))

    tr_lines = [
        "# Transcricoes",
        "",
        "> Status: transcricoes automaticas; revisao humana pendente",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `transcricoes`, `audio`",
        "",
        "Indice das transcricoes automaticas geradas localmente. Revise nomes proprios, numeros, siglas e servicos antes de usar como citacao.",
        "",
        "| ID | Origem | Transcricao | Duracao | Idioma | Caracteres |",
        "| --- | --- | --- | --- | --- | ---: |",
    ]
    if transcripts:
        for item in transcripts:
            source = item["source"].replace("04-midias-e-evidencias", "").lstrip("\\/").replace("\\", "/")
            output = item["output_markdown"].replace("04-midias-e-evidencias", "").lstrip("\\/").replace("\\", "/")
            tr_lines.append(f"| {item['id']} | [{Path(source).name}]({source}) | [{Path(output).name}]({output}) | {fmt_duration(item.get('duration_seconds'))} | {item.get('language', 'pt')} ({float(item.get('language_probability') or 0):.2f}) | {item.get('text_chars', 0)} |")
    else:
        tr_lines.append("| Aguardando |  |  |  |  |  |")
    write("04-midias-e-evidencias/transcricoes.md", "\n".join(tr_lines))


def build_insight_pages(sessions: list[dict[str, Any]], media: list[dict[str, Any]]) -> None:
    topic_counts = Counter(topic for session in sessions for topic in session.get("event_topics", []))
    total = len(sessions)
    ai_count = topic_counts.get("ai", 0)
    migration_count = topic_counts.get("migrations", 0)
    security_count = topic_counts.get("security-compliance", 0)
    serverless_count = topic_counts.get("serverless", 0)
    analytics_count = topic_counts.get("analytics", 0)

    write(
        "01-resumo-executivo/principais-insights.md",
        f"""
        # Principais insights

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `insights`, `resumo-executivo`

        ## Leitura rapida

        - IA foi o eixo dominante do evento: {ai_count} de {total} sessoes do catalogo oficial estavam marcadas com o topico de inteligencia artificial.
        - Modernizacao apareceu como tema pratico, nao apenas tecnologico: as evidencias locais mostram EBA, Working Backwards, inventario orientado a decisao, AWS Transform, Kiro e POCs.
        - Agentes em producao exigem uma camada operacional propria: contexto, identidade, memoria, ferramentas, observabilidade, auditoria, escala e controles de seguranca.
        - O keynote reforcou tres mensagens executivas: planejar/governar antes de escalar, medir o processo alem do codigo e investir em pessoas antes de ferramentas.
        - Dados, analytics e RAG aparecem como fundacao de agentes: conhecimento gerenciado, dados publicos, dados nao estruturados e dados estruturados precisam entrar em um desenho governado.

        ## Numeros uteis do catalogo oficial

        | Tema | Sessoes |
        | --- | ---: |
        | Inteligencia artificial | {ai_count} |
        | Dados e analytics | {analytics_count} |
        | Migracoes/modernizacao | {migration_count} |
        | Serverless | {serverless_count} |
        | Seguranca e compliance | {security_count} |

        ## Evidencias locais mais fortes

        | Evidencia | O que mostra | Pagina relacionada |
        | --- | --- | --- |
        | Fotos 005-036 | Mod-AI, EBA, Working Backwards, ISV tools e anti-patterns de modernizacao | [Arquitetura e Modernizacao](../03-topicos/arquitetura-modernizacao.md) |
        | Fotos 037-054 | AgentCore, AWS Context, Managed Knowledge Base, Web Search, AWS Continuum e seguranca | [Generative AI e Machine Learning](../03-topicos/generative-ai-machine-learning.md) |
        | Fotos 055-064 | Mensagens executivas e keynote | [Sumario para lideranca](sumario-para-lideranca.md) |
        | Fotos 081-083 | Workshop de SQL Server com AWS Transform | [MAM311](../02-agenda-e-sessoes/sessoes/mam311-acelerando-a-modernizacao-de-net-e-sql-server-com-ia-agentica.md) |
        """,
    )

    write(
        "01-resumo-executivo/mapa-de-temas.md",
        """
        # Mapa de temas

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `mapa`, `temas`

        ```mermaid
        flowchart LR
          evento[AWS Summit Sao Paulo 2026] --> ia[IA agentica e generativa]
          evento --> modernizacao[Modernizacao com IA]
          evento --> dados[Dados, analytics e RAG]
          evento --> plataforma[Serverless, containers e plataforma]
          evento --> seguranca[Seguranca, governanca e compliance]

          ia --> agentcore[Amazon Bedrock AgentCore]
          ia --> bedrock[Amazon Bedrock]
          ia --> context[AWS Context / Knowledge Bases]
          ia --> observabilidade[Observabilidade de agentes]

          modernizacao --> transform[AWS Transform]
          modernizacao --> kiro[Kiro]
          modernizacao --> eba[EBA / Working Backwards]
          modernizacao --> isv[ISV tools]

          dados --> rag[RAG e busca vetorial]
          dados --> opensearch[OpenSearch]
          dados --> s3[S3 / dados estruturados e nao estruturados]

          plataforma --> lambda[AWS Lambda]
          plataforma --> stepfunctions[AWS Step Functions]
          plataforma --> ecs[Amazon ECS]
          plataforma --> eks[Amazon EKS]

          seguranca --> identity[Identidade e acesso para agentes]
          seguranca --> continuum[AWS Continuum]
          seguranca --> threat[Threat modeling / code review]
        ```
        """,
    )

    write(
        "01-resumo-executivo/recomendacoes.md",
        """
        # Recomendacoes

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `recomendacoes`, `acoes`

        ## Para lideranca

        - Tratar IA agentica como programa de mudanca, nao como ferramenta isolada: definir governanca, criterios de risco, medicao de processo e capacitacao.
        - Priorizar um caso de uso com dado disponivel, dono de negocio e resultado mensuravel antes de expandir para varios agentes.
        - Usar Working Backwards para conectar modernizacao a valor de negocio antes de escolher ferramenta.

        ## Para arquitetura e plataforma

        - Criar uma landing zone de agentes com identidade, logs, auditoria, avaliacao, custos, limites e observabilidade desde o primeiro experimento.
        - Desenhar a arquitetura de conhecimento antes do prompt: fontes, frescor, classificacao, qualidade, permissao e rastreabilidade.
        - Em modernizacao, transformar inventario em mapa decisorio: criticidade, dependencias, custos, riscos, dados, donos e ondas.

        ## Para engenharia

        - Experimentar um fluxo de AI-DLC com Kiro/Amazon Q Developer/AWS Transform em uma aplicacao de baixo risco.
        - Medir lead time, taxa de retrabalho, cobertura de teste, custo por execucao e incidentes, nao apenas linhas de codigo geradas.
        - Validar guardrails de seguranca para agentes antes de permitir acoes em sistemas produtivos.
        """,
    )


def build_topic_pages() -> None:
    write(
        "03-topicos/arquitetura-modernizacao.md",
        f"""
        # Arquitetura e Modernizacao

        > Status: revisao comunitaria
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

        - [AWS Transform]({SERVICE_LINKS["AWS Transform"]})
        - [AWS Database Migration Service]({SERVICE_LINKS["AWS Database Migration Service"]})
        - [AWS Schema Conversion Tool]({SERVICE_LINKS["AWS Schema Conversion Tool"]})
        - [AWS Application Migration Service]({SERVICE_LINKS["AWS Application Migration Service"]})
        """,
    )

    write(
        "03-topicos/generative-ai-machine-learning.md",
        f"""
        # Generative AI e Machine Learning

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `genai`, `agentic-ai`, `bedrock`

        ## Insights

        - Agentic AI foi o tema mais recorrente do catalogo oficial e das evidencias locais.
        - Amazon Bedrock AgentCore aparece como pilar para construir, conectar, proteger, observar e escalar agentes.
        - Conhecimento e contexto sao parte da arquitetura: Managed Knowledge Base, web search governado, memoria e dados estruturados/nao estruturados.
        - O desafio de producao nao e apenas modelo: envolve logica, contexto, seguranca, deploy, auditoria e escala.

        ## Arquitetura conceitual de agentes

        ```mermaid
        flowchart TD
          usuario[Usuario ou sistema] --> gateway[Gateway/API]
          gateway --> agente[Agente]
          agente --> modelo[Modelo/foundation model]
          agente --> contexto[Contexto e memoria]
          contexto --> kb[Knowledge bases / RAG]
          contexto --> dados[Dados publicos, nao estruturados e estruturados]
          agente --> ferramentas[Tools e acoes]
          agente --> identidade[Identidade e permissoes]
          agente --> obs[Observabilidade e auditoria]
          obs --> avaliacao[Avaliacao e melhoria]
        ```

        ## Evidencias locais

        - Fotos 037-054 em [Fotos](../04-midias-e-evidencias/fotos.md#agrupamentos-curados)
        - Sessoes relacionadas: [AIM202](../02-agenda-e-sessoes/sessoes/aim202-democratizacao-governada-de-agentes-de-ia-com-amazon-bedrock-agentcore.md), [DVT203](../02-agenda-e-sessoes/sessoes/dvt203-debug-mais-rapido-governe-melhor-ai-dlc-e-observabilidade.md)

        ## Referencias oficiais

        - [Amazon Bedrock]({SERVICE_LINKS["Amazon Bedrock"]})
        - [Amazon Bedrock AgentCore]({SERVICE_LINKS["Amazon Bedrock AgentCore"]})
        - [Amazon Q Developer]({SERVICE_LINKS["Amazon Q Developer"]})
        - [Amazon SageMaker]({SERVICE_LINKS["Amazon SageMaker"]})
        """,
    )

    write(
        "03-topicos/seguranca-identidade-compliance.md",
        """
        # Seguranca, Identidade e Compliance

        > Status: revisao comunitaria
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
        """,
    )

    write(
        "03-topicos/devops-platform-engineering.md",
        f"""
        # DevOps e Platform Engineering

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `devops`, `platform-engineering`, `ai-dlc`

        ## Insights

        - AI-DLC amplia o SDLC: agentes passam a apoiar entendimento, planejamento, codificacao, teste, revisao, deploy e operacao.
        - Kiro e Amazon Q Developer entram como ferramentas de especificacao, desenvolvimento assistido e reducao de divida tecnica.
        - A recomendacao executiva foi medir o processo, nao apenas o codigo gerado.

        ## Fluxo AI-DLC sugerido

        ```mermaid
        flowchart LR
          ideacao[Ideia / problema] --> spec[Spec e criterios]
          spec --> decomposicao[Decomposicao em tarefas]
          decomposicao --> codigo[Codigo assistido]
          codigo --> testes[Testes e avaliacao]
          testes --> review[Code review e seguranca]
          review --> deploy[Deploy]
          deploy --> operacao[Observabilidade]
          operacao --> melhoria[Backlog de melhoria]
        ```

        ## Referencias oficiais

        - [Amazon Q Developer]({SERVICE_LINKS["Amazon Q Developer"]})
        - [AWS Transform]({SERVICE_LINKS["AWS Transform"]})
        - [Kiro]({SERVICE_LINKS["Kiro"]})
        """,
    )

    write(
        "03-topicos/dados-analytics.md",
        f"""
        # Dados e Analytics

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `dados`, `analytics`, `rag`

        ## Insights

        - A qualidade do agente depende da qualidade do contexto: dados publicos, nao estruturados e estruturados precisam de governanca.
        - RAG e busca vetorial aparecem como padroes para transformar conhecimento corporativo em resposta confiavel.
        - Dados para modernizacao tambem importam: dependencias, custos, proprietarios e telemetria orientam priorizacao.

        ## Referencias oficiais

        - [Amazon Bedrock]({SERVICE_LINKS["Amazon Bedrock"]})
        - [Amazon OpenSearch Service]({SERVICE_LINKS["Amazon OpenSearch Service"]})
        - [Amazon S3]({SERVICE_LINKS["Amazon S3"]})
        - [AWS Glue]({SERVICE_LINKS["AWS Glue"]})
        """,
    )

    write(
        "03-topicos/serverless-containers-kubernetes.md",
        f"""
        # Serverless, Containers e Kubernetes

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `serverless`, `containers`, `kubernetes`

        ## Insights

        - Serverless e containers aparecem como fundacao de modernizacao e execucao de workloads agenticos.
        - Slides do Mod-AI citam Lambda, Step Functions, EventBridge, ECS/EKS, API Gateway e bancos gerenciados como blocos cloud-native.
        - A decisao entre serverless, ECS e EKS deve considerar modelo operacional, escala, equipe, integracao e padroes de deploy.

        ## Referencias oficiais

        - [AWS Lambda]({SERVICE_LINKS["AWS Lambda"]})
        - [AWS Step Functions]({SERVICE_LINKS["AWS Step Functions"]})
        - [Amazon EventBridge]({SERVICE_LINKS["Amazon EventBridge"]})
        - [Amazon ECS]({SERVICE_LINKS["Amazon ECS"]})
        - [Amazon EKS]({SERVICE_LINKS["Amazon EKS"]})
        - [Amazon API Gateway]({SERVICE_LINKS["Amazon API Gateway"]})
        """,
    )


def build_knowledge_pages() -> None:
    write(
        "05-conhecimento-compartilhado/padroes-e-boas-praticas.md",
        """
        # Padroes e boas praticas

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `boas-praticas`

        - Comece por objetivo de negocio e criterios de sucesso antes de escolher ferramenta.
        - Planeje governanca e seguranca antes de escalar agentes.
        - Trate contexto, memoria e dados como componentes arquiteturais.
        - Use POCs pequenas para validar valor, risco, custo e operabilidade.
        - Em modernizacao, priorize ondas por dependencias, valor, risco e prontidao, nao so por inventario.
        - Meça o processo de engenharia: lead time, retrabalho, incidentes, teste, revisao e custo.
        """,
    )
    write(
        "05-conhecimento-compartilhado/riscos-e-alertas.md",
        """
        # Riscos e alertas

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `riscos`

        | Risco | Sinal de alerta | Mitigacao |
        | --- | --- | --- |
        | Agente com permissao ampla | Uso de credenciais compartilhadas ou `AdministratorAccess` | IAM granular, ambientes separados, aprovacao humana para acoes sensiveis |
        | RAG sem governanca | Fontes duplicadas, antigas ou sem dono | Catalogo, classificacao, freshness e controles de acesso |
        | Modernizacao por inventario | Lista grande de servidores sem criterio de negocio | Priorizacao por valor, dependencia, risco e dados |
        | POC sem caminho para producao | Demo funciona, mas nao ha observabilidade/custo/seguranca | Definir landing zone, SLOs, guardrails e ownership desde o inicio |
        | IA como substituta de processo | Medicao apenas de codigo gerado | Medir fluxo completo e qualidade operacional |
        """,
    )
    write(
        "05-conhecimento-compartilhado/oportunidades-para-pocs.md",
        """
        # Oportunidades para POCs

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `poc`, `ideias`

        | POC | Hipotese | Evidencia do Summit | Criterio de sucesso |
        | --- | --- | --- | --- |
        | Modernizacao assistida de aplicacao .NET/SQL Server | AWS Transform/Kiro reduzem tempo de assessment e transformacao | Fotos 081-083, sessao MAM311 | Plano de ondas + app migrada em ambiente controlado |
        | Agente RAG governado | AgentCore + knowledge base entregam resposta rastreavel com controles | Fotos 044-053, sessoes AIM202/AIM312 | Respostas com fontes, logs e controle de acesso |
        | Observabilidade de agente | Telemetria reduz tempo de debug e auditoria | Fotos 050-052, sessao DVT203 | Dashboard com tool calls, custo, latencia e falhas |
        | AI-DLC em equipe piloto | Fluxo assistido melhora lead time sem perder qualidade | Fotos 037, 055-056 | Lead time menor com teste/review preservados |
        """,
    )


def build_reference_pages() -> None:
    links_lines = [
        "# Links oficiais",
        "",
        "> Status: referencia comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `referencias`, `aws`",
        "",
        "## Evento",
        "",
    ]
    for label, url in EVENT_LINKS.items():
        links_lines.append(f"- [{label}]({url})")
    links_lines.extend(["", "## Servicos e materiais tecnicos", ""])
    for label, url in sorted(SERVICE_LINKS.items()):
        links_lines.append(f"- [{label}]({url})")
    links_lines.extend(
        [
            "",
            "## Midias publicas",
            "",
            "Mantenha aqui links publicos oficiais ou de palestrantes/parceiros sobre o evento. Preferir link e credito em vez de re-hospedar imagens de redes sociais sem licenca explicita.",
            "",
            "| Titulo | Autor/organizacao | Link | Observacao |",
            "| --- | --- | --- | --- |",
            "| AWS Summit Sao Paulo 2026 | AWS | [Pagina oficial](https://aws.amazon.com/pt/events/summits/sao-paulo/) | Fonte principal do evento |",
            "| Agenda AWS Summit Sao Paulo 2026 | AWS | [Agenda oficial](https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/) | Fonte do catalogo de sessoes |",
        ]
    )
    write("06-referencias/links-oficiais.md", "\n".join(links_lines))

    write(
        "06-referencias/glossario.md",
        """
        # Glossario

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
        > Ultima revisao: 2026-09-04
        > Tags: `aws-summit-2026`, `glossario`

        | Termo | Definicao de trabalho | Ver tambem |
        | --- | --- | --- |
        | Agentic AI | Sistemas de IA que planejam, usam ferramentas, mantem contexto e executam acoes com algum grau de autonomia. | [Amazon Bedrock AgentCore](servicos-aws-citados.md) |
        | AI-DLC | Ciclo de desenvolvimento assistido por IA, cobrindo descoberta, especificacao, codigo, teste, revisao, deploy e operacao. | [DevOps e Platform Engineering](../03-topicos/devops-platform-engineering.md) |
        | Amazon Bedrock | Servico AWS para criar e escalar aplicacoes de IA generativa com foundation models. | [Amazon Bedrock](https://aws.amazon.com/bedrock/) |
        | Amazon Bedrock AgentCore | Conjunto de capacidades para criar, conectar, proteger, observar e escalar agentes. | [AgentCore](https://aws.amazon.com/bedrock/agentcore/) |
        | AWS Transform | Servico/familia de capacidades AWS para acelerar modernizacao e transformacao de workloads com IA. | [AWS Transform](https://aws.amazon.com/transform/) |
        | EBA | Experience-Based Acceleration; abordagem imersiva para acelerar transformacao e criar capacidade organizacional. | [Arquitetura e Modernizacao](../03-topicos/arquitetura-modernizacao.md) |
        | Kiro | IDE/ferramenta orientada a especificacoes para desenvolvimento assistido por IA. | [Kiro](https://kiro.dev/) |
        | MCP | Model Context Protocol; padrao para conectar modelos/agentes a ferramentas, dados e contexto. | [Generative AI](../03-topicos/generative-ai-machine-learning.md) |
        | RAG | Retrieval-Augmented Generation; padrao que recupera conhecimento externo para fundamentar respostas de modelos. | [Dados e Analytics](../03-topicos/dados-analytics.md) |
        | Working Backwards | Metodo de partir do resultado desejado para identificar dependencias, capacidades e caminho de execucao. | [Modernizacao](../03-topicos/arquitetura-modernizacao.md) |
        | AWS Continuum | Termo usado nos slides para capacidades de seguranca no fluxo de desenvolvimento, como pentest, code review, threat modeling e vulnerabilidades. | [Seguranca](../03-topicos/seguranca-identidade-compliance.md) |
        | Guardrails | Controles que restringem comportamento, dados, permissoes ou saidas de um sistema de IA/agente. | [Seguranca](../03-topicos/seguranca-identidade-compliance.md) |
        | Landing zone de agentes | Fundacao operacional para agentes: identidade, rede, logs, auditoria, observabilidade, custos e politicas. | [Generative AI](../03-topicos/generative-ai-machine-learning.md) |
        """,
    )

    write(
        "06-referencias/arquitetura-de-referencia.md",
        """
        # Arquitetura de referencia

        > Status: revisao comunitaria
        > Dono: Vitor Ferreira
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
        """,
    )


def patch_selected_session_pages(sessions: list[dict[str, Any]], media: list[dict[str, Any]]) -> None:
    sessions_map = session_by_code(sessions)
    media_map = media_by_id(media)
    for group in LOCAL_EVIDENCE_GROUPS:
        for code in group["sessions"]:
            session = sessions_map.get(code)
            if not session:
                continue
            page = ROOT / session["page_path"]
            if not page.exists():
                continue
            text = page.read_text(encoding="utf-8")
            rows = []
            for photo_id in group["photos"]:
                item = media_map.get(photo_id)
                if item:
                    rel = "../../" + item["relative_output_path"].replace("\\", "/")
                    rows.append(f"| [{photo_id}]({rel}) | foto | {md_cell(group['title'])}: {md_cell(group['note'])} |")
            evidence = "\n".join(
                [
                    "## Evidencias locais",
                    "",
                    "Associacao automatica por conteudo visual, agenda e temas. Validar manualmente antes de citar como evidencia final da sessao.",
                    "",
                    "| Evidencia | Tipo | Observacao |",
                    "| --- | --- | --- |",
                    *rows,
                    "",
                    "## Insights",
                ]
            )
            text = text.replace(
                "## Evidencias locais\n\nAinda nao ha evidencias locais associadas a esta sessao. Quando houver, adicione links no indice de midias e nesta pagina.\n\n| Evidencia | Tipo | Observacao |\n| --- | --- | --- |\n|  |  |  |\n\n## Insights",
                evidence,
            )
            page.write_text(text, encoding="utf-8")


def main() -> int:
    sessions = load_json(SESSIONS_JSON, [])
    media = load_json(MEDIA_JSON, [])
    transcripts = load_json(TRANSCRIPTS_JSON, [])
    build_palestrantes(sessions)
    build_trilhas(sessions)
    build_media_pages(media, transcripts)
    build_insight_pages(sessions, media)
    build_topic_pages()
    build_knowledge_pages()
    build_reference_pages()
    patch_selected_session_pages(sessions, media)
    print(f"updated wiki summaries from {len(sessions)} sessions, {len(media)} media items and {len(transcripts)} transcripts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
