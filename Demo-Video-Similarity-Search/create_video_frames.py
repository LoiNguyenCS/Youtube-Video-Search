import cv2
import os

# Relevant paths
main_folder_path = 'DataMiningNPRVideos'  
frames_folder_path = 'NPRVideoFrames'  
os.makedirs(frames_folder_path, exist_ok=True)

# Loop through each folder in the main folder
for folder_name in os.listdir(main_folder_path):
    folder_path = os.path.join(main_folder_path, folder_name)

    # Check if the item in the main folder is a directory
    if os.path.isdir(folder_path):
        video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

        # Loop through each video in the subfolder
        for video_file in video_files:
            video_path = os.path.join(folder_path, video_file)

            # Open the video file
            cap = cv2.VideoCapture(video_path)

            # Check if the video file is opened successfully
            if not cap.isOpened():
                print(f"Error: Could not open video {video_path}.")
                continue

            # Create a subfolder for each video in the frames folder
            video_name = os.path.splitext(video_file)[0]
            video_frame_folder = os.path.join(frames_folder_path, video_name)
            os.makedirs(video_frame_folder, exist_ok=True)

            frame_count = 0
            frame_capture_rate = 25

            # Read and save frames until the user presses 'q' key
            while True:
                ret, frame = cap.read() 

                # Check if the video is over
                if not ret:
                    print(f"End of video: {video_path}")
                    break
                
                # Capture frames only at the specified rate
                if frame_count % frame_capture_rate == 0:
                    # Save the frame as an image in the subfolder
                    frame_name = f"{video_name}_frame_{frame_count:04d}.jpg"
                    frame_path = os.path.join(video_frame_folder, frame_name)
                    cv2.imwrite(frame_path, frame)

                frame_count += 1

                # Break the loop if the user presses 'q' key
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break


            cap.release()

        cv2.destroyAllWindows()
