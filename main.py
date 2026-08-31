from utils import read_video, save_video
from trackers import Tracker
import cv2

def main():
    #Read Video
    video_frames = read_video('input_videos/08fd33_4.mp4')

    #initialize Tracker
    tracker = Tracker('models/best.pt')

    #Get Object Tracks
    tracks = tracker.get_object_tracks(
        video_frames,
        read_from_stub=True,
        stub_path='stubs/track_stub.pkl'
    )

    #save cropped image of a player
    if tracks['players'][0]:
        for track_id, player in tracks['players'][0].items():
            bbox = player['bbox']
            frame = video_frames[0]

            #crop bbox from frame
            cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

            #save cropped image
            cv2.imwrite(f'output_videos/cropped_image.jpg', cropped_image)
            break #since we only want to save one image.

        else:
            print("No players detected in the first frame.")

    #Draw output
    ##Draw object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks)

    #Save Video
    save_video(output_video_frames, 'output_videos/output_video.avi')

if __name__ == '__main__':
    main()

print("Done! Output saved to output_videos/")