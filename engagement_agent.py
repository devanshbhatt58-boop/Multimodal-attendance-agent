from datetime import datetime


class ClassroomEngagementAgent:
    """Fuses vision and audio signals to score engagement and suggest teaching actions."""

    def __init__(self, vision_weight: float = 0.65, audio_weight: float = 0.35):
        total = vision_weight + audio_weight
        self.vision_weight = vision_weight / total
        self.audio_weight = audio_weight / total
        self.history = []

    def evaluate(self, vision_data: dict, audio_data: dict) -> dict:
        face_count = vision_data.get("face_count", 0)
        attendance_status = vision_data.get("attendance_status", "Observing")
        visual_eng = float(vision_data.get("visual_engagement", 0.0))
        audio_eng = float(audio_data.get("audio_engagement", 0.0))
        audio_activity = audio_data.get("audio_activity", "Silent / Low Activity")

        # If no participants are detected on camera, keep score conservative
        if face_count == 0:
            overall_score = round(audio_eng * 0.25, 1)
        else:
            overall_score = round(
                (visual_eng * self.vision_weight) + (audio_eng * self.audio_weight),
                1,
            )

        if overall_score >= 75.0:
            engagement_level = "High"
        elif overall_score >= 45.0:
            engagement_level = "Moderate"
        else:
            engagement_level = "Low"

        suggestion = self._generate_teaching_suggestion(
            face_count=face_count,
            engagement_level=engagement_level,
            audio_activity=audio_activity,
        )

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "face_count": face_count,
            "attendance_status": attendance_status,
            "visual_engagement": visual_eng,
            "audio_engagement": audio_eng,
            "audio_activity": audio_activity,
            "overall_engagement": overall_score,
            "engagement_level": engagement_level,
            "teaching_suggestion": suggestion,
        }
        self.history.append(record)
        return record

    def _generate_teaching_suggestion(
        self, face_count: int, engagement_level: str, audio_activity: str
    ) -> str:
        if face_count == 0:
            return (
                "Koi participant camera range mein nahi dikh raha hai — "
                "session start ya camera framing check karein."
            )
        if engagement_level == "Low" and "Silent" in audio_activity:
            return (
                "Engagement aur audio activity dono low hain — ek quick poll, "
                "live question, ya real-world example se class ko active karein."
            )
        if engagement_level == "Moderate" and "Silent" in audio_activity:
            return (
                "Students visual tor par dekh rahe hain par bol nahi rahe — "
                "2-3 learners se chhota sa concept recap ya doubt poochein."
            )
        if "High Noise" in audio_activity:
            return (
                "Audio noise/overlapping talk zyada hai — topic recap karke "
                "structured Q&A ya group turn-taking set karein."
            )
        return (
            "Class ka engagement healthy hai — current teaching pace aur "
            "interactive flow ko continue rakhein."
        )


if __name__ == "__main__":
    agent = ClassroomEngagementAgent()
    sample_vision = {
        "face_count": 3,
        "attendance_status": "Present (Sustained)",
        "visual_engagement": 78.0,
    }
    sample_audio = {
        "audio_activity": "Silent / Low Activity",
        "audio_engagement": 35.0,
    }
    print("Agent Test Output:", agent.evaluate(sample_vision, sample_audio))