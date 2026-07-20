"use client";

import { useEffect, useRef, useState } from "react";
import AlertModal from "./AlertModal";

// ===============================
// ScanLine Frontend (Next.js)
// Ported 1:1 from the original vanilla script.js
// Backend endpoints / base URL are untouched.
// ===============================

const API = "http://127.0.0.1:8000";

function formatDuration(seconds) {
  if (!seconds) {
    return "Unknown";
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
}

export default function ScanlineApp() {
  const [videoUrlValue, setVideoUrlValue] = useState("");
  const [statusText, setStatusText] = useState("Waiting...");
  const [progressWidth, setProgressWidth] = useState(0);
  const [extractDisabled, setExtractDisabled] = useState(true);
  const [preview, setPreview] = useState(null); // { thumbnail, title, channel, duration } | null
  const [downloadFile, setDownloadFile] = useState(null);
  const [alertMessage, setAlertMessage] = useState(null);

  const currentUrlRef = useRef("");
  const videoReadyRef = useRef(false);
  const pollIntervalRef = useRef(null);

  // ===============================
  // Custom "Scanline says" alert (replaces window.alert)
  // ===============================
  const showAlert = (message) => setAlertMessage(message);
  const closeAlert = () => setAlertMessage(null);

  // ===============================
  // Animated tab title — cycles "ScanLine | scan" -> "ScanLine | analyse"
  // -> "ScanLine | rebuild" with a typewriter effect, looping forever.
  // ===============================
  useEffect(() => {
    const prefix = "ScanLine | ";
    const words = ["scan", "analyse", "rebuild"];

    let wordIndex = 0;
    let charIndex = 0;
    let deleting = false;
    let timeoutId;

    const TYPE_SPEED = 110;
    const DELETE_SPEED = 55;
    const HOLD_AFTER_TYPE = 1300;
    const HOLD_AFTER_DELETE = 300;

    const tick = () => {
      const word = words[wordIndex];

      if (!deleting) {
        charIndex += 1;
        document.title = prefix + word.slice(0, charIndex);

        if (charIndex === word.length) {
          deleting = true;
          timeoutId = setTimeout(tick, HOLD_AFTER_TYPE);
          return;
        }

        timeoutId = setTimeout(tick, TYPE_SPEED);
      } else {
        charIndex -= 1;
        document.title = prefix + word.slice(0, charIndex);

        if (charIndex === 0) {
          deleting = false;
          wordIndex = (wordIndex + 1) % words.length;
          timeoutId = setTimeout(tick, HOLD_AFTER_DELETE);
          return;
        }

        timeoutId = setTimeout(tick, DELETE_SPEED);
      }
    };

    timeoutId = setTimeout(tick, HOLD_AFTER_DELETE);

    return () => {
      clearTimeout(timeoutId);
      document.title = "ScanLine";
    };
  }, []);

  // Clean up any running polling interval on unmount
  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  // ===============================
  // Generate Preview
  // ===============================
  const handleGenerate = async () => {
    const url = videoUrlValue.trim();

    if (url === "") {
      showAlert("Please enter a video URL.");
      return;
    }

    currentUrlRef.current = url;
    videoReadyRef.current = false;
    setExtractDisabled(true);

    setStatusText("Getting video information...");

    try {
      const response = await fetch(API + "/preview", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          youtube_url: url,
        }),
      });

      const data = await response.json();

      console.log(data);

      if (data.error) {
        setStatusText("Unable to load video.");
        return;
      }

      setPreview({
        thumbnail: data.thumbnail,
        title: data.title,
        channel: data.channel,
        duration: data.duration,
      });

      setStatusText("Video ready.");

      videoReadyRef.current = true;
      setExtractDisabled(false);
    } catch (error) {
      console.error(error);
      setStatusText("Backend connection failed.");
    }
  };

  // ===============================
  // Progress Tracking
  // ===============================
  const startProgressPolling = () => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(API + "/progress");
        const data = await response.json();

        console.log(data);

        setProgressWidth(data.progress);
        setStatusText(data.message);

        if (data.progress >= 100) {
          clearInterval(interval);
          pollIntervalRef.current = null;

          setStatusText("Extraction Complete!");

          if (data.file) {
            setDownloadFile(data.file);
          }
        }
      } catch (error) {
        console.error(error);
        clearInterval(interval);
        pollIntervalRef.current = null;

        setStatusText("Progress tracking failed.");
      }
    }, 1000);

    pollIntervalRef.current = interval;
  };

  // ===============================
  // Start Extraction
  // ===============================
  const handleExtract = async () => {
    if (!videoReadyRef.current) {
      showAlert("Please generate a preview first.");
      return;
    }

    setStatusText("Starting ScanLine...");
    setProgressWidth(0);

    try {
      const response = await fetch(API + "/scan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          youtube_url: currentUrlRef.current,
        }),
      });

      const data = await response.json();

      console.log(data);

      setStatusText(data.message);

      startProgressPolling();
    } catch (error) {
      console.error(error);
      setStatusText("Unable to start scan.");
    }
  };

  // ===============================
  // Download
  // ===============================
  const handleDownload = () => {
    window.open(`${API}/download/${downloadFile}`, "_blank");
  };

  // ===============================
  // Reset
  // ===============================
  const handleReset = () => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }

    currentUrlRef.current = "";
    videoReadyRef.current = false;

    setExtractDisabled(true);
    setVideoUrlValue("");
    setPreview(null);
    setStatusText("Waiting...");
    setProgressWidth(0);
    setDownloadFile(null);
  };

  return (
    <>
      <AlertModal message={alertMessage} onClose={closeAlert} />

      <div className="scan-overlay" aria-hidden="true"></div>

      <div className="page-wrap">
        <div className="intro">
          <span className="intro-tag">&#9656; how it works</span>
          <h2>
            Turn 5-hour coding tutorials into downloadable projects &mdash; in
            minutes
          </h2>
          <p>Just paste the video URL or upload the file to get started.</p>
        </div>

        <div className="terminal">
          <div className="terminal-bar">
            <div className="terminal-dots">
              <span className="dot dot-red"></span>
              <span className="dot dot-yellow"></span>
              <span className="dot dot-green"></span>
            </div>
            <div className="terminal-title">
              scanline&nbsp;&mdash;&nbsp;video-extractor
            </div>
            <div className="terminal-beam" aria-hidden="true"></div>
          </div>

          <div className="container">
            <h1>
              <span className="prompt-caret">&gt;</span> ScanLine
              <span className="cursor-blink">_</span>
            </h1>
            <p>Extract and analyze videos from URLs</p>

            <div className="url-section">
              <div className="input-wrap">
                <span className="input-glyph">$</span>
                <input
                  type="text"
                  id="videoUrl"
                  placeholder="paste video URL here..."
                  spellCheck="false"
                  autoComplete="off"
                  value={videoUrlValue}
                  onChange={(e) => setVideoUrlValue(e.target.value)}
                />
              </div>

              <button id="generateBtn" onClick={handleGenerate}>
                <span className="btn-glyph">&#9656;</span> Generate
              </button>
            </div>

            {/* Video Preview */}
            <div className="preview-box">
              <h3>Video Preview</h3>

              <video id="videoPreview" controls hidden></video>

              {preview ? (
                <div id="previewText">
                  {preview.thumbnail && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={preview.thumbnail}
                      width="100%"
                      style={{ borderRadius: "10px" }}
                      alt={preview.title || "video thumbnail"}
                    />
                  )}
                  <h3>{preview.title}</h3>
                  <p>Channel: {preview.channel}</p>
                  <p>Duration: {formatDuration(preview.duration)}</p>
                </div>
              ) : (
                <p id="previewText">No video loaded</p>
              )}
            </div>

            {/* Actions */}
            <div className="actions">
              <button
                id="extractBtn"
                disabled={extractDisabled}
                onClick={handleExtract}
              >
                <span className="btn-icon icon-extract" aria-hidden="true"></span>
                Extract Full Video
              </button>

              <button id="resetBtn" onClick={handleReset}>
                <span className="btn-icon icon-reset" aria-hidden="true"></span>
                Reset
              </button>
            </div>

            {/* Progress */}
            <div className="progress-box">
              <h3>Status</h3>

              <p id="status">{statusText}</p>

              <div className="progress-bar">
                <div
                  id="progressFill"
                  style={{ width: `${progressWidth}%` }}
                ></div>
              </div>

              {downloadFile && (
                <button
                  id="downloadBtn"
                  style={{
                    marginTop: "15px",
                    padding: "12px",
                    width: "100%",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    background: "#2563eb",
                    color: "white",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                  onClick={handleDownload}
                >
                  <span
                    className="btn-icon icon-download"
                    aria-hidden="true"
                    style={{ marginRight: "8px" }}
                  ></span>
                  Download Result
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
