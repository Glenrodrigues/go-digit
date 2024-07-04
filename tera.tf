##############################################################
#s3 setup
provider "aws" {
  region = "us-east-1"  # Change this to your preferred region
}

resource "aws_s3_bucket" "example" {
  bucket = "examplegodigit"
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_object" "folder" {
  bucket = aws_s3_bucket.example.bucket
  key    = "my-folder/"  # This is the "folder" name
}

#######################################################################################
# RDS Setup
resource "aws_security_group" "rds" {
  name_prefix = "example-"
  ingress {
    from_port   = 0
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "rds" {
  engine                 = "mysql"
  db_name                = "examplerds"
  identifier             = "example-rds"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  publicly_accessible    = true
  username               = "admin"
  password               = "admin123"
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot    = true

  tags = {
    Name = "example-db"
  }
}



#################################################################################################
#Glue Setup

resource "aws_iam_role" "example" {
  name               = "example-glue-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "example_s3_access_policy" {
  name        = "example-glue-s3-access-policy"
  description = "Policy to allow access to S3 for Glue"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource  = [
          "arn:aws:s3:::go-digit-bucket/*",
          "arn:aws:s3:::go-digit-bucket"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "example_attach_policy" {
  role       = aws_iam_role.example.name
  policy_arn = aws_iam_policy.example_s3_access_policy.arn
}

resource "aws_iam_role_policy" "example_cloudwatch_logs_policy" {
  name   = "example-glue-cloudwatch-logs-policy"
  role   = aws_iam_role.example.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "glue:*"
        Resource  = "*"
      }
    ]
  })
}


resource "aws_glue_catalog_database" "example" {
  name = "example_database"
}

resource "aws_glue_crawler" "example" {
  database_name = aws_glue_catalog_database.example.name
  name          = "example"
  role          = aws_iam_role.example.arn

  s3_target {
    path = "s3://go-digit-bucket/"
  }
}
