import	streamlit	as	st
import	requests
from	datetime	import	datetime
import	os
import  time
import  json



API_URL = "http://127.0.0.1:8000"
COOLDOWN=20 


st.title ( "CS350 IITK Programming Languages TimeWaster " )
query   = st.text_area  ( "Enter your query" )


# initialize session history
if "history" not in st.session_state:
    st.session_state.history = []
st.session_state.setdefault("last_submit", 0.0)
export_items = []

user_id="test_student_001"

# cooldown logic
now = time.time()
elapsed = now - st.session_state["last_submit"]
remaining = max(0, int(COOLDOWN - elapsed))
disabled = remaining > 0

if disabled:
    st.info(f"Please wait {remaining} s before submitting another query.")

    
if st.button ( "Submit Query", key="submit_btn", disabled=disabled ) and user_id and query :
    st.session_state["last_submit"] = time.time()
    with st.spinner ( "Waiting for Godot..."):
        res = requests.post (
            f"{API_URL}/query",
            json = { "user_id" : user_id,
                     "query_text" : query,
                     "captcha_code" : "dummy"
                    }
            )
        if res.status_code == 200:
            data = res.json ()
            st.session_state.history.append({
                "query": query,
                "response": data["response_text"],
                "input_tokens": data["input_tokens"],
                "output_tokens": data["output_tokens"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            st.error ( f"Error: { res.status_code }")


# export button

export_items = [
    {"question": entry["query"], "answer": entry["response"]}
    for entry in st.session_state.get("history", [])
]

if export_items:
    json_data = json.dumps(export_items, ensure_ascii=False, indent=2)
    fname = f"cs350_chats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    st.download_button(
        label="Export chats (JSON)",
        data=json_data,
        file_name=fname,
        mime="application/json",
        key="export_chats"
    )
 

# Show response history chronologically reversed.
if st.session_state.history:
    st.markdown("---")
    st.markdown("## Previous Queries")
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {entry['query'][:60]}... ({entry['timestamp']})"):
            st.write(entry["response"])
            st.markdown(f"**Input tokens:** {entry['input_tokens']}  \n**Output tokens:** {entry['output_tokens']}")

