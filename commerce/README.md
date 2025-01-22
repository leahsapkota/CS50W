CS50W Commerce Project-2

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

OBJECTIVE: 
The e-commerce auction site will provide a dynamic platform for users to create, bid on,
and track auction listings. Users can register securely, log in, and access personalized dashboards 
showing their created listings, watchlist items, and bidding history.Sellers can post auction 
listings by providing item details such as title, description, starting bid, category, and optional images. 
Each listing will display the highest bid, number of bids, and a countdown timer for the auction's end, fostering engagement and competition.
Buyers can place bids, with the system accepting only bids higher than the current highest. A “watchlist” feature allows users to save
and monitor listings of interest, while commenting on listings enables community interaction. This platform combines functionality and
user engagement to create an intuitive auction experience.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Youtube video link: https://www.youtube.com/watch?v=0KsbDMmeHM4
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Requirements for this project:
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Models:
Your application should have at least three models in addition to the User model,
Listings: Stores details about items being auctioned, such as title, description, starting bid, category, and optional images.
Bids: Tracks user bids, including the bid amount, bidder, and associated listing.
Comments: Saves user comments with fields for the comment text, author, and related listing.
You can add more models if needed for additional features.

2.Create Listing:
Users should have access to a page where they can create new listings. On this page, they can enter a title, a text description,
and set a starting bid for the listing. Additionally, users can optionally include an image by providing its URL and select a category, such as Fashion, Toys, Electronics, or Home.

3.Active Listings Page:
The homepage of your web application should show all currently active auction listings.
Each listing displayed should include, at a minimum, the title, description, current price, and a photo if one is available. This ensures users can easily browse all active items.

4.Listing Page:
Clicking a listing opens a detailed page for that item, showing all its information,
including the current price. Signed-in users can add or remove the item from their watchlist.
They can also place bids, which must meet or exceed the starting bid and outbid any current offers.
If the bid is invalid, an error is shown. The creator of the listing can close the auction,
marking the highest bidder as the winner and deactivating the listing. On closed listings, winners are notified. Signed-in users can post comments, and the page displays all comments on the listing.

5.Watchlist:
Signed-in users can access a Watchlist page showing all the listings they’ve added. Clicking on a listing from the Watchlist will take the user to the specific page for that item.

6.Categories:
Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

7.Django Admin Interface:
In the Django admin interface, site administrators should have the ability to view, add, edit, and delete any listings, comments, or bids on the site.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
I've completed all the requirements for this Commerce project, Thank you!
