"""
One-time (re-runnable) script to generate AI-polished "About"
paragraphs for every society and save them into the `societies`
table, in a new `ai_about` column.

Why this exists: generating the paragraph live on every page load was
slow (an AI call per society, every time) and fragile (if the API
failed, users saw a broken/dull fallback). This script does the AI
call ONCE per society and persists the result, so the app never has
to call the AI at runtime — Recommendation.py just reads `ai_about`
directly from the database, which is instant.

USAGE:
    python generate_society_blurbs.py            # only fills societies
                                                    # missing ai_about
    python generate_society_blurbs.py --force     # regenerates ALL of
                                                    # them, even ones that
                                                    # already have a value
                                                    # (use after editing
                                                    # description/activities/
                                                    # other_aspects for a
                                                    # society)

REQUIRES:
    1. The `societies` table must have an `ai_about` column (type:
       text, nullable). Add it once via Supabase's Table Editor — no
       SQL needed: open the `societies` table → "+" to add a column →
       name it `ai_about`, type `text`, leave it nullable.
    2. A SUPABASE_SERVICE_ROLE_KEY in your .env — the regular anon key
       can't write to this table (RLS blocks it silently, no error).
       Get it from: Supabase dashboard → Project Settings → API →
       service_role key. This is a powerful key — only use it here,
       never in the deployed app's secrets.
"""

import os
import sys

from dotenv import load_dotenv
from supabase import create_client

from ai_engine.society_blurb import generate_society_blurb

load_dotenv()


def get_admin_client():
    """
    This script needs to UPDATE the societies table, which RLS likely
    restricts to authenticated/admin roles — the regular anon-key
    client (used by the app for normal browsing) silently updates 0
    rows if RLS blocks it (no error is raised, which is why the first
    run showed "✅ Saved" for everything but nothing actually persisted).

    The service_role key bypasses RLS entirely. Get it from:
    Supabase dashboard → Project Settings → API → service_role key
    (NOT the anon/public key). Add it to .env as
    SUPABASE_SERVICE_ROLE_KEY — never put this key in the deployed
    app's secrets, it's for local admin scripts only.
    """

    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not service_key:
        print(
            "ERROR: SUPABASE_SERVICE_ROLE_KEY is not set in .env.\n"
            "This script needs the service_role key (not the anon key) "
            "to bypass RLS and actually persist updates.\n"
            "Get it from: Supabase dashboard → Project Settings → API "
            "→ service_role key, and add it to .env as "
            "SUPABASE_SERVICE_ROLE_KEY=<key>"
        )
        sys.exit(1)

    return create_client(url, service_key)


def main():
    force = "--force" in sys.argv

    supabase = get_admin_client()

    response = supabase.table("societies").select("*").execute()
    societies = response.data or []

    if not societies:
        print("No societies found — nothing to do.")
        return

    print(f"Found {len(societies)} societies.")

    generated = 0
    skipped = 0
    failed = 0

    for society in societies:
        name = society.get("society_name", "Unknown")

        already_has_one = bool(str(society.get("ai_about") or "").strip())

        if already_has_one and not force:
            print(f"  ⏭  Skipping '{name}' (already has ai_about)")
            skipped += 1
            continue

        print(f"  ⏳ Generating for '{name}'...")

        blurb = generate_society_blurb(
            society.get("society_name"),
            society.get("domain"),
            society.get("description"),
            society.get("activities"),
            society.get("other_aspects"),
        )

        if not blurb:
            print(f"  ❌ Failed for '{name}' (no info available, or AI call failed)")
            failed += 1
            continue

        supabase.table("societies").update(
            {"ai_about": blurb}
        ).eq("id", society["id"]).execute()

        print(f"  ✅ Saved for '{name}'")
        generated += 1

    print()
    print(f"Done. Generated: {generated}, Skipped: {skipped}, Failed: {failed}")


if __name__ == "__main__":
    main()