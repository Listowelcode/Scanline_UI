"use client";

export default function AlertModal({ message, onClose }) {
  if (!message) return null;

  return (
    <div
      className="alert-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="alertTitle"
      onClick={onClose}
    >
      <div className="alert-box" onClick={(e) => e.stopPropagation()}>
        <div className="alert-title" id="alertTitle">
          <span className="prompt-caret">&gt;</span> Scanline says
        </div>
        <p className="alert-message">{message}</p>
        <button className="alert-ok-btn" autoFocus onClick={onClose}>
          OK
        </button>
      </div>
    </div>
  );
}
