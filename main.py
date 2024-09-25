import os
import shutil
import uuid
import json
import logging
from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from pydantic import BaseModel
from models.face_recognition import detect_faces_in_scene
from models.face_classification import match_faces, load_actors_info

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Models
class SceneTimestamp(BaseModel):
    start_time: float  # in seconds
    end_time: float    # in seconds

class ActorInfo(BaseModel):
    actor_id: int
    name: str
    height: str
    profile_picture: str

class SceneResult(BaseModel):
    timestamp: str
    actors: List[ActorInfo]

@app.post("/upload_video", response_model=List[SceneResult])
async def upload_video(
    video_file: UploadFile = File(...)
):
    logger.info(f"Received video upload: {video_file.filename}")
    
    # Parse scenes from JSON string
    scenes_list = [
        {'start_time': 0.0, 'end_time': 30.0}
    ]
    scene_timestamps = [(scene['start_time'], scene['end_time']) for scene in scenes_list]
    logger.info(f"Parsed scene timestamps: {scene_timestamps}")

    # Save uploaded video
    os.makedirs('data/uploaded_videos', exist_ok=True)
    video_filename = f"{uuid.uuid4()}_{video_file.filename}"
    video_path = os.path.join('data/uploaded_videos', video_filename)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)
    logger.info(f"Saved uploaded video to: {video_path}")

    # Detect faces
    face_encodings_per_scene = detect_faces_in_scene(video_path, scene_timestamps)
    logger.info(f"Detected faces in {len(face_encodings_per_scene)} scenes")
    for scene, encodings in face_encodings_per_scene.items():
        logger.debug(f"Scene {scene}: {len(encodings)} faces detected")

    # Load actor information
    actors_info_list = load_actors_info()
    logger.info(f"Loaded information for {len(actors_info_list)} actors")

    # Process each scene
    scenes_results = []
    for idx, face_encodings in face_encodings_per_scene.items():
        matched_actor_ids = match_faces(face_encodings)
        logger.info(f"Scene {idx}: Matched {len(matched_actor_ids)} actors")
        
        actors_info = []
        for actor_id in set(matched_actor_ids):
            actor_info_data = next((actor for actor in actors_info_list if actor['actor_id'] == actor_id), None)
            if actor_info_data:
                actor_info = ActorInfo(
                    actor_id=actor_info_data['actor_id'],
                    name=actor_info_data['name'],
                    height=actor_info_data.get('height', '5\'8"'),
                    profile_picture=actor_info_data.get('profile_picture', '')
                )
                logger.debug(f"Actor info for ID {actor_id}: {actor_info}")
                actors_info.append(actor_info)

        scene_result = SceneResult(
            timestamp=f"{scene_timestamps[idx][0]}-{scene_timestamps[idx][1]}",
            actors=actors_info
        )
        scenes_results.append(scene_result)
        logger.info(f"Processed scene {idx}: {len(actors_info)} actors identified")

    # Save the results to a JSON file
    os.makedirs('data/results', exist_ok=True)
    result_path = 'data/results/result.json'
    with open(result_path, 'w') as json_file:
        json.dump([scene_result.dict() for scene_result in scenes_results], json_file, indent=4)
    logger.info(f"Saved results to: {result_path}")

    # Clean up uploaded video
    os.remove(video_path)
    logger.info(f"Removed uploaded video: {video_path}")

    
    logger.info(f"Returning results for {len(scenes_results)} scenes")
    return scenes_results

@app.get("/get-movie-x-ray/{movie_id}")
async def get_movie_x_ray(movie_id: str):
    logger.info(f"Received request for movie x-ray data: {movie_id}")
    
    try:
        result_path = 'data/results/result.json'
        with open(result_path, 'r') as json_file:
            movie_data = json.load(json_file)
        
        logger.info(f"Successfully loaded data for movie ID: {movie_id}")
        return movie_data
    except FileNotFoundError:
        logger.error(f"result.json not found for movie ID: {movie_id}")
        raise HTTPException(status_code=404, detail="Movie x-ray data not found")
    except json.JSONDecodeError:
        logger.error(f"Error decoding result.json for movie ID: {movie_id}")
        raise HTTPException(status_code=500, detail="Error processing movie x-ray data")


@app.get("/test")
async def test():
    logger.info("Received test request")
    return {"message": "Server is working"}