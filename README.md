# P12 — Implementasi Pipeline CI/CD Dasar dengan GitHub Actions

Project praktikum Flask + Semgrep + Pylint + Docker + GitHub self-hosted runner.

## Isi project

- `app.py`: aplikasi Flask dengan query SQLite berparameter.
- `templates/index.html`: halaman login.
- `requirements.txt`: dependensi Flask.
- `Dockerfile`: image Docker berjalan sebagai user non-root.
- `.github/workflows/devsecops.yml`: pipeline Semgrep, Pylint, dan deployment ke VM.
- `/health`: endpoint pemeriksaan sederhana.

## Jalankan lokal

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / WSL:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Buka `http://127.0.0.1:5000/`. Akun demo: `admin` / `supersecret`.
Endpoint pemeriksaan: `http://127.0.0.1:5000/health`.

## Uji Docker

```bash
docker build -t secure-flask-app:latest .
docker run --rm -p 5000:5000 --name web-flask secure-flask-app:latest
```

## Setup GitHub

1. Buat repository GitHub baru, misalnya `belajar-devsecops-pipeline`.
2. Extract/copy isi folder project ini ke root repository.
3. Commit dan push ke branch `main`:

```bash
git add .
git commit -m "feat: implement basic DevSecOps CI/CD pipeline"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Jika remote sudah ada, jangan jalankan `git remote add origin` lagi.

## Setup self-hosted runner di Ubuntu VM

1. Siapkan Ubuntu Server VM dengan akses internet dan jaringan host-only yang dapat dijangkau host.
2. Install Docker Engine sesuai dokumentasi resmi Docker untuk Ubuntu.
3. Tambahkan user runner ke grup Docker, lalu login ulang atau jalankan `newgrp docker`.
4. Di repository GitHub buka **Settings → Actions → Runners → New self-hosted runner**.
5. Pilih Linux x64 dan jalankan perintah konfigurasi yang diberikan GitHub langsung di VM. Jangan bagikan token runner.
6. Jalankan runner dan pastikan statusnya **Idle**.
7. Setelah CI lolos pada push ke `main`/`master`, job deploy membangun image dan menjalankan container pada VM.

Akses aplikasi dari host menggunakan `http://IP_VM:5000/`. Pastikan port 5000 diizinkan dan IP VM benar.

## Branch protection / ruleset

Buat ruleset aktif untuk default branch, aktifkan **Require a pull request before merging**, **Require status checks to pass**, **Require branches to be up to date before merging**, **Restrict deletions**, dan **Block force pushes**. Tambahkan checks bernama persis:

- `Semgrep SAST Scan`
- `Pylint Code Quality Gate`

Nama status check yang tersedia dapat sedikit berbeda tergantung tampilan GitHub; pilih nama job yang muncul setelah workflow pernah berjalan.

## Catatan keamanan

Ini aplikasi demo praktikum, bukan autentikasi produksi. Akun demo dan password masih berupa teks biasa agar sesuai dengan contoh modul. Jangan gunakan kredensial nyata. Untuk produksi, gunakan hash password yang kuat, secret/configuration management, proteksi CSRF, HTTPS, dan pengelolaan database yang sesuai.
