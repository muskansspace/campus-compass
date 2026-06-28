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

def best_combinations(selected_societies, available_hrs):
    """
    Returns top 3 best combinations within comfortable zone
    """
    
    # Edge cases
    if len(selected_societies) == 0:
        return None, "No societies saved yet. "
    
    if len(selected_societies) == 1:
        return None, "Save at least 2 societies for suggestions💡"
    
    comfortable_limit = available_hrs * 0.80  # 80% threshold
    
    valid_combos = []
    
    # Saari possible combinations try karo (size 2 se max tak)
    for size in range(2, len(selected_societies) + 1):
        for combo in combinations(selected_societies, size):
            total_hrs = sum(s['commitment_per_week'] 
                           for s in combo)
            
            if total_hrs <= comfortable_limit:
                # Domain variety count karo
                domains = set(s['domain'] for s in combo)
                avg_match = sum(s.get('match_pct', 0) for s in combo) / len(combo)
                
                valid_combos.append({
                    'societies': combo,
                    'total_hrs': total_hrs,
                    'domain_variety': len(domains),
                    'avg_match': avg_match
                })
    
    if not valid_combos:
        return None, "No combination fits in comfortable zone - try adding more hours or removing societies ⚠️"
    
    # Rank karo: match% > domain variety > low hours
    valid_combos.sort(key=lambda x: (
        -x['avg_match'],      # match % high ho
        -x['domain_variety'], # domains varied hon
        x['total_hrs']        # hours kam hon
    ))
    
    # Top 3 return karo
    return valid_combos[:3], None

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
    
# ─── PEER MATCHING ────────────────────────────
def peer_matching(current_user_id, all_saved_data):
    """
    current_user_id: logged in user ka id
    
    all_saved_data: list of dicts — Supabase se aayega
    e.g. [
        {
            'user_id': 'u2',
            'name': 'Priya',
            'society_name': 'AI Club',
            'linkedin_url': 'linkedin.com/in/priya',
            'linkedin_share': True
        },
        ...
    ]
    
    Returns: dict — society wise peers
    e.g. {
        'AI Club': [
            {'name': 'Priya', 'linkedin_url': '...'},
            {'name': 'Sneha', 'linkedin_url': '...'}
        ],
        'NSS': [...]
    }
    """
    
    # Sirf opt-in users aur current user nahi
    filtered = [
        d for d in all_saved_data
        if d.get('linkedin_share') == True
        and d.get('user_id') != current_user_id
    ]
    
    # Society wise group karo
    society_peers = {}
    
    for entry in filtered:
        society = entry['society_name']
        
        if society not in society_peers:
            society_peers[society] = []
        
        # Duplicate user same society mein nahi aaye
        already_added = any(
            p['user_id'] == entry['user_id'] 
            for p in society_peers[society]
        )
        
        if not already_added:
            society_peers[society].append({
                'user_id': entry['user_id'],
                'name': entry['name'],
                'linkedin_url': entry['linkedin_url']
            })
    
    return society_peers


# ─── PEER MATCHING — FILTER BY USER SAVED ─────
def get_my_peers(current_user_id, current_user_saved, all_saved_data):
    """
    Sirf current user ki saved societies ke peers dikhao

    current_user_saved: list of society names current user ne save ki hain
    e.g. ['AI Club', 'NSS', 'Dance']
    """
    
    all_peers = peer_matching(current_user_id, all_saved_data)
    
    # Sirf current user ki societies filter karo
    my_peers = {
        society: peers
        for society, peers in all_peers.items()
        if society in current_user_saved
    }
    
    # Empty societies remove karo
    my_peers = {
        society: peers
        for society, peers in my_peers.items()
        if len(peers) > 0
    }
    
    if not my_peers:
        return None, "No peers found yet — check back later as more students join! 🙂"
    
    return my_peers, None

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
    combos, error = best_combinations(test_societies, 25)
    if error:
        print(error)
    else:
        for i, c in enumerate(combos):
            names = [s['name'] for s in c['societies']]
            print(f"Combo {i+1}: {names} | {c['total_hrs']}hrs | {c['avg_match']}% match")

    # Peer matching test
    test_all_saved = [
        {'user_id': 'u2', 'name': 'Priya', 'society_name': 'AI Club',
         'linkedin_url': 'linkedin.com/in/priya', 'linkedin_share': True},
        {'user_id': 'u3', 'name': 'Sneha', 'society_name': 'NSS',
         'linkedin_url': 'linkedin.com/in/sneha', 'linkedin_share': True},
        {'user_id': 'u4', 'name': 'Riya', 'society_name': 'AI Club',
         'linkedin_url': 'linkedin.com/in/riya', 'linkedin_share': False},
        {'user_id': 'u5', 'name': 'Ananya', 'society_name': 'Dance',
         'linkedin_url': 'linkedin.com/in/ananya', 'linkedin_share': True},
    ]
    
    current_user_saved = ['AI Club', 'NSS', 'Dance']
    
    peers, error = get_my_peers('u1', current_user_saved, test_all_saved)
    if error:
        print(error)
    else:
        for society, people in peers.items():
            print(f"\nThese people are interested in the same society as you \n 🎯{society}")
            for p in people:
                print(f"   → {p['name']} — {p['linkedin_url']}")

