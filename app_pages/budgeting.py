"""
app_pages/budgeting.py — Budget planner and financial goal tracker.

Features:
- Monthly income + expense budget planner (50/30/20 with override)
- Visual breakdown chart
- Goal tracker (savings progress bars)
- Add/edit/delete goals
- Currency localisation
"""

from __future__ import annotations

import streamlit as st
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core import state
from core.data import get_currency, get_country_name, PRESET_GOALS
from core.i18n import t


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _currency_symbol(code: str) -> str:
    SYMBOLS = {
        "USD": "$", "GBP": "£", "EUR": "€", "CAD": "C$", "AUD": "A$",
        "INR": "₹", "NGN": "₦", "ZAR": "R", "BRL": "R$", "MXN": "MX$",
        "JPY": "¥", "PHP": "₱", "KES": "KSh", "EGP": "E£",
    }
    return SYMBOLS.get(code, code + " ")


def _goal_preset_label(goal_id: str) -> str:
    for g in PRESET_GOALS:
        if g["id"] == goal_id:
            return g["label"]
    return goal_id.replace("_", " ").title()


def _pct_bar(pct: float, color: str = "#7c3aed") -> str:
    pct_clamped = min(max(pct, 0), 100)
    return (
        f"<div style='background:#e5e7eb;border-radius:6px;height:12px;overflow:hidden'>"
        f"<div style='background:{color};width:{pct_clamped:.1f}%;height:100%'></div>"
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render() -> None:
    state.init()

    country = st.session_state.get("profile_country", "US")
    currency_code = get_currency(country)
    sym = _currency_symbol(currency_code)

    st.title(t(":material/account_balance_wallet: Budget & Goals"))
    st.caption(
        t("Your budget planner — currency: **{currency_code}** ({country}). "
          "All figures are monthly unless noted.").format(
            currency_code=currency_code, country=get_country_name(country)
        )
    )

    tab_budget, tab_goals = st.tabs([
        t(":material/bar_chart: Monthly budget"),
        t(":material/savings: Financial goals"),
    ])

    # ── TAB 1: Monthly Budget ────────────────────────────────────────────────
    with tab_budget:
        _render_budget_tab(sym, currency_code)

    # ── TAB 2: Financial Goals ───────────────────────────────────────────────
    with tab_goals:
        _render_goals_tab(sym, currency_code)


def _render_budget_tab(sym: str, currency_code: str) -> None:
    st.subheader(t("Monthly income"))
    income = st.number_input(
        t("Monthly take-home income ({sym})").format(sym=sym),
        min_value=0.0,
        value=float(st.session_state.get("budget_income", 0.0)),
        step=100.0,
        format="%.2f",
    )
    st.session_state.budget_income = income

    if income <= 0:
        st.info(t("Enter your monthly take-home income above to see your budget breakdown."), icon=":material/info:")
        return

    st.divider()
    st.subheader(t("50/30/20 framework"))
    st.caption(t("Adjust the percentages to fit your reality. The total must equal 100%."))

    col1, col2, col3 = st.columns(3)
    with col1:
        needs_pct = st.number_input(t("Needs (%)"), min_value=0, max_value=100, value=50, step=1)
    with col2:
        wants_pct = st.number_input(t("Wants (%)"), min_value=0, max_value=100, value=30, step=1)
    with col3:
        savings_pct = st.number_input(t("Savings / Debt (%)"), min_value=0, max_value=100, value=20, step=1)

    total_pct = needs_pct + wants_pct + savings_pct
    if total_pct != 100:
        st.warning(t("Percentages total {total}% — adjust to reach exactly 100%.").format(total=total_pct), icon=":material/warning:")

    needs_amt = income * needs_pct / 100
    wants_amt = income * wants_pct / 100
    savings_amt = income * savings_pct / 100

    col_a, col_b, col_c = st.columns(3)
    col_a.metric(t("Needs"), f"{sym}{needs_amt:,.2f}", t("{pct}% of income").format(pct=needs_pct))
    col_b.metric(t("Wants"), f"{sym}{wants_amt:,.2f}", t("{pct}% of income").format(pct=wants_pct))
    col_c.metric(t("Savings / Debt"), f"{sym}{savings_amt:,.2f}", t("{pct}% of income").format(pct=savings_pct))

    # Visual bar chart using Altair
    import pandas as pd
    import altair as alt

    df = pd.DataFrame({
        "Category": [t("Needs"), t("Wants"), t("Savings / Debt")],
        "Amount": [needs_amt, wants_amt, savings_amt],
        "Colour": ["#7c3aed", "#a78bfa", "#10b981"],
    })
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Category:N", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Amount:Q", title=t("Amount ({currency_code})").format(currency_code=currency_code)),
            color=alt.Color("Colour:N", scale=None, legend=None),
            tooltip=["Category", alt.Tooltip("Amount", format=".2f")],
        )
        .properties(height=220)
    )
    st.altair_chart(chart, width="stretch")

    st.divider()
    st.subheader(t("Expense tracker"))
    st.caption(t("Log your actual monthly expenses to compare against your plan."))

    budget_items: list[dict] = list(st.session_state.get("budget_items", []))

    # Add new item form
    with st.form("add_expense", clear_on_submit=True):
        fc1, fc2, fc3, fc4 = st.columns([3, 2, 2, 1])
        with fc1:
            item_name = st.text_input(t("Description"), placeholder="e.g., Rent")
        with fc2:
            item_amount = st.number_input(t("Amount ({sym})").format(sym=sym), min_value=0.0, step=10.0, format="%.2f")
        with fc3:
            # Display translated, store the underlying English value — matches
            # the pattern used for goals/life-stages elsewhere in the app.
            type_options_en = ["Need", "Want", "Saving / Debt"]
            type_options_display = [t(o) for o in type_options_en]
            item_type_display = st.selectbox(t("Type"), type_options_display)
            item_type = type_options_en[type_options_display.index(item_type_display)]
        with fc4:
            submitted = st.form_submit_button(t(":material/add: Add"), type="primary")
        if submitted and item_name.strip():
            budget_items.append({
                "name": item_name.strip(),
                "amount": item_amount,
                "type": item_type,
            })
            st.session_state.budget_items = budget_items
            st.rerun()

    if budget_items:
        total_expenses = sum(i["amount"] for i in budget_items)
        remaining = income - total_expenses

        import pandas as pd
        df_items = pd.DataFrame(budget_items)
        df_items["Amount"] = df_items["amount"].map(lambda x: f"{sym}{x:,.2f}")
        df_items["type"] = df_items["type"].map(t)
        st.dataframe(
            df_items[["name", "Amount", "type"]].rename(
                columns={"name": t("Description"), "type": t("Category")}
            ),
            hide_index=True,
            width="stretch",
        )

        col_tot, col_rem = st.columns(2)
        col_tot.metric(t("Total expenses"), f"{sym}{total_expenses:,.2f}")
        col_rem.metric(
            t("Remaining (unallocated)"),
            f"{sym}{remaining:,.2f}",
            delta=f"{sym}{remaining:,.2f}",
            delta_color="normal" if remaining >= 0 else "inverse",
        )

        if st.button(t(":material/delete: Clear all expenses"), type="secondary"):
            st.session_state.budget_items = []
            st.rerun()
    else:
        st.info(t("No expenses logged yet. Add your first expense above."), icon=":material/info:")


def _render_goals_tab(sym: str, currency_code: str) -> None:
    budget_goals: list[dict] = list(st.session_state.get("budget_goals", []))

    st.subheader(t("Your financial goals"))

    # Add new goal
    with st.expander(t(":material/add_circle: Add a new goal"), expanded=len(budget_goals) == 0):
        with st.form("add_goal", clear_on_submit=True):
            gc1, gc2, gc3 = st.columns([3, 2, 2])
            with gc1:
                # Combine preset goal names + custom goals. Display translated,
                # but resolve back to the original (English preset / as-typed
                # custom) value, which is what actually gets stored.
                preset_names = [g["label"] for g in PRESET_GOALS]
                custom_names = st.session_state.get("profile_custom_goals", [])
                custom_sentinel = t("Custom…")
                all_names = preset_names + custom_names + ["Custom…"]
                all_names_display = [t(n) for n in preset_names] + custom_names + [custom_sentinel]
                goal_choice_display = st.selectbox(t("Goal type"), all_names_display)
                goal_choice = all_names[all_names_display.index(goal_choice_display)]
            with gc2:
                goal_target = st.number_input(
                    t("Target ({sym})").format(sym=sym), min_value=0.0, step=100.0, format="%.2f"
                )
            with gc3:
                goal_saved = st.number_input(
                    t("Already saved ({sym})").format(sym=sym), min_value=0.0, step=100.0, format="%.2f"
                )

            if goal_choice == "Custom…":
                goal_label = st.text_input(t("Custom goal name"))
            else:
                goal_label = goal_choice

            goal_monthly = st.number_input(
                t("Monthly contribution ({sym})").format(sym=sym), min_value=0.0, step=50.0, format="%.2f"
            )
            add_goal = st.form_submit_button(t(":material/savings: Add goal"), type="primary")
            if add_goal and goal_label.strip() and goal_target > 0:
                import uuid
                budget_goals.append({
                    "id": str(uuid.uuid4()),
                    "label": goal_label.strip(),
                    "target": goal_target,
                    "saved": goal_saved,
                    "monthly": goal_monthly,
                    "currency": currency_code,
                })
                st.session_state.budget_goals = budget_goals
                st.rerun()

    if not budget_goals:
        st.info(
            t("No goals set up yet. Add a goal above to start tracking your progress."),
            icon=":material/savings:",
        )
        return

    for idx, goal in enumerate(budget_goals):
        with st.container(border=True):
            pct = (goal["saved"] / goal["target"] * 100) if goal["target"] > 0 else 0
            remaining = max(goal["target"] - goal["saved"], 0)
            months_left = (
                round(remaining / goal["monthly"])
                if goal.get("monthly", 0) > 0
                else None
            )

            col_label, col_del = st.columns([8, 1])
            with col_label:
                st.markdown(f"**{t(goal['label'])}**")
            with col_del:
                if st.button(
                    ":material/delete:",
                    key=f"del_goal_{goal['id']}",
                    help=t("Delete this goal"),
                ):
                    budget_goals.pop(idx)
                    st.session_state.budget_goals = budget_goals
                    st.rerun()

            colour = "#10b981" if pct >= 100 else "#7c3aed"
            st.markdown(_pct_bar(pct, colour), unsafe_allow_html=True)
            st.caption(t("{pct}% complete").format(pct=f"{pct:.1f}"))

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric(t("Target"), f"{sym}{goal['target']:,.0f}")
            mc2.metric(t("Saved"), f"{sym}{goal['saved']:,.0f}")
            mc3.metric(t("Remaining"), f"{sym}{remaining:,.0f}")
            if months_left is not None:
                mc4.metric(
                    t("Est. months left"),
                    f"{months_left}",
                    help=t("At {sym}{monthly}/month").format(sym=sym, monthly=f"{goal.get('monthly', 0):,.0f}"),
                )
            else:
                mc4.caption(t("Set a monthly contribution to estimate completion date."))

            # Update saved amount inline
            new_saved = st.number_input(
                t("Update saved amount ({sym})").format(sym=sym),
                min_value=0.0,
                max_value=float(goal["target"]) * 2,
                value=float(goal["saved"]),
                step=50.0,
                format="%.2f",
                key=f"saved_{goal['id']}",
            )
            if new_saved != goal["saved"]:
                budget_goals[idx]["saved"] = new_saved
                st.session_state.budget_goals = budget_goals
                st.rerun()

    st.divider()
    # Summary
    total_target = sum(g["target"] for g in budget_goals)
    total_saved = sum(g["saved"] for g in budget_goals)
    overall_pct = (total_saved / total_target * 100) if total_target > 0 else 0
    st.markdown(t("**Overall progress across all goals:** {pct}%").format(pct=f"{overall_pct:.1f}"))
    st.markdown(_pct_bar(overall_pct), unsafe_allow_html=True)
    st.caption(
        t("{sym}{saved} saved toward {sym}{target} total").format(
            sym=sym, saved=f"{total_saved:,.0f}", target=f"{total_target:,.0f}"
        )
    )


# ── Module-level call required by st.Page ────────────────────────────────────
render()
