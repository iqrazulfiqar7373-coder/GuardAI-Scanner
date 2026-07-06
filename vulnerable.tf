# Security Risk 1: Open SSH Port to the world
resource "aws_security_group" "bad_sg" {
  name        = "vulnerable-sg"
  description = "Cybersecurity Risk Open Port"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Dangerous!
  }
}

# Security Risk 2: Public S3 Bucket
resource "aws_s3_bucket" "bad_bucket" {
  bucket = "my-very-secret-raw-data-bucket"
  acl    = "public-read" # Dangerous!
}