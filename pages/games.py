import streamlit as st
import random
import time

def show(db):
    st.title("🎮 Games")

    # -------------------------------
    # Session State (Game Tracking)
    # -------------------------------
    if "active_game" not in st.session_state:
        st.session_state.active_game = None

    if "puzzle_numbers" not in st.session_state:
        st.session_state.puzzle_numbers = random.sample(range(1, 9), 8) + [0]  # 0 = empty tile

    if "garden_level" not in st.session_state:
        st.session_state.garden_level = 0

    if "cafe_score" not in st.session_state:
        st.session_state.cafe_score = 0

    if "memory_seq" not in st.session_state:
        st.session_state.memory_seq = []

    if "focus_score" not in st.session_state:
        st.session_state.focus_score = 0

    # -------------------------------
    # CSS (Your Original UI)
    # -------------------------------
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
        }

        .games-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 50px 30px;
            border-radius: 20px;
            color: white;
            margin-bottom: 40px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.35);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .games-header h1 {
            font-weight: 800;
            font-size: 3.2em;
            margin: 0;
        }

        .games-header p {
            font-size: 1.4em;
            opacity: 0.95;
            margin-top: 15px;
            font-weight: 300;
        }

        .game-card {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 18px;
            padding: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(100, 116, 139, 0.3);
            height: 100%;
        }

        .game-card.puzzle { border-top: 5px solid #667eea; }
        .game-card.cozy { border-top: 5px solid #f59e0b; }
        .game-card.focus { border-top: 5px solid #10b981; }

        .game-icon {
            font-size: 3.5em;
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
        }

        .game-title {
            font-size: 1.6em;
            font-weight: 700;
            color: white;
            margin: 0 0 15px 0;
            text-align: center;
        }

        .game-desc {
            font-size: 1.1em;
            color: #94a3b8;
            text-align: center;
            line-height: 1.6;
            margin-bottom: 25px;
        }

        .coming-soon {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border-left: 4px solid #667eea;
            border-radius: 0 12px 12px 0;
            padding: 25px;
            margin: 40px 0;
            color: #cbd5e1;
            font-size: 1.1em;
            font-weight: 500;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------
    # Header
    # -------------------------------
    st.markdown("""
    <div class="games-header">
        <h1>🎮 Relaxing Games</h1>
        <p>Take a break and play calming games to reduce stress</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="coming-soon">
        🎮 <strong>Featured Games</strong> - Play directly inside this page!
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # Helper: Close Game
    # -------------------------------
    def close_game():
        st.session_state.active_game = None

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3 = st.tabs(["🧩 Puzzles", "🎨 Cozy Games", "🎯 Focus Games"])

    # ======================================================
    # 🧩 TAB 1
    # ======================================================
    with tab1:
        st.subheader("🧩 Relaxing Puzzle Games")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("""
            <div class="game-card puzzle">
                <div class="game-icon">🧩</div>
                <h3 class="game-title">Zen Puzzles</h3>
                <p class="game-desc">Simple 3x3 sliding puzzle. Arrange tiles in correct order.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play Zen Puzzle", key="zen_puzzles"):
                st.session_state.active_game = "zen_puzzle"

        with col2:
            st.markdown("""
            <div class="game-card puzzle">
                <div class="game-icon">🌈</div>
                <h3 class="game-title">Color Match</h3>
                <p class="game-desc">Guess the correct color quickly. Improve focus & speed.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play Color Match", key="color_match"):
                st.session_state.active_game = "color_match"

        # -------------------------------
        # Zen Puzzle Game
        # -------------------------------
        if st.session_state.active_game == "zen_puzzle":
            st.markdown("## 🧩 Zen Puzzle (3x3)")

            st.info("Goal: Arrange tiles from 1 → 8. 0 means empty space.")

            grid = st.session_state.puzzle_numbers

            cols = st.columns(3)
            for i in range(9):
                val = grid[i]
                label = "⬜" if val == 0 else str(val)

                with cols[i % 3]:
                    if st.button(label, key=f"tile_{i}"):
                        empty_index = grid.index(0)

                        # Valid moves: left right up down
                        valid_moves = []
                        if empty_index - 1 >= 0 and empty_index % 3 != 0:
                            valid_moves.append(empty_index - 1)
                        if empty_index + 1 < 9 and empty_index % 3 != 2:
                            valid_moves.append(empty_index + 1)
                        if empty_index - 3 >= 0:
                            valid_moves.append(empty_index - 3)
                        if empty_index + 3 < 9:
                            valid_moves.append(empty_index + 3)

                        if i in valid_moves:
                            grid[empty_index], grid[i] = grid[i], grid[empty_index]
                            st.session_state.puzzle_numbers = grid
                            st.rerun()

            if grid == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
                st.success("🎉 Puzzle Solved! Amazing focus 😄")

            colA, colB = st.columns(2)
            with colA:
                if st.button("🔄 Reset Puzzle"):
                    st.session_state.puzzle_numbers = random.sample(range(1, 9), 8) + [0]
                    st.rerun()
            with colB:
                if st.button("❌ Exit Game"):
                    close_game()
                    st.rerun()

        # -------------------------------
        # Color Match Game
        # -------------------------------
        if st.session_state.active_game == "color_match":
            st.markdown("## 🌈 Color Match Game")

            colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
            correct = random.choice(colors)

            st.write("🎯 Select the correct color:")
            st.markdown(f"### 👉 {correct}")

            options = random.sample(colors, 4)
            if correct not in options:
                options[random.randint(0, 3)] = correct
            random.shuffle(options)

            choice = st.radio("Choose:", options, key="color_choice")

            if st.button("Submit Answer"):
                if choice == correct:
                    st.success("✅ Correct! +1 Score")
                else:
                    st.error("❌ Wrong! Try again 😄")

            if st.button("❌ Exit Game"):
                close_game()
                st.rerun()

    # ======================================================
    # 🎨 TAB 2
    # ======================================================
    with tab2:
        st.subheader("🎨 Cozy Games")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("""
            <div class="game-card cozy">
                <div class="game-icon">🌸</div>
                <h3 class="game-title">Garden Sim</h3>
                <p class="game-desc">Water your plant and watch it grow 🌱</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play Garden Sim", key="garden_sim"):
                st.session_state.active_game = "garden_sim"

        with col2:
            st.markdown("""
            <div class="game-card cozy">
                <div class="game-icon">☕</div>
                <h3 class="game-title">Café Manager</h3>
                <p class="game-desc">Serve customers and earn points ☕</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play Café Manager", key="cafe_manager"):
                st.session_state.active_game = "cafe_manager"

        # Garden Sim
        if st.session_state.active_game == "garden_sim":
            st.markdown("## 🌸 Garden Sim")

            st.progress(st.session_state.garden_level / 10)

            st.write(f"🌱 Plant Growth Level: **{st.session_state.garden_level}/10**")

            if st.button("💧 Water Plant"):
                if st.session_state.garden_level < 10:
                    st.session_state.garden_level += 1
                st.rerun()

            if st.session_state.garden_level == 10:
                st.success("🌷 Your plant fully grew! Relaxing win 😍")

            colA, colB = st.columns(2)
            with colA:
                if st.button("🔄 Reset Garden"):
                    st.session_state.garden_level = 0
                    st.rerun()
            with colB:
                if st.button("❌ Exit Game"):
                    close_game()
                    st.rerun()

        # Cafe Manager
        if st.session_state.active_game == "cafe_manager":
            st.markdown("## ☕ Café Manager")

            st.write(f"⭐ Your Score: **{st.session_state.cafe_score}**")

            customer = random.choice(["👩 Customer wants Latte", "👨 Customer wants Cappuccino", "🧑 Customer wants Espresso"])

            st.info(customer)

            if st.button("☕ Serve"):
                st.session_state.cafe_score += 1
                st.success("Served! +1 ⭐")
                st.rerun()

            colA, colB = st.columns(2)
            with colA:
                if st.button("🔄 Reset Café"):
                    st.session_state.cafe_score = 0
                    st.rerun()
            with colB:
                if st.button("❌ Exit Game"):
                    close_game()
                    st.rerun()

    # ======================================================
    # 🎯 TAB 3
    # ======================================================
    with tab3:
        st.subheader("🎯 Focus Games")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("""
            <div class="game-card focus">
                <div class="game-icon">🧠</div>
                <h3 class="game-title">Memory Master</h3>
                <p class="game-desc">Remember the numbers and type them back.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play Memory Master", key="memory_master"):
                st.session_state.active_game = "memory_master"

        with col2:
            st.markdown("""
            <div class="game-card focus">
                <div class="game-icon">🎯</div>
                <h3 class="game-title">Focus Quest</h3>
                <p class="game-desc">30-second focus timer. Stay calm & win.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play Focus Quest", key="focus_quest"):
                st.session_state.active_game = "focus_quest"

        # Memory Master
        if st.session_state.active_game == "memory_master":
            st.markdown("## 🧠 Memory Master")

            if st.button("Generate New Sequence"):
                st.session_state.memory_seq = [random.randint(1, 9) for _ in range(5)]

            if st.session_state.memory_seq:
                st.warning(f"Memorize this: {st.session_state.memory_seq}")
                user_input = st.text_input("Enter sequence (space separated):")

                if st.button("Check"):
                    try:
                        nums = list(map(int, user_input.split()))
                        if nums == st.session_state.memory_seq:
                            st.success("🎉 Perfect Memory!")
                        else:
                            st.error("❌ Wrong. Try again!")
                    except:
                        st.error("Enter numbers properly like: 1 2 3 4 5")

            if st.button("❌ Exit Game"):
                close_game()
                st.rerun()

        # Focus Quest
        if st.session_state.active_game == "focus_quest":
            st.markdown("## 🎯 Focus Quest")

            st.write("Click start and stay focused for 10 seconds 😄")

            if st.button("Start Timer"):
                st.write("⏳ Focusing...")
                time.sleep(10)
                st.session_state.focus_score += 1
                st.success("✅ You stayed focused! +1 Score")

            st.write(f"🏆 Focus Score: **{st.session_state.focus_score}**")

            colA, colB = st.columns(2)
            with colA:
                if st.button("🔄 Reset Score"):
                    st.session_state.focus_score = 0
                    st.rerun()
            with colB:
                if st.button("❌ Exit Game"):
                    close_game()
                    st.rerun()
