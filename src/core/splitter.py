"""
Video Splitter core logic for AviCut
"""
import os
from typing import List, Callable, Optional
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from .ffmpeg import FFmpegWrapper
from .utils import calculate_segments, generate_output_filename, ensure_dir_exists


@dataclass
class SplitResult:
    """Result of a single video split operation."""
    input_file: str
    success: bool
    output_files: List[str]
    error_message: str = ""
    segments_created: int = 0


@dataclass
class BatchResult:
    """Result of batch splitting operation."""
    total_files: int
    successful: int
    failed: int
    total_segments: int
    results: List[SplitResult]


class SplitterWorker(QThread):
    """Worker thread for video splitting."""

    # Signals
    progress = pyqtSignal(int, int, str, float)  # current_file, total_files, filename, file_progress
    file_complete = pyqtSignal(str, bool, list)  # filename, success, output_files
    all_complete = pyqtSignal(object)  # BatchResult
    error = pyqtSignal(str)  # error message

    def __init__(
        self,
        files: List[str],
        segment_minutes: float,
        output_dir: str,
        parent: Optional[QObject] = None
    ):
        super().__init__(parent)
        self.files = files
        self.segment_minutes = segment_minutes
        self.output_dir = output_dir
        self._cancelled = False
        self._ffmpeg = FFmpegWrapper()

    def cancel(self):
        """Cancel the splitting operation."""
        self._cancelled = True

    def run(self):
        """Run the splitting operation."""
        if not self._ffmpeg.is_available():
            self.error.emit("FFmpeg not found")
            return

        if not ensure_dir_exists(self.output_dir):
            self.error.emit(f"Cannot create output directory: {self.output_dir}")
            return

        results: List[SplitResult] = []
        total_files = len(self.files)

        for idx, file_path in enumerate(self.files):
            if self._cancelled:
                break

            filename = os.path.basename(file_path)
            self.progress.emit(idx + 1, total_files, filename, 0.0)

            result = self._split_file(file_path, idx + 1, total_files)
            results.append(result)

            self.file_complete.emit(filename, result.success, result.output_files)

        # Create batch result
        batch_result = BatchResult(
            total_files=total_files,
            successful=sum(1 for r in results if r.success),
            failed=sum(1 for r in results if not r.success),
            total_segments=sum(r.segments_created for r in results),
            results=results
        )

        self.all_complete.emit(batch_result)

    def _split_file(self, file_path: str, file_num: int, total_files: int) -> SplitResult:
        """Split a single video file."""
        output_files: List[str] = []
        filename = os.path.basename(file_path)

        try:
            # Get video duration
            duration = self._ffmpeg.get_duration(file_path)
            if duration <= 0:
                return SplitResult(
                    input_file=file_path,
                    success=False,
                    output_files=[],
                    error_message="Could not determine video duration"
                )

            # Calculate segments
            segments = calculate_segments(duration, self.segment_minutes)
            total_segments = len(segments)

            for seg_idx, (start_time, end_time) in enumerate(segments):
                if self._cancelled:
                    return SplitResult(
                        input_file=file_path,
                        success=False,
                        output_files=output_files,
                        error_message="Cancelled",
                        segments_created=len(output_files)
                    )

                # Generate output path
                output_path = generate_output_filename(
                    file_path,
                    seg_idx + 1,
                    self.output_dir
                )

                # Progress callback
                def progress_cb(seg_progress: float):
                    # Calculate overall file progress
                    file_progress = (seg_idx + seg_progress) / total_segments
                    self.progress.emit(file_num, total_files, filename, file_progress)

                # Split segment
                success = self._ffmpeg.split_video(
                    file_path,
                    output_path,
                    start_time,
                    end_time,
                    progress_cb
                )

                if success and os.path.exists(output_path):
                    output_files.append(output_path)
                else:
                    return SplitResult(
                        input_file=file_path,
                        success=False,
                        output_files=output_files,
                        error_message=f"Failed to create segment {seg_idx + 1}",
                        segments_created=len(output_files)
                    )

            return SplitResult(
                input_file=file_path,
                success=True,
                output_files=output_files,
                segments_created=len(output_files)
            )

        except Exception as e:
            return SplitResult(
                input_file=file_path,
                success=False,
                output_files=output_files,
                error_message=str(e),
                segments_created=len(output_files)
            )


class VideoSplitter:
    """Main video splitter class."""

    def __init__(self):
        self._ffmpeg = FFmpegWrapper()

    def is_ffmpeg_available(self) -> bool:
        """Check if FFmpeg is available."""
        return self._ffmpeg.is_available()

    def get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds."""
        return self._ffmpeg.get_duration(video_path)

    def get_video_info(self, video_path: str) -> dict:
        """Get video information."""
        return self._ffmpeg.get_video_info(video_path)

    def create_worker(
        self,
        files: List[str],
        segment_minutes: float,
        output_dir: str
    ) -> SplitterWorker:
        """Create a worker thread for splitting.

        Args:
            files: List of video file paths
            segment_minutes: Segment duration in minutes
            output_dir: Output directory path

        Returns:
            SplitterWorker thread
        """
        return SplitterWorker(files, segment_minutes, output_dir)
