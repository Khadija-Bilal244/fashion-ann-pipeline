# Assignment 3 — Full Walkthrough

This guide gives you the exact commands for every sub-task (A1–E5), plus the
written explanations the assignment asks for. Run these yourself, in order,
in your own terminal — take the screenshots as you go, since only you can
produce those (they have to show *your* GitHub account, *your* Google Drive
folder, and *your* terminal). The `src/`, `params.yaml`, and `dvc.yaml` files
in this bundle are ready to drop in as-is.

---

## Part A — Git Fundamentals

### A1. Init + first commit

```bash
mkdir fashion-ann-pipeline && cd fashion-ann-pipeline
git init
# copy README.md, .gitignore, requirements.txt from this bundle in here
git add README.md .gitignore requirements.txt
git commit -m "Initial commit: README, gitignore, requirements"
git branch -M main
git remote add origin https://github.com/<your-username>/fashion-ann-pipeline.git
git push -u origin main
```

### A2. Create `dev`, do the feature work there

```bash
git checkout -b dev
```

Copy in `src/prepare.py`, then `src/preprocess.py`, then `src/train.py`,
then `src/evaluate.py`, then `params.yaml`, then `dvc.yaml`, committing each
one separately so you get at least 6 incremental commits, e.g.:

```bash
git add src/prepare.py        && git commit -m "Add prepare.py (B1)"
git add src/preprocess.py     && git commit -m "Add preprocess.py (B2)"
git add src/train.py          && git commit -m "Add train.py (B3)"
git add src/evaluate.py       && git commit -m "Add evaluate.py (B4)"
git add params.yaml           && git commit -m "Add params.yaml (D1)"
git add dvc.yaml              && git commit -m "Add dvc.yaml pipeline (D2)"
```

### A3. Log variants — screenshot each, then explain

```bash
git log --oneline --graph --all
git log --stat -3
git log -p -1
git log main..dev
```

What each reveals that plain `git log` doesn't:
- `--oneline --graph --all` — compresses each commit to one line and draws
  the branch/merge topology across *every* branch, so you see how `dev`,
  `main`, and any other branch relate structurally.
- `--stat -3` — for the last 3 commits, lists which files changed and how
  many lines were added/removed per file, without showing the actual diff.
- `-p -1` — shows the full patch (line-by-line diff) for the single most
  recent commit, not just its message.
- `main..dev` — lists only the commits reachable from `dev` but not from
  `main`, i.e. exactly what `dev` has added since it diverged.

### A4. Diff variants — screenshot each, then explain

```bash
# edit a tracked file without staging it
git diff                    # (a) unstaged working-directory changes
git add <file>
git diff --staged           # (b) staged changes not yet committed
git diff main..dev           # (c) two-dot
git diff main...dev          # (c) three-dot
```

Two-dot vs three-dot: `main..dev` diffs the current tip of `main` directly
against the current tip of `dev` (a straight snapshot comparison of the two
tips). `main...dev` diffs `dev` against the *merge base* (common ancestor)
of `main` and `dev`, so it shows only what changed on `dev` since it
branched off — it excludes changes that happened on `main` in the meantime.

### A5. Stash scenario

```bash
# mid-edit on src/preprocess.py, uncommitted
git stash
git stash list
git checkout main
# ...check something...
git checkout dev
git stash pop
```

### A6. Rebase scenario

```bash
git checkout main
git checkout -b hotfix
# fix a README typo
git add README.md && git commit -m "Fix typo in README"
git checkout main
git merge hotfix
git branch -d hotfix

git checkout dev
git rebase main
# resolve any conflict:
#   edit the conflicting file, then:
git add <resolved-file>
git rebase --continue

git log --oneline --graph --all   # before/after screenshot
```

### A7. Reset scenario

```bash
git checkout -b scratch
echo "throwaway 1" >> scratch.txt && git add scratch.txt && git commit -m "throwaway 1"
echo "throwaway 2" >> scratch.txt && git add scratch.txt && git commit -m "throwaway 2"

git reset --soft HEAD~1
git status   # changes from "throwaway 2" are staged, ready to re-commit

git reset --hard HEAD~1
git status   # working directory is clean; the discarded commit's changes are gone
```

Observed difference: `--soft` rewinds the branch pointer but leaves the
commit's changes staged in the index — nothing is lost, you're just back
to "ready to commit." `--hard` rewinds the pointer *and* overwrites the
working directory and index to match, so the changes are gone entirely
(unless recovered via `git reflog`).

### A8. Reorganize

```bash
git mv old_script.py src/old_script.py   # example — adjust to your actual layout
git rm scratch_notes.py
git commit -m "Reorganize scripts into src/ and remove scratch file"
```

---

## Part C — DVC with Google Drive Remote

### C1–C2

```bash
pip install "dvc[gdrive]"
dvc init          # run on dev, after A1's initial commit exists
git add .dvc .dvcignore
git commit -m "dvc init"
```

### C3. Create the remote

Create a folder in your Google Drive, copy its ID from the URL
(`https://drive.google.com/drive/folders/<FOLDER_ID>`), then:

```bash
dvc remote add -d gdrive_storage gdrive://<FOLDER_ID>
git add .dvc/config
git commit -m "Configure Google Drive DVC remote"
```

### C4. Authenticate — GCP OAuth app (avoids Error 2 / Error 4 below)

Google blocks DVC's shared default OAuth client, so create your own:

1. Google Cloud Console → **APIs & Services → Library** → search
   **Google Drive API** → **Enable**.
2. **APIs & Services → OAuth consent screen** → **External** → fill in app
   name + your email → in **Test users**, click **+ ADD USERS** and add
   your own Google account email (required while the app is in "Testing").
3. **APIs & Services → Credentials** → **+ Create Credentials → OAuth
   client ID** → Application type **Desktop app** → **Create**. Copy the
   **Client ID** and **Client Secret**.
4. Wire them into DVC:

```bash
dvc remote modify gdrive_storage gdrive_client_id YOUR_CLIENT_ID
dvc remote modify gdrive_storage gdrive_client_secret YOUR_CLIENT_SECRET
```

5. Run any `dvc push` (see C5). A browser window opens for consent — click
   **Advanced → Go to [App Name] (unsafe)** (this is expected for an app
   still in "Testing" mode), grant access, and confirm.

Confirm the credential/token file is excluded from Git — it already is,
via the `.dvc/cache`, `.dvc/tmp`, and `gdrive-user-credentials.json`
entries in `.gitignore`.

### C5. Track artifacts and push

```bash
python src/prepare.py
python src/preprocess.py
python src/train.py
python src/evaluate.py

dvc add data/raw data/processed models
git add data/raw.dvc data/processed.dvc models.dvc .gitignore
git commit -m "Track raw/processed data and models with DVC"
dvc push
```

Then open your Google Drive folder in the browser and screenshot the
uploaded files.

### Troubleshooting reference (if something breaks)

| Symptom | Cause | Fix |
|---|---|---|
| `module 'lib' has no attribute 'GEN_EMAIL'` | pyOpenSSL/cryptography version mismatch | `pip install "pyOpenSSL==24.2.1" cryptography --upgrade` |
| `This app is blocked` | Using DVC's shared default OAuth client | Configure your own GCP OAuth client (C4 above) |
| `400. That's an error... malformed` | Stale cached token, or quotes around client ID/secret | Delete `.dvc/tmp/gdrive-user-credentials.json`, re-run `dvc remote modify` **without** quotes |
| `Access blocked... has not completed verification / 403 access_denied` | Your account isn't in the app's **Test users** list | Add your exact email under OAuth consent screen → Test users, delete the cached token, re-run `dvc push` |

---

## Part D — DVC Pipeline

### D1–D2

`params.yaml` and `dvc.yaml` are already in this bundle — copy them in,
then:

```bash
git add params.yaml dvc.yaml
git commit -m "Add params.yaml and dvc.yaml pipeline definition"
```

### D3. First run

```bash
dvc repro
```

Capture the console output — you should see all four stages
(`prepare`, `preprocess`, `train`, `evaluate`) run in sequence, and a new
`dvc.lock` file appear. Commit it:

```bash
git add dvc.lock
git commit -m "Run pipeline, generate dvc.lock (v1)"
git tag v1
```

### D4. Change a hyperparameter, re-run

```yaml
# params.yaml
train:
  dense_units: 256   # was 128
```

```bash
dvc repro
```

What reruns and why: DVC hashes each stage's declared `deps` and the
specific `params.yaml` keys it lists. `prepare` and `preprocess` depend
only on their scripts and `data/raw` / their own params — since neither
their scripts, `data/raw`, nor `preprocess.*` params changed, DVC finds a
cache hit and **skips** them. `train` lists `train.dense_units` as a
param dependency, so its hash changes and it **reruns**. `evaluate`
depends on `train`'s output (`models/model.h5`), which just changed, so
it **reruns** too, cascading downstream of the edited stage only.

### D5. Commit v2

```bash
git add params.yaml dvc.yaml dvc.lock metrics.json
git commit -m "Increase dense_units, rerun pipeline (v2)"
git tag v2
dvc push
```

---

## Part E — Simulated Conflict

### E1

```bash
git checkout main
git checkout -b teammate-sim
# edit preprocess.py's normalization, e.g. switch to (x - mean) / std instead of x / 255
python src/preprocess.py
dvc add data/processed
git add src/preprocess.py data/processed.dvc
git commit -m "teammate-sim: alternate normalization"
dvc push
```

### E2

```bash
git checkout main
# independently edit preprocess.py's normalization differently,
# e.g. min-max scaling with clipping
python src/preprocess.py
dvc add data/processed
git add src/preprocess.py data/processed.dvc
git commit -m "main: alternate normalization (independent change)"
dvc push
```

### E3. Merge — expect two conflicts

```bash
git merge teammate-sim
```

You should see a **text conflict** in `src/preprocess.py` (conflict
markers `<<<<<<<` / `=======` / `>>>>>>>`) and a **conflict in
`data/processed.dvc`** (two different hashes recorded for the same path).
Screenshot both.

### E4. Resolve

```bash
# open src/preprocess.py, manually reconcile both normalization
# approaches into one function, remove conflict markers
git add src/preprocess.py

# decide which processed-data version is authoritative, OR regenerate
# a merged version by re-running preprocess.py after resolving the code:
python src/preprocess.py
dvc add data/processed
git add data/processed.dvc

dvc checkout   # sync working directory to the resolved pointer
```

### E5. Finish

```bash
dvc status          # should report a clean state
git commit -m "Merge teammate-sim: resolve normalization + data conflict"
dvc repro            # prove the merged pipeline is still reproducible
git push origin main
dvc push
```

---

## Report checklist (2–4 page PDF)

- [ ] Screenshots + explanations for A3 (log variants) and A4 (diff variants,
      two-dot vs three-dot)
- [ ] A6 before/after graph, A7 soft-vs-hard explanation
- [ ] C5 Google Drive folder screenshot showing uploaded files
- [ ] Final `params.yaml` and `dvc.yaml`
- [ ] D3 and D4 `dvc repro` console logs + your rerun/skip explanation
- [ ] E3 conflict screenshots (code + `.dvc` pointer) and E4 resolution
- [ ] v1 vs v2 `metrics.json` comparison table
