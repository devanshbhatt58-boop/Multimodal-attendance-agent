import cv2
import streamlit as st

from modules.analytics import SessionAnalytics
from modules.audio_module import ClassroomAudioAnalyzer
from modules.engagement_agent import ClassroomEngagementAgent
from modules.vision_module import ClassroomVisionAnalyzer

st.set_page_config(
    page_title="Multimodal Attendance & Engagement Agent",
    layout="wide",
)

st.title("Multimodal Attendance & Engagement Agent")
st.caption(
    "Offline classroom intelligence for sustained attendance, engagement analysis, and teaching suggestions."
)

if "vision_analyzer" not in st.session_state:
    st.session_state.vision_analyzer = ClassroomVisionAnalyzer(required_presence_seconds=3.0)
if "audio_analyzer" not in st.session_state:
    st.session_state.audio_analyzer = ClassroomAudioAnalyzer(duration=0.4)
if "agent" not in st.session_state:
    st.session_state.agent = ClassroomEngagementAgent()
if "analytics" not in st.session_state:
    st.session_state.analytics = SessionAnalytics()

mode = st.sidebar.radio(
    "Input Mode",
    ["Simulated Classroom Sample (Safe / No Camera Needed)", "Webcam Snapshot"],
)

if st.button("Analyze Current Classroom State"):
    if mode == "Webcam Snapshot":
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            vision_res = st.session_state.vision_analyzer.analyze_frame(frame)
            st.image(
                cv2.cvtColor(vision_res["annotated_frame"], cv2.COLOR_BGR2RGB),
                caption="Analyzed Camera Frame",
                use_container_width=True,
            )
        else:
            st.warning("Webcam open nahi ho paaya — simulated sample use kiya ja raha hai.")
            vision_res = {
                "face_count": 2,
                "attendance_status": "Present (Sustained)",
                "presence_ratio": 82.0,
                "motion_score": 4.5,
                "visual_engagement": 84.0,
            }
    else:
        vision_res = {
            "face_count": 4,
            "attendance_status": "Present (Sustained)",
            "presence_ratio": 88.0,
            "motion_score": 5.2,
            "visual_engagement": 82.5,
        }

    audio_res = st.session_state.audio_analyzer.capture_and_analyze(simulate_if_unavailable=True)
    record = st.session_state.agent.evaluate(vision_res, audio_res)
    log_file = st.session_state.analytics.save_records(st.session_state.agent.history)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Detected Faces", record["face_count"])
    col2.metric("Attendance", record["attendance_status"])
    col3.metric("Overall Engagement", f"{record['overall_engagement']} / 100")
    col4.metric("Level", record["engagement_level"])

    st.info(f"**AI Teaching Suggestion:** {record['teaching_suggestion']}")
    st.caption(f"Log saved to: `{log_file}` | Audio source: `{audio_res['source']}`")

if st.session_state.agent.history:
    summary = st.session_state.analytics.summarize(st.session_state.agent.history)
    st.subheader("Session Summary")
    st.json(summary)

    st.subheader("Engagement & Attendance History")
    st.dataframe(st.session_state.agent.history, use_container_width=True)