import streamlit as st  # type: ignore

from whiteout_tools.data import PACKS
from whiteout_tools.data.equipment_upgrades import EQUIPMENT_UPGRADES  # noqa: F401
from whiteout_tools.models.target import Target
from whiteout_tools.optimizer.craftsman_shop import CraftsmanShopOptimizer
from whiteout_tools.services.equipment_upgrade_calculator import (
    calculate_equipment_upgrade_cost,  # noqa: F401
)

PRICE_TIERS = [800, 1600, 3200, 8000, 15800]

st.set_page_config(
    page_title="Whiteout Tools",
    page_icon="❄️",
    layout="centered",
)


def main() -> None:
    with st.sidebar:
        st.markdown("## ❄ Whiteout Lab")
        st.caption("Whiteout Survival Utility Suite")

        st.divider()

        st.markdown("### 現在のツール")
        st.success("工商の匠 Optimizer")

        st.divider()

        st.markdown(
                """
            <div style="
                padding: 1.5rem;
                border-radius: 16px;
                background: linear-gradient(
                    135deg,
                    rgba(77,163,255,0.18),
                    rgba(19,29,46,0.92)
                );
            ">

            <h1 style="margin:0;">
            ❄ Whiteout Lab
            </h1>

            <p style="margin-top:8px;">
            工商の匠 Optimizer
            </p>

            <p style="color:#B8C5D8;">
            現在所持数と目標数から、
            不足分を満たす最適な購入ルートを計算します。
            </p>

            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown("### ステータス")
        st.caption("Engine: Stable")
        st.caption("UI: Preview")
        st.caption("Version 0.4.0")

    with st.form("optimizer_form", border=False):
        equipment_names = [
            upgrade.name
            for upgrade in EQUIPMENT_UPGRADES
        ]

        current_name = st.selectbox(  # noqa: F841
            "現在装備",
            equipment_names,
        )

        target_name = st.selectbox(  # noqa: F841
            "目標装備",
            equipment_names,
            index=len(equipment_names) - 1,
        )
        current_upgrade = next(  # noqa: F841
            upgrade
            for upgrade in EQUIPMENT_UPGRADES
            if upgrade.name == current_name
        )

        required = calculate_equipment_upgrade_cost(  # noqa: F841
        upgrades=EQUIPMENT_UPGRADES,
        current_order=current_upgrade.order,
        target_order=target_upgrade.order,  # noqa: F821
)

        target_upgrade = next(  # noqa: F841
            upgrade
            for upgrade in EQUIPMENT_UPGRADES
            if upgrade.name == target_name
        )
        with st.container(border=True):
            st.subheader("素材条件")

            current_col, target_col = st.columns(2, gap="large")

            with current_col:
                st.markdown("#### 現在所持")

                current_alloy = st.number_input(
                    "合金",
                    min_value=0,
                    value=0,
                    step=1_000,
                    key="current_alloy",
                )
                current_polish = st.number_input(
                    "研磨剤",
                    min_value=0,
                    value=0,
                    step=100,
                    key="current_polish",
                )
                current_blueprint = st.number_input(
                    "図面",
                    min_value=0,
                    value=0,
                    step=10,
                    key="current_blueprint",
                )

            with target_col:
                st.markdown("#### 目標")

                target_alloy = st.number_input(  # noqa: F841
                    "合金",
                    min_value=0,
                    value=100_000,
                    step=1_000,
                    key="target_alloy",
                )
                target_polish = st.number_input(  # noqa: F841
                    "研磨剤",
                    min_value=0,
                    value=3_800,
                    step=100,
                    key="target_polish",
                )
                target_blueprint = st.number_input(  # noqa: F841
                    "図面",
                    min_value=0,
                    value=1_600,
                    step=10,
                    key="target_blueprint",
                )

            needed_alloy = max(
                0,
                required.alloy - current_alloy,
            )

            needed_polish = max(
                0,
                required.polish - current_polish,
            )

            needed_blueprint = max(
                0,
                required.blueprint - current_blueprint,
            )

            st.subheader("📋 強化に必要な素材")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("🔩 合金", f"{required.alloy:,}")
            col2.metric("🧪 研磨剤", f"{required.polish:,}")
            col3.metric("📜 図面", f"{required.blueprint:,}")
            col4.metric("🌙 月光琥珀", f"{required.moon_amber:,}")

            st.markdown("#### 不足数")

            need_col1, need_col2, need_col3 = st.columns(3)

            need_col1.metric(
                "合金",
                f"{needed_alloy:,}",
            )
            need_col2.metric(
                "研磨剤",
                f"{needed_polish:,}",
            )
            need_col3.metric(
                "図面",
                f"{needed_blueprint:,}",
            )

            optimize_clicked = st.form_submit_button(
                "最適な購入ルートを計算",
                type="primary",
                width="stretch",
            )

    if not optimize_clicked:
        return

    target = Target(
        alloy=needed_alloy,
        polish=needed_polish,
        blueprint=needed_blueprint,
    )

    optimizer = CraftsmanShopOptimizer(PACKS)
    result = optimizer.optimize(target)

    is_reached = (
        result.total_alloy >= needed_alloy
        and result.total_polish >= needed_polish
        and result.total_blueprint >= needed_blueprint
    )

    status_label = "目標達成" if is_reached else "目標未達"
    status_icon = "✅" if is_reached else "⚠️"

    with st.container(border=True):
        header_col, price_col = st.columns([3, 1])

        with header_col:
            st.markdown("### 最適化結果")
            st.caption(f"{status_icon} {status_label}")

        with price_col:
            st.metric(
                "合計金額",
                f"{result.total_price:,}円",
            )

        material_col1, material_col2, material_col3 = st.columns(3)

        material_col1.metric(
            "合金",
            f"{result.total_alloy:,}",
            delta=f"{result.total_alloy - needed_alloy:+,}",
        )
        material_col2.metric(
            "研磨剤",
            f"{result.total_polish:,}",
            delta=f"{result.total_polish - needed_polish:+,}",
        )
        material_col3.metric(
            "図面",
            f"{result.total_blueprint:,}",
            delta=f"{result.total_blueprint - needed_blueprint:+,}",
        )

    with st.container(border=True):
        st.subheader("購入シミュレーション")

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
                f"#### {index}. {pack.price_tier:,}円　{pack.category.value}"
            )

            pack_col1, pack_col2, pack_col3, pack_col4 = st.columns(4)

            pack_col1.metric(
                "価格",
                f"{pack.price_tier:,}円",
            )
            pack_col2.metric(
                "合金",
                f"{pack.alloy:,}",
            )
            pack_col3.metric(
                "研磨剤",
                f"{pack.polish:,}",
            )
            pack_col4.metric(
                "図面",
                f"{pack.blueprint:,}",
            )

            st.caption("この時点での累計")

            total_col1, total_col2, total_col3, total_col4 = st.columns(4)

            total_col1.metric(
                "累計金額",
                f"{running_price:,}円",
            )
            total_col2.metric(
                "累計合金",
                f"{running_alloy:,}",
                delta=f"{running_alloy - needed_alloy:+,}",
            )
            total_col3.metric(
                "累計研磨剤",
                f"{running_polish:,}",
                delta=f"{running_polish - needed_polish:+,}",
            )
            total_col4.metric(
                "累計図面",
                f"{running_blueprint:,}",
                delta=f"{running_blueprint - needed_blueprint:+,}",
            )

            reached_at_this_step = (
                running_alloy >= needed_alloy
                and running_polish >= needed_polish
                and running_blueprint >= needed_blueprint
            )

            if reached_at_this_step:
                st.success(
                    "この段階で目標達成です。ここで購入を止められます。"
                )
            else:
                st.info(
                    "まだ目標未達です。次の価格帯へ進みます。"
                )

            if index < len(result.packs):
                st.divider()

    with st.container(border=True):
        st.subheader("Discord共有用レシート")

        route_lines = [
            f"{index}. {pack.price_tier:,}円　{pack.category.value}"
            for index, pack in enumerate(result.packs, start=1)
        ]

        receipt_text = "\n".join(
            [
                "【工商の匠 購入レシート】",
                "",
                *route_lines,
                "",
                f"合計金額：{result.total_price:,}円",
                "",
                "獲得素材",
                f"合金：{result.total_alloy:,}",
                f"研磨剤：{result.total_polish:,}",
                f"図面：{result.total_blueprint:,}",
                "",
                "不足分に対する余剰・不足",
                f"合金：{result.total_alloy - needed_alloy:+,}",
                f"研磨剤：{result.total_polish - needed_polish:+,}",
                f"図面：{result.total_blueprint - needed_blueprint:+,}",
                "",
                f"判定：{status_label}",
            ]
        )

        st.code(
            receipt_text,
            language=None,
        )

    with st.container(border=True):
        st.subheader("この結果について")

        if is_reached:
            st.success("入力された不足素材を満たしています。")
            st.write(
                f"{len(result.packs)}段階目で目標達成するため、"
                "それ以降の購入は不要です。"
            )
        else:
            shortage_alloy = max(
                0,
                needed_alloy - result.total_alloy,
            )
            shortage_polish = max(
                0,
                needed_polish - result.total_polish,
            )
            shortage_blueprint = max(
                0,
                needed_blueprint - result.total_blueprint,
            )

            st.warning(
                "工商の匠を最大まで進めても、"
                "入力された不足素材には届きません。"
            )

            shortage_col1, shortage_col2, shortage_col3 = st.columns(3)

            shortage_col1.metric(
                "不足合金",
                f"{shortage_alloy:,}",
            )
            shortage_col2.metric(
                "不足研磨剤",
                f"{shortage_polish:,}",
            )
            shortage_col3.metric(
                "不足図面",
                f"{shortage_blueprint:,}",
            )

        st.write(
            f"推奨ルートの合計金額は "
            f"**{result.total_price:,}円** です。"
        )
        st.write(
            f"購入するパックは "
            f"**{len(result.packs)}個** です。"
        )


if __name__ == "__main__":
    main()