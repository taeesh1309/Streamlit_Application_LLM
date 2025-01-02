import streamlit as st


def show() -> None:
	with st.sidebar:
		st.markdown(f"""
			<a href="/" style="color:black;text-decoration: none;">
				<div style="display:table;margin-top:-16rem;margin-left:0%;">
					<img src="/app/static/logo2.png" width="30" ><span style="font-size: 0.8em; color: white">DUCKY</span>
					<span style="font-size: 0.8em; color: white">&nbsp;&nbsp;v0.1.0</span>
					<br>
					<span style="font-size: 0.8em; color: white">Your AI-powered personal coding assistant!</span>
				</div>
			</a>
			<br>
				""", unsafe_allow_html=True)

		reload_button = st.button("↪︎  Reload Page")
		if reload_button:
			st.session_state.clear()
			st.experimental_rerun()

