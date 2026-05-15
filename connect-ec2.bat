@echo off
echo ========================================
echo Connecting to VartaIQ EC2 Instance
echo IP: 65.2.158.83
echo User: ec2-user (Amazon Linux)
echo ========================================
echo.

ssh -i "vartaiq-key.pem" ec2-user@65.2.158.83

pause
