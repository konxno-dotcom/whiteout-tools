import streamlit as st  # type: ignore

from whiteout_tools.data import PACKS
from whiteout_tools.models.target import Target
from whiteout_tools.optimizer.craftsman_shop import CraftsmanShopOptimizer

PRICE_TIERS = [800, 1600, 3200, 8000, 15800]


def main() -> None:
    st.title("工商の匠 Optimizer")
    st.write("現在所持数と目標数から、不足分を計算して最安の購入組み合わせを出します。")

    st.header("素材入力")

    current_col, target_col = st.columns(2)

    with current_col:
        st.subheader("現在所持")
        current_alloy = st.number_input("現在の合金", min_value=0, value=0, step=1_000)
        current_polish = st.number_input("現在の研磨剤", min_value=0, value=0, step=100)
        current_blueprint = st.number_input("現在の図面", min_value=0, value=0, step=10)

    with target_col:
        st.subheader("目標")
        target_alloy = st.number_input("目標の合金", min_value=0, value=100_000, step=1_000)
        target_polish = st.number_input("目標の研磨剤", min_value=0, value=3_800, step=100)
        target_blueprint = st.number_input("目標の図面", min_value=0, value=1_600, step=10)

    needed_alloy = max(0, int(target_alloy) - int(current_alloy))
    needed_polish = max(0, int(target_polish) - int(current_polish))
    needed_blueprint = max(0, int(target_blueprint) - int(current_blueprint))

    st.header("不足数")
    need_col1, need_col2, need_col3 = st.columns(3)
    need_col1.metric("🔩 合金", f"{needed_alloy:,}")
    need_col2.metric("🧪 研磨剤", f"{needed_polish:,}")
    need_col3.metric("📐 図面", f"{needed_blueprint:,}")

    if st.button("最適化する"):
        target = Target(
            alloy=needed_alloy,
            polish=needed_polish,
            blueprint=needed_blueprint,
        )

        optimizer = CraftsmanShopOptimizer(PACKS)
        result = optimizer.optimize(target)

        st.subheader("結果")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💴 合計金額", f"{result.total_price:,}円")
        col2.metric("🔩 合金", f"{result.total_alloy:,}")
        col3.metric("🧪 研磨剤", f"{result.total_polish:,}")
        col4.metric("📐 図面", f"{result.total_blueprint:,}")

        st.write("### 購入順")

        selected = {pack.price_tier: pack.category.value for pack in result.packs}

        for index, price in enumerate(PRICE_TIERS, start=1):
            if price in selected:
                st.success(f"{index}. {price:,}円　{selected[price]}")
            else:
                st.info(f"{index}. {price:,}円　購入なし")

            if index < len(PRICE_TIERS):
                st.write("↓")

        rows = [
            {
                "価格": f"{pack.price_tier:,}円",
                "種類": pack.category.value,
                "合金": pack.alloy,
                "研磨剤": pack.polish,
                "図面": pack.blueprint,
            }
            for pack in result.packs
        ]

        st.write("### 購入パック詳細")
        st.dataframe(rows, use_container_width=True)

        st.write("### 余剰素材")
        surplus_col1, surplus_col2, surplus_col3 = st.columns(3)
        surplus_col1.metric("🔩 合金余剰", f"+{result.total_alloy - needed_alloy:,}")
        surplus_col2.metric("🧪 研磨剤余剰", f"+{result.total_polish - needed_polish:,}")
        surplus_col3.metric("📐 図面余剰", f"+{result.total_blueprint - needed_blueprint:,}")


if __name__ == "__main__":
    main()