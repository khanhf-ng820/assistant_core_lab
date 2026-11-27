"""Streamlit chat UI.   Run:  streamlit run ui/app.py      (the API must be running on port 8000)

The UI never imports assistant_core: it only talks to the backend through the HTTP API.
"""
import os
import sys
import uuid
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so "import ui..." works under streamlit

from ui.api_client import AssistantClient
from ui.logic import EXAMPLES, WELCOME, format_sources, status_note, validate_input
from ui.streaming import should_stream_message, stream_text

st.set_page_config(page_title="FIT Study Assistant", page_icon="🎓")
client = AssistantClient(os.getenv("ASSISTANT_API_URL", "http://127.0.0.1:8000"))

# ---- session state: remembered between reruns of this script ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:12]
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
if "rated" not in st.session_state:
    st.session_state.rated = set()
if "streamed_up_to" not in st.session_state:
    st.session_state.streamed_up_to = 0

st.title("🎓 FIT Study Assistant")
if toast := st.session_state.pop("toast", None):
    st.toast(toast)
if not client.healthy():
    st.error("The assistant backend is not reachable. Start it with: uvicorn assistant_api.main:create_app --factory")
st.caption("AI assistant — check important decisions with the Training Office.")

with st.sidebar:
    st.subheader("Try an example")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex
    st.caption("This is an AI assistant. Check important decisions with the Training Office.")

# ---- history -------------------------------------------------------------------
total_messages = len(st.session_state.messages)
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        if should_stream_message(i, m["role"], total_messages, st.session_state.streamed_up_to):
            st.write_stream(stream_text(m["content"]))
            st.session_state.streamed_up_to = i
        else:
            st.markdown(m["content"])
        if m.get("sources"):
            st.caption(m["sources"])
        if m.get("note"):
            st.info(m["note"])
        rid = m.get("request_id")
        if rid and rid not in st.session_state.rated:
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("👍", key=f"up{i}", help="Helpful"):
                client.send_feedback(rid, 1)
                st.session_state.rated.add(rid)
                st.toast("Thanks for your feedback!")
            if c2.button("👎", key=f"down{i}"):
                client.send_feedback(rid, -1)
                st.session_state.rated.add(rid)
                st.session_state.toast = "Thanks — we will look at this answer."
                st.rerun()  # redraw now so both buttons disappear; the toast is shown on the next run

# ---- new question ----------------------------------------------------------------
question = st.chat_input("Ask about fees, offices or the handbook…") or st.session_state.pop("pending", None)
if question:
    problem = validate_input(question)
    if problem:
        st.warning(problem)
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking…"):
            result = client.ask(question, st.session_state.session_id)
        if result.ok:
            st.session_state.messages.append({"role": "assistant", "content": result.answer,
                                              "sources": format_sources(result.sources),
                                              "note": status_note(result), "request_id": result.request_id})
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {result.error}"})
        st.rerun()
