import os
import face_recognition
import pickle
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

KNOWN_FACES_PATH = 'data/known_faces.pkl'
KNOWN_ACTORS_DIR = 'data/known_actors/'
ACTORS_JSON_PATH = 'data/actors.json'

def create_known_faces_database():
    """
    Create and serialize known face encodings database.
    Also, create actors.json file with actor information.
    """
    known_faces = []
    actors_info = []

    logger.info("Starting to create known faces database")
    for actor_id, actor_name in enumerate(os.listdir(KNOWN_ACTORS_DIR), start=1):
        actor_dir = os.path.join(KNOWN_ACTORS_DIR, actor_name)
        encodings = []

        logger.info(f"Processing actor: {actor_name}")
        for image_name in os.listdir(actor_dir):
            image_path = os.path.join(actor_dir, image_name)
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            face_enc = face_recognition.face_encodings(image, face_locations)

            if face_enc:
                encodings.append(face_enc[0])
                logger.debug(f"Encoded face for {actor_name} from {image_name}")
            else:
                logger.warning(f"No face found in {image_name} for {actor_name}")

        known_faces.append({
            'actor_id': actor_id,
            'name': actor_name,
            'encodings': encodings
        })

        actors_info.append({
            'actor_id': actor_id,
            'name': actor_name,
            'height': 'Unknown', 
            'profile_picture': f"/images/{actor_name}.jpg" 
        })

    logger.info("Saving known faces database")
    with open(KNOWN_FACES_PATH, 'wb') as f:
        pickle.dump(known_faces, f)

    logger.info("Saving actors information")
    with open(ACTORS_JSON_PATH, 'w') as f:
        json.dump(actors_info, f, indent=4)

    return known_faces



def match_faces(unknown_face_encodings, tolerance=0.6):
    """
    Match unknown faces to known actors.

    Args:
        unknown_face_encodings (list): List of face encodings from the video.

    Returns:
        list: List of matched actor IDs.
    """
    known_faces = load_known_faces()
    matched_actor_ids = []

    logger.info(f"Matching {len(unknown_face_encodings)} unknown faces")
    for i, unknown_encoding in enumerate(unknown_face_encodings):
        distances = []
        actor_ids = []
        for actor in known_faces:
            for known_encoding in actor['encodings']:
                distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
                if distance <= tolerance:
                    distances.append(distance)
                    actor_ids.append(actor['actor_id'])

        if distances:
            best_match_index = distances.index(min(distances))
            matched_actor_id = actor_ids[best_match_index]
            matched_actor_ids.append(matched_actor_id)
            logger.debug(f"Face {i+1} matched with actor ID: {matched_actor_id}")
        else:
            logger.debug(f"No match found for face {i+1}")

    logger.info(f"Matched {len(matched_actor_ids)} faces")
    return matched_actor_ids

def load_known_faces():
    """
    Load known face encodings from serialized file.
    """
    logger.info("Loading known faces database")
    with open(KNOWN_FACES_PATH, 'rb') as f:
        known_faces = pickle.load(f)
    return known_faces

def load_actors_info():
    """
    Load actor information from JSON file.
    """
    logger.info("Loading actors information")
    with open(ACTORS_JSON_PATH, 'r') as f:
        actors_info = json.load(f)
    return actors_info