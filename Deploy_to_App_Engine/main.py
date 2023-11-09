import os
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from PIL import Image
#from google.cloud import storage


app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def show_enter():
    # POST(入力後)
    if request.method == "POST":
        # ファイル選択：ファイルアップロード
        file = request.files["enter_file"]
        # ファイルの名前を取得（拡張子付き：xxx.jpg）
        filename = file.filename
        # ファイルの拡張子を取り除く（xxx.jpg ⇒ (xxx, .jpg) ⇒ xxx）
        filename = os.path.splitext(filename)[0]
        
        # 変換後拡張子選択：セレクトボックス
        exit_extension = request.form.get("exit_extension")

        # 拡張子の変換
        img = Image.open(file)
        tmp_save_path = f"/tmp/{filename}.{exit_extension}"
        img.save(tmp_save_path)

        """
        # GCSにファイルを保存
        gcs = storage.Client()
        bucket_name = "cloud-build-test-403611.appspot.com"
        bucket = gcs.get_bucket(bucket_name)
        blob_name = f"temp_folder/{filename}.{exit_extension}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(tmp_save_path, content_type=f"image/{exit_extension}")
        """
        return send_file(tmp_save_path, as_attachment=True)

    # GET(入力前)
    else:
       return render_template("index.html")