# Multimodal Attendance & Engagement Agent

An offline classroom intelligence system for automated attendance tracking, engagement dynamics analysis, AI-driven teaching suggestions, and session analytics.

## Overview
Traditional manual roll calls or basic biometric checks miss learner attention and classroom participation context. This project combines computer vision, audio activity analysis, agent-based reasoning, and analytics to support educators in real time while keeping processing offline and privacy-preserving.

## Project Structure & Modules
- `app.py`: Streamlit dashboard for running simulated or webcam snapshots, viewing metrics, and inspecting session history.
- `modules/vision_module.py`: Detects faces/participants, tracks sustained presence for attendance, and estimates visual engagement.
- `modules/audio_module.py`: Captures or simulates audio chunks to classify classroom activity and audio engagement.
- `modules/engagement_agent.py`: Fuses vision and audio signals into an overall engagement score (`0`–`100`), level (`High`, `Moderate`, `Low`), and actionable teaching suggestions.
- `modules/analytics.py`: Saves session records to `data/logs/session_logs.csv` and computes summary statistics.

## How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt