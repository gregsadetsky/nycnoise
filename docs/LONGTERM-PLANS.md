- potentially look into django only serving as an api and using a cdn-distributed next.js middle/frontend for the frontend (using netlify?)
- the site could send emails? like an email calendar? with events for the next days? this requires coordination with Jessica as events get updated very frequently
- more/better devops
  - deploy `dev` branch to separate domain with own database
  - deploy PR previews i.e. each PR gets its own deployment url+database
- connect site in search console -- monitor new site issues/suggestions
- venues should have a default age/access value BUT every event should be able to optionally override those values
- venues could have an 'affiliation' either pop-up or checkbox or something to note that they are ticketmaster or AEG -- then, there could be a filter on the homepage (default on or off) to hide events related to those venues
- when we figure out a good way of having "extra" information that maybe is only revealed on click -- it might be a good idea to have many extra/optional links per event. this would allow for an event to have all the links to the artists' homepages+bandcamps, etc.
- a lot more calendar integrations -- we can really go wild here :-)
  - first, ability to see ALL nycnoise events in an ical feed
  - then, offer the ability to 'star' events on nycnoise (like on craigslist! -- https://www.craigslist.org/about/help/favorites) and then only see those events in the ical feed!! we'd have to talk/think about sessions/logins here, or do it all cookie/temporary session based...? more discussion is needed here
- have ability to mark events that you went to, and then go to page to see all shows you attended
- "remind me" option to get a text or email x hours prior to the show (email - possible! notifications - using PWA!)
- PWA !!!!!!!!!!!!!!!!
  - because, notifications!
  - and home screen!
  - and offline!
  - gps/show events close to me, etc.
- map/venues/locations -- ability to see closest subway station(s)? (per event)
- ticketing
