<<<<<<< HEAD
resource "aws_security_group" "bad_group" {
  name        = "allow_all"
  description = "Vulnerable security group setup"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "my-very-vulnerable-data-bucket"
  # Missing logging, encryption, or versioning block
=======
resource "aws_security_group" "bad_group" {
  name        = "allow_all"
  description = "Vulnerable security group setup"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "my-very-vulnerable-data-bucket"
  # Missing logging, encryption, or versioning block
>>>>>>> 4dfec665576d0cde98b4a5e657fc11c1b4aa51e7
}