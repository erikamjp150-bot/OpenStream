import ffmpeg
import os
import uuid
from typing import Dict, Any
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.output_dir = "/tmp/video_processing"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_video(self, input_path: str) -> Dict[str, Any]:
        video_id = str(uuid.uuid4())
        
        # Extract metadata
        probe = ffmpeg.probe(input_path)
        metadata = self._extract_metadata(probe)
        
        # Transcode to standard formats
        output_paths = self._transcode_video(input_path, video_id)
        
        # Generate thumbnail
        thumbnail_path = self._generate_thumbnail(input_path, video_id)
        
        return {
            'video_id': video_id,
            'output_path': output_paths.get('720p', output_paths.get('original')),
            'thumbnail_path': thumbnail_path,
            'metadata': metadata
        }
    
    def _extract_metadata(self, probe: Dict) -> Dict:
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        return {
            "duration": float(probe['format'].get('duration', 0)),
            "width": int(video_stream.get('width', 0)) if video_stream else 0,
            "height": int(video_stream.get('height', 0)) if video_stream else 0,
            "file_size": int(probe['format'].get('size', 0))
        }
    
    def _transcode_video(self, input_path: str, video_id: str) -> Dict[str, str]:
        output_files = {}
        qualities = [
            {'name': '720p', 'width': 1280, 'height': 720, 'bitrate': '2M'},
            {'name': '480p', 'width': 854, 'height': 480, 'bitrate': '1M'},
        ]
        
        for quality in qualities:
            output_path = f"{self.output_dir}/{video_id}_{quality['name']}.mp4"
            try:
                stream = ffmpeg.input(input_path)
                stream = ffmpeg.output(
                    stream,
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    video_bitrate=quality['bitrate'],
                    s=f"{quality['width']}x{quality['height']}",
                    **{'movflags': 'faststart'}
                )
                ffmpeg.run(stream, overwrite_output=True, quiet=True)
                output_files[quality['name']] = output_path
            except Exception as e:
                logger.error(f"Failed to transcode to {quality['name']}: {e}")
                # Fallback: keep original
                output_path = f"{self.output_dir}/{video_id}_original.mp4"
                stream = ffmpeg.input(input_path)
                stream = ffmpeg.output(stream, output_path, vcodec='copy', acodec='copy')
                ffmpeg.run(stream, overwrite_output=True, quiet=True)
                output_files['original'] = output_path
                break
        
        return output_files
    
    def _generate_thumbnail(self, input_path: str, video_id: str) -> str:
        output_path = f"{self.output_dir}/{video_id}_thumbnail.jpg"
        try:
            stream = ffmpeg.input(input_path, ss=2)
            stream = ffmpeg.output(stream, output_path, vframes=1, s='320x180')
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
            # Fallback: first frame
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path, vframes=1)
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
        return output_path
