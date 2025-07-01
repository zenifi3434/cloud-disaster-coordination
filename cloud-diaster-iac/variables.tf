variable "region" {
  default = "eu-north-1"
}

variable "ami_id" {
  description = "ami-042b4708b1d05f512"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "ec2-keypair"
}