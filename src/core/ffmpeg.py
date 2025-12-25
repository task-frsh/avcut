"""
FFmpeg wrapper for AviCut
"""
import os
import subprocess
import re
import sys
from typing import Optional, Callable


class FFmpegWrapper:
    """Wrapper class for FFmpeg operations."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        """Initialize FFmpeg wrapper.

        Args:
            ffmpeg_path: Path to ffmpeg executable. If None, searches in common locations.
        """
        self._ffmpeg_path = ffmpeg_path or self._find_ffmpeg()

    def _find_ffmpeg(self) -> str:
        """Find FFmpeg executable."""
        # Check if running as bundled exe
        if getattr(sys, 'frozen', False):
            # Running as compiled
            base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            bundled_ffmpeg = os.path.join(base_path, 'ffmpeg', 'ffmpeg.exe')
            if os.path.exists(bundled_ffmpeg):
                return bundled_ffmpeg

            # Check same directory as exe
            exe_dir = os.path.dirname(sys.executable)
            local_ffmpeg = os.path.join(exe_dir, 'ffmpeg', 'ffmpeg.exe')
            if os.path.exists(local_ffmpeg):
                return local_ffmpeg

        # Check project directory
        project_ffmpeg = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ffmpeg', 'ffmpeg.exe')
        if os.path.exists(project_ffmpeg):
            return project_ffmpeg

        # Check PATH
        try:
            result = subprocess.run(
                ['where', 'ffmpeg'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except Exception:
            pass

        # Default to 'ffmpeg' and hope it's in PATH
        return 'ffmpeg'

    @property
    def ffmpeg_path(self) -> str:
        return self._ffmpeg_path

    def is_available(self) -> bool:
        """Check if FFmpeg is available."""
        try:
            result = subprocess.run(
                [self._ffmpeg_path, '-version'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_duration(self, video_path: str) -> float:
        """Get video duration in seconds (fast method - reads metadata only)."""
        try:
            # Fast method: just read file info, don't decode
            result = subprocess.run(
                [
                    self._ffmpeg_path,
                    '-i', video_path,
                ],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=10,  # 10 second timeout
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            # Parse duration from stderr
            output = result.stderr
            duration_match = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', output)

            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = float(duration_match.group(3))
                return hours * 3600 + minutes * 60 + seconds

        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass

        return 0.0

    def split_video(
        self,
        input_path: str,
        output_path: str,
        start_time: float,
        end_time: float,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """Split a video segment.

        Args:
            input_path: Path to input video
            output_path: Path for output segment
            start_time: Start time in seconds
            end_time: End time in seconds
            progress_callback: Optional callback for progress updates (0.0 to 1.0)

        Returns:
            True if successful, False otherwise
        """
        duration = end_time - start_time

        try:
            # Build FFmpeg command for lossless split
            cmd = [
                self._ffmpeg_path,
                '-y',  # Overwrite output
                '-ss', str(start_time),  # Start time
                '-i', input_path,
                '-t', str(duration),  # Duration
                '-c', 'copy',  # Copy codecs (lossless)
                '-avoid_negative_ts', 'make_zero',
                output_path
            ]

            # Run with progress tracking
            process = subprocess.Popen(
                cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            # Read output for progress
            if progress_callback:
                while True:
                    line = process.stderr.readline()
                    if not line and process.poll() is not None:
                        break

                    # Parse time from ffmpeg output
                    time_match = re.search(r'time=(\d+):(\d+):(\d+(?:\.\d+)?)', line)
                    if time_match:
                        hours = int(time_match.group(1))
                        minutes = int(time_match.group(2))
                        seconds = float(time_match.group(3))
                        current_time = hours * 3600 + minutes * 60 + seconds
                        progress = min(current_time / duration, 1.0)
                        progress_callback(progress)

            process.wait()
            return process.returncode == 0

        except Exception as e:
            print(f"FFmpeg error: {e}")
            return False

    def get_video_info(self, video_path: str) -> dict:
        """Get video information."""
        info = {
            'duration': 0.0,
            'width': 0,
            'height': 0,
            'codec': '',
            'fps': 0.0
        }

        try:
            result = subprocess.run(
                [
                    self._ffmpeg_path,
                    '-i', video_path
                ],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            output = result.stderr

            # Duration
            duration_match = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', output)
            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = float(duration_match.group(3))
                info['duration'] = hours * 3600 + minutes * 60 + seconds

            # Resolution
            resolution_match = re.search(r'(\d{2,5})x(\d{2,5})', output)
            if resolution_match:
                info['width'] = int(resolution_match.group(1))
                info['height'] = int(resolution_match.group(2))

            # Codec
            codec_match = re.search(r'Video: (\w+)', output)
            if codec_match:
                info['codec'] = codec_match.group(1)

            # FPS
            fps_match = re.search(r'(\d+(?:\.\d+)?)\s*fps', output)
            if fps_match:
                info['fps'] = float(fps_match.group(1))

        except Exception:
            pass

        return info
