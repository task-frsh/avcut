# AVcut - Video Splitter / 동영상 분할기

<p align="center">
  <img src="assets/icon.png" alt="AVcut Logo" width="128" height="128">
</p>

<p align="center">
  <strong>Simple, intuitive video splitting tool</strong><br>
  <strong>간단하고 직관적인 동영상 분할 도구</strong>
</p>

<p align="center">
  <a href="#features--기능">Features</a> •
  <a href="#download--다운로드">Download</a> •
  <a href="#usage--사용법">Usage</a> •
  <a href="#building--빌드">Building</a> •
  <a href="#license--라이센스">License</a>
</p>

---

## Features / 기능

### English
- **Drag & Drop**: Simply drag video files onto the app
- **Batch Processing**: Split multiple videos at once
- **Time-based Splitting**: Split videos into segments of specified minutes
- **Lossless Cutting**: Uses FFmpeg for quality-preserving splits
- **Bilingual**: Supports English and Korean
- **Portable**: No installation required, just run the exe

### 한국어
- **드래그 앤 드롭**: 동영상 파일을 앱에 끌어다 놓기만 하면 됩니다
- **일괄 처리**: 여러 동영상을 한 번에 분할
- **시간 기반 분할**: 지정한 분 단위로 동영상 분할
- **무손실 자르기**: FFmpeg를 사용하여 품질 손실 없이 분할
- **이중 언어**: 영어와 한국어 지원
- **포터블**: 설치 없이 exe 파일 실행

---

## Screenshots / 스크린샷

### Main Interface / 메인 화면
```
┌─────────────────────────────────────────────┐
│  AviCut                          [한국어]   │
├─────────────────────────────────────────────┤
│                                             │
│                    +                        │
│                                             │
│     Drag & Drop video files here            │
│                                             │
│     [Select Files]  [Select Folder]         │
│                                             │
├─────────────────────────────────────────────┤
│  Split Duration (minutes): [ 5 ]            │
│  Output Folder: [~/Videos/AviCut_Output]    │
│                                             │
│           [ ▶ Start Split ]                 │
└─────────────────────────────────────────────┘
```

---

## Download / 다운로드

### Latest Release / 최신 버전
- [AVcut-v1.0.0-win64.zip](https://github.com/yourusername/avcut/releases/latest)

### Requirements / 요구사항
- Windows 10/11 (64-bit)
- FFmpeg required (download separately or use bundled version)

---

## Usage / 사용법

### Quick Start / 빠른 시작

1. **Download & Extract** / 다운로드 및 압축 해제
   - Download the zip file / zip 파일 다운로드
   - Extract to any folder / 원하는 폴더에 압축 해제

2. **Run** / 실행
   - `python run.py` / 파이썬으로 실행

3. **Add Videos** / 동영상 추가
   - Drag & drop files / 파일 드래그 앤 드롭
   - Or click "Select Files" / 또는 "파일 선택" 클릭

4. **Set Duration** / 시간 설정
   - Enter split duration in minutes / 분 단위로 분할 시간 입력
   - Example: 5 = 5 minutes per segment / 예: 5 = 세그먼트당 5분

5. **Start Split** / 분할 시작
   - Click "Start Split" button / "분할 시작" 버튼 클릭
   - Wait for completion / 완료까지 대기

For detailed usage instructions, see:
- [English Usage Guide](docs/USAGE_EN.md)
- [한국어 사용 가이드](docs/USAGE_KO.md)

---

## Supported Formats / 지원 포맷

| Format | Extension |
|--------|-----------|
| MP4 | .mp4 |
| AVI | .avi |
| MKV | .mkv |
| MOV | .mov |
| WebM | .webm |
| WMV | .wmv |
| FLV | .flv |
| M4V | .m4v |
| MPEG | .mpeg, .mpg |

---

## Building / 빌드

### Requirements / 요구사항
- Python 3.10+
- pip

### Setup / 설정

```bash
# Clone repository / 저장소 복제
git clone https://github.com/yourusername/avicut.git
cd avicut

# Create virtual environment / 가상환경 생성
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies / 의존성 설치
pip install -r requirements.txt
```

### Run from Source / 소스에서 실행

```bash
python src/main.py
```

### Build Executable / 실행파일 빌드

```bash
# Install PyInstaller / PyInstaller 설치
pip install pyinstaller

# Build / 빌드
pyinstaller build/avicut.spec
```

The executable will be in `dist/AviCut/` folder.

---

## Project Structure / 프로젝트 구조

```
avi_cut/
├── src/
│   ├── main.py              # Entry point
│   ├── ui/                  # UI components
│   │   ├── main_window.py
│   │   ├── drop_zone.py
│   │   ├── file_list.py
│   │   ├── progress.py
│   │   └── result.py
│   ├── core/                # Core logic
│   │   ├── splitter.py
│   │   ├── ffmpeg.py
│   │   └── utils.py
│   └── i18n/                # Translations
│       ├── en.json
│       └── ko.json
├── assets/                  # Icons
├── docs/                    # Documentation
├── build/                   # Build scripts
├── ffmpeg/                  # FFmpeg binary
├── requirements.txt
├── README.md
└── LICENSE
```

---

## FFmpeg Setup / FFmpeg 설정

### For Development / 개발용
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract `ffmpeg.exe` to `avi_cut/ffmpeg/` folder

### For Release / 배포용
FFmpeg is bundled with the release package.

---

## Contributing / 기여하기

Contributions are welcome! / 기여를 환영합니다!

1. Fork the repository / 저장소 포크
2. Create your feature branch / 기능 브랜치 생성
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes / 변경사항 커밋
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch / 브랜치에 푸시
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request / 풀 리퀘스트 열기

---

## License / 라이센스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

이 프로젝트는 MIT 라이센스 하에 배포됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## Acknowledgments / 감사

- [FFmpeg](https://ffmpeg.org/) - Video processing
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [LosslessCut](https://github.com/mifi/lossless-cut) - Inspiration

---

## Contact / 연락처

- Issues: [GitHub Issues](https://github.com/task-frsh/avicut/issues)
- Email: geumgang_0@​aol.com

---

<p align="center">
  Made with ❤️ by AviCut Team
</p>
