import streamlit as st  # type: ignore

from whiteout_tools.data import PACKS
from whiteout_tools.models.target import Target
from whiteout_tools.optimizer.craftsman_shop import CraftsmanShopOptimizer


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
        st.metric("合計金額", f"{result.total_price:,}円")

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

        st.write("### 購入パック")
        st.dataframe(rows, use_container_width=True)

        st.write("### 合計獲得素材")
        st.write(f"- 合金：{result.total_alloy:,}")
        st.write(f"- 研磨剤：{result.total_polish:,}")
        st.write(f"- 図面：{result.total_blueprint:,}")


if __name__ == "__main__":
    main()