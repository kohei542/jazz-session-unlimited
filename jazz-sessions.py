import pyxel

class App:
    def __init__(self):
        pyxel.init(256, 256)  # ウィンドウサイズを設定
        pyxel.load("my_resource.pyxres")  # リソースファイルを読み込む
        pyxel.mouse(True)  # マウスカーソルを表示する

        #シード系データ
        self.spawn_note_timing = [30, 60, 90, 110, 140, 160, 210, 230, 270, 300, 360, 420]  # 音符を流すタイミング（フレーム単位）
        self.hit_position = 80  # 音符をヒットさせる位置

        #初期値(0)を設定
        self.reset_game()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.current_frame += 1

        if self.frame == 1:
            self.update_game()
        if self.frame == 2:
            self.update_result()

        pass

    def update_game(self) :

        # 音符を生成
        if self.current_frame in self.spawn_note_timing:
            self.notes.append(256)  # 画面の右端から開始

        # 音符を動かす
        for i, x in enumerate(self.notes):
            self.notes[i] -= 2  # 音符のスピード

        # ヒットコメントのタイミングを更新
        if self.hit_comment is not None:
            if pyxel.frame_count - self.hit_comment_time > 10:  # 60フレーム（約1秒）が経過したら
                self.hit_comment = None  # ヒットコメントをクリア
        
        # 音符をヒット
        if pyxel.btnp(pyxel.KEY_SPACE):
            for i, note in enumerate(self.notes):
                if abs(note - self.hit_position) < 10:  # 中央に近い
                    self.hit_comment = "Nice!"
                    self.score += 100
                    self.hit_comment_time = pyxel.frame_count
                    self.notes[i] = -1  #ヒットした音符をマーク
                elif abs(note - self.hit_position) < 20: # 少し離れている
                    self.hit_comment = "Bad..."
                    self.score -= 50
                    self.hit_comment_time = pyxel.frame_count
                    self.bad_count += 1
                    self.notes[i] = -1 # ヒットした音符をマーク

        # 枠外に出た音符をチェック
        for i, note in enumerate(self.notes):
            if note < self.hit_position - 20 and note != -1:  # 枠を通過し、未ヒット
                self.hit_comment = "Bad..."
                self.score -= 50
                self.hit_comment_time = pyxel.frame_count
                self.bad_count += 1
                self.notes[i] = -1  # 処理済みの音符をマーク

        # 処理済みの音符を削除
        self.notes = [note for note in self.notes if note != -1]

        # 音楽の段階を更新
        if self.current_frame == 264:  # 最初の4回の再生が終わったら
            pyxel.stop()  # 現在の音楽を停止
            pyxel.playm(1, loop=True)

        # 音符が全部流れたか、Badが2回出たら結果発表へ
        if self.current_frame == 533 or self.bad_count >= 2:
            self.frame = 2
            pyxel.stop()
            if self.bad_count >= 2:
                self.result = 0
            else: 
                self.result = 1
        pass

    def update_result(self):
        if self.result == 0 and (self.is_played_result_music == False):
            pyxel.playm(3, loop=False)
        elif self.is_played_result_music == False:
            pyxel.playm(2, loop=False)

        self.is_played_result_music = True

        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()  # ゲームを再起動
        pass

    def draw(self):
        if self.frame == 1:
            self.draw_game()
        if self.frame == 2:
            self.draw_result()

    def draw_game(self):
        pyxel.cls(7)  # 背景を黒でクリア
        # (128, 0)から(256, 256)の範囲を画面の下部に描画
        cut_x = 100
        cut_y = 256
        pyxel.blt(0, cut_x, 0, 0, cut_x, cut_y, 256 - cut_x)
        pyxel.text(5, 5, f"Score: {self.score}", 0)

        if self.hit_comment is not None:
            pyxel.text(60, 80, f"{self.hit_comment}", 0)

        # 音符を描画
        for note in self.notes:
            pyxel.blt(note, 55, 0, 217, 29, 16, 16)  # 画像のサイズや位置は適宜調整してください
        
        # ヒット枠を描画
        pyxel.circb(self.hit_position , 60, 15, 8) # 枠の位置とサイズは適宜調整してください

    def draw_result(self):
        pyxel.cls(0)
        if self.result == 0:
            pyxel.text(104, 128, "Game Over", pyxel.COLOR_RED)
            pyxel.text(98, 140, f"Score: {self.score}", pyxel.COLOR_WHITE)
        else:
            pyxel.text(100, 128, "Game Clear", pyxel.COLOR_GREEN)
            pyxel.text(98, 140, f"Score: {self.score}", pyxel.COLOR_WHITE)
        
        pyxel.text(68, 200, f"Re-Start: Push the [R] Key", pyxel.COLOR_WHITE)
        pass

    def reset_game(self):
        # ゲームの状態を初期化する
        self.notes = []  # 音符のリスト
        self.score = 0  # スコア
        self.hit_comment = None
        self.hit_comment_time = 0  # ヒットコメントを表示開始した時刻
        self.current_frame = 0
        self.frame = 1 #(1=ゲーム画面, 2=リザルト画面)
        self.bad_count = 0 # Badのカウント
        self.note_count = 0 # 流した音符の数
        self.result = 0 #(0=game over, 1=game clear)
        self.current_measure = 0
        self.is_played_result_music = False

        pyxel.playm(0, loop=True)  # 最初の音楽を再生

App()