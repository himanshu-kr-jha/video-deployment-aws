# Scalable Video Processing Using AWS ECS, Fargate, Lambda, and S3

## Introduction

This guide outlines how to use AWS services to implement an automated, scalable video processing pipeline that converts colored movies to grayscale upon upload to S3 storage.

### Goal

Implement a video processing pipeline to convert colored videos to grayscale automatically using serverless computing.

### Key Services Used

- **AWS Lambda**: Serverless compute service for triggering tasks.
- **Elastic Container Registry (ECR)**: To store Docker images.
- **Elastic Container Service (ECS) with Fargate**: To manage, scale, and deploy processing containers.
- **AWS S3**: Storage service for input and output videos.
- **Python**: To write processing code.
- **Docker**: To create container images.

## Workflow

1. **Upload File to S3**: Trigger the pipeline when a file is uploaded to an S3 bucket.
2. **Lambda Function**: Detects the file upload and triggers an ECS task.
3. **ECS Task**: Uses a Docker container to process the video.
4. **Process Video**: Write your own processing method (Here implemented -> motion detection in region of interest)
5. **Store Output**: Upload the processed video back to S3.

## Technologies and Services

- **Python Script**: `process_video.py` to convert RGB video to grayscale.
- **Docker**: Create a Docker image with the Python script, stored on ECR.
- **AWS Lambda**: Monitor S3 and trigger ECS tasks.
- **ECS with Fargate**: To run Docker containers for video processing.
- **AWS CLI**: To interact with AWS services from the command line.

## Setup Steps

### Prerequisites

- **AWS Account**: With sufficient permissions.
- **AWS CLI**: Installed on the local machine.

### S3 Buckets

1. **Create Buckets**: `video-processor-input` and `video-processor--output`.
2. **Settings**: Default settings, private access.

### Python Script

1. **Folder Structure**: Create a `code` folder with `requirements.txt` and `process_video.py` files.
2. **requirements.txt**: List Python dependencies.
3. **process_video.py**: Contains the video processing script using OpenCV and Click CLI.

### Docker Setup

1. **Dockerfile**: Create in the same folder as the Python script.
2. **Install Docker**: Ensure Docker is installed and running on your machine.
3. **Build Image**: Run commands to build the Docker image, verify with `docker images` command.

### Elastic Container Registry (ECR)

1. **Create Repository**: `video-processor` to store Docker image.
2. **Push Image**: Authenticate Docker with ECR, tag and push the image.

### Elastic Container Service (ECS) and Fargate

1. **Get Started with ECS**: Use ECS to configure container, task, and cluster.
2. **Container Definition**: Use the URL of Docker image, leave other settings default.
3. **Task Definition and Service**: Set meaningful names and default settings.
4. **Cluster**: Name the cluster and create it.

### IAM Roles and Policies

1. **Create Policies**: For S3 read access (input bucket) and write access (output bucket).
2. **Create Roles**: ECS task role with required policies attached.

### AWS Lambda Function

1. **Create Function**: Define from scratch with Python 3.9 runtime, S3 read-only permission.
2. **Add Trigger**: S3 bucket events trigger for object create events.
3. **Add Permissions**: Attach ECS full access policy to Lambda function's role.
4. **Add Code**: Update Lambda function with code to trigger ECS tasks.

## Testing

1. **Upload Videos**: To the input S3 bucket.
2. **Monitor Lambda**: Check invocations and logs in CloudWatch.
3. **Check ECS Tasks**: Ensure tasks are running and then stopped after processing.
4. **Output Verification**: Download and verify the processed videos from the output bucket.

## Considerations and Alternatives

- **Limitations**: Static Docker images require rebuilding and pushing for code updates, high data transfer costs for large files.
- **Alternatives**: Explore Kubernetes and AWS Batch for different batch processing solutions.

## Conclusion

- **Outcome**: Successfully create an automated, scalable video processing pipeline using AWS services.
- **Recommendation**: Compare performance, portability, and cost of different solutions for future implementations.

## Resources

- **[AWS CLI Installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)**: Instructions for different operating systems.

## Author - Himanshu Kumar Jha
