import sys
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import ml
import tensorflow as tf


def init_app():
    with open("./secrets.json") as json_file:
        json_data = json.load(json_file)

    storage_bucket = json_data["storage_bucket"]
    account_key = json_data["account_key"]

    app = firebase_admin.initialize_app(
        credentials.Certificate(account_key),
        options={
            'storageBucket': storage_bucket,
        })

    return app


def create_model():
    app = init_app()
    # source = ml.TFLiteGCSModelSource.from_saved_model('./model') 텐서플로우 모델이면

    # model = tf.keras.models.load_model('./model/파일이름.h5') kreas 모델이면
    # source = ml.TFLiteGCSModelSource.from_keras_model(model)

    tflite_format = ml.TFLiteFormat(model_source=source)
    model = ml.Model(
        display_name="image_model",
        tags=["image"],
        model_format=tflite_format)

    new_model = ml.create_model(model, app)
    ml.publish_model(model_id=new_model.model_id, app=app)


def update_model():
    app = init_app()
    models = ml.list_models(list_filter="tags: image", app=app).iterate_all()
    model = next(models)

    # source = ml.TFLiteGCSModelSource.from_saved_model('./model') 텐서플로우 모델이면

    # new_model = tf.keras.models.load_model('./model/파일이름.h5') kreas 모델이면
    # source = ml.TFLiteGCSModelSource.from_keras_model(new_model)
    model.model_format = ml.TFLiteFormat(model_source=source)

    updated_model = ml.update_model(model, app)
    ml.publish_model(model_id=updated_model.model_id, app=app)


if __name__ == "__main__":
    argument = sys.argv
    if len(argument) < 2:
        print("명령어를 입력하세요 ex) python app.py create or python app.py update")

        sys.exit(0)

    command = argument[1]

    if command == "create":
        create_model()
    elif command == "update":
        update_model()
    else:
        print("명령어를 올바르게 입력하세요 ex) python app.py create or python app.py update")
        sys.exit(0)
