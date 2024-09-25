import cv2
import face_recognition
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def detect_faces_in_scene(video_path, scene_timestamps, frame_skip=5):
    """
    Detect faces in specified scenes of a video.

    Args:
        video_path (str): Path to the video file.
        scene_timestamps (list): List of tuples indicating start and end times of scenes in seconds.
        frame_skip (int): Number of frames to skip between processing.

    Returns:
        dict: A dictionary with scene indices as keys and lists of face encodings as values.
    """
    logger.info(f"Starting face detection in video: {video_path}")
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    face_encodings_per_scene = {}

    for idx, (start_time, end_time) in enumerate(scene_timestamps):
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        face_encodings = []

        logger.info(f"Processing scene {idx+1}: {start_time}s to {end_time}s")
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frame_count = 0
        start_time = time.time()
        for frame_num in range(start_frame, end_frame + 1, frame_skip):
            ret, frame = video_capture.read()
            if not ret:
                logger.warning(f"Failed to read frame {frame_num}")
                break

            frame_count += 1
            if frame_count % 10 == 0:
                elapsed_time = time.time() - start_time
                logger.info(f"Processed {frame_count} frames in {elapsed_time:.2f} seconds")

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame, model='hog')
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            face_encodings.extend(encodings)
            
            logger.debug(f"Processed frame {frame_num}, found {len(encodings)} faces")

            # Skip frames
            for _ in range(frame_skip - 1):
                video_capture.read()

        face_encodings_per_scene[idx] = face_encodings
        logger.info(f"Scene {idx+1} processing complete. Total faces found: {len(face_encodings)}")

    video_capture.release()
    logger.info("Face detection completed for all scenes")
    return face_encodings_per_scene
