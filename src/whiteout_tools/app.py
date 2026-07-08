import streamlit as st  # type: ignore

from whiteout_tools.data import PACKS
from whiteout_tools.models.target import Target
from whiteout_tools.optimizer.craftsman_shop import CraftsmanShopOptimizer

PRICE_TIERS = [800, 1600, 3200, 8000, 15800]


def main() -> None:
    st.title("工商の匠 Optimizer")
    st.write("必要素材を入力すると、最安の購入組み合わせを計算します。")

    alloy = st.number_input("必要な合金", min_value=0, value=100_000, step=1_000)
    polish = st.number_input("必要な研磨剤", min_value=0, value=3_800, step=100)
    blueprint = st.number_input("必要な図面", min_value=0, value=1_600, step=10)

    if st.button("最適化する"):
        target = Target(
            alloy=int(alloy),
            polish=int(polish),
            blueprint=int(blueprint),
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

        selected = {
            pack.price_tier: pack.category.value
            for pack in result.packs
        }

        for price in PRICE_TIERS:
            if price in selected:
                st.success(f"{price:,}円　{selected[price]}")
            else:
                st.info(f"{price:,}円　購入なし")

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
        surplus_col1.metric("🔩 合金余剰", f"+{result.total_alloy - target.alloy:,}")
        surplus_col2.metric("🧪 研磨剤余剰", f"+{result.total_polish - target.polish:,}")
        surplus_col3.metric("📐 図面余剰", f"+{result.total_blueprint - target.blueprint:,}")


if __name__ == "__main__":
    main()