from supabase import create_client

SUPABASE_URL = "https://tnphdphfrayejvzmgtrd.supabase.co"
SUPABASE_KEY = "sb_publishable_iR3SqKqZeFqFGV3XuVy-MA_QOCZm2bH"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)