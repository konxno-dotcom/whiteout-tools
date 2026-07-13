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

        try:
            result = optimizer.optimize(target)
        except NotImplementedError:
            max_packs = [
                max(
                    [pack for pack in PACKS if pack.price_tier == price],
                    key=lambda pack: pack.alloy + pack.polish + pack.blueprint,
                )
                for price in PRICE_TIERS
            ]

            max_alloy = sum(pack.alloy for pack in max_packs)
            max_polish = sum(pack.polish for pack in max_packs)
            max_blueprint = sum(pack.blueprint for pack in max_packs)
            max_price = sum(pack.price_tier for pack in max_packs)

            st.error("工商の匠だけでは必要素材に届きません。最大まで購入した場合の不足分を表示します。")

            st.metric("最大購入金額", f"{max_price:,}円")

            st.write("### 最大購入した場合の獲得素材")
            st.write(f"- 合金：{max_alloy:,}")
            st.write(f"- 研磨剤：{max_polish:,}")
            st.write(f"- 図面：{max_blueprint:,}")

            st.write("### それでも足りない素材")
            st.write(f"- 合金：{max(0, needed_alloy - max_alloy):,}")
            st.write(f"- 研磨剤：{max(0, needed_polish - max_polish):,}")
            st.write(f"- 図面：{max(0, needed_blueprint - max_blueprint):,}")

            return

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
        st.write("## 購入シミュレーション")

        running_price = 0
        running_alloy = 0
        running_polish = 0
        running_blueprint = 0

        for index, pack in enumerate(result.packs, start=1):
            running_price += pack.price_tier
            running_alloy += pack.alloy
            running_polish += pack.polish
            running_blueprint += pack.blueprint

            st.markdown(
                f"### {index}. {pack.price_tier:,}円　{pack.category.value}"
            )

            pack_col1, pack_col2, pack_col3, pack_col4 = st.columns(4)
            pack_col1.metric("💴 価格", f"{pack.price_tier:,}円")
            pack_col2.metric("🔩 合金", f"{pack.alloy:,}")
            pack_col3.metric("🧪 研磨剤", f"{pack.polish:,}")
            pack_col4.metric("📐 図面", f"{pack.blueprint:,}")

            st.caption("この時点での累計")

            total_col1, total_col2, total_col3, total_col4 = st.columns(4)
            total_col1.metric("💴 累計金額", f"{running_price:,}円")
            total_col2.metric(
                "🔩 累計合金",
                f"{running_alloy:,}",
                delta=f"{running_alloy - needed_alloy:,}",
            )
            total_col3.metric(
                "🧪 累計研磨剤",
                f"{running_polish:,}",
                delta=f"{running_polish - needed_polish:,}",
            )
            total_col4.metric(
                "📐 累計図面",
                f"{running_blueprint:,}",
                delta=f"{running_blueprint - needed_blueprint:,}",
            )

            is_reached_at_step = (
                running_alloy >= needed_alloy
                and running_polish >= needed_polish
                and running_blueprint >= needed_blueprint
            )

            if is_reached_at_step:
                st.success("この段階で目標達成です。ここで購入を止められます。")
            else:
                st.warning("まだ目標未達です。次の価格帯へ進みます。")

            st.divider()


        st.write("### 余剰素材")
        surplus_col1, surplus_col2, surplus_col3 = st.columns(3)
        surplus_col1.metric("🔩 合金余剰", f"+{result.total_alloy - needed_alloy:,}")
        surplus_col2.metric("🧪 研磨剤余剰", f"+{result.total_polish - needed_polish:,}")
        surplus_col3.metric("📐 図面余剰", f"+{result.total_blueprint - needed_blueprint:,}")


if __name__ == "__main__":
    main()