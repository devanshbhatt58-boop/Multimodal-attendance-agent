import time
import cv2
import numpy as np


class ClassroomVisionAnalyzer:
    """Tracks participant detection, sustained presence attendance, and visual engagement."""

    def __init__(self, required_presence_seconds: float = 5.0):
        self.required_presence_seconds = required_presence_seconds
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        self.start_time = time.time()
        self.total_frames = 0
        self.active_frames = 0
        self.prev_gray = None

    def analyze_frame(self, frame: np.ndarray) -> dict:
        self.total_frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(40, 40),
        )
        face_count = int(len(faces))

        motion_score = 0.0
        if self.prev_gray is not None:
            diff = cv2.absdiff(self.prev_gray, gray)
            motion_score = float(np.mean(diff))
        self.prev_gray = gray

        if face_count > 0:
            self.active_frames += 1

        elapsed_seconds = max(0.0, time.time() - self.start_time)
        presence_ratio = self.active_frames / max(1, self.total_frames)
        sustained_present = (
            elapsed_seconds >= self.required_presence_seconds and presence_ratio >= 0.4
        )
        attendance_status = "Present (Sustained)" if sustained_present else "Observing"

        presence_component = min(1.0, presence_ratio) * 70.0
        if face_count == 0:
            motion_component = 0.0
        elif motion_score < 1.0:
            motion_component = 12.0
        elif motion_score <= 12.0:
            motion_component = 30.0
        else:
            motion_component = 18.0

        visual_engagement = round(min(100.0, presence_component + motion_component), 1)

        annotated = frame.copy()
        for idx, (x, y, w, h) in enumerate(faces, start=1):
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 200, 90), 2)
            cv2.putText(
                annotated,
                f"Participant {idx}",
                (x, max(20, y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 200, 90),
                2,
            )

        return {
            "face_count": face_count,
            "attendance_status": attendance_status,
            "presence_ratio": round(presence_ratio * 100, 1),
            "motion_score": round(motion_score, 2),
            "visual_engagement": visual_engagement,
            "annotated_frame": annotated,
        }


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    analyzer = ClassroomVisionAnalyzer(required_presence_seconds=3.0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result = analyzer.analyze_frame(frame)
        info = (
            f"Faces: {result['face_count']} | "
            f"{result['attendance_status']} | "
            f"Eng: {result['visual_engagement']}"
        )
        cv2.putText(
            result["annotated_frame"],
            info,
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 0),
            2,
        )
        cv2.imshow("Vision Module Test", result["annotated_frame"])
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()