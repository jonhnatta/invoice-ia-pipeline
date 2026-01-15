import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class S3Service:
    def __init__(self):
        self.bucket_name = os.getenv("AWS_S3_BUCKET")
        self.region = os.getenv("AWS_REGION")
            
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=self.region
            )
        except Exception as e:
            print(f"Erro ao inicializar cliente S3: {e}")
            self.s3_client = None

    def upload_json(self, data: dict, filename: str):
        if not self.s3_client or not self.bucket_name:
            return

        try:
            json_str = json.dumps(data, indent=2, ensure_ascii=False, default=str)
            
            s3_key = f"invoices-processed/{filename}"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json_str,
                ContentType='application/json'
            )
            print(f"salvo no S3: s3://{self.bucket_name}/{s3_key}")
            
        except Exception as e:
            print(f"Erro ao salvar no S3: {e}")
            raise e
