# Work Process and Notes of Predict

## To go back to:
1. Why RDS is trusted in the Role created
    - EC2 is by default to have access to S3, RDSdata and SNS
    - Why does RDS require it and where does it fit in

## Steps followed
Quick summary of each resource on AWS used and processed followed to complete predict. With some notes, hints and hacks to complete this.

### AWS IAM Roles
Create a Role in IAM linked specific AWS Service (to an EC2 instance).
This role then allows the EC2 instance (and the added RDS Postgres SQL database hosted on an instance) to call AWS services on your behalf - based on the policies attached.
- attached the required policies to the role
- edit the trust relationships
    1. include RDS service to allow same policies
    ```
    "Service": [
                    "ec2.amazonaws.com",
                    "rds.amazonaws.com"
                ]
    ```
### AWS EC2 Security Groups
Set up the communication between various AWS services and components. Set the inbound and outbound (EC2 Instance) rules that control network traffic in pipeline.
- navigate to ec2 security groups and create new
- set inbound and outbound rules
    - note to first create and complete security group creation
    - then edit inbound rules to add current security group to `Source`

### AWS S3 Bucket
Create bucket to store source (raw data) data of the stock market stuff.
- normal bucket create process and upload files into custom created folders

### AWS RDS
Standard create steps - nothing special just attached the new created security groups for the inboud and outbound rules

### AWS EC2
Standard create steps
* After creation modify the IAM Role to the created one above!!!
Allocate the Elastic IP:

    1. Navigate to EC2 and select “Elastic IPs” on the left panel.
    2. Click on “Allocate Elastic IP address”. On the next page, leave everything as default and click “Allocate”.
    3. Highlight the newly created Elastic IP, then click on “Actions” at the top, on the drop down, select “Associate Elastic IP address”.
    4. Under “Resource type”, select Instance. On “Instance”, select your newly created instance.
    5. Leave the “Private IP address” and “Reassociation” empty.

Important command to connect vio ssh `ssh -i {your-key-pair.pem} -L 8080:localhost:8080 ubuntu@{your-public-ip-address}` which is `ssh -i DELEOSMI-keypair.pem -L 8080:localhost:8080 ubuntu@54.195.143.179`

Then install packages:
```
sudo apt update
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh
```

`initialize Anaconda3 by running conda init`

```
sudo apt install python3-pip
# may need to restart instance before doing above installation
pip3 install awscli
```

`echo PATH=$PATH:/home/ubuntu/.local/bin >> .bashrc`
<br>This adds ~/.local/bin to the PATH environment variable. This allows the user to run executables from this location without needing to type out the whole path.

`source ~/.bashrc`
<br> this command is used to update or refresh the changes made in the bashrc file to be applicable in shells permanently.

Configure AWS on the EC2 instance with `aws configure` command and follow prompts.

### Mount S3 to EC2
Using the package **s3fs** to mount s3 on ec2 as a local file system.

Install it with `sudo apt install s3fs`

The s3fs refuses all other users access by default - we have 2x already on EC2 (ubuntu and root) but will not recognize airflow therefore uncomment the following in s3fs config file.
Run:
`sudo nano /etc/fuse.conf`
Then uncomment *“user_allow_other”*

Finally create defaiult folder for S3 bucket --> `mkdir ~/s3-drive`

Mount it with following command and fill in relevant info:

`s3fs -o iam_role=<ec2-default-role> -o url="https://s3.eu-west-1.amazonaws.com/" -o endpoint=eu-west-1 -o allow_other -o curldbg <bucket-name> ~/s3-drive`


### Notebook - `python_processing_questions.ipynb`
Notebook contains all the info - clear and simple steps

#### Python Script - historical_processing_ec2.py
Copy paste code



### AWS RDS Database Tables create
Use pgAdim to setup the RDS server
- Remeber the password and username created during the AWS RDS setup --> type it in here at pgAdmin
