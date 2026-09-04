from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "04-midias-e-evidencias" / "assets" / "audio"
VIDEOS = ROOT / "04-midias-e-evidencias" / "assets" / "videos"
TRANSCRIPTS = ROOT / "04-midias-e-evidencias" / "assets" / "transcricoes"
REPORTS = ROOT / "_work" / "reports"


@dataclass
class TranscriptItem:
    id: str
    source: str
    output_markdown: str
    duration_seconds: float
    language: str
    language_probability: float
    text_chars: int


def fmt_time(seconds: float) -> str:
    seconds = max(0, float(seconds))
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def transcribe_file(model: WhisperModel, source: Path) -> TranscriptItem:
    media_id = source.name.split("__", 1)[0]
    output = TRANSCRIPTS / f"{media_id}__transcricao-automatica.md"
    print(f"transcribing {source.name}")
    segments, info = model.transcribe(
        str(source),
        language="pt",
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 700},
        word_timestamps=False,
    )

    rows = []
    full_text_parts = []
    for segment in segments:
        text = segment.text.strip()
        if not text:
            continue
        rows.append((fmt_time(segment.start), fmt_time(segment.end), text))
        full_text_parts.append(text)

    full_text = "\n".join(full_text_parts)
    lines = [
        f"# Transcricao automatica - {media_id}",
        "",
        "> Status: transcricao automatica; revisao humana pendente",
        "> Dono: Vitor Ferreira",
        "> Ultima revisao: 2026-09-04",
        f"> Tags: `aws-summit-2026`, `transcricao`, `{media_id.lower()}`",
        "",
        "## Aviso",
        "",
        "Transcricao automatica gerada localmente. Revise nomes proprios, servicos AWS, numeros e termos tecnicos antes de usar como citacao final.",
        "",
        "## Origem",
        "",
        f"- Arquivo: [{source.name}](../audio/{source.name})" if source.parent == AUDIO else f"- Arquivo: [{source.name}](../videos/{source.name})",
        f"- Duracao estimada: {fmt_time(getattr(info, 'duration', 0.0))}",
        f"- Idioma detectado/configurado: {getattr(info, 'language', 'pt')} ({getattr(info, 'language_probability', 0.0):.2f})",
        "",
        "## Texto corrido",
        "",
        full_text,
        "",
        "## Segmentos",
        "",
        "| Inicio | Fim | Texto |",
        "| --- | --- | --- |",
    ]
    for start, end, text in rows:
        safe_text = text.replace("|", "\\|")
        lines.append(f"| {start} | {end} | {safe_text} |")

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return TranscriptItem(
        id=media_id,
        source=str(source.relative_to(ROOT)),
        output_markdown=str(output.relative_to(ROOT)),
        duration_seconds=float(getattr(info, "duration", 0.0) or 0.0),
        language=str(getattr(info, "language", "pt")),
        language_probability=float(getattr(info, "language_probability", 0.0) or 0.0),
        text_chars=len(full_text),
    )


def main() -> int:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    sources = sorted(AUDIO.glob("*.m4a")) + sorted(VIDEOS.glob("*.mp4"))
    if not sources:
        print("No audio/video files found to transcribe.", file=sys.stderr)
        return 1

    model_name = sys.argv[1] if len(sys.argv) > 1 else "small"
    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4, num_workers=1)
    items = [transcribe_file(model, source) for source in sources]
    (REPORTS / "transcript_manifest.json").write_text(
        json.dumps([asdict(item) for item in items], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"transcribed {len(items)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
