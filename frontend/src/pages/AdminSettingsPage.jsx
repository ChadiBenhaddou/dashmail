import { useState, useEffect } from "react";
import { getSettings, updateSettings } from "../services/api.js";

const MASKED = "••••••••";

export default function AdminSettingsPage() {
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [feedback, setFeedback] = useState("");

  useEffect(() => {
    getSettings()
      .then(setForm)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const set = (key, value) => setForm((f) => ({ ...f, [key]: value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    setFeedback("");
    try {
      const updated = await updateSettings(form);
      setForm(updated);
      setFeedback("Configuration enregistree et appliquee.");
      setTimeout(() => setFeedback(""), 4000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading)
    return (
      <div className="upload-page">
        <div className="loading-spinner" />
      </div>
    );

  if (!form)
    return (
      <div className="upload-page">
        <div className="auth-error">{error || "Impossible de charger la configuration"}</div>
      </div>
    );

  const SecretField = ({ keyName, label, placeholder, help }) => {
    const isSet = form[`${keyName}_is_set`];
    const currentValue = form[keyName];
    return (
      <div className="form-group">
        <label htmlFor={keyName}>
          {label}
          {isSet && (
            <span className="settings-dot" title="Valeur enregistree">
              ●
            </span>
          )}
        </label>
        <input
          id={keyName}
          type="password"
          value={isSet && currentValue === MASKED ? "" : currentValue || ""}
          onChange={(e) => set(keyName, e.target.value)}
          placeholder={isSet ? "Laissez vide pour conserver la valeur actuelle" : placeholder}
          autoComplete="off"
        />
        {help && <span className="settings-help">{help}</span>}
      </div>
    );
  };

  return (
    <div className="reports-page">
      <div className="reports-container admin-settings">
        <div className="reports-header">
          <div>
            <h1 className="reports-title">Configuration</h1>
            <p className="reports-subtitle">
              Parametres de l'IA et des emails — enregistres en base, priorite
              sur les variables d'environnement
            </p>
          </div>
        </div>

        {feedback && <div className="settings-feedback success">{feedback}</div>}
        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="settings-form">
          {/* LLM */}
          <div className="card settings-section">
            <div className="settings-section-header">
              <span className="settings-section-icon">AI</span>
              <div>
                <h3 className="settings-section-title">Intelligence artificielle</h3>
                <p className="settings-section-desc">
                  Cle d'API et modele OpenAI utilises pour l'analyse des fichiers.
                </p>
              </div>
            </div>
            <div className="settings-fields">
              <SecretField
                keyName="llm_api_key"
                label="Cle API (OpenAI)"
                placeholder="sk-..."
                help="Conservee au format masque. Laissez vide pour garder la valeur actuelle."
              />
              <div className="form-group">
                <label htmlFor="llm_api_base_url">URL de base API</label>
                <input
                  id="llm_api_base_url"
                  type="text"
                  value={form.llm_api_base_url || ""}
                  onChange={(e) => set("llm_api_base_url", e.target.value)}
                  placeholder="https://api.openai.com/v1"
                />
                <span className="settings-help">Optionnel — provider compatible OpenAI.</span>
              </div>
              <div className="form-group">
                <label htmlFor="llm_model">Modele</label>
                <input
                  id="llm_model"
                  type="text"
                  value={form.llm_model || ""}
                  onChange={(e) => set("llm_model", e.target.value)}
                  placeholder="gpt-4o"
                />
                <span className="settings-help">Optionnel — defaut gpt-4o.</span>
              </div>
            </div>
          </div>

          {/* SMTP */}
          <div className="card settings-section">
            <div className="settings-section-header">
              <span className="settings-section-icon">@</span>
              <div>
                <h3 className="settings-section-title">Email — envoi (SMTP)</h3>
                <p className="settings-section-desc">
                  Utilise pour envoyer les liens vers les dashboards.
                </p>
              </div>
            </div>
            <div className="settings-fields">
              <div className="settings-grid-2">
                <div className="form-group">
                  <label htmlFor="email_host">Serveur SMTP</label>
                  <input
                    id="email_host"
                    type="text"
                    value={form.email_host || ""}
                    onChange={(e) => set("email_host", e.target.value)}
                    placeholder="smtp.gmail.com"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="email_port">Port</label>
                  <input
                    id="email_port"
                    type="number"
                    value={form.email_port ?? 587}
                    onChange={(e) => set("email_port", Number(e.target.value))}
                  />
                </div>
              </div>
              <div className="settings-grid-2">
                <div className="form-group">
                  <label htmlFor="email_host_user">Utilisateur</label>
                  <input
                    id="email_host_user"
                    type="text"
                    value={form.email_host_user || ""}
                    onChange={(e) => set("email_host_user", e.target.value)}
                    placeholder="vous@example.com"
                  />
                </div>
                <SecretField
                  keyName="email_host_password"
                  label="Mot de passe SMTP"
                  placeholder="Mot de passe / app password"
                />
              </div>
              <div className="settings-grid-2">
                <div className="form-group">
                  <label htmlFor="email_from">Email expediteur</label>
                  <input
                    id="email_from"
                    type="email"
                    value={form.email_from || ""}
                    onChange={(e) => set("email_from", e.target.value)}
                    placeholder="reports@example.com"
                  />
                </div>
                <div className="form-group settings-check">
                  <label className="settings-check-label">
                    <input
                      type="checkbox"
                      checked={form.email_use_tls}
                      onChange={(e) => set("email_use_tls", e.target.checked)}
                    />
                    Utiliser TLS
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* IMAP */}
          <div className="card settings-section">
            <div className="settings-section-header">
              <span className="settings-section-icon">in</span>
              <div>
                <h3 className="settings-section-title">Email — reception (IMAP)</h3>
                <p className="settings-section-desc">
                  Boite de reception pour creer des dashboards a partir de fichiers joints.
                </p>
              </div>
            </div>
            <div className="settings-fields">
              <div className="settings-grid-2">
                <div className="form-group">
                  <label htmlFor="imap_host">Serveur IMAP</label>
                  <input
                    id="imap_host"
                    type="text"
                    value={form.imap_host || ""}
                    onChange={(e) => set("imap_host", e.target.value)}
                    placeholder="imap.gmail.com"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="imap_port">Port</label>
                  <input
                    id="imap_port"
                    type="number"
                    value={form.imap_port ?? 993}
                    onChange={(e) => set("imap_port", Number(e.target.value))}
                  />
                </div>
              </div>
              <div className="settings-grid-2">
                <div className="form-group">
                  <label htmlFor="imap_user">Utilisateur</label>
                  <input
                    id="imap_user"
                    type="text"
                    value={form.imap_user || ""}
                    onChange={(e) => set("imap_user", e.target.value)}
                    placeholder="vous@example.com"
                  />
                </div>
                <SecretField
                  keyName="imap_password"
                  label="Mot de passe IMAP"
                  placeholder="Mot de passe / app password"
                />
              </div>
            </div>
          </div>

          <div className="settings-footer">
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? (
                <span className="btn-loading">
                  <span className="spinner-small" />
                  Enregistrement...
                </span>
              ) : (
                "Enregistrer la configuration"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
