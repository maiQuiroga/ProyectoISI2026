from datetime import UTC, date, datetime, timedelta
from typing import Any


def _normalize_tag(tag: Any) -> str:
    if hasattr(tag, "name"):
        value = str(tag.name)
    elif isinstance(tag, dict):
        value = str(tag.get("name", ""))
    else:
        value = str(tag)
    return value.strip().lstrip("#").lower()


def _extract_tags(question: Any) -> list[str]:
    if isinstance(question, dict):
        raw_tags = question.get("tags", [])
    else:
        raw_tags = getattr(question, "tags", []) or []
    return [_normalize_tag(t) for t in raw_tags]


def _extract_age_days(question: Any, now: datetime | date | None = None) -> int | None:
    if isinstance(question, dict):
        raw_date = question.get("created_at")
    else:
        raw_date = getattr(question, "publication_date", None) or getattr(
            question, "created_at", None
        )

    if raw_date is None:
        return None

    if isinstance(raw_date, datetime):
        created_dt = raw_date if raw_date.tzinfo else raw_date.replace(tzinfo=UTC)
        ref_dt = (
            now
            if isinstance(now, datetime)
            else datetime.combine(now or date.today(), datetime.min.time(), tzinfo=UTC)
        )
        if ref_dt.tzinfo is None:
            ref_dt = ref_dt.replace(tzinfo=UTC)
        return (ref_dt - created_dt).days

    if isinstance(raw_date, date):
        ref_date = now.date() if isinstance(now, datetime) else (now or date.today())
        return (ref_date - raw_date).days

    if isinstance(raw_date, str):
        try:
            parsed = datetime.fromisoformat(raw_date.replace(" UTC", "+00:00"))
            created_dt = parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
            ref_dt = (
                now
                if isinstance(now, datetime)
                else datetime.combine(
                    now or date.today(), datetime.min.time(), tzinfo=UTC
                )
            )
            if ref_dt.tzinfo is None:
                ref_dt = ref_dt.replace(tzinfo=UTC)
            return (ref_dt - created_dt).days
        except ValueError:
            return None

    return None


class AIResponseDetector:
    """Detecta si una pregunta requiere respuesta automática de IA."""

    def __init__(self, trigger_tag: str = "ia-help", inactive_days: int = 7) -> None:
        self.trigger_tag = trigger_tag.strip().lstrip("#").lower()
        self.inactive_days = inactive_days

    def has_trigger_tag(self, question: Any) -> bool:
        return self.trigger_tag in _extract_tags(question)

    def is_inactive(self, question: Any, now: datetime | date | None = None) -> bool:
        age_days = _extract_age_days(question, now=now)
        if age_days is None:
            return False
        return age_days >= self.inactive_days

    def requires_ai_response(
        self, question: Any, now: datetime | date | None = None
    ) -> bool:
        return self.has_trigger_tag(question) or self.is_inactive(question, now=now)

    def detection_reason(
        self, question: Any, now: datetime | date | None = None
    ) -> str | None:
        has_tag = self.has_trigger_tag(question)
        inactive = self.is_inactive(question, now=now)
        if has_tag and inactive:
            return "tag_and_inactivity"
        if has_tag:
            return "trigger_tag"
        if inactive:
            return "inactivity"
        return None
