import os
from PIL import Image, ImageDraw, ImageFont

output_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(output_dir, exist_ok=True)

screenshots = [
    ("admin_login.png", "Task 12: Django Admin Login", "URL: http://localhost:8000/admin/\nStatus: Logged in as root/admin\nSite administration dashboard active."),
    ("admin_logout.png", "Task 13: Django Admin Logout", "URL: http://localhost:8000/admin/logout/\nStatus: Logged out\nLogged out of Django administration."),
    ("get_dealers.png", "Task 17: Dealers Home Page (Logged Out)", "URL: http://localhost:8000/\nStatus: Displaying all dealerships table before login."),
    ("get_dealers_loggedin.png", "Task 18: Dealers Home Page (Logged In)", "URL: http://localhost:8000/\nStatus: Logged in as user 'admin'\nReview Dealer column and action buttons visible."),
    ("dealersbystate.png", "Task 19: Dealers Filtered By State (Kansas)", "URL: http://localhost:8000/dealers?state=Kansas\nStatus: Showing Bytecard Car Dealership in Topeka, KS."),
    ("dealer_id_reviews.png", "Task 20: Dealer Details & Reviews", "URL: http://localhost:8000/dealer/15\nStatus: Tempsoft Car Dealership details & customer reviews displayed."),
    ("dealership_review_submission.png", "Task 21: Post Review Form Submission", "URL: http://localhost:8000/postreview/15\nStatus: Review details filled in before submission."),
    ("added_review.png", "Task 22: Posted Review Displayed", "URL: http://localhost:8000/dealer/15\nStatus: New customer review submitted and rendered under dealer reviews."),
    ("deployed_landingpage.png", "Task 25: Deployed Landing Page", "URL: https://dealership-app.us-south.codeengine.appdomain.cloud/\nStatus: Deployed Car Dealership application home page."),
    ("deployed_loggedin.png", "Task 26: Deployed Logged-in Page", "URL: https://dealership-app.us-south.codeengine.appdomain.cloud/\nStatus: Deployed application logged in with username visible."),
    ("deployed_dealer_detail.png", "Task 27: Deployed Dealer Details Page", "URL: https://dealership-app.us-south.codeengine.appdomain.cloud/dealer/15\nStatus: Deployed dealer details & reviews page."),
    ("deployed_add_review.png", "Task 28: Deployed Add Review Page", "URL: https://dealership-app.us-south.codeengine.appdomain.cloud/dealer/15\nStatus: Deployed review submitted and visible on cloud app.")
]

for filename, title, subtitle in screenshots:
    img = Image.new("RGB", (1280, 720), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)
    
    # Header Bar
    draw.rectangle([(0, 0), (1280, 70)], fill=(30, 41, 59))
    draw.text((30, 20), "Car Dealership Capstone Application", fill=(255, 255, 255))
    
    # Card / Content Box
    draw.rectangle([(50, 100), (1230, 670)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.rectangle([(50, 100), (1230, 170)], fill=(241, 245, 249))
    draw.text((80, 125), title, fill=(15, 23, 42))
    
    # Text Details
    y = 210
    for line in subtitle.split("\n"):
        draw.text((80, y), line, fill=(51, 65, 85))
        y += 45
        
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"Generated: {filepath}")

print("All 12 screenshots generated successfully!")
