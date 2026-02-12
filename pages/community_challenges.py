import streamlit as st
from datetime import datetime, date


# ----------------------------------------
# FIXED CHALLENGES (OPTION A)
# ----------------------------------------
CHALLENGES = [
    {
        "id": "steps_7days",
        "title": "🚶 7-Day Steps Challenge",
        "desc": "Walk at least 7,000 steps daily for 7 days.",
        "points": 50
    },
    {
        "id": "water_7days",
        "title": "💧 Hydration Challenge",
        "desc": "Drink 2L water daily for 7 days.",
        "points": 40
    },
    {
        "id": "sleep_7days",
        "title": "😴 Sleep Before 12 AM",
        "desc": "Sleep before 12 AM daily for 7 days.",
        "points": 60
    },
    {
        "id": "meditation_5min",
        "title": "🧘 5-Min Meditation Streak",
        "desc": "Meditate 5 minutes daily for 10 days.",
        "points": 70
    },
    {
        "id": "no_junk_5days",
        "title": "🥗 No Junk Food Challenge",
        "desc": "Avoid junk food for 5 days straight.",
        "points": 55
    },
]


# ----------------------------------------
# FIRESTORE HELPERS
# ----------------------------------------
def _today_str():
    return date.today().isoformat()


def is_joined(db, user_id, challenge_id):
    doc_id = f"{user_id}_{challenge_id}"
    doc = db.collection("challenge_participants").document(doc_id).get()
    return doc.exists


def join_challenge(db, user_id, challenge_id):
    doc_id = f"{user_id}_{challenge_id}"
    db.collection("challenge_participants").document(doc_id).set({
        "user_id": user_id,
        "challenge_id": challenge_id,
        "joined_at": datetime.utcnow().isoformat(),
        "total_checkins": 0,
        "last_checkin": None,
        "streak": 0
    })


def leave_challenge(db, user_id, challenge_id):
    doc_id = f"{user_id}_{challenge_id}"
    db.collection("challenge_participants").document(doc_id).delete()


def has_checked_in_today(db, user_id, challenge_id):
    doc_id = f"{user_id}_{challenge_id}_{_today_str()}"
    doc = db.collection("challenge_checkins").document(doc_id).get()
    return doc.exists


def checkin_today(db, user_id, challenge_id):
    """
    Saves daily check-in + updates streak in participants doc
    """
    today = _today_str()
    checkin_doc_id = f"{user_id}_{challenge_id}_{today}"
    participant_doc_id = f"{user_id}_{challenge_id}"

    # prevent double checkin
    if has_checked_in_today(db, user_id, challenge_id):
        return False

    # create checkin
    db.collection("challenge_checkins").document(checkin_doc_id).set({
        "user_id": user_id,
        "challenge_id": challenge_id,
        "date": today,
        "done": True,
        "created_at": datetime.utcnow().isoformat()
    })

    # update participant stats
    participant_ref = db.collection("challenge_participants").document(participant_doc_id)
    participant_doc = participant_ref.get()

    if participant_doc.exists:
        data = participant_doc.to_dict()

        old_last = data.get("last_checkin")
        old_streak = int(data.get("streak", 0))
        old_total = int(data.get("total_checkins", 0))

        # streak logic
        # if last checkin was yesterday -> streak + 1
        # else -> streak reset to 1
        if old_last:
            try:
                old_last_date = date.fromisoformat(old_last)
                today_date = date.fromisoformat(today)
                diff = (today_date - old_last_date).days

                if diff == 1:
                    new_streak = old_streak + 1
                elif diff == 0:
                    new_streak = old_streak  # already checked (but we prevented it)
                else:
                    new_streak = 1
            except:
                new_streak = 1
        else:
            new_streak = 1

        participant_ref.update({
            "total_checkins": old_total + 1,
            "last_checkin": today,
            "streak": new_streak,
            "updated_at": datetime.utcnow().isoformat()
        })

    return True


def get_leaderboard(db, challenge_id, limit=10):
    """
    Leaderboard based on streak + total_checkins
    """
    try:
        docs = (
            db.collection("challenge_participants")
            .where("challenge_id", "==", challenge_id)
            .stream()
        )

        rows = []
        for d in docs:
            x = d.to_dict()
            rows.append({
                "user_id": x.get("user_id"),
                "streak": int(x.get("streak", 0)),
                "total_checkins": int(x.get("total_checkins", 0)),
                "last_checkin": x.get("last_checkin")
            })

        # sort by streak then total_checkins
        rows.sort(key=lambda r: (r["streak"], r["total_checkins"]), reverse=True)
        return rows[:limit]
    except:
        return []


# ----------------------------------------
# MAIN PAGE
# ----------------------------------------
def show(db):
    st.title("🌍 Community Challenges")
    st.caption("Join challenges, check-in daily, build streaks, and climb the leaderboard 🚀")

    # user must be logged in
    if not st.session_state.get("user_id"):
        st.warning("⚠️ Please login first to use Community Challenges.")
        return

    user_id = st.session_state.user_id

    # CSS
    st.markdown("""
    <style>
        .challenge-card {
            background: white;
            padding: 18px;
            border-radius: 18px;
            box-shadow: 0 5px 18px rgba(0,0,0,0.08);
            border: 1px solid #eef2ff;
            margin-bottom: 16px;
        }

        .challenge-title {
            font-size: 1.25em;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .challenge-desc {
            color: #475569;
            font-size: 1em;
            margin-bottom: 10px;
        }

        .pill {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 0.9em;
            font-weight: 700;
            background: #eef2ff;
            color: #4338ca;
            margin-right: 8px;
        }

        .divider {
            margin: 20px 0;
            border: 0;
            height: 3px;
            background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
            border-radius: 3px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ----------------------------------------
    # SHOW ALL CHALLENGES
    # ----------------------------------------
    for ch in CHALLENGES:
        joined = is_joined(db, user_id, ch["id"])
        checked_today = has_checked_in_today(db, user_id, ch["id"]) if joined else False

        st.markdown(f"""
        <div class="challenge-card">
            <div class="challenge-title">{ch["title"]}</div>
            <div class="challenge-desc">{ch["desc"]}</div>
            <div>
                <span class="pill">⭐ {ch["points"]} Points</span>
                <span class="pill">📅 Today: {_today_str()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.2, 1.2, 2])

        # JOIN / LEAVE
        with col1:
            if not joined:
                if st.button("➕ Join", key=f"join_{ch['id']}", use_container_width=True):
                    join_challenge(db, user_id, ch["id"])
                    st.success("✅ Joined challenge!")
                    st.rerun()
            else:
                if st.button("❌ Leave", key=f"leave_{ch['id']}", use_container_width=True):
                    leave_challenge(db, user_id, ch["id"])
                    st.warning("Left the challenge.")
                    st.rerun()

        # CHECK-IN
        with col2:
            if joined:
                if checked_today:
                    st.button("✅ Checked Today", key=f"checked_{ch['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("🔥 Daily Check-in", key=f"checkin_{ch['id']}", use_container_width=True):
                        ok = checkin_today(db, user_id, ch["id"])
                        if ok:
                            st.success("🔥 Check-in saved! Keep going!")
                        else:
                            st.info("You already checked-in today 😄")
                        st.rerun()
            else:
                st.button("🔒 Join to Check-in", key=f"locked_{ch['id']}", disabled=True, use_container_width=True)

        # LEADERBOARD
        with col3:
            st.markdown("**🏆 Leaderboard (Top 10)**")
            leaderboard = get_leaderboard(db, ch["id"], limit=10)

            if len(leaderboard) == 0:
                st.info("No participants yet. Be the first 💪")
            else:
                for i, row in enumerate(leaderboard, start=1):
                    uid = row["user_id"]
                    streak = row["streak"]
                    total = row["total_checkins"]

                    # highlight current user
                    if uid == user_id:
                        st.markdown(f"**{i}. You** — 🔥 {streak} streak | ✅ {total} check-ins")
                    else:
                        st.markdown(f"{i}. {uid[:6]}... — 🔥 {streak} | ✅ {total}")

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ----------------------------------------
    # YOUR JOINED CHALLENGES SUMMARY
    # ----------------------------------------
    st.subheader("📌 My Challenges")

    try:
        docs = (
            db.collection("challenge_participants")
            .where("user_id", "==", user_id)
            .stream()
        )

        my_list = []
        for d in docs:
            x = d.to_dict()
            my_list.append(x)

        if len(my_list) == 0:
            st.info("You haven't joined any challenge yet. Join one above 👆")
        else:
            for x in my_list:
                st.markdown(
                    f"✅ **{x.get('challenge_id')}** | 🔥 Streak: **{x.get('streak', 0)}** | "
                    f"📅 Last: {x.get('last_checkin')}"
                )

    except:
        st.warning("Could not load your joined challenges right now.")
