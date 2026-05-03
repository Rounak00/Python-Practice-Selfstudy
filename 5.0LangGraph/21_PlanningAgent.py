# Planning Agent (Plan - research - write blogs)
# Planning Agent is a AI Agent that doesnot immediatly jump or answer , 
# instead it first creates a structured plan of what needs to be done and executes the plan step by step.

# two phase task -> break down in sub task and working on those subtask

# Basic blog writting
# for base codes visit -> https://github.dev/campusx-official/blog-writing-agent

# now the application -
from __future__ import annotations

import operator
import os
import re
from datetime import date, timedelta
from pathlib import Path
from typing import TypedDict, List, Optional, Literal, Annotated

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Blog Writer (Router → (Research?) → Orchestrator → Workers → ReducerWithImages)
# Patches image capability using your 3-node reducer flow:
#   merge_content -> decide_images -> generate_and_place_images
# ============================================================


# -----------------------------
# 1) Schemas
# -----------------------------
class Task(BaseModel):
    id: int
    title: str
    goal: str = Field(..., description="One sentence describing what the reader should do/understand.")
    bullets: List[str] = Field(..., min_length=3, max_length=6)
    target_words: int = Field(..., description="Target words (120–550).")

    tags: List[str] = Field(default_factory=list)
    requires_research: bool = False
    requires_citations: bool = False
    requires_code: bool = False


class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str
    blog_kind: Literal["explainer", "tutorial", "news_roundup", "comparison", "system_design"] = "explainer"
    constraints: List[str] = Field(default_factory=list)
    tasks: List[Task]


class EvidenceItem(BaseModel):
    title: str
    url: str
    published_at: Optional[str] = None  # ISO "YYYY-MM-DD" preferred
    snippet: Optional[str] = None
    source: Optional[str] = None


class RouterDecision(BaseModel):
    needs_research: bool
    mode: Literal["closed_book", "hybrid", "open_book"]
    reason: str
    queries: List[str] = Field(default_factory=list)
    max_results_per_query: int = Field(5)


class EvidencePack(BaseModel):
    evidence: List[EvidenceItem] = Field(default_factory=list)


# ---- Image planning schema (ported from your image flow) ----
class ImageSpec(BaseModel):
    placeholder: str = Field(..., description="e.g. [[IMAGE_1]]")
    filename: str = Field(..., description="Save under images/, e.g. qkv_flow.png")
    alt: str
    caption: str
    prompt: str = Field(..., description="Prompt to send to the image model.")
    size: Literal["1024x1024", "1024x1536", "1536x1024"] = "1024x1024"
    quality: Literal["low", "medium", "high"] = "medium"


class GlobalImagePlan(BaseModel):
    md_with_placeholders: str
    images: List[ImageSpec] = Field(default_factory=list)

class State(TypedDict):
    topic: str

    # routing / research
    mode: str
    needs_research: bool
    queries: List[str]
    evidence: List[EvidenceItem]
    plan: Optional[Plan]

    # recency
    as_of: str
    recency_days: int

    # workers
    sections: Annotated[List[tuple[int, str]], operator.add]  # (task_id, section_md)

    # reducer/image
    merged_md: str
    md_with_placeholders: str
    image_specs: List[dict]

    final: str


# -----------------------------
# 2) LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-4.1-mini")

# -----------------------------
# 3) Router
# -----------------------------
ROUTER_SYSTEM = """You are a routing module for a technical blog planner.

Decide whether web research is needed BEFORE planning.

Modes:
- closed_book (needs_research=false): evergreen concepts.
- hybrid (needs_research=true): evergreen + needs up-to-date examples/tools/models.
- open_book (needs_research=true): volatile weekly/news/"latest"/pricing/policy.

If needs_research=true:
- Output 3–10 high-signal, scoped queries.
- For open_book weekly roundup, include queries reflecting last 7 days.
"""

def router_node(state: State) -> dict:
    decider = llm.with_structured_output(RouterDecision)
    decision = decider.invoke(
        [
            SystemMessage(content=ROUTER_SYSTEM),
            HumanMessage(content=f"Topic: {state['topic']}\nAs-of date: {state['as_of']}"),
        ]
    )

    if decision.mode == "open_book":
        recency_days = 7
    elif decision.mode == "hybrid":
        recency_days = 45
    else:
        recency_days = 3650

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": recency_days,
    }

def route_next(state: State) -> str:
    return "research" if state["needs_research"] else "orchestrator"

# -----------------------------
# 4) Research (Tavily)
# -----------------------------
def _tavily_search(query: str, max_results: int = 5) -> List[dict]:
    if not os.getenv("TAVILY_API_KEY"):
        return []
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults  # type: ignore
        tool = TavilySearchResults(max_results=max_results)
        results = tool.invoke({"query": query})
        out: List[dict] = []
        for r in results or []:
            out.append(
                {
                    "title": r.get("title") or "",
                    "url": r.get("url") or "",
                    "snippet": r.get("content") or r.get("snippet") or "",
                    "published_at": r.get("published_date") or r.get("published_at"),
                    "source": r.get("source"),
                }
            )
        return out
    except Exception:
        return []

def _iso_to_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except Exception:
        return None

RESEARCH_SYSTEM = """You are a research synthesizer.

Given raw web search results, produce EvidenceItem objects.

Rules:
- Only include items with a non-empty url.
- Prefer relevant + authoritative sources.
- Normalize published_at to ISO YYYY-MM-DD if reliably inferable; else null (do NOT guess).
- Keep snippets short.
- Deduplicate by URL.
"""

def research_node(state: State) -> dict:
    queries = (state.get("queries") or [])[:10]
    raw: List[dict] = []
    for q in queries:
        raw.extend(_tavily_search(q, max_results=6))

    if not raw:
        return {"evidence": []}

    extractor = llm.with_structured_output(EvidencePack)
    pack = extractor.invoke(
        [
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(
                content=(
                    f"As-of date: {state['as_of']}\n"
                    f"Recency days: {state['recency_days']}\n\n"
                    f"Raw results:\n{raw}"
                )
            ),
        ]
    )

    dedup = {}
    for e in pack.evidence:
        if e.url:
            dedup[e.url] = e
    evidence = list(dedup.values())

    if state.get("mode") == "open_book":
        as_of = date.fromisoformat(state["as_of"])
        cutoff = as_of - timedelta(days=int(state["recency_days"]))
        evidence = [e for e in evidence if (d := _iso_to_date(e.published_at)) and d >= cutoff]

    return {"evidence": evidence}

# -----------------------------
# 5) Orchestrator (Plan)
# -----------------------------
ORCH_SYSTEM = """You are a senior technical writer and developer advocate.
Produce a highly actionable outline for a technical blog post.

Requirements:
- 5–9 tasks, each with goal + 3–6 bullets + target_words.
- Tags are flexible; do not force a fixed taxonomy.

Grounding:
- closed_book: evergreen, no evidence dependence.
- hybrid: use evidence for up-to-date examples; mark those tasks requires_research=True and requires_citations=True.
- open_book: weekly/news roundup:
  - Set blog_kind="news_roundup"
  - No tutorial content unless requested
  - If evidence is weak, plan should explicitly reflect that (don’t invent events).

Output must match Plan schema.
"""

def orchestrator_node(state: State) -> dict:
    planner = llm.with_structured_output(Plan)
    mode = state.get("mode", "closed_book")
    evidence = state.get("evidence", [])

    forced_kind = "news_roundup" if mode == "open_book" else None

    plan = planner.invoke(
        [
            SystemMessage(content=ORCH_SYSTEM),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n"
                    f"Mode: {mode}\n"
                    f"As-of: {state['as_of']} (recency_days={state['recency_days']})\n"
                    f"{'Force blog_kind=news_roundup' if forced_kind else ''}\n\n"
                    f"Evidence:\n{[e.model_dump() for e in evidence][:16]}"
                )
            ),
        ]
    )
    if forced_kind:
        plan.blog_kind = "news_roundup"

    return {"plan": plan}


# -----------------------------
# 6) Fanout
# -----------------------------
def fanout(state: State):
    assert state["plan"] is not None
    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "topic": state["topic"],
                "mode": state["mode"],
                "as_of": state["as_of"],
                "recency_days": state["recency_days"],
                "plan": state["plan"].model_dump(),
                "evidence": [e.model_dump() for e in state.get("evidence", [])],
            },
        )
        for task in state["plan"].tasks
    ]

# -----------------------------
# 7) Worker
# -----------------------------
WORKER_SYSTEM = """You are a senior technical writer and developer advocate.
Write ONE section of a technical blog post in Markdown.

Constraints:
- Cover ALL bullets in order.
- Target words ±15%.
- Output only section markdown starting with "## <Section Title>".

Scope guard:
- If blog_kind=="news_roundup", do NOT drift into tutorials (scraping/RSS/how to fetch).
  Focus on events + implications.

Grounding:
- If mode=="open_book": do not introduce any specific event/company/model/funding/policy claim unless supported by provided Evidence URLs.
  For each supported claim, attach a Markdown link ([Source](URL)).
  If unsupported, write "Not found in provided sources."
- If requires_citations==true (hybrid tasks): cite Evidence URLs for external claims.

Code:
- If requires_code==true, include at least one minimal snippet.
"""

def worker_node(payload: dict) -> dict:
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]

    bullets_text = "\n- " + "\n- ".join(task.bullets)
    evidence_text = "\n".join(
        f"- {e.title} | {e.url} | {e.published_at or 'date:unknown'}"
        for e in evidence[:20]
    )

    section_md = llm.invoke(
        [
            SystemMessage(content=WORKER_SYSTEM),
            HumanMessage(
                content=(
                    f"Blog title: {plan.blog_title}\n"
                    f"Audience: {plan.audience}\n"
                    f"Tone: {plan.tone}\n"
                    f"Blog kind: {plan.blog_kind}\n"
                    f"Constraints: {plan.constraints}\n"
                    f"Topic: {payload['topic']}\n"
                    f"Mode: {payload.get('mode')}\n"
                    f"As-of: {payload.get('as_of')} (recency_days={payload.get('recency_days')})\n\n"
                    f"Section title: {task.title}\n"
                    f"Goal: {task.goal}\n"
                    f"Target words: {task.target_words}\n"
                    f"Tags: {task.tags}\n"
                    f"requires_research: {task.requires_research}\n"
                    f"requires_citations: {task.requires_citations}\n"
                    f"requires_code: {task.requires_code}\n"
                    f"Bullets:{bullets_text}\n\n"
                    f"Evidence (ONLY cite these URLs):\n{evidence_text}\n"
                )
            ),
        ]
    ).content.strip()

    return {"sections": [(task.id, section_md)]}

# ============================================================
# 8) ReducerWithImages (subgraph)
#    merge_content -> decide_images -> generate_and_place_images
# ============================================================
def merge_content(state: State) -> dict:
    plan = state["plan"]
    if plan is None:
        raise ValueError("merge_content called without plan.")
    ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]
    body = "\n\n".join(ordered_sections).strip()
    merged_md = f"# {plan.blog_title}\n\n{body}\n"
    return {"merged_md": merged_md}


DECIDE_IMAGES_SYSTEM = """You are an expert technical editor.
Decide if images/diagrams are needed for THIS blog.

Rules:
- Max 3 images total.
- Each image must materially improve understanding (diagram/flow/table-like visual).
- Insert placeholders exactly: [[IMAGE_1]], [[IMAGE_2]], [[IMAGE_3]].
- If no images needed: md_with_placeholders must equal input and images=[].
- Avoid decorative images; prefer technical diagrams with short labels.
Return strictly GlobalImagePlan.
"""

def decide_images(state: State) -> dict:
    planner = llm.with_structured_output(GlobalImagePlan)
    merged_md = state["merged_md"]
    plan = state["plan"]
    assert plan is not None

    image_plan = planner.invoke(
        [
            SystemMessage(content=DECIDE_IMAGES_SYSTEM),
            HumanMessage(
                content=(
                    f"Blog kind: {plan.blog_kind}\n"
                    f"Topic: {state['topic']}\n\n"
                    "Insert placeholders + propose image prompts.\n\n"
                    f"{merged_md}"
                )
            ),
        ]
    )

    return {
        "md_with_placeholders": image_plan.md_with_placeholders,
        "image_specs": [img.model_dump() for img in image_plan.images],
    }


def _gemini_generate_image_bytes(prompt: str) -> bytes:
    """
    Returns raw image bytes generated by Gemini.
    Requires: pip install google-genai
    Env var: GOOGLE_API_KEY
    """
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set.")

    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_ONLY_HIGH",
                )
            ],
        ),
    )

    # Depending on SDK version, parts may hang off resp.candidates[0].content.parts
    parts = getattr(resp, "parts", None)
    if not parts and getattr(resp, "candidates", None):
        try:
            parts = resp.candidates[0].content.parts
        except Exception:
            parts = None

    if not parts:
        raise RuntimeError("No image content returned (safety/quota/SDK change).")

    for part in parts:
        inline = getattr(part, "inline_data", None)
        if inline and getattr(inline, "data", None):
            return inline.data

    raise RuntimeError("No inline image bytes found in response.")


def _safe_slug(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9 _-]+", "", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s or "blog"


def generate_and_place_images(state: State) -> dict:
    plan = state["plan"]
    assert plan is not None

    md = state.get("md_with_placeholders") or state["merged_md"]
    image_specs = state.get("image_specs", []) or []

    # If no images requested, just write merged markdown
    if not image_specs:
        filename = f"{_safe_slug(plan.blog_title)}.md"
        Path(filename).write_text(md, encoding="utf-8")
        return {"final": md}

    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)

    for spec in image_specs:
        placeholder = spec["placeholder"]
        filename = spec["filename"]
        out_path = images_dir / filename

        # generate only if needed
        if not out_path.exists():
            try:
                img_bytes = _gemini_generate_image_bytes(spec["prompt"])
                out_path.write_bytes(img_bytes)
            except Exception as e:
                # graceful fallback: keep doc usable
                prompt_block = (
                    f"> **[IMAGE GENERATION FAILED]** {spec.get('caption','')}\n>\n"
                    f"> **Alt:** {spec.get('alt','')}\n>\n"
                    f"> **Prompt:** {spec.get('prompt','')}\n>\n"
                    f"> **Error:** {e}\n"
                )
                md = md.replace(placeholder, prompt_block)
                continue

        img_md = f"![{spec['alt']}](images/{filename})\n*{spec['caption']}*"
        md = md.replace(placeholder, img_md)

    filename = f"{_safe_slug(plan.blog_title)}.md"
    Path(filename).write_text(md, encoding="utf-8")
    return {"final": md}

# build reducer subgraph
reducer_graph = StateGraph(State)
reducer_graph.add_node("merge_content", merge_content)
reducer_graph.add_node("decide_images", decide_images)
reducer_graph.add_node("generate_and_place_images", generate_and_place_images)
reducer_graph.add_edge(START, "merge_content")
reducer_graph.add_edge("merge_content", "decide_images")
reducer_graph.add_edge("decide_images", "generate_and_place_images")
reducer_graph.add_edge("generate_and_place_images", END)
reducer_subgraph = reducer_graph.compile()

# -----------------------------
# 9) Build main graph
# -----------------------------
g = StateGraph(State)
g.add_node("router", router_node)
g.add_node("research", research_node)
g.add_node("orchestrator", orchestrator_node)
g.add_node("worker", worker_node)
g.add_node("reducer", reducer_subgraph)

g.add_edge(START, "router")
g.add_conditional_edges("router", route_next, {"research": "research", "orchestrator": "orchestrator"})
g.add_edge("research", "orchestrator")

g.add_conditional_edges("orchestrator", fanout, ["worker"])
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()
app



# Frontnedn
from __future__ import annotations

import json
import os
import re
import zipfile
from datetime import date
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Optional, List, Iterator, Tuple

import pandas as pd
import streamlit as st

# -----------------------------
# Import your compiled LangGraph app
# -----------------------------
from bwa_backend import app


# -----------------------------
# Helpers
# -----------------------------
def safe_slug(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9 _-]+", "", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s or "blog"


def bundle_zip(md_text: str, md_filename: str, images_dir: Path) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(md_filename, md_text.encode("utf-8"))

        if images_dir.exists() and images_dir.is_dir():
            for p in images_dir.rglob("*"):
                if p.is_file():
                    z.write(p, arcname=str(p))
    return buf.getvalue()


def images_zip(images_dir: Path) -> Optional[bytes]:
    if not images_dir.exists() or not images_dir.is_dir():
        return None
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in images_dir.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(p))
    return buf.getvalue()


def try_stream(graph_app, inputs: Dict[str, Any]) -> Iterator[Tuple[str, Any]]:
    """
    Stream graph progress if available; else invoke.
    Yields ("updates"/"values"/"final", payload).
    """
    try:
        for step in graph_app.stream(inputs, stream_mode="updates"):
            yield ("updates", step)
        out = graph_app.invoke(inputs)
        yield ("final", out)
        return
    except Exception:
        pass

    try:
        for step in graph_app.stream(inputs, stream_mode="values"):
            yield ("values", step)
        out = graph_app.invoke(inputs)
        yield ("final", out)
        return
    except Exception:
        pass

    out = graph_app.invoke(inputs)
    yield ("final", out)


def extract_latest_state(current_state: Dict[str, Any], step_payload: Any) -> Dict[str, Any]:
    if isinstance(step_payload, dict):
        if len(step_payload) == 1 and isinstance(next(iter(step_payload.values())), dict):
            inner = next(iter(step_payload.values()))
            current_state.update(inner)
        else:
            current_state.update(step_payload)
    return current_state


# -----------------------------
# Markdown renderer that supports local images
# -----------------------------
_MD_IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)")
_CAPTION_LINE_RE = re.compile(r"^\*(?P<cap>.+)\*$")


def _resolve_image_path(src: str) -> Path:
    src = src.strip().lstrip("./")
    return Path(src).resolve()


def render_markdown_with_local_images(md: str):
    matches = list(_MD_IMG_RE.finditer(md))
    if not matches:
        st.markdown(md, unsafe_allow_html=False)
        return

    parts: List[Tuple[str, str]] = []
    last = 0
    for m in matches:
        before = md[last : m.start()]
        if before:
            parts.append(("md", before))

        alt = (m.group("alt") or "").strip()
        src = (m.group("src") or "").strip()
        parts.append(("img", f"{alt}|||{src}"))
        last = m.end()

    tail = md[last:]
    if tail:
        parts.append(("md", tail))

    i = 0
    while i < len(parts):
        kind, payload = parts[i]

        if kind == "md":
            st.markdown(payload, unsafe_allow_html=False)
            i += 1
            continue

        alt, src = payload.split("|||", 1)

        caption = None
        if i + 1 < len(parts) and parts[i + 1][0] == "md":
            nxt = parts[i + 1][1].lstrip()
            if nxt.strip():
                first_line = nxt.splitlines()[0].strip()
                mcap = _CAPTION_LINE_RE.match(first_line)
                if mcap:
                    caption = mcap.group("cap").strip()
                    rest = "\n".join(nxt.splitlines()[1:])
                    parts[i + 1] = ("md", rest)

        if src.startswith("http://") or src.startswith("https://"):
            st.image(src, caption=caption or (alt or None), use_container_width=True)
        else:
            img_path = _resolve_image_path(src)
            if img_path.exists():
                st.image(str(img_path), caption=caption or (alt or None), use_container_width=True)
            else:
                st.warning(f"Image not found: `{src}` (looked for `{img_path}`)")

        i += 1


# -----------------------------
# ✅ NEW: Past blogs helpers
# -----------------------------
def list_past_blogs() -> List[Path]:
    """
    Returns .md files in current working directory, newest first.
    Filters out obvious non-blog markdown files if needed.
    """
    cwd = Path(".")
    files = [p for p in cwd.glob("*.md") if p.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def read_md_file(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def extract_title_from_md(md: str, fallback: str) -> str:
    """
    Use first '# ' heading as title if present.
    """
    for line in md.splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            return t or fallback
    return fallback


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="LangGraph Blog Writer", layout="wide")

st.title("Blog Writing Agent")

with st.sidebar:
    st.header("Generate New Blog")
    topic = st.text_area(
        "Topic",
        height=120,
    )
    as_of = st.date_input("As-of date", value=date.today())
    run_btn = st.button("🚀 Generate Blog", type="primary")

    # ✅ NEW: Past blogs list (keeps everything else intact)
    st.divider()
    st.subheader("Past blogs")

    past_files = list_past_blogs()
    if not past_files:
        st.caption("No saved blogs found (*.md in current folder).")
        selected_md_file = None
    else:
        # Build labels from file name + (optional) parsed title
        options: List[str] = []
        file_by_label: Dict[str, Path] = {}
        for p in past_files[:50]:
            try:
                md_text = read_md_file(p)
                title = extract_title_from_md(md_text, p.stem)
            except Exception:
                title = p.stem
            label = f"{title}  ·  {p.name}"
            options.append(label)
            file_by_label[label] = p

        selected_label = st.radio(
            "Select a blog to load",
            options=options,
            index=0,
            label_visibility="collapsed",
        )
        selected_md_file = file_by_label.get(selected_label)

        if st.button("📂 Load selected blog"):
            if selected_md_file:
                md_text = read_md_file(selected_md_file)
                # Load into session_state as if it were a run output
                st.session_state["last_out"] = {
                    "plan": None,          # old files don't include plan
                    "evidence": [],        # old files don't include evidence
                    "image_specs": [],     # optional (not persisted)
                    "final": md_text,      # markdown body
                }
                # also update the topic input to the title (best-effort) without changing UI
                st.session_state["topic_prefill"] = extract_title_from_md(md_text, selected_md_file.stem)

    

# Keep your topic input as-is; optionally prefill for next run after loading a blog
if "topic_prefill" in st.session_state and isinstance(st.session_state["topic_prefill"], str):
    # Do not mutate widgets; just keep as a hint.
    pass

# Storage for latest run
if "last_out" not in st.session_state:
    st.session_state["last_out"] = None

# Layout
tab_plan, tab_evidence, tab_preview, tab_images, tab_logs = st.tabs(
    ["🧩 Plan", "🔎 Evidence", "📝 Markdown Preview", "🖼️ Images", "🧾 Logs"]
)

logs: List[str] = []


def log(msg: str):
    logs.append(msg)


if run_btn:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    inputs: Dict[str, Any] = {
        "topic": topic.strip(),
        "mode": "",
        "needs_research": False,
        "queries": [],
        "evidence": [],
        "plan": None,
        "as_of": as_of.isoformat(),
        "recency_days": 7,
        "sections": [],
        "merged_md": "",
        "md_with_placeholders": "",
        "image_specs": [],
        "final": "",
    }

    status = st.status("Running graph…", expanded=True)
    progress_area = st.empty()

    current_state: Dict[str, Any] = {}
    last_node = None

    for kind, payload in try_stream(app, inputs):
        if kind in ("updates", "values"):
            node_name = None
            if isinstance(payload, dict) and len(payload) == 1 and isinstance(next(iter(payload.values())), dict):
                node_name = next(iter(payload.keys()))
            if node_name and node_name != last_node:
                status.write(f"➡️ Node: `{node_name}`")
                last_node = node_name

            current_state = extract_latest_state(current_state, payload)

            summary = {
                "mode": current_state.get("mode"),
                "needs_research": current_state.get("needs_research"),
                "queries": current_state.get("queries", [])[:5] if isinstance(current_state.get("queries"), list) else [],
                "evidence_count": len(current_state.get("evidence", []) or []),
                "tasks": len((current_state.get("plan") or {}).get("tasks", [])) if isinstance(current_state.get("plan"), dict) else None,
                "images": len(current_state.get("image_specs", []) or []),
                "sections_done": len(current_state.get("sections", []) or []),
            }
            progress_area.json(summary)

            log(f"[{kind}] {json.dumps(payload, default=str)[:1200]}")

        elif kind == "final":
            out = payload
            st.session_state["last_out"] = out
            status.update(label="✅ Done", state="complete", expanded=False)
            log("[final] received final state")

# Render last result (if any)
out = st.session_state.get("last_out")
if out:
    # --- Plan tab ---
    with tab_plan:
        st.subheader("Plan")
        plan_obj = out.get("plan")
        if not plan_obj:
            st.info("No plan found in output.")
        else:
            if hasattr(plan_obj, "model_dump"):
                plan_dict = plan_obj.model_dump()
            elif isinstance(plan_obj, dict):
                plan_dict = plan_obj
            else:
                plan_dict = json.loads(json.dumps(plan_obj, default=str))

            st.write("**Title:**", plan_dict.get("blog_title"))
            cols = st.columns(3)
            cols[0].write("**Audience:** " + str(plan_dict.get("audience")))
            cols[1].write("**Tone:** " + str(plan_dict.get("tone")))
            cols[2].write("**Blog kind:** " + str(plan_dict.get("blog_kind", "")))

            tasks = plan_dict.get("tasks", [])
            if tasks:
                df = pd.DataFrame(
                    [
                        {
                            "id": t.get("id"),
                            "title": t.get("title"),
                            "target_words": t.get("target_words"),
                            "requires_research": t.get("requires_research"),
                            "requires_citations": t.get("requires_citations"),
                            "requires_code": t.get("requires_code"),
                            "tags": ", ".join(t.get("tags") or []),
                        }
                        for t in tasks
                    ]
                ).sort_values("id")
                st.dataframe(df, use_container_width=True, hide_index=True)

                with st.expander("Task details"):
                    st.json(tasks)

    # --- Evidence tab ---
    with tab_evidence:
        st.subheader("Evidence")
        evidence = out.get("evidence") or []
        if not evidence:
            st.info("No evidence returned (maybe closed_book mode or no Tavily key/results).")
        else:
            rows = []
            for e in evidence:
                if hasattr(e, "model_dump"):
                    e = e.model_dump()
                rows.append(
                    {
                        "title": e.get("title"),
                        "published_at": e.get("published_at"),
                        "source": e.get("source"),
                        "url": e.get("url"),
                    }
                )
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # --- Preview tab ---
    with tab_preview:
        st.subheader("Markdown Preview")
        final_md = out.get("final") or ""
        if not final_md:
            st.warning("No final markdown found.")
        else:
            render_markdown_with_local_images(final_md)

            plan_obj = out.get("plan")
            if hasattr(plan_obj, "blog_title"):
                blog_title = plan_obj.blog_title
            elif isinstance(plan_obj, dict):
                blog_title = plan_obj.get("blog_title", "blog")
            else:
                # fallback: parse from markdown title
                blog_title = extract_title_from_md(final_md, "blog")

            md_filename = f"{safe_slug(blog_title)}.md"
            st.download_button(
                "⬇️ Download Markdown",
                data=final_md.encode("utf-8"),
                file_name=md_filename,
                mime="text/markdown",
            )

            bundle = bundle_zip(final_md, md_filename, Path("images"))
            st.download_button(
                "📦 Download Bundle (MD + images)",
                data=bundle,
                file_name=f"{safe_slug(blog_title)}_bundle.zip",
                mime="application/zip",
            )

    # --- Images tab ---
    with tab_images:
        st.subheader("Images")
        specs = out.get("image_specs") or []
        images_dir = Path("images")

        if not specs and not images_dir.exists():
            st.info("No images generated for this blog.")
        else:
            if specs:
                st.write("**Image plan:**")
                st.json(specs)

            if images_dir.exists():
                files = [p for p in images_dir.iterdir() if p.is_file()]
                if not files:
                    st.warning("images/ exists but is empty.")
                else:
                    for p in sorted(files):
                        st.image(str(p), caption=p.name, use_container_width=True)

                z = images_zip(images_dir)
                if z:
                    st.download_button(
                        "⬇️ Download Images (zip)",
                        data=z,
                        file_name="images.zip",
                        mime="application/zip",
                    )

    # --- Logs tab ---
    with tab_logs:
        st.subheader("Logs")
        if "logs" not in st.session_state:
            st.session_state["logs"] = []
        if logs:
            st.session_state["logs"].extend(logs)

        st.text_area("Event log", value="\n\n".join(st.session_state["logs"][-80:]), height=520)
else:
    st.info("Enter a topic and click **Generate Blog**.")
