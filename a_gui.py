"""IAplay: Tkinter로 만든 가상 돈벌기 게임. 실제 돈은 사용하지 않습니다."""

import random
import tkinter as tk
from tkinter import messagebox, simpledialog


def money(amount):
    """게임 화폐 IA를 보기 쉬운 모양으로 표시합니다."""
    return f"{amount:,.0f} IA"


class IAplay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IAplay | 나의 머니 게임")
        self.geometry("1000x760")
        self.minsize(760, 650)
        self.configure(bg="#070d19")

        self.player = {
            "name": "플레이어", "cash": 300, "energy": 10, "max_energy": 10,
            "work_bonus": 1.0, "invest_bonus": 0, "day": 1,
            "owned": set(), "factory": False,
        }
        self.colors = {"bg": "#070d19", "panel": "#101b2d", "blue": "#51d9ff", "text": "#edf7ff", "muted": "#b5bfd3", "line": "#354968"}
        self.button_palette = ["#17658b", "#684493", "#a84470", "#247768", "#a36327", "#365da7"]
        self.button_color_index = 0
        self.panel_color_index = 0
        self.ask_name()
        self.build_screen()
        self.refresh_status()
        self.log("IAplay에 온 걸 환영해요! 활동으로 돈을 모으고 나만의 부자가 되어 보세요.")

    def ask_name(self):
        name = simpledialog.askstring("플레이어 이름", "이름을 입력해 주세요:", parent=self)
        if name and name.strip():
            self.player["name"] = name.strip()[:18]

    def make_button(self, parent, label, command, accent=False):
        bg = "#12658a" if accent else self.button_palette[self.button_color_index % len(self.button_palette)]
        self.button_color_index += 1
        active = "#1786ae" if accent else "#405678"
        return tk.Button(parent, text=label, command=command, bg=bg, fg=self.colors["text"],
                         activebackground=active, activeforeground="white", relief="flat",
                         bd=0, padx=12, pady=10, font=("Arial", 10, "bold"), cursor="hand2")

    def build_screen(self):
        top = tk.Frame(self, bg=self.colors["bg"], padx=24, pady=18)
        top.pack(fill="x")
        tk.Label(top, text="◆ IAplay", bg=self.colors["bg"], fg=self.colors["blue"],
                 font=("Arial", 25, "bold")).pack(side="left")
        tk.Label(top, text="돈을 벌고, 투자하고, 성장하는 게임", bg=self.colors["bg"], fg="#d28cff",
                 font=("Arial", 11)).pack(side="left", padx=16, pady=(9, 0))
        tk.Label(top, text="가상 화폐 IA · 실제 돈 없음", bg=self.colors["bg"], fg="#ffbd69",
                 font=("Arial", 9)).pack(side="right", pady=(12, 0))

        status = tk.Frame(self, bg=self.colors["panel"], padx=18, pady=14,
                          highlightbackground=self.colors["line"], highlightthickness=1)
        status.pack(fill="x", padx=24, pady=(0, 16))
        self.name_label = tk.Label(status, bg=self.colors["panel"], fg=self.colors["text"], font=("Arial", 12, "bold"))
        self.name_label.pack(side="left", padx=(0, 25))
        self.cash_label = tk.Label(status, bg=self.colors["panel"], fg=self.colors["blue"], font=("Arial", 16, "bold"))
        self.cash_label.pack(side="left", padx=10)
        self.energy_label = tk.Label(status, bg=self.colors["panel"], fg=self.colors["text"], font=("Arial", 11, "bold"))
        self.energy_label.pack(side="left", padx=20)
        self.day_label = tk.Label(status, bg=self.colors["panel"], fg=self.colors["muted"], font=("Arial", 10))
        self.day_label.pack(side="right", padx=8)

        columns = tk.Frame(self, bg=self.colors["bg"])
        columns.pack(fill="both", expand=True, padx=24)
        columns.grid_columnconfigure(0, weight=3, uniform="col")
        columns.grid_columnconfigure(1, weight=2, uniform="col")
        columns.grid_rowconfigure(0, weight=1)

        left = self.panel(columns, "💼  돈 버는 활동")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.action_button(left, "동네 아르바이트", "체력 2 · 보통 수입", self.work)
        self.action_button(left, "배달 미션", "체력 2 · 성공 보너스", self.delivery)
        self.action_button(left, "코딩 의뢰", "체력 3 · 계산 문제 도전", self.coding)
        self.action_button(left, "지식 퀴즈", "체력 1 · 정답 상금", self.quiz)
        self.action_button(left, "재활용품 모으기", "체력 2 · 작은 보물 찾기", self.collect)
        self.action_button(left, "F키 정확히 100번", "체력 4 · 제한 시간 미션", self.start_f_mission)
        self.make_button(left, "🌙  휴식하고 다음 날로", self.rest).pack(fill="x", padx=14, pady=(10, 14))

        right = self.panel(columns, "📈  투자와 상점")
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.action_button(right, "투자하기", "안전 · 기술 · 우주 신기술", self.invest)
        self.action_button(right, "도박", "3개 중 1개는 5배 · 나머지는 전액 손실", self.gamble)
        self.action_button(right, "일반 상점", "일 능률과 체력을 올려요", self.open_general_shop)
        self.action_button(right, "수상한 비밀 시장", "비싼 상품 · 실제 사기 확률 2%", self.open_secret_shop)
        self.bonus_label = tk.Label(right, bg=right.panel_bg, fg=self.colors["muted"],
                                    justify="left", anchor="w", font=("Arial", 10), wraplength=280)
        self.bonus_label.pack(fill="x", padx=16, pady=(18, 8))

        log_frame = self.panel(self, "📜  게임 소식")
        log_frame.pack(fill="both", padx=24, pady=16)
        self.history = tk.Text(log_frame, height=8, bg="#091321", fg=self.colors["text"],
                               insertbackground="white", relief="flat", wrap="word",
                               font=("Arial", 10), padx=12, pady=8, state="disabled")
        self.history.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def panel(self, parent, title):
        palette = [("#101b2d", "#51d9ff"), ("#1b1730", "#d28cff"), ("#102622", "#64e3bd")]
        panel_bg, title_color = palette[self.panel_color_index % len(palette)]
        self.panel_color_index += 1
        frame = tk.Frame(parent, bg=panel_bg, highlightbackground=self.colors["line"], highlightthickness=1)
        frame.panel_bg = panel_bg
        tk.Label(frame, text=title, bg=panel_bg, fg=title_color,
                 font=("Arial", 13, "bold")).pack(anchor="w", padx=16, pady=14)
        return frame

    def action_button(self, parent, title, detail, command):
        button = self.make_button(parent, title + "\n" + detail, command)
        button.configure(justify="left", anchor="w")
        button.pack(fill="x", padx=12, pady=5)

    def log(self, message):
        self.history.configure(state="normal")
        self.history.insert("end", "• " + message + "\n")
        self.history.see("end")
        self.history.configure(state="disabled")

    def refresh_status(self):
        p = self.player
        self.name_label.configure(text=f"👤  {p['name']}  ·  능률 x{p['work_bonus']:.1f}")
        self.cash_label.configure(text=f"💰  {money(p['cash'])}")
        self.energy_label.configure(text=f"⚡ 체력 {p['energy']}/{p['max_energy']}")
        self.day_label.configure(text=f"{p['day']}일 차  ·  투자 감각 +{p['invest_bonus']}%p")
        owned = {"work": "작업 도구", "computer": "노트북", "energy": "도시락", "invest": "투자 공부책",
                 "factory": "코인 공장", "suit": "만능 작업복", "legend_pc": "투자 컴퓨터"}
        items = [label for key, label in owned.items() if key in p["owned"]]
        self.bonus_label.configure(text="보유 아이템\n" + (" · ".join(items) if items else "아직 없어요. 상점에서 장비를 마련해 보세요!"))

    def enough_energy(self, amount):
        if self.player["energy"] < amount:
            messagebox.showinfo("체력 부족", "체력이 부족해요. 휴식 버튼을 눌러 다음 날로 넘어가세요.", parent=self)
            return False
        self.player["energy"] -= amount
        return True

    def paid(self, amount, message):
        self.player["cash"] += amount
        self.log(f"{message}  +{money(amount)}")
        self.refresh_status()

    def work(self):
        if not self.enough_energy(2): return
        earned = int(random.randint(65, 115) * self.player["work_bonus"])
        self.paid(earned, "아르바이트를 마쳤어요!")

    def delivery(self):
        if not self.enough_energy(2): return
        if random.random() < .72:
            earned = int(random.randint(120, 300) * self.player["work_bonus"])
            message = "배달 성공! 보너스를 받았어요."
        else:
            earned = random.randint(15, 55)
            message = "길을 헤맸지만 작은 보수를 받았어요."
        self.paid(earned, message)

    def coding(self):
        if not self.enough_energy(3): return
        a, b = random.randint(8, 24), random.randint(3, 12)
        sign = random.choice(("+", "-", "×"))
        answer = a + b if sign == "+" else a - b if sign == "-" else a * b
        guess = simpledialog.askstring("코딩 의뢰", f"계산 문제를 풀어 의뢰를 완료해요!\n\n{a} {sign} {b} = ?", parent=self)
        if guess is None:
            self.player["energy"] += 3
            self.refresh_status()
            return
        if guess.strip() == str(answer):
            self.paid(int(random.randint(450, 700) * self.player["work_bonus"]), "정답! 코딩 의뢰를 완료했어요.")
        else:
            self.paid(35, f"아쉽지만 참가비를 받았어요. 정답은 {answer}였어요.")

    def quiz(self):
        if not self.enough_energy(1): return
        question, answer = random.choice([
            ("파이썬에서 글자를 출력하는 명령은?", "print"),
            ("한 시간은 몇 분일까요?", "60"),
            ("물의 화학식은?", "H2O"),
            ("삼각형의 변은 몇 개일까요?", "3"),
        ])
        guess = simpledialog.askstring("지식 퀴즈", question, parent=self)
        if guess is None:
            self.player["energy"] += 1
            self.refresh_status()
            return
        if guess.strip().lower() == answer.lower():
            self.paid(int(180 * self.player["work_bonus"]), "퀴즈 정답! 상금을 받았어요.")
        else:
            self.paid(10, f"참가비를 받았어요. 정답은 {answer}예요.")

    def collect(self):
        if not self.enough_energy(2): return
        earned = int(random.randint(20, 180) * self.player["work_bonus"])
        self.paid(earned, "재활용품을 모아 팔았어요.")

    def start_f_mission(self):
        """20초 안에 F 키를 정확히 100번 눌러 보상을 받는 미션입니다."""
        if not self.enough_energy(4): return
        window = self.dialog("집중력 미션: F 키 100번", "20초 안에 키보드의 F 키를 정확히 100번 누르세요.\n다른 키는 횟수에 포함되지 않아요.")
        count = {"value": 0, "time": 20, "done": False}
        count_label = tk.Label(window, text="0 / 100", bg=window.cget("bg"), fg="#64e3bd", font=("Arial", 28, "bold"))
        count_label.pack(pady=(0, 6))
        time_label = tk.Label(window, text="남은 시간: 20초", bg=window.cget("bg"), fg="#ffbd69", font=("Arial", 12, "bold"))
        time_label.pack(pady=(0, 14))
        self.make_button(window, "여기를 클릭한 다음 F 키를 눌러요", lambda: window.focus_force()).pack(padx=14, pady=(0, 14))

        def finish(success, message):
            if count["done"]: return
            count["done"] = True
            if success:
                earned = int(900 * self.player["work_bonus"])
                self.player["cash"] += earned
                self.log(f"F키 미션 성공! {money(earned)} 획득!")
                self.refresh_status()
                messagebox.showinfo("미션 성공!", f"정확히 100번 눌렀어요!\n보상: {money(earned)}", parent=self)
            else:
                self.log("F키 미션 실패. 다음에 다시 도전해 봐요.")
                messagebox.showinfo("미션 실패", message, parent=self)
            if window.winfo_exists(): window.destroy()

        def on_key(event):
            if count["done"] or event.keysym.lower() != "f": return
            count["value"] += 1
            count_label.configure(text=f"{count['value']} / 100")
            if count["value"] == 100:
                finish(True, "성공!")
            elif count["value"] > 100:
                finish(False, "100번을 넘게 눌렀어요. 횟수를 정확히 맞춰야 합니다.")

        def tick():
            if count["done"] or not window.winfo_exists(): return
            count["time"] -= 1
            time_label.configure(text=f"남은 시간: {count['time']}초")
            if count["time"] <= 0:
                finish(False, f"시간이 끝났어요. {count['value']}번 눌렀습니다.")
            else:
                window.after(1000, tick)

        window.bind("<KeyPress>", on_key)
        window.protocol("WM_DELETE_WINDOW", lambda: finish(False, "미션을 중단했어요."))
        window.after(1000, tick)
        window.focus_force()

    def rest(self):
        p = self.player
        recovered = p["max_energy"] - p["energy"]
        p["day"] += 1
        p["energy"] = p["max_energy"]
        message = f"하루 쉬었어요. 체력 {recovered} 회복!"
        if p["factory"]:
            p["cash"] += 500000
            message += " 코인 공장 수입 +500,000 IA!"
        self.log(message)
        self.refresh_status()

    def invest(self):
        p = self.player
        options = {
            "안전 펀드": (70, 1.4, .5),
            "기술 주식": (40, 2, 0),
            "우주 신기술": (15, 5, 0),
        }
        window = self.dialog("투자하기", "투자할 종류를 고르세요. 성공하면 원금 포함 표시된 배수만큼 돌려받아요.")
        for name, (chance, multiplier, loss) in options.items():
            text = f"{name}  |  성공 {min(95, chance+p['invest_bonus'])}% · 성공 시 {multiplier}배"
            if loss == 0: text += " · 실패 시 전액 손실"
            else: text += " · 실패 시 절반 손실"
            self.make_button(window, text, lambda n=name: self.ask_invest_amount(n, options[n])).pack(fill="x", padx=14, pady=5)

    def ask_invest_amount(self, name, setting):
        amount = simpledialog.askinteger("투자 금액", f"{name}\n얼마를 투자할까요? (보유 {money(self.player['cash'])})",
                                         minvalue=1, maxvalue=self.player["cash"], parent=self)
        if amount is None: return
        chance, multiplier, loss = setting
        chance = min(95, chance + self.player["invest_bonus"])
        self.player["cash"] -= amount
        if random.randint(1, 100) <= chance:
            returned = int(amount * multiplier)
            self.player["cash"] += returned
            self.log(f"{name} 투자 성공! 원금 포함 {money(returned)}을 돌려받았어요.")
        else:
            returned = int(amount * loss)
            self.player["cash"] += returned
            self.log(f"{name} 투자 실패... {money(returned)}만 남았어요.")
        self.refresh_status()

    def gamble(self):
        cash = self.player["cash"]
        if cash < 1:
            messagebox.showinfo("돈이 없어요", "걸 수 있는 돈이 없어요.", parent=self)
            return
        amount = simpledialog.askinteger("도박 금액", f"세 선택지 중 하나만 맞아요.\n맞히면 건 돈의 5배, 틀리면 전부 잃습니다.\n얼마를 걸까요? (보유 {money(cash)})", minvalue=1, maxvalue=cash, parent=self)
        if amount is None: return
        if not messagebox.askyesno("도박 확인", f"{money(amount)}을 걸까요?\n3개 중 1개만 5배를 얻고, 나머지는 전부 잃어요.\n가상 화폐 IA만 사용합니다.", parent=self): return
        self.player["cash"] -= amount
        winning_choice = random.randrange(3)
        window = self.dialog("도박", "세 개 중 하나를 골라 보세요.\n한 개는 5배, 나머지는 꽝입니다.")

        def choose(index):
            window.destroy()
            if index == winning_choice:
                prize = amount * 5
                self.player["cash"] += prize
                self.log(f"도박 성공! 5배 당첨으로 {money(prize)} 획득!")
                messagebox.showinfo("5배 당첨!", f"정답을 골랐어요!\n{money(prize)}을 받았습니다.", parent=self)
            else:
                self.log(f"도박 실패. 건 돈 {money(amount)}을 모두 잃었어요.")
                messagebox.showinfo("꽝!", f"아쉽게도 꽝이에요.\n건 돈 {money(amount)}을 모두 잃었습니다.", parent=self)
            self.refresh_status()

        def cancel_choice():
            self.player["cash"] += amount
            self.log("도박 선택을 취소했어요. 건 돈을 돌려받았습니다.")
            self.refresh_status()
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", cancel_choice)

        for index, label in enumerate(("선택지 1  ✦", "선택지 2  ◆", "선택지 3  ★")):
            self.make_button(window, label, lambda i=index: choose(i)).pack(fill="x", padx=14, pady=6)

    def dialog(self, title, description):
        window = tk.Toplevel(self)
        window.title(title)
        window.configure(bg=self.colors["panel"])
        window.resizable(False, False)
        window.transient(self)
        tk.Label(window, text=description, bg=self.colors["panel"], fg=self.colors["text"],
                 justify="left", wraplength=420, padx=18, pady=16).pack(fill="x")
        return window

    def open_general_shop(self):
        products = [
            ("튼튼한 작업 도구", 500, "활동 수입 x1.4", "work"),
            ("든든한 도시락", 350, "최대 체력 +2, 체력 모두 회복", "energy"),
            ("투자 공부책", 900, "투자 성공 확률 +5%p", "invest"),
            ("작업용 노트북", 1800, "일 능률 x2", "computer"),
        ]
        window = self.dialog("일반 상점", "모든 효과는 게임 안에서만 적용됩니다.")
        for name, price, effect, kind in products:
            self.make_button(window, f"{name}  ·  {money(price)}\n{effect}",
                             lambda product=(name, price, kind): self.buy_general(product)).pack(fill="x", padx=14, pady=5)

    def buy_general(self, product):
        name, price, kind = product
        p = self.player
        if kind in p["owned"]:
            messagebox.showinfo("이미 구매했어요", "이 아이템은 이미 가지고 있어요.", parent=self)
            return
        if p["cash"] < price:
            messagebox.showinfo("돈이 부족해요", "먼저 돈을 모아 주세요.", parent=self)
            return
        p["cash"] -= price
        p["owned"].add(kind)
        if kind == "work": p["work_bonus"] *= 1.4
        elif kind == "energy": p["max_energy"] += 2; p["energy"] = p["max_energy"]
        elif kind == "invest": p["invest_bonus"] += 5
        elif kind == "computer": p["work_bonus"] *= 2
        self.log(f"일반 상점에서 {name}을 구매했어요.")
        self.refresh_status()

    def open_secret_shop(self):
        products = [
            ("황금빛 자동 코인 공장", 5000000, "휴식할 때마다 500,000 IA", "factory"),
            ("초고속 만능 작업복", 15000000, "모든 일 수입 x50", "suit"),
            ("전설의 투자 컴퓨터", 40000000, "투자 성공 확률 +60%p", "legend_pc"),
        ]
        window = self.dialog("수상한 비밀 시장", "상인의 안내: '사기 확률은 70% 정도예요!'\n가끔 표시 가격보다 2~5배 더 청구할 수도 있대요. 상품의 효과는 엄청나지만 조심하세요.")
        for name, price, effect, kind in products:
            self.make_button(window, f"{name}  ·  {money(price)}\n{effect}",
                             lambda product=(name, price, kind): self.buy_secret(product)).pack(fill="x", padx=14, pady=5)

    def buy_secret(self, product):
        name, price, kind = product
        p = self.player
        if kind in p["owned"]:
            messagebox.showinfo("이미 가지고 있어요", "이 아이템은 이미 가지고 있어요.", parent=self)
            return
        if p["cash"] < price:
            messagebox.showinfo("돈이 부족해요", f"필요한 금액은 {money(price)}입니다.", parent=self)
            return
        if not messagebox.askyesno("구매 확인", f"{name}\n표시 가격: {money(price)}\n상인이 추가 요금을 요구할 수도 있어요.\n구매할까요?", parent=self): return

        # 상인은 절반의 확률로 표시 가격의 2~5배를 받아요.
        final_price = price
        if random.random() < 0.5:
            multiplier = random.randint(2, 5)
            final_price = price * multiplier
            if p["cash"] < final_price:
                self.log(f"상인이 {money(final_price)}을 요구했지만 돈이 부족해 거래가 취소됐어요.")
                messagebox.showinfo("추가 요금이 너무 비싸요", f"상인이 표시 가격의 {multiplier}배인 {money(final_price)}을 요구했어요.\n보유 IA가 부족해 거래가 취소됐습니다.", parent=self)
                return
            messagebox.showwarning("추가 요금 발생", f"상인이 가격을 올렸어요!\n표시 가격의 {multiplier}배: {money(final_price)}", parent=self)

        p["cash"] -= final_price
        if random.randint(1, 100) <= 98:
            self.log(f"비밀 시장에서 사기를 당했어요. {money(final_price)}을 잃었습니다.")
            messagebox.showwarning("사기당했어요!", f"상인이 돈을 받고 도망갔어요.\n잃은 돈: {money(final_price)}\n상인이 말한 확률과 달리 실제 사기 확률은 98%예요.", parent=self)
        else:
            p["owned"].add(kind)
            if kind == "factory": p["factory"] = True
            elif kind == "suit": p["work_bonus"] *= 50
            elif kind == "legend_pc": p["invest_bonus"] += 60
            self.log(f"비밀 시장에서 {name}을 얻었어요! 강력한 효과가 적용됩니다.")
        self.refresh_status()


if __name__ == "__main__":
    game = IAplay()
    game.mainloop()
