from __future__ import annotations

import csv
import html
import json
import re
import unicodedata
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "_work" / "reports"
AGENDA_HTML = REPORTS / "aws-agenda-page.html"
FULL_AGENDA_JSON = REPORTS / "aws_dirs_items_search_full_browser.json"
SESSIONS_DIR = ROOT / "02-agenda-e-sessoes" / "sessoes"
OFFICIAL_URL = "https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/"


TOPIC_MAP = {
    "ai": ("Generative AI e Machine Learning", "../../03-topicos/generative-ai-machine-learning.md"),
    "analytics": ("Dados e Analytics", "../../03-topicos/dados-analytics.md"),
    "app-integration": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
    "architecture": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
    "biz-app": ("Casos de Uso por Industria", "../../03-topicos/casos-de-uso-industria.md"),
    "cloud-ops": ("Observabilidade e Operacoes", "../../03-topicos/observabilidade-operacoes.md"),
    "compute": ("Serverless, Containers e Kubernetes", "../../03-topicos/serverless-containers-kubernetes.md"),
    "containers": ("Serverless, Containers e Kubernetes", "../../03-topicos/serverless-containers-kubernetes.md"),
    "databases": ("Dados e Analytics", "../../03-topicos/dados-analytics.md"),
    "euc-bus-app": ("Casos de Uso por Industria", "../../03-topicos/casos-de-uso-industria.md"),
    "industry": ("Casos de Uso por Industria", "../../03-topicos/casos-de-uso-industria.md"),
    "migration": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
    "migrations": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
    "network-cont-delivery": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
    "networking": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
    "open-source": ("Serverless, Containers e Kubernetes", "../../03-topicos/serverless-containers-kubernetes.md"),
    "security": ("Seguranca, Identidade e Compliance", "../../03-topicos/seguranca-identidade-compliance.md"),
    "security-compliance": ("Seguranca, Identidade e Compliance", "../../03-topicos/seguranca-identidade-compliance.md"),
    "serverless": ("Serverless, Containers e Kubernetes", "../../03-topicos/serverless-containers-kubernetes.md"),
    "storage": ("Arquitetura e Modernizacao", "../../03-topicos/arquitetura-modernizacao.md"),
}


TAG_LABELS = {
    "academic": "Academico",
    "advisor": "Advisor",
    "aerospace": "Aeroespacial",
    "agriculture": "Agronegocio",
    "ai": "Inteligencia artificial",
    "analytics": "Analytics",
    "app-integration": "Integracao de aplicacoes",
    "app-security": "Seguranca de aplicacoes",
    "architecture": "Arquitetura",
    "automotive": "Automotivo",
    "automation": "Automacao",
    "aws-partners": "AWS Partners",
    "biz-app": "Aplicacoes de negocio",
    "biz-ex": "Executivos de negocio",
    "biz-intel": "Business intelligence",
    "chalk-talk": "Chalk talk",
    "cloud-ops": "Cloud operations",
    "cloud-sec": "Seguranca em cloud",
    "code-talk": "Code talk",
    "community-led": "Comunidade",
    "compute": "Computacao",
    "culture-of-security": "Cultura de seguranca",
    "cust-enblemnt": "Customer enablement",
    "customer-story": "Historia de cliente",
    "data-eng": "Engenharia de dados",
    "data-scientist": "Ciencia de dados",
    "databases": "Bancos de dados",
    "dev-chat": "Dev chat",
    "devops": "DevOps",
    "devops-eng": "Engenharia DevOps",
    "digital-sovereignty": "Soberania digital",
    "discussion": "Discussao",
    "dis-res-rec": "Disaster recovery",
    "education": "Educacao",
    "edge-comp": "Edge computing",
    "energy": "Energia",
    "engineer": "Engenharia",
    "entrepreneur": "Empreendedorismo",
    "euc-bus-app": "End-user computing",
    "event-driven-architecture": "Arquitetura orientada a eventos",
    "financial": "Financeiro",
    "gen-ai": "Generative AI",
    "global-infra": "Infraestrutura global",
    "government": "Governo",
    "hands-on": "Hands-on",
    "healthcare": "Saude",
    "iam": "IAM",
    "inc-diversity": "Inclusao e diversidade",
    "industry": "Industria",
    "innovation": "Inovacao",
    "it-admin": "Administracao de TI",
    "it-exec": "Executivos de TI",
    "it-pro": "Profissionais de TI",
    "kubernetes": "Kubernetes",
    "lambda-based-applications": "Aplicacoes baseadas em Lambda",
    "laptop-required": "Requer laptop",
    "lecture-style": "Apresentacao",
    "lightning-talk": "Lightning talk",
    "machine-learning": "Machine Learning",
    "management-governance": "Management and Governance",
    "manufacturing": "Manufatura",
    "marketing-advertising": "Marketing e publicidade",
    "media-entertainment": "Midia e entretenimento",
    "microsoft": "Microsoft",
    "migrations": "Migracoes",
    "monitoring-and-observability": "Monitoramento e observabilidade",
    "network-cont-delivery": "Networking e entrega de conteudo",
    "nis": "NIS",
    "nonprofit": "Terceiro setor",
    "opn-data": "Dados abertos",
    "open-source": "Open source",
    "price-per": "Otimizacao de custos",
    "professional-services": "Servicos profissionais",
    "res-ai": "Responsible AI",
    "resilience": "Resiliencia",
    "retail-wholesale": "Varejo e atacado",
    "saas": "SaaS",
    "sales-mar": "Vendas e marketing",
    "sap": "SAP",
    "security-compliance": "Seguranca e compliance",
    "serverless": "Serverless",
    "session": "Sessao paralela",
    "social-impct": "Impacto social",
    "software-internet": "Software e internet",
    "sports": "Esportes",
    "start-up": "Startup",
    "state-local-government": "Governo estadual/local",
    "storage": "Storage",
    "student": "Estudantes",
    "sus": "Sustentabilidade",
    "sys-admin": "Administracao de sistemas",
    "sys-architect": "Arquitetura de sistemas",
    "tdr": "Threat detection and response",
    "tech-explorer": "Exploradores tecnicos",
    "telecommunications": "Telecomunicacoes",
    "training-certification": "Treinamento e certificacao",
    "travel": "Viagens",
    "vmware": "VMware",
    "wdv": "Desenvolvimento web",
    "workshop": "Workshop",
}


SERVICE_LINKS = {
    "Amazon API Gateway": "https://aws.amazon.com/api-gateway/",
    "Amazon Bedrock": "https://aws.amazon.com/bedrock/",
    "Amazon Bedrock AgentCore": "https://aws.amazon.com/bedrock/agentcore/",
    "Amazon CloudWatch": "https://aws.amazon.com/cloudwatch/",
    "Amazon DynamoDB": "https://aws.amazon.com/dynamodb/",
    "Amazon EC2": "https://aws.amazon.com/ec2/",
    "Amazon ECS": "https://aws.amazon.com/ecs/",
    "Amazon EKS": "https://aws.amazon.com/eks/",
    "Amazon Elastic Container Service (Amazon ECS)": "https://aws.amazon.com/ecs/",
    "Amazon EventBridge": "https://aws.amazon.com/eventbridge/",
    "Amazon Kendra": "https://aws.amazon.com/kendra/",
    "Amazon OpenSearch Service": "https://aws.amazon.com/opensearch-service/",
    "Amazon Q Business": "https://aws.amazon.com/q/business/",
    "Amazon Q Developer": "https://aws.amazon.com/q/developer/",
    "Amazon RDS": "https://aws.amazon.com/rds/",
    "Amazon SageMaker": "https://aws.amazon.com/sagemaker/",
    "Amazon S3": "https://aws.amazon.com/s3/",
    "AWS App2Container": "https://aws.amazon.com/app2container/",
    "AWS Application Migration Service": "https://aws.amazon.com/application-migration-service/",
    "AWS CloudFormation": "https://aws.amazon.com/cloudformation/",
    "AWS Database Migration Service": "https://aws.amazon.com/dms/",
    "AWS Glue": "https://aws.amazon.com/glue/",
    "AWS Lambda": "https://aws.amazon.com/lambda/",
    "AWS Schema Conversion Tool": "https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html",
    "AWS Step Functions": "https://aws.amazon.com/step-functions/",
    "AWS Transform": "https://aws.amazon.com/transform/",
    "OpenSearch": "https://aws.amazon.com/opensearch-service/",
}


SERVICE_ALIASES = {
    "amazon elastic container service": "Amazon ECS",
    "amazon ecs": "Amazon ECS",
    "amazon elastic kubernetes service": "Amazon EKS",
    "amazon eks": "Amazon EKS",
    "opensearch": "Amazon OpenSearch Service",
}


@dataclass
class Session:
    id: str
    code: str
    title: str
    session_type: str
    level: str
    time: str
    timezone: str
    location: str
    speakers: str
    description: str
    event_topics: list[str]
    areas_of_interest: list[str]
    roles: list[str]
    industries: list[str]
    services: list[str]
    features: list[str]
    source_url: str
    page_path: str


def slugify(value: str, max_length: int = 90) -> str:
    value = repair_mojibake(value).lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-") or "sessao"
    return value[:max_length].strip("-") or "sessao"


def fetch_html() -> str:
    REPORTS.mkdir(parents=True, exist_ok=True)
    if not AGENDA_HTML.exists() or AGENDA_HTML.stat().st_size < 1000:
        with urllib.request.urlopen(OFFICIAL_URL, timeout=60) as response:
            AGENDA_HTML.write_bytes(response.read())
    return AGENDA_HTML.read_text(encoding="utf-8", errors="replace")


def iter_json_scripts(page_html: str):
    pattern = re.compile(r"<script\b[^>]*>(.*?)</script>", flags=re.IGNORECASE | re.DOTALL)
    for match in pattern.finditer(page_html):
        raw = html.unescape(match.group(1)).strip()
        if not raw:
            continue
        if not (raw.startswith("{") or raw.startswith("[")):
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def clean_text(value: Any) -> str:
    text = repair_mojibake(html.unescape(str(value or "")))
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def repair_mojibake(text: str) -> str:
    markers = ("Ã", "Â", "â€", "â€“", "â€”", "â€¢", "ƒ", "‡")
    if not any(marker in text for marker in markers):
        return text

    def score(value: str) -> int:
        return sum(value.count(marker) for marker in markers)

    best = text
    for source_encoding in ("latin-1", "cp1252"):
        try:
            candidate = text.encode(source_encoding).decode("utf-8")
        except UnicodeError:
            continue
        if score(candidate) < score(best):
            best = candidate
    return best


def tag_tail(tag_id: str) -> str:
    return tag_id.rsplit("#", 1)[-1].strip()


def tag_key(value: str) -> str:
    return value.strip().lower().replace(" ", "-").replace("&", "and")


def tags_by_group(metadata_or_tags: dict[str, Any] | list[dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:
    if isinstance(metadata_or_tags, dict):
        tags = metadata_or_tags.get("tags", []) or []
    else:
        tags = metadata_or_tags or []

    topics: list[str] = []
    areas: list[str] = []
    roles: list[str] = []
    industries: list[str] = []
    services: list[str] = []
    features: list[str] = []

    for tag in tags:
        tag_id = str(tag.get("id", ""))
        namespace = str(tag.get("tagNamespaceId", ""))
        tail = tag_tail(tag_id)
        name = clean_text(tag.get("name"))
        key = tail or tag_key(name)

        if "event-topic" in namespace or "event-topic" in tag_id:
            topics.append(key)
        elif namespace.endswith("area-of-interest") or "area-of-interest" in tag_id:
            areas.append(key)
        elif namespace.endswith("role") or "role" in tag_id:
            roles.append(key)
        elif namespace.endswith("industry") or "session-industry" in namespace or "industry" in tag_id:
            industries.append(key)
        elif namespace == "GLOBAL#aws-aws-products-and-services":
            services.append(name or key)
        elif "session-type" in namespace or "session-type" in tag_id or "aws-session-feature" in namespace:
            features.append(key)

    return (
        sorted(set(topics)),
        sorted(set(areas)),
        sorted(set(roles)),
        sorted(set(industries)),
        sorted(set(services)),
        sorted(set(features)),
    )


def parse_badge(value: Any) -> str:
    if not value:
        return ""
    if not isinstance(value, str):
        return clean_text(value)
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return clean_text(value)
    if isinstance(parsed, dict):
        badge_values = parsed.get("value")
        if isinstance(badge_values, list):
            return ", ".join(clean_text(v) for v in badge_values if clean_text(v))
    return clean_text(value)


def normalize_time(value: Any) -> str:
    text = clean_text(value)
    match = re.match(r"^(\d{2}:\d{2})", text)
    return match.group(1) if match else text


def normalize_timezone(value: Any) -> str:
    """Normalize the event API's Brazil timezone label for public-facing pages."""
    text = clean_text(value).upper()
    return "BRT" if text in {"BET", "BRT", "UTC-3", "GMT-3"} else text


def code_from_title(title: str, fallback: str) -> str:
    match = re.search(r"\|\s*([A-Z]{2,8}\d{2,4}(?:-[A-Z0-9]+)?|KEYNOTE)\s*$", title)
    if match:
        return match.group(1)
    clean_fallback = re.sub(r"[^A-Za-z0-9]+", "", fallback or "").upper()
    return clean_fallback or "SESSAO"


def title_without_code(title: str) -> str:
    return re.sub(r"\s*\|\s*([A-Z]{2,8}\d{2,4}(?:-[A-Z0-9]+)?|KEYNOTE)\s*$", "", title).strip()


def infer_services(session_text: str, services: list[str]) -> list[str]:
    found = list(services)
    haystack = session_text.lower()
    for service in SERVICE_LINKS:
        if service.lower() in haystack and service not in found:
            found.append(service)
    for alias, service in SERVICE_ALIASES.items():
        if alias in haystack and service not in found:
            found.append(service)
    return sorted(set(found))


def session_slug(code: str, title: str, position: int) -> str:
    prefix = slugify(code or f"sessao-{position}", max_length=24)
    return f"{prefix}-{slugify(title_without_code(title))}"


def session_from_card(card: dict[str, Any], position: int) -> Session | None:
    fields = card.get("fields")
    if not isinstance(fields, dict) or "itemTitle" not in fields:
        return None
    title = clean_text(fields.get("itemTitle"))
    if not title:
        return None
    metadata = card.get("metadata") if isinstance(card.get("metadata"), dict) else {}
    topics, areas, roles, industries, services, features = tags_by_group(metadata)
    code = code_from_title(title, str(fields.get("id", f"S{position:03d}")).replace("ams#", ""))
    slug = session_slug(code, title, position)
    page_path = f"02-agenda-e-sessoes/sessoes/{slug}.md"
    description = clean_text(fields.get("itemExpandedBodyBack"))
    speakers = clean_text(str(fields.get("itemBody", "")).replace("Speakers:", ""))
    services = infer_services(" ".join([title, description, speakers]), services)
    return Session(
        id=str(fields.get("id", f"session-{position}")),
        code=code,
        title=title,
        session_type=clean_text(fields.get("itemExpandedHeading")) or label(features) or "Sessao",
        level=clean_text(fields.get("itemBadge")),
        time=normalize_time(fields.get("itemMetaTime")),
        timezone=normalize_timezone(fields.get("itemMetaTimeZone")),
        location=clean_text(fields.get("itemMetaLocation")),
        speakers=speakers,
        description=description,
        event_topics=topics,
        areas_of_interest=areas,
        roles=roles,
        industries=industries,
        services=services,
        features=features,
        source_url=OFFICIAL_URL,
        page_path=page_path,
    )


def session_from_directory_item(entry: dict[str, Any], position: int) -> Session | None:
    item = entry.get("item")
    if not isinstance(item, dict):
        return None
    fields = item.get("additionalFields")
    if not isinstance(fields, dict):
        return None
    title = clean_text(fields.get("title"))
    if not title:
        return None

    topics, areas, roles, industries, services, features = tags_by_group(entry.get("tags", []))
    code = code_from_title(title, str(item.get("name", f"S{position:03d}")))
    slug = session_slug(code, title, position)
    page_path = f"02-agenda-e-sessoes/sessoes/{slug}.md"
    description = clean_text(fields.get("bodyBack"))
    speakers = clean_text(str(fields.get("body", "")).replace("Speakers:", ""))
    services = infer_services(" ".join([title, description, speakers]), services)

    return Session(
        id=str(item.get("id", f"session-{position}")),
        code=code,
        title=title,
        session_type=clean_text(fields.get("heading")) or label(features) or "Sessao",
        level=parse_badge(fields.get("badge")),
        time=normalize_time(fields.get("time")),
        timezone=normalize_timezone(fields.get("timeZone")),
        location=clean_text(fields.get("location")),
        speakers=speakers,
        description=description,
        event_topics=topics,
        areas_of_interest=areas,
        roles=roles,
        industries=industries,
        services=services,
        features=features,
        source_url=OFFICIAL_URL,
        page_path=page_path,
    )


def extract_sessions_from_directory_json() -> list[Session]:
    if not FULL_AGENDA_JSON.exists():
        return []
    data = json.loads(FULL_AGENDA_JSON.read_text(encoding="utf-8"))
    by_key: dict[str, Session] = {}
    for position, entry in enumerate(data.get("items", []) or [], start=1):
        session = session_from_directory_item(entry, position)
        if session is None:
            continue
        key = session.code if session.code else session.title
        by_key.setdefault(key, session)
    return sorted(by_key.values(), key=lambda s: (s.time or "99:99", s.code, s.title))


def extract_sessions_from_html(page_html: str) -> list[Session]:
    by_key: dict[str, Session] = {}
    position = 1
    for script in iter_json_scripts(page_html):
        for node in walk(script):
            session = session_from_card(node, position)
            if session is None:
                continue
            key = session.code if session.code else session.title
            if key not in by_key:
                by_key[key] = session
                position += 1
    return sorted(by_key.values(), key=lambda s: (s.time or "99:99", s.code, s.title))


def extract_sessions(page_html: str) -> list[Session]:
    sessions = extract_sessions_from_directory_json()
    if sessions:
        return sessions
    return extract_sessions_from_html(page_html)


def label(values: list[str]) -> str:
    return ", ".join(TAG_LABELS.get(v, v) for v in values)


def topic_links(session: Session) -> str:
    links = []
    for topic in session.event_topics:
        mapped = TOPIC_MAP.get(topic)
        if mapped:
            name, path = mapped
            links.append(f"[{name}]({path})")
    if not links:
        return ""
    return ", ".join(dict.fromkeys(links))


def official_service_links(services: list[str]) -> list[str]:
    links = []
    for service in services:
        url = SERVICE_LINKS.get(service)
        if url:
            links.append(f"- [{service}]({url})")
        else:
            links.append(f"- {service}")
    return links


def md_table_cell(value: str) -> str:
    return (value or "").replace("\n", " ").replace("|", "\\|")


def write_reports(sessions: list[Session]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "aws_summit_sp_2026_sessions.json").write_text(
        json.dumps([asdict(s) for s in sessions], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with (REPORTS / "aws_summit_sp_2026_sessions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(sessions[0]).keys()) if sessions else ["id"])
        writer.writeheader()
        for session in sessions:
            row = asdict(session)
            for field_name in ["event_topics", "areas_of_interest", "roles", "industries", "services", "features"]:
                row[field_name] = ", ".join(getattr(session, field_name))
            writer.writerow(row)


def write_catalog(sessions: list[Session]) -> None:
    lines = [
        "# Catalogo oficial AWS Summit Sao Paulo 2026",
        "",
        "> Status: catalogo oficial; revisao comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `catalogo-oficial`, `aws-summit-sao-paulo`",
        "",
        "Catalogo extraido da pagina oficial da AWS em 2026-09-04. Use como base de consulta e revise caso a pagina oficial seja atualizada.",
        "",
        f"Fonte oficial: [Agenda - AWS Summit Sao Paulo 2026]({OFFICIAL_URL})",
        "",
        f"Total de sessoes extraidas: {len(sessions)}",
        "",
        "| Horario | Codigo | Sessao | Tipo | Nivel | Local | Palestrantes/Organizacoes | Topicos | Servicos detectados |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for session in sessions:
        rel_page = session.page_path.replace("02-agenda-e-sessoes/", "")
        lines.append(
            "| "
            + " | ".join(
                [
                    md_table_cell(session.time),
                    md_table_cell(session.code),
                    f"[{md_table_cell(session.title)}]({rel_page})",
                    md_table_cell(session.session_type),
                    md_table_cell(session.level),
                    md_table_cell(session.location),
                    md_table_cell(session.speakers),
                    md_table_cell(label(session.event_topics)),
                    md_table_cell(", ".join(session.services)),
                ]
            )
            + " |"
        )
    (ROOT / "02-agenda-e-sessoes" / "catalogo-oficial-aws.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_session_pages(sessions: list[Session]) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    for stale_page in SESSIONS_DIR.glob("*.md"):
        stale_page.unlink()
    order = []
    for session in sessions:
        page = ROOT / session.page_path
        order.append(page.stem)
        service_links = official_service_links(session.services)
        lines = [
            f"# {session.title}",
            "",
            "> Status: catalogo oficial; revisao comunitaria",
            "> Dono: Vitor Ferreira",
            "> Ultima revisao: 2026-09-04",
            f"> Tags: `aws-summit-2026`, `sessao`, `{session.code.lower()}`",
            "",
            "## Creditos",
            "",
            f"- Palestrante(s)/organizacao(oes): {session.speakers or 'Nomes individuais nao informados no catalogo oficial; confirmar em materiais publicados.'}",
            f"- Fonte: [Agenda oficial AWS Summit Sao Paulo 2026]({session.source_url})",
            "",
            "## Metadados oficiais",
            "",
            "| Campo | Valor |",
            "| --- | --- |",
            f"| Codigo | {md_table_cell(session.code)} |",
            f"| Horario | {md_table_cell(session.time)} {md_table_cell(session.timezone)} |",
            f"| Local | {md_table_cell(session.location)} |",
            f"| Tipo | {md_table_cell(session.session_type)} |",
            f"| Nivel | {md_table_cell(session.level)} |",
            f"| Topicos AWS | {md_table_cell(label(session.event_topics))} |",
            f"| Areas de interesse | {md_table_cell(label(session.areas_of_interest))} |",
            f"| Publico indicado | {md_table_cell(label(session.roles))} |",
            f"| Industrias | {md_table_cell(label(session.industries))} |",
            f"| Servicos AWS detectados | {md_table_cell(', '.join(session.services))} |",
            f"| Formato/recursos | {md_table_cell(label(session.features))} |",
            "",
            "## Descricao oficial",
            "",
            session.description or "Descricao nao informada no catalogo oficial.",
            "",
            "## Topicos relacionados na wiki",
            "",
            topic_links(session) or "- A classificar",
            "",
            "## Referencias oficiais relacionadas",
            "",
            "\n".join(service_links) if service_links else "- Nenhum servico AWS especifico foi detectado automaticamente nesta descricao.",
            "",
            "## Evidencias locais",
            "",
            "Ainda nao ha evidencias locais associadas a esta sessao. Quando houver, adicione links no indice de midias e nesta pagina.",
            "",
            "| Evidencia | Tipo | Observacao |",
            "| --- | --- | --- |",
            "|  |  |  |",
            "",
            "## Insights",
            "",
            "| Insight | Evidencia | Impacto | Proxima acao |",
            "| --- | --- | --- | --- |",
            "|  |  |  |  |",
            "",
            "## Agradecimento",
            "",
            "Agradecimento aos palestrantes e organizacoes por compartilhar conhecimento com a comunidade AWS.",
        ]
        page.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (SESSIONS_DIR / ".order").write_text("\n".join(order) + "\n", encoding="utf-8")


def write_sessions_index(sessions: list[Session]) -> None:
    topic_counts: dict[str, int] = {}
    level_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for session in sessions:
        for topic in session.event_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        if session.level:
            level_counts[session.level] = level_counts.get(session.level, 0) + 1
        if session.session_type:
            type_counts[session.session_type] = type_counts.get(session.session_type, 0) + 1

    lines = [
        "# Paginas por sessao",
        "",
        "> Status: catalogo oficial; revisao comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `agenda`, `sessoes`",
        "",
        "Indice das paginas individuais geradas a partir do catalogo oficial da AWS.",
        "",
        f"- Total de sessoes: {len(sessions)}",
        f"- Catalogo consolidado: [Catalogo oficial AWS](catalogo-oficial-aws.md)",
        f"- Fonte oficial: [Agenda AWS Summit Sao Paulo 2026]({OFFICIAL_URL})",
        "",
        "## Visao por topico",
        "",
        "| Topico | Sessoes |",
        "| --- | ---: |",
    ]
    for topic, count in sorted(topic_counts.items(), key=lambda item: (-item[1], label([item[0]]))):
        lines.append(f"| {md_table_cell(label([topic]))} | {count} |")

    lines.extend(
        [
            "",
            "## Visao por nivel",
            "",
            "| Nivel | Sessoes |",
            "| --- | ---: |",
        ]
    )
    for level, count in sorted(level_counts.items()):
        lines.append(f"| {md_table_cell(level)} | {count} |")

    lines.extend(
        [
            "",
            "## Visao por formato",
            "",
            "| Formato | Sessoes |",
            "| --- | ---: |",
        ]
    )
    for session_type, count in sorted(type_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {md_table_cell(session_type)} | {count} |")

    lines.extend(
        [
            "",
            "## Todas as paginas",
            "",
            "| Horario | Codigo | Sessao | Topicos |",
            "| --- | --- | --- | --- |",
        ]
    )
    for session in sessions:
        rel_page = session.page_path.replace("02-agenda-e-sessoes/", "")
        lines.append(
            "| "
            + " | ".join(
                [
                    md_table_cell(session.time),
                    md_table_cell(session.code),
                    f"[{md_table_cell(session.title)}]({rel_page})",
                    md_table_cell(label(session.event_topics)),
                ]
            )
            + " |"
        )
    (ROOT / "02-agenda-e-sessoes" / "sessoes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_services_reference(sessions: list[Session]) -> None:
    services = sorted({service for session in sessions for service in session.services})
    lines = [
        "# Servicos AWS citados",
        "",
        "> Status: referencia comunitaria",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        "> Tags: `aws-summit-2026`, `referencias`, `servicos-aws`",
        "",
        "Indice de servicos detectados no catalogo oficial e nas evidencias locais. Os links apontam para materiais oficiais da AWS quando disponiveis.",
        "",
        "| Servico | Referencia oficial | Sessoes relacionadas |",
        "| --- | --- | --- |",
    ]
    for service in services:
        url = SERVICE_LINKS.get(service, "")
        ref = f"[{service}]({url})" if url else service
        related = []
        for session in sessions:
            if service in session.services:
                rel_path = "../02-agenda-e-sessoes/" + session.page_path.replace("02-agenda-e-sessoes/", "")
                related.append(f"[{session.code}]({rel_path})")
        lines.append(f"| {md_table_cell(service)} | {ref} | {', '.join(related[:20])} |")
    if not services:
        lines.append("| A classificar |  |  |")
    (ROOT / "06-referencias" / "servicos-aws-citados.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    page_html = fetch_html()
    sessions = extract_sessions(page_html)
    if not sessions:
        raise RuntimeError("No sessions were extracted from the AWS agenda page.")
    write_reports(sessions)
    write_catalog(sessions)
    write_session_pages(sessions)
    write_sessions_index(sessions)
    write_services_reference(sessions)
    print(f"extracted {len(sessions)} session(s)")
    for session in sessions[:10]:
        print(f"{session.time} {session.code} {session.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
