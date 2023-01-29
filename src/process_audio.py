import pytube
import whisper
import time

MODEL_NAMES = ["tiny.en", "base.en", "small.en", "medium.en", "large", "large-v2"]
MODEL_NAME = MODEL_NAMES[0]


def download_video(url: str):
    data = pytube.YouTube(url)
    video = data.streams.get_highest_resolution()
    video_path = video.download()
    return video_path


def get_model(model_name: str):
    if model_name not in MODEL_NAMES:
        raise Exception("Model name not found")
    return whisper.load_model(model_name)


def get_transcript(model, video_path: str):
    result = model.transcribe(video_path, language='english')
    return result


if __name__ == "__main__":
    start_time = time.time()
    video_path = download_video("https://www.youtube.com/watch?v=A60q6dcoCjw")
    end_time1 = time.time()
    print(f"Time taken to download video: {end_time1 - start_time}")
    
    model = get_model(MODEL_NAME)
    end_time2 = time.time()
    print(f"Time taken to load model: {end_time2 - end_time1}")
    
    transcript = get_transcript(model, video_path)
    end_time3 = time.time()
    print(f"Time taken to get transcript: {end_time3 - end_time2}")
    
    print(transcript["text"])
    