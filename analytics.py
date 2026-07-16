# analytics.py — M4 Logic & Analytics

# ─── BURNOUT CALCULATOR ───────────────────────
def burnout_calculator(selected_societies, available_hrs):
    """
    selected_societies: list of dicts
    
    available_hrs: int (from user profile form)
    """
    if available_hrs <= 0:
        return 0, "Please enter valid available hours"
    
    if not selected_societies:
        return 0, "No societies saved. Please add your favourites."
    
    selected_societies = selected_societies[:6]
    
    total_hrs = sum(s['commitment_per_week'] 
                    for s in selected_societies)
    
    burnout_pct = round((total_hrs / available_hrs) * 100, 1)
    
    if burnout_pct <= 80:
        status = "🟢 Comfortable"
    elif burnout_pct <= 100:
        status = "🟡 Manageable, but tight"
    elif burnout_pct <= 130:
        status = "🟠 Overcommitted"
    else:
        status = "🔴 Burnout Risk"
    
    return burnout_pct, status


# ─── BEST COMBINATION LOGIC ───────────────────
from itertools import combinations

def _find_valid_combos(selected_societies, limit):
    """
    Helper — saari combinations (size 2+) find karta hai jo
    total_hrs <= limit ke andar fit hoti hain, ranked by
    match% > domain variety > low hours
    """
    valid_combos = []

    for size in range(2, len(selected_societies) + 1):
        for combo in combinations(selected_societies, size):
            total_hrs = sum(s['commitment_per_week']
                           for s in combo)

            if total_hrs <= limit:
                domains = set(s['domain'] for s in combo)
                avg_match = sum(s.get('match_pct', 0) for s in combo) / len(combo)

                valid_combos.append({
                    'societies': combo,
                    'total_hrs': total_hrs,
                    'domain_variety': len(domains),
                    'avg_match': avg_match
                })

    valid_combos.sort(key=lambda x: (
        -x['avg_match'],      # match % high ho
        -x['domain_variety'], # domains varied hon
        x['total_hrs']        # hours kam hon
    ))

    return valid_combos


def best_combinations(selected_societies, available_hrs):
    """
    Returns top 3 best combinations.
    Pehle comfortable zone (<=80%) try karta hai, agar wahan
    kuch nahi milta toh manageable zone (<=100%) mein try karta hai.

    Returns: (combos, error, zone)
        zone = "comfortable" | "manageable" | None (jab error ho)
    """

    # Edge cases
    if len(selected_societies) == 0:
        return None, "No societies saved yet. ", None

    if len(selected_societies) == 1:
        return None, "Save at least 2 societies for suggestions💡", None

    # Cap input size — checking every combination of N societies grows
    # exponentially (2^N). With 15+ saved societies this measurably
    # freezes the page; past ~20 it's multiple seconds. Keep the
    # highest-match ones since those are the most relevant anyway.
    if len(selected_societies) > 12:
        selected_societies = sorted(
            selected_societies,
            key=lambda s: s.get('match_pct', 0),
            reverse=True
        )[:12]

    comfortable_limit = available_hrs * 0.80  # 80% threshold
    manageable_limit = available_hrs * 1.00   # 100% threshold

    # ── Try comfortable zone first ──
    comfortable_combos = _find_valid_combos(selected_societies, comfortable_limit)
    if comfortable_combos:
        return comfortable_combos[:3], None, "comfortable"

    # ── Fallback: manageable zone (80-100%) ──
    manageable_combos = _find_valid_combos(selected_societies, manageable_limit)
    if manageable_combos:
        return manageable_combos[:3], None, "manageable"

    return None, "No combination fits even within your full available hours - try adding more hours or removing societies ⚠️", None


def get_burnout_advice(burnout_pct, combos):
    """
    Simple advice string return karta hai
    burnout status + combination suggestion ke saath
    """
    if burnout_pct <= 80:
        return "You're in a great spot! Your selected societies fit well within your schedule."
    elif burnout_pct <= 100:
        return "Manageable but keep an eye on deadlines. Consider the suggested combinations below."
    elif burnout_pct <= 130:
        return "You're overcommitting. We strongly suggest picking a combination from below."
    else:
        return "High burnout risk! Please pick one of the suggested combinations to stay healthy."


# ─── TEST ─────────────────────────────────────
if __name__ == "__main__":
    test_societies = [
        {'name': 'AI Club', 'commitment_per_week': 2, 
         'domain': 'Technology', 'match_pct': 92},
        {'name': 'NSS', 'commitment_per_week': 3, 
         'domain': 'Social', 'match_pct': 78},
        {'name': 'Dance', 'commitment_per_week': 12, 
         'domain': 'Cultural', 'match_pct': 65},
         {'name': 'Tarannum', 'commitment_per_week': 9, 
         'domain': 'Singing', 'match_pct': 70},
    ]
    
    # Burnout test
    pct, status = burnout_calculator(test_societies, 25)
    print(f"Burnout: {pct}% → {status}")
    
    # Combination test
    combos, error, zone = best_combinations(test_societies, 25)
    if error:
        print(error)
    else:
        print(f"Zone: {zone}")
        for i, c in enumerate(combos):
            names = [s['name'] for s in c['societies']]
            print(f"Combo {i+1}: {names} | {c['total_hrs']}hrs | {c['avg_match']}% match")