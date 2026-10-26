# Docker cho do an Vietnamese ASR hien tai

Goi nay la cac file de chep vao E:\ASR_Project, khong phai mot do an moi.
Da giu main.py, asr_runtime.py, audio_analyzer.py, vietnamese_phoneme.py tu ban gui.
Chi sua vietnamese_dictionary.py: bo duong dan E: co dinh, ho tro ASR_DATASET_DIR va ASR_DICTIONARY_FILE.
Bo thu vien container rieng, khong thay requirements.txt/moi truong Python Windows.
Ban CPU, mot worker de tranh tai nhieu ban sao model. Khong co GPU trong cau hinh nay.

## 1. Chep vao do an
Sao luu thu muc web/backend hien tai truoc khi chep.
Mo thu muc ASR_Docker_Pack trong ZIP, chep NOI DUNG vao E:\ASR_Project.
Thu muc web trong goi phai gop vao web hien tai, khong long them mot cap ASR_Docker_Pack.
Dataset van o E:\ASR_Project\dataset (khong kem trong ZIP).
Can co:
- audio/ (audio dung cho giao dien thong ke)
- vietnamese_dictionary_clean.json
- model_comparison.json
- error_statistics_whisper.json / error_statistics_phowhisper.json / error_statistics_wav2vec2.json
- sentence_analysis_whisper.json / sentence_analysis_phowhisper.json / sentence_analysis_wav2vec2.json
Khong can validated.tsv hoac cac script tao dataset de chay API.
Khong doi ten requirements.windows.snapshot.txt thanh requirements.txt.

## 2. Kiem tra Docker
Can Docker Desktop dang chay voi Linux containers tren Windows, hoac Docker Engine + Compose tren Linux.
Trong CMD moi:
    cd /d E:\ASR_Project
    docker --version
    docker compose version
Neu lenh khong duoc nhan dien, dung lai va cai Docker truoc; chua dung lenh chay ben duoi.

## 3. Build va chay
    docker compose up -d --build
    docker compose ps
    docker compose logs --tail=80 api
Kiem tra http://127.0.0.1:8001/health va http://127.0.0.1:8001/ready.
Sau do http://127.0.0.1:8001/docs: thu mot audio voi ca 3 model va ground_truth dung.
Cong 8001 tren Windows dung cho Docker; API Python cu/tunnel cu van dung 8000.
Lan dau can Internet de tai model Whisper va Hugging Face. Cache luu trong volume model_cache.
Khong dung docker compose down -v neu muon giu cache model.
Thay doi may chu van can tai/copy cache tren may moi.
Health chi kiem tra web process; ready kiem tra file dataset, khong chung minh model da nhan dang thanh cong.

## 4. Thu HTTPS voi Docker
Chi lam sau khi nhan dang ca 3 model trong Docker thanh cong.
Dung tunnel cu bang Ctrl+C trong cua so cloudflared (khong can dung backend cu).
Trong CMD moi:
    cd /d E:\ASR_Project\web\backend
    cloudflared.exe tunnel --url http://127.0.0.1:8001
Neu ten file thuc te la cloudflared.exe.exe thi dung ten do, hoac sua thanh cloudflared.exe.
Dung link HTTPS MOI in ra, them /health va /docs. Link tunnel cu co the khong con hoat dong.
Tunnel va Docker van chay tren may ban; chua phai VPS.

## 5. VPS va dia chi on dinh
Chep goi code va dataset sang VPS Linux, giu cung cau truc thu muc.
Dung Docker Compose nhu tren; cong chi bind localhost de reverse proxy/tunnel tren VPS truy cap.
Can chon VPS, co quyen truy cap VPS, va chon ten mien/tunnel co dinh truoc buoc trien khai.
Sau khi kiem tra tai nguyen RAM/CPU thuc te voi ca 3 model, tao named Cloudflare Tunnel tren VPS
hoac reverse proxy HTTPS voi ten mien. Khong co token/mat khau VPS trong goi nay.
Frontend chua duoc dong goi/deploy; link /docs la backend API.

## Van hanh
Xem log: docker compose logs -f api
Dung: docker compose down
Chay lai: docker compose up -d
Doi cong: dat ASR_PORT trong .env o thu muc goc (mac dinh 8001).
CORS_ORIGINS trong .env phai la dia chi frontend thuc te neu deploy frontend rieng.
Link HTTPS cong khai cho phep nguoi co link goi API; goi nay chua them dang nhap.

## Gioi han kiem tra
Da kiem tra cu phap Python, chuoi import noi bo, cau hinh YAML,
duong dan tu dien voi du lieu mau tam thoi, va kiem tra dataset du/thieu.
Chua chay FastAPI hoac ASR trong moi truong tao goi.
Khong co Docker daemon trong moi truong tao goi, khong kem dataset/model thuc,
nen chua build image hoac chay nhan dang that ben trong Docker.
Cac phien ban thu vien container duoc ghim rieng, khac ban Windows da chay;
can kiem tra Docker thuc te truoc khi trien khai VPS.
Nguon: https://pytorch.org/get-started/previous-versions/
https://huggingface.co/vinai/PhoWhisper-base
