"""IAplay - 돈을 벌고, 투자하고, 더 큰 목표에 도전하는 콘솔 게임.

실제 돈은 사용하지 않습니다. 게임 속 돈으로만 플레이하세요!
실행: python a.py
"""

import random


def money(amount):
    """숫자를 보기 쉬운 원 단위 글자로 바꿉니다."""
    return f"{amount:,.0f}원"


def ask_number(message, minimum=1, maximum=None):
    """숫자를 입력받고, 잘못 입력해도 게임이 멈추지 않게 합니다."""
    while True:
        answer = input(message).strip()
        if answer.lower() in ("q", "취소"):
            return None
        try:
            number = int(answer.replace(",", ""))
        except ValueError:
            print("숫자를 입력해 주세요. 취소하려면 q를 입력하세요.")
            continue
        if number < minimum:
            print(f"{minimum} 이상 입력해 주세요.")
        elif maximum is not None and number > maximum:
            print(f"최대 {maximum:,}까지 입력할 수 있어요.")
        else:
            return number


def show_status(player):
    print("\n" + "=" * 52)
    print(f"  IAplay  |  {player['name']}  |  {player['day']}일 차")
    print(f"  보유 돈: {money(player['cash'])}   체력: {player['energy']}/{player['max_energy']}")
    print(f"  일 능률: x{player['work_bonus']:.1f}   투자 감각: +{player['invest_bonus']}%p")
    print("=" * 52)


def spend_energy(player, amount):
    if player["energy"] < amount:
        print("체력이 부족해요. 먼저 휴식해서 하루를 마무리하세요.")
        return False
    player["energy"] -= amount
    return True


def earn_work(player):
    print("\n[1] 동네 아르바이트")
    print("힘들지만 확실하게 돈을 벌어요. 체력 2를 사용합니다.")
    if not spend_energy(player, 2):
        return
    earned = int(random.randint(65, 115) * player["work_bonus"])
    player["cash"] += earned
    print(f"열심히 일했어요! {money(earned)}을 벌었습니다.")


def earn_delivery(player):
    print("\n[2] 배달 미션")
    print("빠르게 배달하면 보너스! 가끔 길을 헤매서 보수가 적어요. 체력 2를 사용합니다.")
    if not spend_energy(player, 2):
        return
    if random.random() < 0.72:
        earned = int(random.randint(120, 300) * player["work_bonus"])
        print(f"배달 성공! 보너스를 포함해 {money(earned)}을 받았어요.")
    else:
        earned = random.randint(15, 55)
        print(f"길을 조금 헤맸어요. 그래도 {money(earned)}을 받았습니다.")
    player["cash"] += earned


def earn_coding(player):
    print("\n[3] 코딩 의뢰")
    print("계산 문제를 풀면 큰 보수! 틀려도 작은 참가비를 받아요. 체력 3을 사용합니다.")
    if not spend_energy(player, 3):
        return
    first, second = random.randint(8, 24), random.randint(3, 12)
    operation = random.choice(("+", "-", "×"))
    answer = first + second if operation == "+" else first - second if operation == "-" else first * second
    guess = input(f"\n  {first} {operation} {second} = ?  답: ").strip()
    if guess == str(answer):
        earned = int(random.randint(450, 700) * player["work_bonus"])
        print(f"정답! 의뢰를 완료해 {money(earned)}을 벌었어요.")
    else:
        earned = 35
        print(f"아쉽지만 괜찮아요. 정답은 {answer}였어요. 참가비 {money(earned)}을 받았습니다.")
    player["cash"] += earned


def earn_quiz(player):
    print("\n[4] 지식 퀴즈")
    questions = [
        ("파이썬에서 화면에 글자를 보여주는 명령은?", "print"),
        ("한 시간은 몇 분일까요?", "60"),
        ("물의 화학식은? (영어 대문자)", "H2O"),
        ("삼각형의 변은 몇 개일까요?", "3"),
    ]
    question, answer = random.choice(questions)
    if not spend_energy(player, 1):
        return
    guess = input(f"  {question} ").strip().lower()
    if guess == answer.lower():
        earned = int(180 * player["work_bonus"])
        print(f"정답! 상금 {money(earned)}을 받았어요.")
    else:
        earned = 10
        print(f"아쉽다! 정답은 {answer}예요. 참가비 {money(earned)}을 받았습니다.")
    player["cash"] += earned


def earn_collect(player):
    print("\n[5] 재활용품 모으기")
    print("동네를 돌아다녀 쓸 만한 물건을 찾아요. 체력 2를 사용합니다.")
    if not spend_energy(player, 2):
        return
    found = random.randint(20, 180)
    earned = int(found * player["work_bonus"])
    player["cash"] += earned
    print(f"물건을 팔아 {money(earned)}을 벌었어요.")


def invest(player):
    print("\n[6] 투자하기")
    print("게임 속 가상 투자예요. 투자금을 전부 잃을 수도 있으니 신중하게 골라요.")
    print("  1. 안전 펀드: 70% 확률로 1.4배, 나머지는 투자금의 절반 손실")
    print("  2. 기술 주식: 40% 확률로 2배, 나머지는 투자금 전부 손실")
    print("  3. 우주 신기술: 15% 확률로 5배, 나머지는 전부 손실")
    choice = input("선택 (1~3, 취소는 q): ").strip()
    settings = {"1": (70, 1.4, 0.5), "2": (40, 2, 0), "3": (15, 5, 0)}
    if choice not in settings:
        print("투자를 취소했어요.")
        return
    if player["cash"] <= 0:
        print("투자할 돈이 없어요.")
        return
    amount = ask_number(f"얼마를 투자할까요? (보유 {player['cash']:,}, q로 취소): ", 1, player["cash"])
    if amount is None:
        return
    chance, multiplier, loss_back = settings[choice]
    chance = min(95, chance + player["invest_bonus"])
    player["cash"] -= amount
    if random.randint(1, 100) <= chance:
        returned = int(amount * multiplier)
        player["cash"] += returned
        print(f"투자 성공! 원금 포함 {money(returned)}을 돌려받았어요.")
    else:
        returned = int(amount * loss_back)
        player["cash"] += returned
        print(f"투자 실패... {money(returned)}만 남았어요.")


def gamble(player):
    print("\n[7] 행운의 10배 도전")
    print("게임 속 가상 화폐만 사용합니다. 당첨 확률 2%, 꽝이면 건 돈을 모두 잃어요.")
    if player["cash"] <= 0:
        print("걸 돈이 없어요.")
        return
    amount = ask_number(f"얼마를 걸까요? (보유 {player['cash']:,}, q로 취소): ", 1, player["cash"])
    if amount is None:
        return
    player["cash"] -= amount
    if random.randint(1, 100) <= 2:
        prize = amount * 10
        player["cash"] += prize
        print(f"대박! 2% 행운이 왔어요. {money(prize)}을 받았습니다!")
    else:
        print(f"꽝! 건 돈 {money(amount)}을 잃었어요.")


def general_shop(player):
    items = {
        "1": ("튼튼한 작업 도구", 500, "일과 활동 수입이 1.4배가 돼요.", "work"),
        "2": ("든든한 도시락", 350, "최대 체력이 2 늘고 체력을 모두 회복해요.", "energy"),
        "3": ("투자 공부책", 900, "투자 성공 확률이 5%p 올라가요.", "invest"),
        "4": ("작업용 노트북", 1800, "일 능률이 2배가 돼요.", "computer"),
    }
    print("\n[일반 상점] 차근차근 도움이 되는 물건")
    for key, (name, price, description, _) in items.items():
        print(f"  {key}. {name} - {money(price)} | {description}")
    choice = input("구매할 번호 (취소는 q): ").strip()
    if choice not in items:
        print("구매를 취소했어요.")
        return
    name, price, _, kind = items[choice]
    if player["cash"] < price:
        print("돈이 부족해요. 여러 활동으로 모아 보세요.")
        return
    if kind in player["owned"]:
        print("이미 가지고 있어요.")
        return
    player["cash"] -= price
    player["owned"].add(kind)
    if kind == "work":
        player["work_bonus"] *= 1.4
    elif kind == "energy":
        player["max_energy"] += 2
        player["energy"] = player["max_energy"]
    elif kind == "invest":
        player["invest_bonus"] += 5
    elif kind == "computer":
        player["work_bonus"] *= 2
    print(f"{name} 구매 완료!")


def strange_market(player):
    goods = {
        "1": ("황금빛 자동 코인 공장", 50000, "휴식할 때마다 8,000원을 벌어요.", "factory"),
        "2": ("초고속 만능 작업복", 120000, "모든 일 수입이 8배가 돼요.", "suit"),
        "3": ("전설의 투자 컴퓨터", 300000, "투자 성공 확률이 25%p 올라가요.", "legend_pc"),
    }
    print("\n[수상한 비밀 시장] 가격도 효과도 엄청난 물건들")
    print("상인의 광고: '사기 위험 90%!' 음... 정말일까요? 직접 알아보세요.")
    for key, (name, price, description, _) in goods.items():
        print(f"  {key}. {name} - {money(price)} | {description}")
    print("※ 비밀 시장 상품은 실제 가치가 크지만, 구매할 때 2% 확률로 사기를 당할 수 있어요.")
    choice = input("살 물건 (취소는 q): ").strip()
    if choice not in goods:
        print("시장을 나왔어요.")
        return
    name, price, _, kind = goods[choice]
    if kind in player["owned"]:
        print("이미 가지고 있어요.")
        return
    if player["cash"] < price:
        print("돈이 부족해요. 큰돈을 모은 뒤 다시 와보세요.")
        return
    confirm = input(f"{money(price)}을 내고 구매할까요? (y/n): ").strip().lower()
    if confirm != "y":
        print("구매를 취소했어요.")
        return
    player["cash"] -= price
    if random.randint(1, 100) <= 2:
        print("상인이 돈을 받고 도망갔어요! 사기당했습니다! (실제 확률 2%)")
        return
    player["owned"].add(kind)
    if kind == "factory":
        player["factory"] = True
    elif kind == "suit":
        player["work_bonus"] *= 8
    elif kind == "legend_pc":
        player["invest_bonus"] += 25
    print(f"{name} 획득! 효과가 적용됐어요. 광고가 과장이었나 봐요!")


def rest(player):
    recovered = player["max_energy"] - player["energy"]
    player["day"] += 1
    player["energy"] = player["max_energy"]
    income = 8000 if player["factory"] else 0
    player["cash"] += income
    print(f"하루 푹 쉬었어요. 체력 {recovered} 회복!")
    if income:
        print(f"자동 코인 공장이 쉬는 동안 {money(income)}을 벌었어요.")


def main():
    print("""
╔══════════════════════════════════════════════╗
║   ██╗ █████╗ ██████╗ ██╗      █████╗ ██╗   ║
║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗██║   ║
║   ██║███████║██████╔╝██║     ███████║██║   ║
║   ██║██╔══██║██╔═══╝ ██║     ██╔══██║██║   ║
║   ██║██║  ██║██║     ███████╗██║  ██║██║   ║
║   ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝   ║
║       돈 벌고 투자하는 생활 시뮬레이션       ║
╚══════════════════════════════════════════════╝
실제 돈은 전혀 사용하지 않는 가상 경제 게임입니다.
""")
    name = input("플레이어 이름을 입력하세요: ").strip() or "플레이어"
    player = {
        "name": name, "cash": 300, "energy": 10, "max_energy": 10,
        "work_bonus": 1.0, "invest_bonus": 0, "day": 1,
        "owned": set(), "factory": False,
    }

    while True:
        show_status(player)
        print("무엇을 할까요?")
        print("  1. 동네 아르바이트       2. 배달 미션")
        print("  3. 코딩 의뢰             4. 지식 퀴즈")
        print("  5. 재활용품 모으기       6. 투자하기")
        print("  7. 행운의 10배 도전      8. 일반 상점")
        print("  9. 수상한 비밀 시장      10. 휴식하고 다음 날로")
        print("  0. 게임 종료")
        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            earn_work(player)
        elif choice == "2":
            earn_delivery(player)
        elif choice == "3":
            earn_coding(player)
        elif choice == "4":
            earn_quiz(player)
        elif choice == "5":
            earn_collect(player)
        elif choice == "6":
            invest(player)
        elif choice == "7":
            gamble(player)
        elif choice == "8":
            general_shop(player)
        elif choice == "9":
            strange_market(player)
        elif choice == "10":
            rest(player)
        elif choice == "0":
            print(f"\n게임을 종료합니다. {name}의 마지막 보유액은 {money(player['cash'])}입니다. 또 만나요!")
            break
        else:
            print("메뉴에 있는 번호를 입력해 주세요.")


if __name__ == "__main__":
    main()
