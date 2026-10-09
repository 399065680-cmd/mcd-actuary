"""
McActuary Core Algorithms
=========================
辅助算法模块：优惠券组合优化、抽奖期望值计算、积分性价比排行。

这些算法在 SKILL.md 的决策流程中被 AI 引用，用于支撑跨模块价值决策。
MCP 工具返回的原始数据经过这些算法处理后，输出可读的决策建议。
"""

import itertools
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CouponInfo:
    coupon_id: str
    title: str
    discount_amount: float = 0.0
    discount_rate: float = 0.0
    min_spend: float = 0.0
    expire_days: int = 999


@dataclass
class MealItem:
    meal_code: str
    name: str
    price: float


@dataclass
class PriceResult:
    """calculate-price MCP Tool 返回的结果"""
    original_price: float
    discount: float
    delivery_fee: float
    final_price: float
    applied_coupons: list[str] = field(default_factory=list)


@dataclass
class MallProduct:
    product_id: str
    name: str
    points_cost: int
    estimated_value: float  # estimated cash value


@dataclass
class LotteryPrize:
    name: str
    value: float
    probability: float  # 0.0 - 1.0


# ============================================================
# 1. Coupon Combination Optimizer
# ============================================================

def find_best_coupon_combination(
    items: list[MealItem],
    coupons: list[CouponInfo],
    calculate_price_fn,
) -> PriceResult:
    """
    优惠券组合优化器。

    遍历所有可能的优惠券组合，调用 calculate-price MCP Tool
    计算每组的价格，返回最优（最低总价）方案。

    算法：
      - 生成优惠券的所有子集（含空集 = 原价）
      - 过滤不满足最低消费的子集
      - 对每个有效子集调用 calculate-price
      - 返回 final_price 最小的结果

    Args:
        items: 用户想购买的餐品列表
        coupons: 用户持有的优惠券列表
        calculate_price_fn: 回调函数，模拟 MCP calculate-price Tool
            签名: (items, coupon_ids) -> PriceResult

    Returns:
        最优价格方案 PriceResult
    """
    original_total = sum(item.price for item in items)

    best_result = PriceResult(
        original_price=original_total,
        discount=0,
        delivery_fee=0,
        final_price=original_total,
        applied_coupons=[],
    )

    n = len(coupons)

    for r in range(1, n + 1):
        for combo in itertools.combinations(coupons, r):
            combo_min_spend = max(c.min_spend for c in combo)
            if original_total < combo_min_spend:
                continue

            coupon_ids = [c.coupon_id for c in combo]
            result = calculate_price_fn(items, coupon_ids)

            if result and result.final_price < best_result.final_price:
                best_result = result

    return best_result


def format_savings_report(result: PriceResult) -> str:
    """格式化省钱报告"""
    savings = result.original_price - result.final_price
    rate = (savings / result.original_price * 100) if result.original_price > 0 else 0

    lines = [
        f"Original price: ¥{result.original_price:.2f}",
        f"Coupons applied: {', '.join(result.applied_coupons) if result.applied_coupons else 'None'}",
        f"Discount: ¥{result.discount:.2f}",
        f"Delivery fee: ¥{result.delivery_fee:.2f}",
        f"Final price: ¥{result.final_price:.2f}",
        f"You saved: ¥{savings:.2f} ({rate:.0f}%)",
    ]
    return "\n".join(lines)


# ============================================================
# 2. Lottery Expected Value Calculator
# ============================================================

def calculate_lottery_ev(
    prizes: list[LotteryPrize],
    cost_per_draw: float,
) -> dict:
    """
    计算抽奖期望值（Expected Value）。

    EV = Σ(Prize_Value × Probability) − Cost_Per_Draw

    Args:
        prizes: 奖品列表（含价值和概率）
        cost_per_draw: 每次抽奖的成本（积分等价价值）

    Returns:
        dict with EV, recommendation, breakdown
    """
    total_ev = sum(p.value * p.probability for p in prizes)
    net_ev = total_ev - cost_per_draw

    if net_ev > 0:
        recommendation = (
            f"Lottery EV = ¥{net_ev:.2f} > 0. "
            f"Statistically profitable, but variance is high. "
            f"Recommend small-scale attempts only."
        )
        should_draw = True
    elif net_ev == 0:
        recommendation = (
            f"Lottery EV = ¥0.00. Break-even. "
            f"Only if you enjoy the thrill."
        )
        should_draw = False
    else:
        recommendation = (
            f"Lottery EV = ¥{net_ev:.2f} < 0. "
            f"Not worth it. Recommend spending points on mall redemption instead."
        )
        should_draw = False

    breakdown = []
    for p in prizes:
        contribution = p.value * p.probability
        breakdown.append(
            f"  {p.name}: ¥{p.value:.2f} × {p.probability*100:.1f}% = ¥{contribution:.2f}"
        )

    return {
        "gross_ev": round(total_ev, 2),
        "cost_per_draw": cost_per_draw,
        "net_ev": round(net_ev, 2),
        "should_draw": should_draw,
        "recommendation": recommendation,
        "breakdown": "\n".join(breakdown),
    }


# ============================================================
# 3. Points Value Ranker
# ============================================================

def rank_products_by_value(
    products: list[MallProduct],
    top_n: int = 3,
) -> list[dict]:
    """
    按积分性价比对商城商品排序。

    性价比 = 估算现金价值 / 所需积分

    Args:
        products: 商城商品列表
        top_n: 返回前 N 个

    Returns:
        排行榜列表，每项含 product, value_per_point, stars
    """
    ranked = []
    for product in products:
        if product.points_cost <= 0:
            continue
        vpp = product.estimated_value / product.points_cost

        if vpp >= 0.05:
            stars = 5
        elif vpp >= 0.03:
            stars = 4
        elif vpp >= 0.02:
            stars = 3
        elif vpp >= 0.01:
            stars = 2
        else:
            stars = 1

        ranked.append({
            "product": product,
            "value_per_point": round(vpp, 4),
            "estimated_value": product.estimated_value,
            "points_cost": product.points_cost,
            "stars": stars,
            "star_str": "*" * stars,
        })

    ranked.sort(key=lambda x: x["value_per_point"], reverse=True)
    return ranked[:top_n]


# ============================================================
# 4. Cross-Module Decision Engine
# ============================================================

@dataclass
class DecisionOption:
    """一个购买方案"""
    label: str
    method: str  # "coupon", "points", "lottery", "original"
    cost: float  # monetary cost
    points_cost: int = 0
    savings: float = 0.0
    risk_note: str = ""
    is_recommended: bool = False


def make_cross_module_decision(
    coupon_option: Optional[PriceResult],
    points_option: Optional[MallProduct],
    lottery_ev: Optional[dict],
    user_points: int,
    expiring_points: int = 0,
    expiring_days: int = 999,
) -> list[DecisionOption]:
    """
    跨模块决策引擎。

    综合优惠券、积分兑换、抽奖三种方案，推荐最优。

    推荐规则：
      1. 积分即将过期 + 可兑换目标 -> 推荐积分兑换
      2. 优惠券折扣 > 30% -> 推荐优惠券
      3. 抽奖 EV > 0 且积分充足 -> 可建议小额尝试
      4. 以上都不满足 -> 推荐原价或换其他餐品
    """
    options: list[DecisionOption] = []

    if coupon_option:
        savings = coupon_option.original_price - coupon_option.final_price
        discount_rate = savings / coupon_option.original_price if coupon_option.original_price > 0 else 0
        options.append(DecisionOption(
            label="Plan A: Buy with coupon",
            method="coupon",
            cost=coupon_option.final_price,
            savings=savings,
            risk_note=f"Discount: {discount_rate*100:.0f}%",
        ))

    if points_option:
        options.append(DecisionOption(
            label="Plan B: Redeem with points",
            method="points",
            cost=0.0,
            points_cost=points_option.points_cost,
            risk_note=f"Needs {points_option.points_cost} points, you have {user_points}",
        ))

    if lottery_ev:
        options.append(DecisionOption(
            label="Plan C: Try lottery",
            method="lottery",
            cost=0.0,
            points_cost=int(lottery_ev.get("cost_per_draw", 0)),
            risk_note=lottery_ev.get("recommendation", ""),
        ))

    decision_logic = decide_best(options, expiring_points, expiring_days, user_points)
    for opt in options:
        if opt.method == decision_logic:
            opt.is_recommended = True
            break

    if not any(o.is_recommended for o in options) and options:
        options[0].is_recommended = True

    return options


def decide_best(
    options: list[DecisionOption],
    expiring_points: int,
    expiring_days: int,
    user_points: int,
) -> str:
    """决策逻辑核心"""
    if expiring_points > 0 and expiring_days <= 7:
        for opt in options:
            if opt.method == "points" and opt.points_cost <= user_points:
                return "points"

    for opt in options:
        if opt.method == "coupon" and opt.savings > 0:
            original = opt.cost + opt.savings
            if opt.savings / original > 0.3:
                return "coupon"

    for opt in options:
        if opt.method == "lottery":
            ev_note = opt.risk_note
            if "profitable" in ev_note.lower():
                return "lottery"

    return "coupon" if any(o.method == "coupon" for o in options) else "points"


# ============================================================
# Demo / Self-Test
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("McActuary Calculator - Demo")
    print("=" * 50)

    # Demo 1: Coupon optimizer
    print("\n--- Coupon Combination Optimizer ---")
    items = [
        MealItem("BG001", "Big Mac", 25.0),
        MealItem("DR001", "Cola", 10.0),
    ]
    coupons = [
        CouponInfo("C1", "Minus 10", discount_amount=10, min_spend=20),
        CouponInfo("C2", "20% off", discount_rate=0.2, min_spend=0),
        CouponInfo("C3", "Minus 5", discount_amount=5, min_spend=15),
    ]

    def mock_calculate_price(items, coupon_ids):
        original = sum(i.price for i in items)
        discount = 0
        for cid in coupon_ids:
            c = next(x for x in coupons if x.coupon_id == cid)
            if c.discount_amount > 0:
                discount += c.discount_amount
            if c.discount_rate > 0:
                discount += original * c.discount_rate
        discount = min(discount, original)
        return PriceResult(
            original_price=original,
            discount=discount,
            delivery_fee=0,
            final_price=original - discount,
            applied_coupons=coupon_ids,
        )

    best = find_best_coupon_combination(items, coupons, mock_calculate_price)
    print(format_savings_report(best))

    # Demo 2: Lottery EV
    print("\n--- Lottery EV Calculator ---")
    prizes = [
        LotteryPrize("Big Mac voucher", 25.0, 0.02),
        LotteryPrize("Fries", 10.0, 0.05),
        LotteryPrize("Cola", 5.0, 0.10),
        LotteryPrize("Nothing", 0.0, 0.83),
    ]
    ev_result = calculate_lottery_ev(prizes, cost_per_draw=2.5)
    print(f"Gross EV: ¥{ev_result['gross_ev']}")
    print(f"Net EV: ¥{ev_result['net_ev']}")
    print(f"Recommendation: {ev_result['recommendation']}")
    print(f"Breakdown:\n{ev_result['breakdown']}")

    # Demo 3: Points value ranker
    print("\n--- Points Value Ranker ---")
    products = [
        MallProduct("P1", "Big Mac Voucher", 2000, 25.0),
        MallProduct("P2", "Fries Voucher", 800, 10.0),
        MallProduct("P3", "McFlurry Voucher", 1500, 12.0),
        MallProduct("P4", "Coffee Voucher", 500, 3.0),
    ]
    ranked = rank_products_by_value(products, top_n=3)
    for i, item in enumerate(ranked, 1):
        print(f"  {i}. {item['product'].name} - "
              f"{item['points_cost']} pts, "
              f"value ¥{item['estimated_value']}, "
              f"VPP ¥{item['value_per_point']}, "
              f"{item['star_str']}")

    # Demo 4: Cross-module decision
    print("\n--- Cross-Module Decision Engine ---")
    coupon_result = PriceResult(
        original_price=25.0, discount=10.0,
        delivery_fee=0, final_price=15.0, applied_coupons=["C1"]
    )
    points_product = MallProduct("P1", "Big Mac Voucher", 2000, 25.0)
    lottery_result = calculate_lottery_ev(prizes, cost_per_draw=2.5)

    decisions = make_cross_module_decision(
        coupon_option=coupon_result,
        points_option=points_product,
        lottery_ev=lottery_result,
        user_points=3500,
        expiring_points=500,
        expiring_days=3,
    )

    for opt in decisions:
        tag = " *** RECOMMENDED ***" if opt.is_recommended else ""
        print(f"  {opt.label}{tag}")
        print(f"    Cost: ¥{opt.cost:.2f}, Points: {opt.points_cost}")
        print(f"    Note: {opt.risk_note}")
