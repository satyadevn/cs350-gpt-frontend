import  streamlit               as      st
import  requests
from    streamlit_js_eval       import  streamlit_js_eval
import  streamlit.components.v1 as components
import os

from    datetime        import  datetime

st.title ( "CS350 IITK Programming Languages TimeWaster " )

user_id = st.text_input ( "Your ID" )
query   = st.text_area  ( "Enter your query" )
API_URL = "https://cs350-gpt-backend.onrender.com/"

# initialize session history
if "history" not in st.session_state:
    st.session_state.history = []


# # recaptcha
# components.html(
#     f"""
#     <script src="https://www.google.com/recaptcha/api.js" async defer></script>
#     <form id="captcha-form" action="?" method="POST"
#         <div class="g-recaptcha" data-sitekey="6LcXAZQrAAAAAIx35-MHiTWyBEdfRyIFYOUEQtJl""></div>
#         <br/>
#         <input type="submit" value="Submit">
#     </form>
#     """,
#     height=150,
# )

# result = streamlit_js_eval(js_expressions="document.getElementById('g-recaptcha-response')?.value")

# if st.button("Submit Captcha") and result:
#     captcha_token = result
    
# # Send captcha_token to your backend if needed
    
if st.button ( "Submit Query" ) and user_id and query:
    with st.spinner ( "Waiting for Godot..."):
        res = requests.post (
            f"{API_URL}/query",
            json = { "user_id" : user_id,
                     "query_text" : query,
#                     "captcha_token" : "dummy"
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
            # st.markdown ( "### Response " )
            # with ts.expander ( "More..." ):
            #     st.write    ( data [ "response_text" ])
            # st.markdown ( f"**Input tokens:** { data [ 'input_tokens' ]} \n**Output tokens** { data [ 'output_tokens' ]}" )
        else:
            st.error ( f"Error: { res.status_code }")


# Show response history
if st.session_state.history:
    st.markdown("---")
    st.markdown("## Previous Queries")
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {entry['query'][:60]}... ({entry['timestamp']})"):
            st.write(entry["response"])
            st.markdown(f"**Input tokens:** {entry['input_tokens']}  \n**Output tokens:** {entry['output_tokens']}")
            
