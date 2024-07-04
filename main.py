import boto3
import pandas as pd
from sqlalchemy import create_engine
import time
import mysql.connector


aws_access_key_id = 'AKIAYXTOYJNVOIM4QC74'
aws_secret_access_key = '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'
region_name = 'us-east-1'


    
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

glue_client = session.client('glue')



s3 = session.client('s3')
bucket_name = 'go-digit-bucket'
file_name = 'Student_performance_data _.csv'


database_name = 'examplerds'
table_name = 'Students'
rds_host = 'example-rds.cjs4aywyeiyg.us-east-1.rds.amazonaws.com'
rds_port = '3306'
rds_user = 'admin'
rds_password = 'admin123'

def read_from_s3(bucket, file):
    file_objects = s3.list_objects_v2(Bucket=bucket, Prefix=file)['Contents']
    dfs = []
    for file_object in file_objects:
        file_key = file_object['Key']
        file_obj = s3.get_object(Bucket=bucket, Key=file_key)
        # Read CSV file from S3 object
        df = pd.read_csv(file_obj['Body'])
        dfs.append(df)
    return pd.concat(dfs)


def load_data(data):
    try:
        conn_str = f'mysql+pymysql://{rds_user}:{rds_password}@{rds_host}:{rds_port}/{database_name}'
        engine = create_engine(conn_str)
    except Exception as e:
        print("Unable to connect RDS")
        return
    
    
   
    print("connected to RDS")
    # Write the DataFrame to RDS
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
    # Closing the connection
    engine.dispose()

    print('Data loaded successfully to RDS!')


def create_connection():
    connection=mysql.connector.connect(
        host = 'example-rds.cjs4aywyeiyg.us-east-1.rds.amazonaws.com',
        user = 'admin',
        password = 'admin123',
        database = 'examplerds'
    )
    return connection

def table(connect):
    cursor=connect.cursor()
   
    cursor.execute("CREATE TABLE Students(StudentID INT PRIMARY KEY,Age INT,Gender INT,Ethnicity INT,ParentalEducation INT,StudyTimeWeekly FLOAT,Absences INT,Tutoring INT,ParentalSupport INT,Extracurricular INT,Sports INT,Music INT,Volunteering INT,GPA FLOAT,GradeClass INT);")


def glue_crawler():

    crawler_name = 'example'

    
        
    
    try:
        response = glue_client.start_crawler(Name=crawler_name)
        print(f'Successfully started the crawler: {crawler_name}')
    except glue_client.exceptions.CrawlerRunningException:
        print(f'The crawler {crawler_name} is already running.Waiting...')
    except glue_client.exceptions.EntityNotFoundException:
        print(f'The crawler {crawler_name} does not exist.')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    
    response_info = glue_client.get_crawler(Name=crawler_name)
    crawler_state = response_info["Crawler"]["State"]
    while crawler_state == 'RUNNING':
        print(f"Crawler {crawler_name} is still running. Waiting...")
        time.sleep(60)  # Wait for 30 seconds before checking again
        response_info = glue_client.get_crawler(Name=crawler_name)
        crawler_state = response_info["Crawler"]["State"]
    print("Crawler Stop")
    return 

def main():
    
    
    data = read_from_s3(bucket_name, file_name)
    try:
        con=create_connection() #Connection
        tab=table(con)          # Creating Table
        rds=load_data(data)     #Loads Data
    except Exception as e:
        print("Data load in RDS is not possible, running glue crawler")
        glue_crawler()

    print("Done")
main()
