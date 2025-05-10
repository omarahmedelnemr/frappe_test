import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_all_posts(category=None, limit=10):
    # print("Hello")
    # print(frappe.local.request.headers)
    # print(frappe.local.response)
     # Set CORS headers for the actual response
    # frappe.local.response['headers']['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'  # or '*' to allow all origins
    # frappe.local.response['headers']['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    # frappe.local.response['headers']['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

    filters = {}
    if category:
        filters["category"] = category

    # Fetch posts with the required fields and limit
    posts = frappe.get_all("post", 
                           filters=filters,
                           fields=["name", "title", "user", "published_at", "preview"], 
                           order_by="modified desc",
                           limit_page_length=limit)

    # Loop through the posts to add user data
    for post in posts:
        if post.get("user"):
            # Get the user details using the `user` field, which references the "auther" doctype
            user = frappe.get_doc("auther", post.user)
            post.user = {
                "name": user.name,
                "bio": user.bio,
                "Profile Image": user.profile_image
            }
    print(posts)
    return posts
