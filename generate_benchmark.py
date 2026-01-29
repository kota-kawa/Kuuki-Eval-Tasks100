import json
import random

def generate_data():
    tasks = []

    # ------------------------------------------------------------------
    # Category 1: Scheduling (Time/Availability Constraints)
    # ------------------------------------------------------------------
    # Context: User mentions a conflict in a previous message.
    # Instruction: Schedule a meeting.
    # Implicit: Avoid the mentioned conflict.

    names = ["佐藤", "鈴木", "田中", "高橋", "伊藤", "渡辺", "山本", "中村", "小林", "加藤"]
    days = ["月曜", "火曜", "水曜", "木曜", "金曜"]
    times = ["午前中", "15時以降", "夕方", "ランチタイム"]

    for i in range(15):
        name = random.choice(names)
        day = random.choice(days)
        time = random.choice(times)
        bad_reason = random.choice(["歯医者がある", "子供の迎え", "集中作業時間", "他部署との定例"])

        context = f"""
チャット履歴:
{name}: 来週の{day}の{time}は{bad_reason}のでブロックしておいてください。
マネージャー: 了解です。
"""
        instruction = f"{name}さんを含めたチーム定例ミーティングを来週設定してください。候補をいくつか挙げてください。"
        implicit = f"{day}の{time}（{bad_reason}）を避けて提案する。"
        response = f"承知いたしました。{name}さんのご予定を考慮し、以下の日時でいかがでしょうか。\n・{day}以外の{time}\n・別日の同時間帯"

        tasks.append({
            "category": "Scheduling",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # ------------------------------------------------------------------
    # Category 2: Tone & Manner (Hierarchy/Relationship)
    # ------------------------------------------------------------------
    # Context: Shows relationship (Client vs. Internal, Senior vs. Junior).
    # Instruction: Write a reply.
    # Implicit: Adjust politeness level (Keigo vs. Casual).

    # Scenario 2a: Casual Internal
    for i in range(10):
        name = random.choice(names)
        context = f"""
送信者: {name} (同期・同じチーム)
件名: おつかれー
本文:
昨日の飲み会楽しかったね！
例の資料だけど、ちょっとだけ直しといたから確認よろしくー。
"""
        instruction = "返信を作成してください。"
        implicit = "同期に対するカジュアルなトーンで返信する（敬語を使いすぎない）。"
        response = "おつかれ！昨日は楽しかったね。\n資料の修正ありがとう！後で確認しておくね。"

        tasks.append({
            "category": "Tone - Casual",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # Scenario 2b: Formal Client Apology
    for i in range(10):
        client_name = random.choice(["株式会社A", "B商事", "Cテック"])
        error = random.choice(["サーバーダウン", "納品遅延", "請求書の誤記載"])
        context = f"""
送信者: {client_name} 担当者
件名: 【至急】{error}について
本文:
先ほど御社のサービスで{error}が発生しているのを確認しました。
至急状況を確認し、報告してください。
"""
        instruction = "返信を作成してください。"
        implicit = "謝罪を最優先し、堅苦しいビジネス敬語（最上級の丁寧語）を使用する。"
        response = f"{client_name} 担当者様\n\n平素より大変お世話になっております。\nこの度は、{error}により多大なるご迷惑をおかけし、深くお詫び申し上げます。\n現在、至急原因の調査を行っております。判明次第、直ちにご報告いたします。\n何卒よろしくお願い申し上げます。"

        tasks.append({
            "category": "Tone - Formal",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # ------------------------------------------------------------------
    # Category 3: Implicit Preferences (Format/Style)
    # ------------------------------------------------------------------
    # Context: Past feedback indicating preference.
    # Instruction: Create a document/summary.
    # Implicit: Follow the preference without being told again.

    preferences = [
        ("長文は読まないから箇条書きにして", "箇条書きで簡潔にまとめる"),
        ("結論から先に書いて", "PREP法（結論・理由・詳細）で書く"),
        ("専門用語は使わないで", "平易な言葉で説明する"),
        ("英語の資料は自動翻訳じゃなくて要約だけくれ", "日本語で要点をまとめる")
    ]

    for i in range(15):
        pref_text, impl_rule = random.choice(preferences)
        name = random.choice(names)

        context = f"""
過去のチャット（1ヶ月前）:
{name}: 前回の報告書、文字ばかりで読む気がしなかったよ。次は{pref_text}。
私: 承知しました。
"""
        instruction = f"{name}部長に、今回のプロジェクト進捗報告を送ってください。"
        implicit = f"過去の指摘「{pref_text}」を踏まえ、{impl_rule}。"
        response = "【進捗報告】\n結論から申し上げますと、予定通り進行中です。\n\nポイント:\n- 機能Aの実装完了\n- テスト工程へ移行中\n..."

        tasks.append({
            "category": "Preferences",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # ------------------------------------------------------------------
    # Category 4: Contextual Reference ("That thing")
    # ------------------------------------------------------------------
    # Context: Mentions a specific item/bug/person earlier.
    # Instruction: "Handle that."
    # Implicit: Identify exactly what "that" is.

    items = [
        ("ログイン画面のレイアウト崩れ", "CSSの修正"),
        ("A社の契約更新", "法務部への確認"),
        ("田中さんの送別会", "お店の予約"),
        ("サーバーの容量不足", "ログファイルの削除")
    ]

    for i in range(15):
        topic, action = random.choice(items)

        context = f"""
チャット履歴:
10:00 Aさん: {topic}が気になってるんだよね。
10:05 Bさん: 確かに、早めに対応したほうがいいかも。
"""
        instruction = "Bさんとして、「例の件、やっておきます」と伝えて、具体的なアクションを追記してください。"
        implicit = f"「例の件」が「{topic}」であることを理解し、それに対する適切な処置（{action}など）を提案する。"
        response = f"例の{topic}の件、やっておきますね。とりあえず{action}を進めます。"

        tasks.append({
            "category": "Context Reference",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # ------------------------------------------------------------------
    # Category 5: Personal/Gift/Empathy
    # ------------------------------------------------------------------
    # Context: Profile or casual chat mentions restriction/preference.
    # Instruction: Suggest something.
    # Implicit: Apply the restriction.

    constraints = [
        ("ナッツアレルギー", "ナッツを含まない菓子折り"),
        ("お酒が飲めない", "ジュースやコーヒーのギフト"),
        ("甘いものが苦手", "煎餅やカタログギフト"),
        ("猫を飼っている", "猫に危険な植物（ユリなど）は避ける")
    ]

    for i in range(15):
        condition, implicit_rule = random.choice(constraints)
        target = random.choice(names)

        context = f"""
{target}さんのプロフィール備考欄:
家族構成: 妻、娘（3歳）。
特記事項: {condition}。
"""
        instruction = f"{target}さんへのお歳暮を選んでください。候補を一つ挙げ、理由を添えてください。"
        implicit = f"特記事項「{condition}」を考慮し、{implicit_rule}を選ぶ。"
        response = f"{implicit_rule}はいかがでしょうか。{condition}とありましたので、安心して召し上がっていただけるものを選びました。"

        tasks.append({
            "category": "Personal Constraints",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # ------------------------------------------------------------------
    # Category 6: Reply Routing / CC
    # ------------------------------------------------------------------
    # Context: Who is involved in which project.
    # Instruction: Send an email.
    # Implicit: Include the right stakeholders in CC.

    for i in range(10):
        project = random.choice(["プロジェクトX", "新卒採用", "オフィス移転"])
        stakeholder = random.choice(names)

        context = f"""
プロジェクト体制図:
{project}リーダー: {stakeholder}
担当者: 私
"""
        instruction = f"{project}に関する重要な仕様変更が決まりました。開発チームへの連絡メールを作成してください。"
        implicit = f"リーダーである{stakeholder}さんを必ずCCに入れる。"
        response = f"To: 開発チーム\nCC: {stakeholder}様\n\n件名: {project}の仕様変更について\n..."

        tasks.append({
            "category": "Routing",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # ------------------------------------------------------------------
    # Category 7: Hidden Emotion/Support
    # ------------------------------------------------------------------
    # Context: User sounds depressed or stressed.
    # Instruction: Give feedback on their work.
    # Implicit: Be encouraging/gentle, not harsh.

    for i in range(10):
        name = random.choice(names)
        context = f"""
{name}のチャットステータス: 「連日残業で限界...」
直前のメッセージ:
やっと資料できました...。ミスあるかもしれませんが、もう目が開かなくて...確認お願いします...。
"""
        instruction = "提出された資料に誤字がいくつかありました。修正を依頼してください。"
        implicit = "相手が疲弊していることを察し、労いの言葉をかけつつ、急ぎでなければ明日でいいと伝えるなど配慮する。"
        response = f"{name}さん、遅くまで本当にお疲れ様です！\n資料ありがとうございます。いくつか修正点がありますが、急ぎではないのでまずはゆっくり休んでください。体調第一でお願いします。"

        tasks.append({
            "category": "Emotional Support",
            "context": context.strip(),
            "instruction": instruction,
            "implicit_needs": implicit,
            "reference_response": response
        })

    # Ensure we have exactly 100 tasks (or slightly more, then slice)
    # Current counts: 15 + 10 + 10 + 15 + 15 + 15 + 10 + 10 = 100 exactly.

    # Shuffle just in case
    random.shuffle(tasks)

    # Add ID and write
    with open('context_reading_benchmark.jsonl', 'w', encoding='utf-8') as f:
        for idx, task in enumerate(tasks):
            record = {
                "id": idx + 1,
                "context": task["context"],
                "instruction": task["instruction"],
                "implicit_needs": task["implicit_needs"],
                "reference_response": task["reference_response"],
                "category": task["category"]
            }
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    generate_data()
