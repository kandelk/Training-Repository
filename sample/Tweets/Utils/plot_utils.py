import io
from datetime import datetime

import boto3
import matplotlib.pyplot as plt
from numpy import arange


def create_and_save_hbar(xval, yval, folder, name):
    fig, ax = plt.subplots()
    position = arange(len(yval))

    ax.barh(position, xval)

    ax.set_yticks(position)
    ax.set_yticklabels(yval)

    now = datetime.now()

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(folder)
    bucket.put_object(Body=img_data, ContentType='image/png', Key=f"{name}/{now.date()}-{now.time().hour}.png")

    # fig.savefig(f"{folder}/{name}-{now.date()}-{now.time().hour}.png")
