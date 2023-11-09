from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
from flask import send_file
import os
import shutil

app = Flask(__name__)

# 変換データ・拡張子：入力
@app.route("/", methods=["POST","GET"])
def show_enter():
    # POST
    if request.method == "POST":
        # ファイル選択：ファイルアップロード
        file = request.files["enter_file"]
        # ファイルの名前を取得（拡張子付き：xxx.jpg）
        filename = file.filename
        # ファイルの拡張子を取り除く（xxx.jpg ⇒ (xxx, .jpg) ⇒ xxx）
        filename = os.path.splitext(filename)[0]

        # 変換後拡張子選択：セレクトボックス
        after_extension = request.form.get("exit_extension")

        # 拡張子の変換
        img = Image.open(file)
        save_path = f"queue_folder/{filename}.{after_extension}"
        # ファイル保存
        img.save(save_path)

        return send_file(save_path,
                         as_attachment=True
                        )

    # GET
    else:
        # データ一時保管場所確保
        shutil.rmtree("queue_folder")
        os.mkdir("queue_folder")
        return render_template("enter.html")


# アプリを実行
if __name__== '__main__':
    app.run()