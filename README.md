# go-digit Assessment

## Step 1: Terraform Code (IaC)

Wrote code for S3, RDS, Glue Crawler.

## Step 2: Python Program

Wrote a Python program to:
1. Get data from S3.
2. If RDS is available, create a table and push data into it.
3. If RDS is not available, run the Glue Crawler which will put data in the Glue Database.

## Step 3: Dockerization

Created a Dockerfile for containerization.

## Step 4: Push to GitHub

Pushed all code to a GitHub repository.

## Step 5: Jenkins Pipeline

Built a Jenkins pipeline that:
1. Retrieves the Dockerfile and runs it.
2. Pushes the image to AWS ECR.
3. Runs Terraform code to provision resources.

## Step 6: Lambda Function

Created a Lambda function to run the container. The Lambda function performs its task of pushing data into the target location but throws errors related to the init phase and invoke phase. These errors were not resolved due to time constraints.


