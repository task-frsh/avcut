"""
Utility functions for AviCut
"""
import os
import re
from typing import List, Tuple

# Supported video extensions
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.webm', '.wmv', '.flv', '.m4v', '.mpeg', '.mpg'}


def is_video_file(file_path: str) -> bool:
    """Check if a file is a supported video format."""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in VIDEO_EXTENSIONS


def get_video_files_from_folder(folder_path: str) -> List[str]:
    """Get all video files from a folder (non-recursive)."""
    if not os.path.isdir(folder_path):
        return []

    video_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and is_video_file(file_path):
            video_files.append(file_path)

    return sorted(video_files)


def format_duration(seconds: float) -> str:
    """Format seconds into HH:MM:SS string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def parse_duration(duration_str: str) -> float:
    """Parse duration string to seconds."""
    # Handle HH:MM:SS.ms format
    pattern = r'(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)'
    match = re.match(pattern, duration_str)

    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2))
        seconds = float(match.group(3))
        return hours * 3600 + minutes * 60 + seconds

    # Try to parse as pure seconds
    try:
        return float(duration_str)
    except ValueError:
        return 0.0


def generate_output_filename(original_path: str, part_number: int, output_dir: str) -> str:
    """Generate output filename for a split segment."""
    basename = os.path.basename(original_path)
    name, ext = os.path.splitext(basename)

    # Create output filename with part number
    output_name = f"{name}_part{part_number:03d}{ext}"
    return os.path.join(output_dir, output_name)


def calculate_segments(total_duration: float, segment_minutes: float) -> List[Tuple[float, float]]:
    """Calculate start and end times for each segment.

    Args:
        total_duration: Total video duration in seconds
        segment_minutes: Desired segment length in minutes

    Returns:
        List of (start_time, end_time) tuples in seconds
    """
    segment_seconds = segment_minutes * 60
    segments = []

    start = 0.0
    while start < total_duration:
        end = min(start + segment_seconds, total_duration)
        segments.append((start, end))
        start = end

    return segments


def ensure_dir_exists(dir_path: str) -> bool:
    """Ensure a directory exists, create if necessary."""
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except OSError:
        return False


def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes."""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except OSError:
        return 0.0


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
