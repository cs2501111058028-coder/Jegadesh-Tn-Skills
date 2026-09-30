"""
Automated Demo Video Recording Script for EduGenie
Uses Playwright with on-screen caption overlays and converts to MP4 with ffmpeg.
Outputs media/Demo_Video.mp4 (~3.5 minutes duration).
"""

import os
import time
import subprocess
import shutil
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MEDIA_DIR = os.path.join(REPO_DIR, "media")
TEMP_VIDEO_DIR = os.path.join(REPO_DIR, "temp_demo_video")

os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(TEMP_VIDEO_DIR, exist_ok=True)

def inject_caption_banner(page):
    """Injects a stylish live caption banner into the browser page."""
    page.evaluate("""
    () => {
        if (!document.getElementById('demo-caption-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'demo-caption-overlay';
            overlay.style.position = 'fixed';
            overlay.style.bottom = '20px';
            overlay.style.left = '50%';
            overlay.style.transform = 'translateX(-50%)';
            overlay.style.width = '88%';
            overlay.style.maxWidth = '900px';
            overlay.style.backgroundColor = 'rgba(15, 23, 42, 0.94)';
            overlay.style.color = '#ffffff';
            overlay.style.padding = '14px 20px';
            overlay.style.borderRadius = '12px';
            overlay.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.4)';
            overlay.style.fontFamily = "'Plus Jakarta Sans', system-ui, sans-serif";
            overlay.style.fontSize = '15px';
            overlay.style.lineHeight = '1.5';
            overlay.style.zIndex = '999999';
            overlay.style.border = '1.5px solid rgba(99, 102, 241, 0.8)';
            overlay.style.backdropFilter = 'blur(10px)';
            overlay.style.transition = 'all 0.3s ease';
            overlay.innerHTML = '<div id="demo-caption-title" style="font-weight: 700; color: #818cf8; margin-bottom: 4px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">EduGenie Demo</div><div id="demo-caption-text">Welcome to EduGenie AI Learning Assistant</div>';
            document.body.appendChild(overlay);
        }
    }
    """)

def update_caption(page, title, text, duration_sec=3):
    """Updates the caption banner and pauses for recorded video view."""
    page.evaluate(f"""
    () => {{
        const titleEl = document.getElementById('demo-caption-title');
        const textEl = document.getElementById('demo-caption-text');
        if (titleEl && textEl) {{
            titleEl.textContent = `{title}`;
            textEl.textContent = `{text}`;
        }}
    }}
    """)
    time.sleep(duration_sec)

def smooth_scroll(page, selector, steps=10, pause=0.05):
    """Smoothly scrolls element into view."""
    page.locator(selector).scroll_into_view_if_needed()
    time.sleep(0.5)

def record_demo():
    print(f"Starting EduGenie demo video recording from {BASE_URL}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=TEMP_VIDEO_DIR,
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        # 1. Introduction (0:00 - 0:20)
        page.goto(BASE_URL)
        page.wait_for_selector(".navbar")
        inject_caption_banner(page)
        update_caption(
            page,
            "Scene 1: Introduction & Architecture",
            "Welcome to EduGenie — An Intelligent Learning Assistant powered by Google Gemini & Generative AI.",
            duration_sec=7
        )
        update_caption(
            page,
            "System Configuration",
            "FastAPI backend with deterministic offline fallbacks, health check monitoring, and multi-model support.",
            duration_sec=7
        )

        # 2. Scenario 1: Smart Q&A (0:20 - 0:45)
        smooth_scroll(page, "#card-qa")
        update_caption(
            page,
            "Scene 2: Scenario 1 — Smart Q&A",
            "A student wants to know about oceans: Querying 'Which is the largest ocean?'...",
            duration_sec=5
        )
        page.fill("#qa-input", "Which is the largest ocean?")
        time.sleep(2)
        page.click("#btn-qa-submit")
        page.wait_for_selector("#result-qa", state="visible")
        update_caption(
            page,
            "Scenario 1: Factual Precision",
            "EduGenie returns a concise, accurate answer: The Pacific Ocean covers over 30% of Earth's surface.",
            duration_sec=12
        )

        # 3. Scenario 2: Concept Explainer - Quantum Computing (0:45 - 1:20)
        smooth_scroll(page, "#card-explain")
        update_caption(
            page,
            "Scene 3: Scenario 2 — Concept Explainer",
            "Explaining 'quantum computing' simply for school students using Gemini AI...",
            duration_sec=6
        )
        page.fill("#explain-input", "quantum computing")
        page.click('input[name="explain-backend"][value="gemini"]')
        time.sleep(2)
        page.click("#btn-explain-submit")
        page.wait_for_selector("#result-explain", state="visible")
        update_caption(
            page,
            "Concept Simplification: Quantum Computing",
            "Complex quantum principles (Superposition, Qubits, Entanglement) broken down with spinning coin analogies.",
            duration_sec=15
        )

        # 4. Scenario 2b: Binary Search Algorithm with Local Option (1:20 - 1:55)
        update_caption(
            page,
            "Scene 4: Scenario 2b — Local Backend Option",
            "Explaining 'binary search algorithm' using local LaMini-Flan-T5-783M inference...",
            duration_sec=6
        )
        page.fill("#explain-input", "binary search algorithm")
        page.click('input[name="explain-backend"][value="local"]')
        time.sleep(2)
        page.click("#btn-explain-submit")
        page.wait_for_selector("#result-explain", state="visible")
        update_caption(
            page,
            "Local Inference: Binary Search Explained",
            "Phonebook analogy demonstrates O(log n) efficiency: 1,000,000 items searched in only 20 comparisons!",
            duration_sec=16
        )

        # 5. Scenario 3: Text Summarization (1:55 - 2:30)
        smooth_scroll(page, "#card-summarize")
        update_caption(
            page,
            "Scene 5: Scenario 3 — Textbook Summarizer",
            "Loading comprehensive Industrial Revolution textbook passage into the multiline input...",
            duration_sec=6
        )
        page.click("#btn-sample-revolution")
        time.sleep(3)
        page.click("#btn-summarize-submit")
        page.wait_for_selector("#result-summarize", state="visible")
        update_caption(
            page,
            "Executive Study Notes",
            "Extracts key breakthroughs: steam power, textile mechanization, rapid urbanization, and global societal impacts.",
            duration_sec=16
        )

        # 6. Scenario 4: Interactive Quiz on Pythagoras Theorem (2:30 - 3:10)
        smooth_scroll(page, "#card-quiz")
        update_caption(
            page,
            "Scene 6: Scenario 4 — Quiz Generation",
            "Generating 3 Multiple-Choice Questions on 'Pythagoras theorem'...",
            duration_sec=6
        )
        page.fill("#quiz-input", "Pythagoras theorem")
        time.sleep(2)
        page.click("#btn-quiz-submit")
        page.wait_for_selector("#result-quiz", state="visible")
        update_caption(
            page,
            "Interactive Quiz Assessment",
            "Answering questions: selecting correct answers for Q1 & Q3, and intentionally testing a wrong choice for Q2...",
            duration_sec=8
        )
        # Select answers: Q0 correct, Q1 wrong, Q2 correct
        page.click('#opt-label-0-0')
        time.sleep(2)
        page.click('#opt-label-1-0')
        time.sleep(2)
        page.click('#opt-label-2-0')
        time.sleep(2)
        page.click("#btn-submit-all-quiz")
        time.sleep(2)
        smooth_scroll(page, "#card-quiz")
        update_caption(
            page,
            "Automated Grader & Score Tracking",
            "Score 2/3 (66.7%): Correct answers highlighted in emerald green, mistakes in red with correct formula revealed.",
            duration_sec=16
        )

        # 7. Scenario 5: Learning Roadmap for SQL (3:10 - 3:35)
        smooth_scroll(page, "#card-learn")
        update_caption(
            page,
            "Scene 7: Scenario 5 — Learning Roadmap",
            "Generating personalized 3-stage curriculum for 'SQL' with timelines and curated resources...",
            duration_sec=6
        )
        page.fill("#learn-input", "SQL")
        time.sleep(2)
        page.click("#btn-learn-submit")
        page.wait_for_selector("#result-learn", state="visible")
        update_caption(
            page,
            "Structured Learning Roadmap: SQL",
            "Stage 1: Beginner Fundamentals • Stage 2: Intermediate Data Manipulation • Stage 3: Advanced Optimization.",
            duration_sec=14
        )

        # 8. Wrap up & OpenAPI Docs (3:35 - 3:45)
        page.goto(f"{BASE_URL}/docs")
        inject_caption_banner(page)
        update_caption(
            page,
            "FastAPI Interactive Swagger Documentation",
            "Comprehensive RESTful API endpoints with full Pydantic schema validation and OpenAPI specification.",
            duration_sec=8
        )

        context.close()
        video_path = page.video.path()
        browser.close()

    print(f"Playwright recording finished at: {video_path}")

    # Convert with ffmpeg to standard MP4
    output_mp4 = os.path.join(MEDIA_DIR, "Demo_Video.mp4")
    print(f"Encoding MP4 video to {output_mp4} using ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Successfully created {output_mp4} ({os.path.getsize(output_mp4) / (1024*1024):.2f} MB)")

    # Cleanup temp
    shutil.rmtree(TEMP_VIDEO_DIR, ignore_errors=True)

if __name__ == "__main__":
    record_demo()
