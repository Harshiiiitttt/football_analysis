from utils import read_video, save_video
from trackers import Tracker
import cv2
from team_assigner import TeamAssigner

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

    # Interpolate ball positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

    #Assign Player teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0],
                                    tracks['players'][0])

    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, player in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], 
                                                 player['bbox'], player_id)

            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]


    # #save cropped image of a player
    # if tracks['players'][0]:
    #     for track_id, player in tracks['players'][0].items():
    #         bbox = player['bbox']
    #         frame = video_frames[0]

    #         #crop bbox from frame
    #         cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

    #         #save cropped image
    #         cv2.imwrite(f'output_videos/cropped_image.jpg', cropped_image)
    #         break #since we only want to save one image.

    #     else:
    #         print("No players detected in the first frame.")

    #Draw output
    ##Draw object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks)

    #Save Video
    save_video(output_video_frames, 'output_videos/output_video.avi')

if __name__ == '__main__':
    main()