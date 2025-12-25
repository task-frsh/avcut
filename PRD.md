# AviCut - Video Splitter PRD
# AviCut - 동영상 분할기 PRD

---

## 1. Product Overview | 제품 개요

### English
**AviCut** is a simple, intuitive video splitting tool that allows users to split video files into segments of a specified duration (in minutes). Unlike complex video editors, AviCut focuses on one task: splitting videos quickly and efficiently.

### 한국어
**AviCut**은 동영상 파일을 지정한 분 단위로 분할하는 간단하고 직관적인 도구입니다. 복잡한 영상 편집기와 달리, AviCut은 동영상을 빠르고 효율적으로 분할하는 한 가지 작업에 집중합니다.

---

## 2. Problem Statement | 문제 정의

### English
- Existing video editors are too complex for simple splitting tasks
- LosslessCut is powerful but has a steep learning curve
- Users need a "one-click" solution for batch video splitting
- No simple tool exists for splitting videos into equal time segments

### 한국어
- 기존 동영상 편집기는 간단한 분할 작업에 비해 너무 복잡함
- LosslessCut은 강력하지만 학습 곡선이 가파름
- 사용자들은 일괄 동영상 분할을 위한 "원클릭" 솔루션이 필요함
- 동영상을 균등한 시간 단위로 분할하는 간단한 도구가 없음

---

## 3. Target Users | 대상 사용자

| User Type | Description |
|-----------|-------------|
| Content Creators / 콘텐츠 크리에이터 | YouTubers, streamers who need to split long recordings |
| Educators / 교육자 | Teachers splitting lecture videos into segments |
| General Users / 일반 사용자 | Anyone needing to split videos for sharing or storage |

---

## 4. Core Features | 핵심 기능

### 4.1 Main Interface | 메인 인터페이스

```
┌─────────────────────────────────────────────────────────────┐
│  AviCut                                [🌐] [─] [□] [×]     │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                       │  │
│  │                                                       │  │
│  │              +                                        │  │
│  │                                                       │  │
│  │      Drag & Drop video files here                     │  │
│  │      동영상 파일을 여기에 드래그하세요                    │  │
│  │                                                       │  │
│  │         [ Select Files ]  [ Select Folder ]           │  │
│  │         [ 파일 선택 ]     [ 폴더 선택 ]                 │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Split Duration (minutes): [    5    ] ▼                    │
│  분할 단위 (분):                                             │
│                                                             │
│  Output Folder: [ C:\Users\...\output        ] [Browse]     │
│  출력 폴더:                                    [찾아보기]     │
│                                                             │
│                    [ ▶ Start Split / 분할 시작 ]             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Feature List | 기능 목록

| Feature | Description (EN) | 설명 (KR) | Priority |
|---------|------------------|-----------|----------|
| **Drag & Drop** | Drop single/multiple video files | 단일/다중 동영상 파일 드롭 | P0 |
| **Folder Selection** | Select folder with multiple videos | 여러 동영상이 있는 폴더 선택 | P0 |
| **Time Input** | Specify split duration in minutes | 분 단위로 분할 시간 지정 | P0 |
| **Output Directory** | Choose where to save split files | 분할된 파일 저장 위치 선택 | P0 |
| **Progress Display** | Show real-time progress | 실시간 진행 상황 표시 | P0 |
| **Result Report** | Display completion summary | 완료 요약 표시 | P0 |
| **Language Toggle** | Switch between EN/KR | 영어/한국어 전환 | P1 |
| **File Preview** | Show video thumbnails | 동영상 썸네일 표시 | P2 |

---

## 5. User Flow | 사용자 흐름

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Launch     │────▶│  Add Files   │────▶│  Set Time    │
│   앱 실행     │     │  파일 추가    │     │  시간 설정    │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Complete   │◀────│  Processing  │◀────│  Start       │
│   완료        │     │  처리 중      │     │  시작        │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 6. UI/UX Requirements | UI/UX 요구사항

### 6.1 Design Principles | 디자인 원칙

| Principle | Description |
|-----------|-------------|
| **Simplicity** / 단순함 | One main screen, minimal options |
| **Clarity** / 명확함 | Large drop zone, clear buttons |
| **Feedback** / 피드백 | Real-time progress, clear status messages |
| **Accessibility** / 접근성 | Bilingual support (EN/KR) |

### 6.2 Color Scheme | 색상 체계

```
Primary:    #2563EB (Blue / 파랑)
Secondary:  #10B981 (Green for success / 성공 시 초록)
Background: #1F2937 (Dark gray / 어두운 회색)
Surface:    #374151 (Medium gray / 중간 회색)
Text:       #F9FAFB (White / 흰색)
Border:     #4B5563 (Light gray / 밝은 회색)
Error:      #EF4444 (Red / 빨강)
```

### 6.3 States | 상태별 화면

#### Initial State | 초기 상태
- Large "+" icon with drag instruction
- File/Folder selection buttons visible

#### Files Added | 파일 추가됨
- File list with names and durations
- Remove individual files option
- Clear all button

#### Processing | 처리 중
- Progress bar for current file
- Overall progress indicator
- Current file name display
- Cancel button

#### Complete | 완료
- Success/failure count
- List of output files
- "Open Output Folder" button
- "Split More" button

---

## 7. Technical Requirements | 기술 요구사항

### 7.1 Technology Stack | 기술 스택

| Component | Technology | Reason |
|-----------|------------|--------|
| **Framework** | Python + PyQt6 | Cross-platform, easy GUI |
| **Video Processing** | FFmpeg | Industry standard, lossless cutting |
| **Packaging** | PyInstaller | Single exe distribution |
| **Installer** | NSIS or Inno Setup | Optional Windows installer |

### 7.2 Supported Formats | 지원 포맷

**Input:** MP4, AVI, MKV, MOV, WebM, WMV, FLV
**Output:** Same as input (preserves format)

### 7.3 System Requirements | 시스템 요구사항

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4GB minimum
- **Disk:** FFmpeg + app (~150MB)
- **Dependencies:** None (FFmpeg bundled)

---

## 8. Output Naming Convention | 출력 파일 명명 규칙

```
Original: vacation_2024.mp4
Duration: 15 minutes
Split: 5 minutes each

Output:
├── vacation_2024_part001.mp4  (0:00 - 5:00)
├── vacation_2024_part002.mp4  (5:00 - 10:00)
└── vacation_2024_part003.mp4  (10:00 - 15:00)
```

---

## 9. Result Report Screen | 결과 보고 화면

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Split Complete! / 분할 완료!                              │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Summary / 요약:                                             │
│  ├── Total Files Processed / 처리된 파일: 3                  │
│  ├── Successful / 성공: 3                                    │
│  ├── Failed / 실패: 0                                        │
│  └── Total Segments Created / 생성된 세그먼트: 12             │
│                                                             │
│  Output Files / 출력 파일:                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ✓ video1_part001.mp4                                  │  │
│  │ ✓ video1_part002.mp4                                  │  │
│  │ ✓ video1_part003.mp4                                  │  │
│  │ ✓ video2_part001.mp4                                  │  │
│  │ ...                                                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  [ Open Output Folder ]        [ Split More Videos ]        │
│  [ 출력 폴더 열기 ]              [ 더 분할하기 ]               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Internationalization (i18n) | 국제화

### Language Files Structure | 언어 파일 구조

```
locales/
├── en.json
└── ko.json
```

### Sample Translations | 번역 샘플

| Key | English | 한국어 |
|-----|---------|--------|
| `app.title` | AviCut - Video Splitter | AviCut - 동영상 분할기 |
| `drop.instruction` | Drag & Drop video files here | 동영상 파일을 여기에 드래그하세요 |
| `btn.select_files` | Select Files | 파일 선택 |
| `btn.select_folder` | Select Folder | 폴더 선택 |
| `btn.start` | Start Split | 분할 시작 |
| `btn.cancel` | Cancel | 취소 |
| `label.duration` | Split Duration (minutes) | 분할 단위 (분) |
| `label.output` | Output Folder | 출력 폴더 |
| `status.processing` | Processing... | 처리 중... |
| `status.complete` | Complete! | 완료! |
| `result.success` | Successful | 성공 |
| `result.failed` | Failed | 실패 |

---

## 11. Project Structure | 프로젝트 구조

```
avi_cut/
├── src/
│   ├── main.py              # Entry point
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main window
│   │   ├── drop_zone.py     # Drag & drop area
│   │   ├── file_list.py     # File list widget
│   │   ├── progress.py      # Progress display
│   │   └── result.py        # Result report
│   ├── core/
│   │   ├── __init__.py
│   │   ├── splitter.py      # Video splitting logic
│   │   ├── ffmpeg.py        # FFmpeg wrapper
│   │   └── utils.py         # Utilities
│   └── i18n/
│       ├── __init__.py      # i18n manager
│       ├── en.json          # English
│       └── ko.json          # Korean
├── assets/
│   ├── icon.ico             # App icon
│   └── icon.png             # App icon (PNG)
├── ffmpeg/                  # Bundled FFmpeg
│   └── ffmpeg.exe
├── build/
│   └── avicut.spec          # PyInstaller spec
├── docs/
│   ├── USAGE_EN.md          # Usage guide (English)
│   └── USAGE_KO.md          # Usage guide (Korean)
├── requirements.txt
├── README.md                # Project README (bilingual)
├── LICENSE
└── PRD.md
```

---

## 12. Documentation Requirements | 문서화 요구사항

### 12.1 README.md 구조

```markdown
# AviCut - Video Splitter / 동영상 분할기

## Features / 기능
## Screenshots / 스크린샷
## Download / 다운로드
## Installation / 설치방법
## Quick Start / 빠른 시작
## Supported Formats / 지원 포맷
## Building from Source / 소스에서 빌드
## License / 라이센스
## Contributing / 기여하기
```

### 12.2 Usage Guide Contents | 사용 가이드 내용

**USAGE_EN.md / USAGE_KO.md:**

1. **Installation** - 설치 방법
   - Download and extract
   - Run exe directly (portable)

2. **Basic Usage** - 기본 사용법
   - Drag & drop files
   - Select folder
   - Set split duration
   - Choose output folder
   - Start splitting

3. **Settings** - 설정
   - Language selection
   - Default output folder

4. **Troubleshooting** - 문제 해결
   - FFmpeg not found
   - Unsupported format
   - Permission errors

5. **FAQ** - 자주 묻는 질문

---

## 13. Distribution | 배포

### 13.1 GitHub Release | GitHub 릴리즈

```
Releases/
├── AviCut-v1.0.0-win64.zip      # Portable version
├── AviCut-v1.0.0-win64-setup.exe # Installer (optional)
└── Source code (zip/tar.gz)
```

### 13.2 Release Checklist | 릴리즈 체크리스트

- [ ] Version bump
- [ ] Build exe with PyInstaller
- [ ] Test on clean Windows machine
- [ ] Create GitHub release
- [ ] Upload artifacts
- [ ] Update README with download links

---

## 14. Development Phases | 개발 단계

### Phase 1: Project Setup | 프로젝트 설정
```
Tasks:
├── 1.1 Create project structure
├── 1.2 Setup virtual environment
├── 1.3 Install dependencies (PyQt6, etc.)
├── 1.4 Create requirements.txt
└── 1.5 Setup FFmpeg integration
```

### Phase 2: Core Backend | 핵심 백엔드
```
Tasks:
├── 2.1 FFmpeg wrapper (get duration, split video)
├── 2.2 Video splitter class
├── 2.3 File utilities (naming, validation)
└── 2.4 Unit tests for core functions
```

### Phase 3: Basic UI | 기본 UI
```
Tasks:
├── 3.1 Main window layout
├── 3.2 Drop zone widget (drag & drop)
├── 3.3 File list widget
├── 3.4 Settings panel (duration, output folder)
└── 3.5 Start button and basic flow
```

### Phase 4: Progress & Results | 진행률 & 결과
```
Tasks:
├── 4.1 Progress bar widget
├── 4.2 Background worker thread
├── 4.3 Real-time status updates
├── 4.4 Result report dialog
└── 4.5 Error handling and display
```

### Phase 5: Internationalization | 국제화
```
Tasks:
├── 5.1 i18n manager class
├── 5.2 English language file
├── 5.3 Korean language file
├── 5.4 Language toggle button
└── 5.5 Dynamic UI text updates
```

### Phase 6: Polish & Testing | 마무리 & 테스트
```
Tasks:
├── 6.1 UI styling and theming
├── 6.2 Edge case handling
├── 6.3 Performance optimization
├── 6.4 Cross-format testing
└── 6.5 User experience testing
```

### Phase 7: Packaging & Documentation | 패키징 & 문서화
```
Tasks:
├── 7.1 PyInstaller configuration
├── 7.2 Bundle FFmpeg
├── 7.3 Create exe build
├── 7.4 Write README.md
├── 7.5 Write USAGE_EN.md
├── 7.6 Write USAGE_KO.md
└── 7.7 Create GitHub release
```

---

## 15. Development Order (Detailed) | 개발 순서 (상세)

```
Step  | Task                          | Description
------|-------------------------------|----------------------------------
  1   | Project structure             | 폴더 및 파일 구조 생성
  2   | requirements.txt              | 의존성 패키지 정의
  3   | i18n/en.json, ko.json         | 언어 파일 생성
  4   | i18n/__init__.py              | 다국어 매니저 클래스
  5   | core/utils.py                 | 유틸리티 함수
  6   | core/ffmpeg.py                | FFmpeg 래퍼 클래스
  7   | core/splitter.py              | 동영상 분할 로직
  8   | ui/drop_zone.py               | 드래그 앤 드롭 영역
  9   | ui/file_list.py               | 파일 목록 위젯
 10   | ui/progress.py                | 진행률 표시 위젯
 11   | ui/result.py                  | 결과 보고 다이얼로그
 12   | ui/main_window.py             | 메인 윈도우 통합
 13   | main.py                       | 앱 엔트리포인트
 14   | Styling & Theme               | UI 스타일링
 15   | Testing                       | 기능 테스트
 16   | avicut.spec                   | PyInstaller 설정
 17   | Build exe                     | 실행파일 빌드
 18   | README.md                     | 프로젝트 설명서
 19   | USAGE_EN.md                   | 영문 사용 가이드
 20   | USAGE_KO.md                   | 한글 사용 가이드
 21   | GitHub Release                | 릴리즈 배포
```

---

## 16. Comparison with LosslessCut | LosslessCut과 비교

| Feature | LosslessCut | AviCut |
|---------|-------------|--------|
| Learning Curve | Medium-High | Very Low |
| Primary Use | Manual editing | Auto splitting |
| Batch Processing | Limited | Full support |
| UI Complexity | Feature-rich | Minimal |
| Target User | Power users | Everyone |

---

## 17. Success Metrics | 성공 지표

| Metric | Target |
|--------|--------|
| GitHub Stars | 100+ in first month |
| Downloads | 500+ in first month |
| User Rating | 4.5+ stars |
| Bug Reports | < 5 critical issues |

---

## 18. Future Enhancements (v2.0) | 향후 개선사항

| Feature | Description |
|---------|-------------|
| Video Preview | Preview video before splitting |
| Custom Split Points | Manual segment markers |
| Re-encoding Options | Quality/format conversion |
| Queue System | Background processing |
| macOS/Linux Support | Cross-platform builds |
| Dark/Light Theme | Theme toggle |

---

**Document Version:** 1.1
**Last Updated:** 2024-12-25
**Author:** AviCut Team
