resource "aws_security_group" "allow_web" {
  name        = "allow_web_traffic"
  description = "Allow SSH and FastAPI HTTP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "disaster_api" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.allow_web.id]

  tags = {
    Name = "disaster-api"
  }

  user_data = file("${path.module}/user_data.sh")
}

output "public_ip" {
  value = aws_instance.disaster_api.public_ip
}