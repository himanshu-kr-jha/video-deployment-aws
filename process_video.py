import os
import logging
import click
import cv2
import boto3
from botocore.exceptions import ClientError 

def bg_movement(frame,threshold, kernel, object_detector, roi_x, roi_y, roi_height, roi_width,counter=0):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    mask = object_detector.apply(blurred_frame)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    roi_mask = mask[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    movement = cv2.countNonZero(roi_mask)
    counter+=1
    if movement > threshold:
        print("Frame-{} : moved".format(counter))
        return "moved"
    else:
        print("Frame - {}: not moved".format(counter))
        return "Not moved"
    
def movement_detection(input_video_path,output_video_path):
    cap =cv2.VideoCapture(input_video_path)
    num_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    roi_x = 250
    roi_y = 200
    roi_width = 500
    roi_height = frame_height - roi_y

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    object_detector = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

    for frame_index in range(num_frames):
        ret,frame=cap.read()
        movement = bg_movement(frame, 8000, kernel, object_detector, roi_x, roi_y, roi_height, roi_width)
        text_x = frame_width - 200
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.putText(frame, f'State: {movement}', (text_x, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 0, 0), 2)
        video_writer.write(frame)
    cap.release()

@click.command(name='process_video')
@click.option("--input_bucket", type=str, required=True, help="path to the input S3 bucket")
@click.option("--input_filepath", type=str, required=True, help="path to the input movie file")
@click.option("--output_filepath", type=str, required=True, help="path to the output movie file")
def cli(input_bucket, input_filepath, output_bucket, output_filepath):
# determine input and output file basenames input_file_basename = os.path.basename(input_filepath)
    input_file_basename=os.path.basename(input_filepath)
    output_file_basename = os.path.basename(output_filepath)

# download video file from S3
    s3=boto3.client('s3')
    s3.download_file(input_bucket, input_filepath, input_file_basename)
    # process video file 
    movement_detection(input_file_basename, output_file_basename)
    # upload processed video file to S3 
    s3.upload_file(output_file_basename, output_bucket, output_filepath)
if __name__== "__main__":
    cli()