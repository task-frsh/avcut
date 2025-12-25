# AviCut Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Adding Videos](#adding-videos)
4. [Setting Options](#setting-options)
5. [Splitting Videos](#splitting-videos)
6. [Viewing Results](#viewing-results)
7. [Language Settings](#language-settings)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Installation

### Portable Version (Recommended)
1. Download `AviCut-vX.X.X-win64.zip` from the [Releases page](https://github.com/yourusername/avicut/releases)
2. Extract the zip file to any folder (e.g., `C:\Tools\AviCut`)
3. Run `AviCut.exe` - no installation needed!

### Requirements
- Windows 10 or Windows 11 (64-bit)
- At least 4GB RAM
- ~150MB disk space

---

## Getting Started

When you first launch AviCut, you'll see the main interface:

```
┌─────────────────────────────────────────────┐
│  AviCut - Video Splitter       [한국어]     │
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
│  Output Folder: [C:\Users\...\AviCut_Output]│
│                                             │
│           [ ▶ Start Split ]                 │
└─────────────────────────────────────────────┘
```

---

## Adding Videos

### Method 1: Drag and Drop
1. Open your file explorer
2. Select video file(s)
3. Drag them onto the AviCut window
4. Drop when you see the drop zone highlight

### Method 2: Select Files Button
1. Click the "Select Files" button
2. Browse to your video files
3. Select one or multiple files
4. Click "Open"

### Method 3: Select Folder Button
1. Click the "Select Folder" button
2. Browse to a folder containing videos
3. Click "Select Folder"
4. All video files in that folder will be added

### Managing Files
Once files are added, you'll see them in a list:
- **File name**: Name of the video file
- **Duration**: Length of the video
- **Remove (×)**: Click to remove individual files
- **Clear All**: Remove all files

---

## Setting Options

### Split Duration
Enter how long each segment should be (in minutes):
- Minimum: 1 minute
- Maximum: 999 minutes
- Default: 5 minutes

**Example:**
- Original video: 15 minutes
- Split duration: 5 minutes
- Result: 3 segments (5 min + 5 min + 5 min)

### Output Folder
Choose where split videos will be saved:
1. Click "Browse" button
2. Select a folder
3. Or type the path directly

**Default location:** `C:\Users\[YourName]\Videos\AviCut_Output`

---

## Splitting Videos

1. **Add videos** using any method above
2. **Set duration** (e.g., 5 minutes)
3. **Choose output folder**
4. **Click "Start Split"**

### During Processing
You'll see:
- Current file being processed
- Progress bar for current file
- Overall progress (e.g., "2 / 5" for 2nd of 5 files)
- Cancel button to stop

### Cancelling
Click "Cancel" to stop the process. Already created segments will be kept.

---

## Viewing Results

When splitting completes, a result dialog appears:

```
┌─────────────────────────────────────────────┐
│  ✓ Split Complete!                          │
├─────────────────────────────────────────────┤
│  Summary:                                   │
│    Total Files Processed: 3                 │
│    Successful: 3                            │
│    Failed: 0                                │
│    Total Segments Created: 12               │
├─────────────────────────────────────────────┤
│  Output Files:                              │
│    ✓ video1_part001.mp4                     │
│    ✓ video1_part002.mp4                     │
│    ✓ video1_part003.mp4                     │
│    ...                                      │
├─────────────────────────────────────────────┤
│  [Open Output Folder]  [Split More Videos]  │
└─────────────────────────────────────────────┘
```

### Output File Naming
Files are named with part numbers:
```
Original: my_video.mp4
Output:   my_video_part001.mp4
          my_video_part002.mp4
          my_video_part003.mp4
```

---

## Language Settings

AviCut supports English and Korean.

### Switching Language
1. Look for the language button in the top-right corner
2. Click "한국어" to switch to Korean
3. Click "English" to switch back to English

The interface updates immediately.

---

## Troubleshooting

### "FFmpeg not found" Error
FFmpeg should be bundled with AviCut. If you see this error:
1. Make sure you extracted the complete zip file
2. Check that `ffmpeg` folder exists next to `AviCut.exe`
3. Try re-downloading the release package

### Video Won't Load
- Check if the file format is supported
- Try playing the video in another player first
- The file might be corrupted

### Splitting Fails
Common causes:
- Disk full - free up space in output folder
- File locked - close other programs using the file
- Permission denied - try running as administrator

### App Won't Start
1. Make sure you have Windows 10/11 64-bit
2. Try running as administrator
3. Check Windows Event Viewer for errors

---

## FAQ

### Q: Is there quality loss when splitting?
**A:** No! AviCut uses FFmpeg's "copy" mode, which means video and audio streams are copied without re-encoding. There's no quality loss.

### Q: Can I split to exact frame positions?
**A:** AviCut cuts at the nearest keyframe to maintain video integrity. For exact frame-accurate cuts, consider using professional video editors.

### Q: Why is the last segment shorter?
**A:** If your video doesn't divide evenly by the split duration, the last segment will be shorter. For example, a 12-minute video split by 5 minutes creates segments of 5, 5, and 2 minutes.

### Q: Can I choose different durations for each segment?
**A:** Currently, AviCut uses uniform durations. For custom segment lengths, consider using LosslessCut.

### Q: Is my video safe?
**A:** Yes! AviCut never modifies your original files. It only creates new files in the output folder.

### Q: What's the maximum file size?
**A:** There's no hard limit. AviCut can handle files of any size, limited only by your available disk space.

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Select Files | Ctrl+O |
| Start Split | Enter (when button focused) |
| Cancel | Escape |

---

## Getting Help

- **GitHub Issues**: Report bugs and request features
- **README**: Check the main documentation
- **This Guide**: Detailed usage instructions

---

*AviCut - Making video splitting simple*
