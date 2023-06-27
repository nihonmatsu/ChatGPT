import openai
import os

#OpenAIのAPIキーを環境変数から取得します。
openai.api_key = os.getenv("OPENAI_API_KEY")

#モデルに役割を指示します。
chat_log = [{"role": "system", "content": "あなたは完璧な執事セバスチャン・ミカエリスです。"},
            {"role": "user", "content": "こんばんは"}]

#Console 出力に色を付けるため、カラーコードを設定します。
gray = '\x1b[90m'
bold = '\033[1m'
reset = '\033[0m'

#初期メッセージ
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.0,
    messages= chat_log
)
print(response["choices"][0]["message"]["content"])


while True:
    #プロンプトの入力
    prompt = input(bold+gray+"> "+reset)
    if prompt.lower() == 'q':
        break

    #チャットログに会話履歴を残します。
    chat_log.append({"role": "user", "content": prompt})

    #APIリクエストからのレスポンスを受け取ります。完璧さを求めtemperatureは0.0です。
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0.0,
        messages= chat_log
    )

    #アシスタントの返信を抽出します。
    messages = response["choices"][0]["message"]["content"]

    #用いられたトークン数を取得します。
    total_tokens = response["usage"]["total_tokens"]

    #メッセージを表示します。
    print(bold+gray+messages+reset, end = "\n")

    #APIで送信可能な4096トークンを想定して、4000トークンで会話履歴を削除します。
    if total_tokens > 4000:
        chat_log.pop(1)
