-- One row per saved high score. Scores are stored in tenths of a second (47.3s = 473).
CREATE TABLE IF NOT EXISTS scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  score_tenths INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  ip_hash TEXT NOT NULL  -- hashed, only used to slow down rapid-fire submissions
);
CREATE INDEX IF NOT EXISTS idx_scores_rank ON scores (score_tenths DESC, id ASC);
CREATE INDEX IF NOT EXISTS idx_scores_ip_time ON scores (ip_hash, created_at);
