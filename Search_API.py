from apiclient.discovery import build
from oauth2client.tools import argparser
from apiclient.errors import HttpError
import gdata.youtube
import gdata.youtube.service

DEVELOPER_KEY = "AIzaSyA6AyVvbP8lRSCDFrnBIOBBU3vnkCJ31OU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options,TEXT):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
	search_response = youtube.search().list(
    q=TEXT,
    type="video",
    location=options.location,
    locationRadius=options.location_radius,
    part="id,snippet",
    maxResults=options.max_results
	).execute()

	search_videos = []

  # Merge video ids
	for search_result in search_response.get("items", []):
		search_videos.append(search_result["id"]["videoId"])
  		video_ids = ",".join(search_videos)

	video_response = youtube.videos().list(
    	id=video_ids,
    	part='snippet, recordingDetails, statistics, contentDetails,id'
  	).execute()

	videos = []

	# Add each result to the list, and then display the list of matching videos.
  	for video_result in video_response.get("items", []):
		#videos.append("title: %s\n likes: %s\n location: (%s,%s)" % (video_result["snippet"]["title"],video_result["statistics"]["likeCount"],video_result["recordingDetails"]["location"]["latitude"],video_result["recordingDetails"]["location"]["longitude"]))
		print "title:"+ video_result["snippet"]["title"]
		print "URL: " + "https://www.youtube.com/watch?v="+video_result["id"]
		print "likes:" + video_result["statistics"]["likeCount"]
		print "dislikes:" + video_result["statistics"]["dislikeCount"]
		print "viewCount:" + video_result["statistics"]["viewCount"]
		print "favoriteCount: " + video_result["statistics"]["favoriteCount"]
		print "commentCount: " + video_result["statistics"]["commentCount"]
		print "location: " ,video_result["recordingDetails"]["location"]["latitude"],video_result["recordingDetails"]["location"]["longitude"]
		print "duration: " , video_result["contentDetails"]["duration"]
		print 
  		# print "Videos:\n", "\n".join(videos), "\n"

if __name__ == "__main__":
	qq = raw_input("What's you want to search? ")
	yt_service = gdata.youtube.service.YouTubeService()
	yt_service.email = 'thushaninipu92@gmail.com'
	yt_service.password = 'anjel0775803676'
	yt_service.source = 'my-example-application'
	yt_service.ProgrammaticLogin()
	argparser.add_argument("--q", help="Search term", default="Google")
	argparser.add_argument("--location", help="Location", default="37.42307,-122.08427")
	argparser.add_argument("--location-radius", help="Location radius", default="10km")
	argparser.add_argument("--max-results", help="Max results", default=50)
	args = argparser.parse_args()

	try:
		youtube_search(args,qq)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)