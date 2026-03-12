from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY

from departments.jkssb import crawl_jkssb
from departments.gad import crawl_gad


# ==========================
# SUPABASE CONNECTION
# ==========================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ==========================
# SAVE FUNCTION
# ==========================

def save_notification(department, title, link):

    data = {
        "department": department,
        "title": title,
        "link": link
    }

    try:

        supabase.table("notifications").insert(data).execute()

        print("Inserted:", title)

    except Exception:

        print("Duplicate skipped:", title)


# ==========================
# MAIN CRAWLER
# ==========================

def main():

    print("\nStarting Crawlers...\n")

    crawl_jkssb(save_notification)

    crawl_gad(save_notification)

    print("\nCrawling Finished\n")


if __name__ == "__main__":
    main()