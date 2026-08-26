import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { uploadFile } from "../services/api.js";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const ACCEPTED = [".csv", ".xlsx", ".xls"];
  const MAX_SIZE = 20 * 1024 * 1024;

  const validate = (f) => {
    if (!f) return "Aucun fichier selectionne.";
    const ext = "." + f.name.split(".").pop().toLowerCase();
    if (!ACCEPTED.includes(ext))
      return `Format non supporte. ${ACCEPTED.join(", ")} acceptes.`;
    if (f.size > MAX_SIZE) return "Fichier trop lourd. 20 Mo max.";
    return null;
  };

  const handleFile = (f) => {
    setError("");
    const err = validate(f);
    if (err) {
      setError(err);
      return;
    }
    setFile(f);
    if (!title) setTitle(f.name.replace(/\.[^.]+$/, ""));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) handleFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Selectionnez un fichier.");
      return;
    }
    setUploading(true);
    setError("");
    try {
      const res = await uploadFile(file, title);
      navigate(`/dashboard/${res.dashboard_link}`, {
        state: { processing: true },
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-card">
        <h1 className="upload-title">Analyser un fichier</h1>
        <p className="upload-subtitle">
          CSV ou Excel — on s'occupe du reste
        </p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="upload-form">
          <div
            className={`upload-zone ${dragActive ? "upload-zone-active" : ""} ${
              file ? "upload-zone-filled" : ""
            }`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
          >
            <input
              ref={inputRef}
              type="file"
              accept={ACCEPTED.join(",")}
              onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              style={{ display: "none" }}
            />
            {file ? (
              <div className="upload-file-info">
                <svg
                  width="28"
                  height="28"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="var(--c-green)"
                  strokeWidth="2"
                >
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
                <span className="upload-file-name">{file.name}</span>
                <span className="upload-file-size">
                  {(file.size / 1024).toFixed(1)} Ko
                </span>
                <button
                  type="button"
                  className="upload-remove"
                  onClick={(e) => {
                    e.stopPropagation();
                    setFile(null);
                    setError("");
                  }}
                >
                  Retirer
                </button>
              </div>
            ) : (
              <div className="upload-placeholder">
                <svg
                  width="40"
                  height="40"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="var(--c-ink-faint)"
                  strokeWidth="1.5"
                >
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
                <p className="upload-text">Glissez votre fichier ici</p>
                <p className="upload-hint">ou cliquez pour parcourir</p>
                <p className="upload-formats">CSV, XLSX — max 20 Mo</p>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="title">Nom du rapport</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Ex: Ventes Q1 2024"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={uploading || !file}
          >
            {uploading ? (
              <span className="btn-loading">
                <span className="spinner-small" />
                Upload en cours...
              </span>
            ) : (
              "Lancer l'analyse"
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
