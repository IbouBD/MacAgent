### phase 1
phase1 = [
    # Safari - Navigation web
    ("Can you please open the Safari browser for me?", "Safari", None),
    ("I want to check something online, open Safari.", "Safari", None),
    ("Launch Safari so I can browse the web.", "Safari", None),
    ("Fire up Safari browser.", "Safari", None),
    ("I need to go online, start Safari.", "Safari", None),
    ("Open Safari to search for something.", "Safari", None),
    ("Launch the web browser Safari.", "Safari", None),
    ("Can you start Safari for web browsing?", "Safari", None),
    
    # Terminal - Ligne de commande
    ("Fire up the terminal, please.", "Terminal", None),
    ("I need to run some commands, open Terminal.", "Terminal", None),
    ("Launch Terminal application.", "Terminal", None),
    ("Open the command line interface.", "Terminal", None),
    ("Start Terminal so I can execute commands.", "Terminal", None),
    ("Can you open Terminal for me?", "Terminal", None),
    ("I want to use the terminal, launch it.", "Terminal", None),
    ("Fire up the command prompt.", "Terminal", None),
    
    # System Settings - Préférences système
    ("Take me to the system preferences.", "System Settings", None),
    ("Open System Settings please.", "System Settings", None),
    ("I need to change some settings, open System Settings.", "System Settings", None),
    ("Launch the system preferences.", "System Settings", None),
    ("Can you open the settings panel?", "System Settings", None),
    ("I want to configure something, open System Settings.", "System Settings", None),
    ("Fire up System Settings.", "System Settings", None),
    ("Take me to the configuration panel.", "System Settings", None),
    
    # Mail - Messagerie, ne fonctionne pas non plus dans la vm, allez savoir pourquoi
    #("Check for new emails — open Mail.", "Mail"),
    #("I want to read my emails, launch Mail.", "Mail"),
    #("Open the Mail application.", "Mail"),
    #("Fire up Mail to check messages.", "Mail"),
    #("Launch Mail so I can send an email.", "Mail"),
    #("I need to check my inbox, open Mail.", "Mail"),
    #("Start the email client.", "Mail"),
    #("Can you open Mail for me?", "Mail"),
    
    # Maps - Cartes et navigation
    ("I need directions, open Maps.", "Maps", None),
    ("Launch Maps application.", "Maps", None),
    ("Fire up Maps to find a location.", "Maps", None),
    ("Open Maps so I can navigate somewhere.", "Maps", None),
    ("I want to check a route, start Maps.", "Maps", None),
    ("Can you open Maps for me?", "Maps", None),
    ("Launch the navigation app.", "Maps", None),
    ("I need to find an address, open Maps.", "Maps", None),
    
    # Finder - Gestionnaire de fichiers
    ("Open Finder to browse files.", "Finder", None),
    ("I need to find a file, launch Finder.", "Finder", None),
    ("Fire up the file manager.", "Finder", None),
    ("Launch Finder please.", "Finder", None),
    ("Can you open Finder so I can navigate folders?", "Finder", None),
    ("I want to browse my files, open Finder.", "Finder", None),
    ("Start the file browser.", "Finder", None),
    ("Take me to the file explorer.", "Finder", None),
    
    # Notes - Prise de notes
    ("I want to write something down, open Notes.", "Notes", None),
    ("Launch Notes application.", "Notes", None),
    ("Fire up Notes so I can take notes.", "Notes", None),
    ("Open Notes to jot something down.", "Notes", None),
    ("I need to make a note, start Notes.", "Notes", None),
    ("Can you open the Notes app?", "Notes", None),
    ("Launch the note-taking app.", "Notes", None),
    ("I want to create a note, open Notes.", "Notes", None),
    
    # Calculator - Calculatrice
    ("I need to do some math, open Calculator.", "Calculator", None),
    ("Launch Calculator application.", "Calculator", None),
    ("Fire up the calculator.", "Calculator", None),
    ("Open Calculator so I can compute something.", "Calculator", None),
    ("I want to calculate something, start Calculator.", "Calculator", None),
    ("Can you open Calculator for me?", "Calculator", None),
    ("Launch the math calculator.", "Calculator", None),
    ("I need to crunch some numbers, open Calculator.", "Calculator", None),
    
    # TextEdit - Éditeur de texte
    ("Open TextEdit to write a document.", "TextEdit", None),
    ("I want to create a text file, launch TextEdit.", "TextEdit", None),
    ("Fire up TextEdit.", "TextEdit", None),
    ("Launch the text editor.", "TextEdit", None),
    ("I need to edit a document, open TextEdit.", "TextEdit", None),
    ("Can you start TextEdit for me?", "TextEdit", None),
    ("Open TextEdit so I can type something.", "TextEdit", None),
    ("I want to write a document, launch TextEdit.", "TextEdit", None),
    
    # Calendar - Calendrier
    ("Check my schedule, open Calendar.", "Calendar", None),
    ("I want to see my appointments, launch Calendar.", "Calendar", None),
    ("Fire up Calendar application.", "Calendar", None),
    ("Open Calendar to check my events.", "Calendar", None),
    ("Launch Calendar so I can schedule something.", "Calendar", None),
    ("I need to check my calendar, open Calendar.", "Calendar", None),
    ("Can you start Calendar for me?", "Calendar", None),
    ("I want to see my agenda, launch Calendar.", "Calendar", None),
    
    # Photos - Gestionnaire de photos
    ("I want to view my pictures, open Photos.", "Photos", None),
    ("Launch Photos application.", "Photos", None),
    ("Fire up Photos to see my images.", "Photos", None),
    ("Open Photos so I can browse my pictures.", "Photos", None),
    ("I need to find a photo, start Photos.", "Photos", None),
    ("Can you open Photos for me?", "Photos", None),
    ("Launch the photo viewer.", "Photos", None),
    ("I want to look at my photos, open Photos.", "Photos", None),
    
    # Music - Lecteur musical
    ("I want to listen to music, open Music.", "Music", None),
    ("Launch Music application.", "Music", None),
    ("Fire up the music player.", "Music", None),
    ("Open Music so I can play songs.", "Music", None),
    ("I need some music, start Music.", "Music", None),
    ("Can you open Music for me?", "Music", None),
    ("Launch the audio player.", "Music", None),
    ("I want to play some tunes, open Music.", "Music", None),
    
    # Preview - Visionneuse de documents, ne fonctionne pas dans la vm pour une certaine raison...
    #("I need to view a document, open Preview.", "Preview"),
    #("Launch Preview application.", "Preview"),
    #("Fire up Preview to see a file.", "Preview"),
    #("Open Preview so I can read a PDF.", "Preview"),
    #("I want to view an image, start Preview.", "Preview"),
    #("Can you open Preview for me?", "Preview"),
    #("Launch the document viewer.", "Preview"),
    #("I need to check a file, open Preview.", "Preview"),
    
    # App Store - Magasin d'applications
    ("I want to download an app, open App Store.", "App Store", None),
    ("Launch App Store application.", "App Store", None),
    ("Fire up the App Store.", "App Store", None),
    ("Open App Store to find software.", "App Store", None),
    ("I need to install an app, start App Store.", "App Store", None),
    ("Can you open App Store for me?", "App Store", None),
    ("Launch the application store.", "App Store", None),
    ("I want to browse apps, open App Store.", "App Store", None),
    
    # Activity Monitor - Moniteur d'activité
    ("Check system performance, open Activity Monitor.", "Activity Monitor", None),
    ("I want to see running processes, launch Activity Monitor.", "Activity Monitor", None),
    ("Fire up Activity Monitor.", "Activity Monitor", None),
    ("Open Activity Monitor to check CPU usage.", "Activity Monitor", None),
    ("I need to monitor the system, start Activity Monitor.", "Activity Monitor", None),
    ("Can you open Activity Monitor for me?", "Activity Monitor", None),
    ("Launch the task manager.", "Activity Monitor", None),
    ("I want to see system resources, open Activity Monitor.", "Activity Monitor", None),
    
    # Console - Console système
    ("I need to check logs, open Console.", "Console", None),
    ("Launch Console application.", "Console", None),
    ("Fire up Console to see system messages.", "Console", None),
    ("Open Console so I can debug something.", "Console", None),
    ("I want to view system logs, start Console.", "Console", None),
    ("Can you open Console for me?", "Console", None),
    ("Launch the log viewer.", "Console", None),
    ("I need to troubleshoot, open Console.", "Console", None),
]

phase2 = [
    # Safari - Recherche et navigation web
    ("I need to search for information on the web.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I want to look up something using a search engine.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I need to visit a website to research a topic.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I want to use Google to find information.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I need to browse the internet for answers.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I want to check a specific website online.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I need to do some online research.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I want to shop online on a website.", "Safari", ["Chrome", "Firefox", "Edge"]),
    
    # Terminal - Tâches système et développement
    ("I need to execute commands in the command line.", "Terminal", ["iTerm2", "Hyper"]),
    ("I want to run a script using the terminal.", "Terminal", ["iTerm2", "Hyper"]),
    ("I need to use command line tools.", "Terminal", ["iTerm2", "Hyper"]),
    ("I want to navigate directories using terminal commands.", "Terminal", ["iTerm2", "Hyper"]),
    ("I need to install software using command line.", "Terminal", ["iTerm2", "Hyper"]),
    ("I want to check network status with terminal commands.", "Terminal", ["iTerm2", "Hyper"]),
    ("I need to run terminal commands for development.", "Terminal", ["iTerm2", "Hyper", "VS Code"]),
    ("I want to debug using command line interface.", "Terminal", ["iTerm2", "Hyper", "VS Code"]),
    
    # System Settings - Configuration système
    ("I need to modify my Mac's display configuration.", "System Settings", None),
    ("I want to change my network settings on Mac.", "System Settings", None),
    ("I need to adjust my privacy settings in macOS.", "System Settings", None),
    ("I want to configure security options on my Mac.", "System Settings", None),
    ("I need to customize my keyboard shortcuts in macOS.", "System Settings", None),
    ("I want to update my user account settings.", "System Settings", None),
    ("I need to manage my notification preferences.", "System Settings", None),
    ("I want to adjust my Mac's audio settings.", "System Settings", None),
    
    # Weather - Météo et prévisions
    ("I need to check today's weather forecast.", "Weather", ["Safari"]),
    ("I want to see if it will rain tomorrow.", "Weather", ["Safari"]),
    ("I need to know the temperature outside.", "Weather", ["Safari"]),
    ("I want to check the weather for this weekend.", "Weather", ["Safari"]),
    ("I need to see the hourly weather forecast.", "Weather", ["Safari"]),
    ("I want to check weather conditions for my trip.", "Weather", ["Safari"]),
    ("I need to know if I should bring an umbrella.", "Weather", ["Safari"]),
    ("I want to see the weekly weather outlook.", "Weather", ["Safari"]),
    
    # Finder - Gestion de fichiers
    ("I need to locate a file stored on my Mac.", "Finder", ["Path Finder", "Commander One"]),
    ("I want to organize files and folders on my computer.", "Finder", ["Path Finder", "Commander One"]),
    ("I need to browse my Downloads folder.", "Finder", ["Path Finder", "Commander One"]),
    ("I want to navigate to a specific folder location.", "Finder", ["Path Finder", "Commander One"]),
    ("I need to manage files on my desktop.", "Finder", ["Path Finder", "Commander One"]),
    ("I want to move files between different folders.", "Finder", ["Path Finder", "Commander One"]),
    ("I need to check available storage space on my Mac.", "Finder", ["Path Finder", "Commander One", "DiskSight"]),
    ("I want to access an external drive or USB.", "Finder", ["Path Finder", "Commander One"]),
    
    # Notes - Prise de notes et mémos
    ("I need to write down thoughts in a note-taking app.", "Notes", ["Notion", "Obsidian", "Bear"]),
    ("I want to create a list using the Notes application.", "Notes", ["Notion", "Obsidian", "Bear", "Todoist"]),
    ("I need to take notes during a meeting.", "Notes", ["Notion", "Obsidian", "Bear", "Evernote"]),
    ("I want to save important information in a note.", "Notes", ["Notion", "Obsidian", "Bear", "Evernote"]),
    ("I need to draft text using the Notes app.", "Notes", ["TextEdit", "Notion", "Obsidian"]),
    ("I want to organize my ideas in digital notes.", "Notes", ["Notion", "Obsidian", "Bear"]),
    ("I need to create a quick memo for myself.", "Notes", ["TextEdit", "Stickies"]),
    ("I want to make a checklist in the Notes app.", "Notes", ["Notion", "Todoist", "Things"]),
    
    # Calculator - Calculs et mathématiques
    ("I need to perform mathematical calculations.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I want to calculate a tip percentage.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I need to do arithmetic operations quickly.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I want to convert units using calculations.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I need to compute my budget numbers.", "Calculator", ["Numi", "Soulver", "Numbers"]),
    ("I want to calculate percentages and ratios.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I need to solve basic math problems.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I want to add up expenses and costs.", "Calculator", ["Numi", "Soulver", "Numbers"]),
    
    # TextEdit - Édition de documents
    ("I need to create a text document for writing.", "TextEdit", ["Microsoft Word", "Notes", "Pages"]),
    ("I want to write a document using a text editor.", "TextEdit", ["Microsoft Word", "Notes", "Pages"]),
    ("I need to edit a plain text file.", "TextEdit", ["VS Code", "Sublime Text", "Vim"]),
    ("I want to create a formatted document.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    ("I need to write instructions in a text document.", "TextEdit", ["Microsoft Word", "Notes", "Pages"]),
    ("I want to create a simple word document.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    ("I need to format text in a document editor.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    ("I want to prepare a document for sharing.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    
    # Calendar - Planification et organisation
    ("I need to schedule an appointment in my calendar.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I want to check my calendar for tomorrow's events.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I need to set a reminder for an upcoming event.", "Calendar", ["Google Calendar", "Outlook", "Fantastical", "Reminders"]),
    ("I want to view my calendar schedule.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I need to plan my week using the calendar app.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I want to create a new calendar event.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I need to check my availability in the calendar.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I want to organize my schedule using the calendar.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    
    # Photos - Gestion d'images
    ("I want to view my photo library and albums.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I need to find a specific photo in my collection.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I want to organize my photos into albums.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I need to edit a photo using the Photos app.", "Photos", ["Adobe Lightroom", "Pixelmator Pro", "Photoshop"]),
    ("I want to share photos from my photo library.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I need to create a photo album collection.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I want to delete unwanted photos from my library.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I need to export photos from the Photos app.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    
    # Music - Écoute musicale
    ("I want to play music from my music library.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I need to listen to songs while working.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I want to discover new music in the Music app.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I need to play relaxing music from my library.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I want to create a playlist in the Music app.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I need to listen to a specific album.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I want to shuffle my music collection.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I need to play energetic music for motivation.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    
    # Preview - Visualisation de documents
    #("I need to open and view a PDF document.", "Preview", ["Adobe Acrobat", "PDF Expert", "Skim"]),
    #("I want to look at an image file using Preview.", "Preview", ["Adobe Photoshop", "Pixelmator Pro", "GIMP"]),
    #("I need to read a PDF manual or guide.", "Preview", ["Adobe Acrobat", "PDF Expert", "Skim"]),
    #("I want to view a scanned document.", "Preview", ["Adobe Acrobat", "PDF Expert", "Skim"]),
    #("I need to examine a PDF presentation.", "Preview", ["Adobe Acrobat", "PDF Expert", "Keynote"]),
    #("I want to look at a diagram or chart.", "Preview", ["Adobe Acrobat", "PDF Expert", "Skim"]),
    #("I need to sign a PDF document.", "Preview", ["Adobe Acrobat", "PDF Expert", "DocuSign"]),
    #("I want to annotate a PDF file.", "Preview", ["Adobe Acrobat", "PDF Expert", "Skim"]),
    
     #App Store - Recherche et installation d'applications
    ("I need to download apps from the Mac App Store.", "App Store", None),
    ("I want to find and install a new application.", "App Store", ["Safari", "Homebrew"]),
    ("I need to update my installed applications.", "App Store", None),
    ("I want to search for software in the App Store.", "App Store", ["Safari", "Homebrew"]),
    ("I need to browse available Mac applications.", "App Store", ["Safari", "Homebrew"]),
    ("I want to find a specific type of utility app.", "App Store", ["Safari", "Homebrew"]),
    ("I need to install software from the App Store.", "App Store", ["Safari", "Homebrew"]),
    ("I want to check for app updates in the store.", "App Store", None),
    
    # Activity Monitor - Surveillance système
    ("I want to monitor my Mac's CPU performance.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I need to check which apps are using my RAM.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I want to see my system's performance metrics.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I need to identify what's consuming system resources.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I want to monitor my Mac's memory usage.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I need to see which processes are currently running.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I want to check my Mac's battery consumption.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I need to force quit a frozen application.", "Activity Monitor", ["Force Quit Applications"]),
    
    # Console - Diagnostic et débogage
    ("I need to check system logs for error messages.", "Console", ["Terminal", "VS Code"]),
    ("I want to view system diagnostic information.", "Console", ["Terminal", "VS Code"]),
    ("I need to debug application crashes using logs.", "Console", ["Terminal", "VS Code", "Xcode"]),
    ("I want to investigate system error reports.", "Console", ["Terminal", "VS Code"]),
    ("I need to monitor system events and messages.", "Console", ["Terminal", "VS Code"]),
    ("I want to check application log files.", "Console", ["Terminal", "VS Code", "Xcode"]),
    ("I need to diagnose system issues using Console.", "Console", ["Terminal", "VS Code"]),
    ("I want to view background system activity logs.", "Console", ["Terminal", "VS Code"]),
    
    # Maps - Navigation et localisation
    ("I need to get driving directions to a location.", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("I want to find nearby businesses using Maps.", "Maps", ["Google Maps", "Yelp", "Safari"]),
    ("I need to check current traffic conditions.", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("I want to plan a route for my upcoming trip.", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("I need to explore a specific area on the map.", "Maps", ["Google Maps", "Safari"]),
    ("I want to search for an address location.", "Maps", ["Google Maps", "Safari"]),
    ("I need to estimate travel time to a destination.", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("I want to find public transit directions.", "Maps", ["Google Maps", "Citymapper", "Safari"]),
]

phase3 = [
    # Safari - Recherche et navigation web
    ("Can you help me find reviews for this restaurant?", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I want to compare prices for this product online.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("Let me check the latest news headlines.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I need to watch a tutorial video on YouTube.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("Can you open my favorite social media platform?", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I want to read articles about this topic.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("Help me find flight deals for my vacation.", "Safari", ["Chrome", "Firefox", "Edge"]),
    ("I need to access my online banking account.", "Safari", ["Chrome", "Firefox", "Edge"]),
    
    # Terminal - Tâches système et développement
    ("I want to check my current directory path.", "Terminal", ["iTerm2", "Hyper"]),
    ("Help me compress these files into an archive.", "Terminal", ["iTerm2", "Hyper"]),
    ("I need to check my system's disk usage.", "Terminal", ["iTerm2", "Hyper"]),
    ("Can you show me running processes?", "Terminal", ["iTerm2", "Hyper"]),
    ("I want to update my Homebrew packages.", "Terminal", ["iTerm2", "Hyper"]),
    ("Help me find files containing specific text.", "Terminal", ["iTerm2", "Hyper"]),
    ("I need to change file permissions.", "Terminal", ["iTerm2", "Hyper", "VS Code"]),
    ("Can you help me clone a Git repository?", "Terminal", ["iTerm2", "Hyper", "VS Code"]),
    
    # System Settings - Configuration système
    ("I want to change my Mac's wallpaper.", "System Settings", None),
    ("Can you help me set up a VPN connection?", "System Settings", None),
    ("I need to adjust my trackpad sensitivity.", "System Settings", None),
    ("Help me configure my external monitor.", "System Settings", None),
    ("I want to change my login password.", "System Settings", None),
    ("Can you help me manage my startup apps?", "System Settings", None),
    ("I need to adjust my screen brightness settings.", "System Settings", None),
    ("Help me configure my Bluetooth devices.", "System Settings", None),
    
    # Weather - Météo et prévisions
    ("What's the weather like right now?", "Weather", ["Safari"]),
    ("Should I plan outdoor activities this weekend?", "Weather", ["Safari"]),
    ("I need to know if it's going to be windy today.", "Weather", ["Safari"]),
    ("Can you check the UV index for this afternoon?", "Weather", ["Safari"]),
    ("Will there be snow in the mountains this week?", "Weather", ["Safari"]),
    ("I want to see the sunrise and sunset times.", "Weather", ["Safari"]),
    ("Is it a good day for a picnic tomorrow?", "Weather", ["Safari"]),
    ("Can you check the humidity levels today?", "Weather", ["Safari"]),
    
    # Finder - Gestion de fichiers
    ("Where did I save that presentation file?", "Finder", ["Path Finder", "Commander One"]),
    ("I need to empty my Trash folder.", "Finder", ["Path Finder", "Commander One"]),
    ("Can you help me create a new folder structure?", "Finder", ["Path Finder", "Commander One"]),
    ("I want to see my recent downloads.", "Finder", ["Path Finder", "Commander One"]),
    ("Help me backup these important documents.", "Finder", ["Path Finder", "Commander One"]),
    ("I need to find duplicate files on my Mac.", "Finder", ["Path Finder", "Commander One"]),
    ("Can you show me what's taking up storage space?", "Finder", ["Path Finder", "Commander One", "DiskSight"]),
    ("I want to organize my desktop files.", "Finder", ["Path Finder", "Commander One"]),
    
    # Notes - Prise de notes et mémos
    ("I need to jot down this phone number quickly.", "Notes", ["Notion", "Obsidian", "Bear"]),
    ("Can you help me create a shopping list?", "Notes", ["Notion", "Obsidian", "Bear", "Todoist"]),
    ("I want to write down my daily goals.", "Notes", ["Notion", "Obsidian", "Bear", "Evernote"]),
    ("Help me brainstorm ideas for my project.", "Notes", ["Notion", "Obsidian", "Bear", "Evernote"]),
    ("I need to save this recipe for later.", "Notes", ["TextEdit", "Notion", "Obsidian"]),
    ("Can you create a note with my meeting agenda?", "Notes", ["Notion", "Obsidian", "Bear"]),
    ("I want to write a quick reminder to myself.", "Notes", ["TextEdit", "Stickies"]),
    ("Help me track my daily habits.", "Notes", ["Notion", "Todoist", "Things"]),
    
    # Calculator - Calculs et mathématiques
    ("How much is 15% of my restaurant bill?", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I need to split the cost between 4 people.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("Can you help me calculate my mortgage payment?", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I want to convert miles to kilometers.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("Help me figure out my monthly savings rate.", "Calculator", ["Numi", "Soulver", "Numbers"]),
    ("What's 30% off this original price?", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("I need to calculate the area of this room.", "Calculator", ["Numi", "Soulver", "PCalc"]),
    ("Can you help me total up these receipts?", "Calculator", ["Numi", "Soulver", "Numbers"]),
    
    # TextEdit - Édition de documents
    ("I want to draft an email response.", "TextEdit", ["Microsoft Word", "Notes", "Pages"]),
    ("Can you help me write a quick letter?", "TextEdit", ["Microsoft Word", "Notes", "Pages"]),
    ("I need to edit this configuration file.", "TextEdit", ["VS Code", "Sublime Text", "Vim"]),
    ("Help me create a professional resume.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    ("I want to write down my thoughts clearly.", "TextEdit", ["Microsoft Word", "Notes", "Pages"]),
    ("Can you help me format this report?", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    ("I need to create a simple flyer design.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    ("Help me write a cover letter for this job.", "TextEdit", ["Microsoft Word", "Pages", "Google Docs"]),
    
    # Calendar - Planification et organisation
    ("What do I have planned for next Monday?", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("Can you block time for my gym session?", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I need to reschedule my doctor appointment.", "Calendar", ["Google Calendar", "Outlook", "Fantastical", "Reminders"]),
    ("Let's check my availability this week.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("Help me plan my vacation days.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("I want to set up a recurring meeting.", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("When is my next free slot today?", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    ("Can you help me organize my work schedule?", "Calendar", ["Google Calendar", "Outlook", "Fantastical"]),
    
    # Photos - Gestion d'images
    ("Can you show me last weekend's photos?", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I want to find photos from my vacation.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("Help me create a slideshow of family photos.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I need to enhance the lighting in this photo.", "Photos", ["Adobe Lightroom", "Pixelmator Pro", "Photoshop"]),
    ("Can you help me send photos to my family?", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I want to make a photo book collection.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("Help me free up space by removing blurry photos.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    ("I need to save these photos to an external drive.", "Photos", ["Adobe Lightroom", "Pixelmator Pro"]),
    
    # Music - Écoute musicale
    ("Can you play some background music for work?", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I want to hear my favorite songs from the 90s.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("Help me find new artists similar to this one.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I need calming music for meditation.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("Can you make a workout playlist for me?", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I want to listen to this entire album.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("Help me discover today's popular hits.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    ("I need upbeat music to boost my energy.", "Music", ["Spotify", "YouTube Music", "Amazon Music"]),
    
    # App Store - Recherche et installation d'applications
    ("I need a better photo editing app.", "App Store", None),
    ("Can you help me find a productivity tool?", "App Store", ["Safari", "Homebrew"]),
    ("My apps need to be updated to latest versions.", "App Store", None),
    ("I want to discover top-rated Mac applications.", "App Store", ["Safari", "Homebrew"]),
    ("Help me find free alternatives to expensive software.", "App Store", ["Safari", "Homebrew"]),
    ("I need a good password manager app.", "App Store", ["Safari", "Homebrew"]),
    ("Can you install this development tool for me?", "App Store", ["Safari", "Homebrew"]),
    ("I want to see what's new in the store today.", "App Store", None),
    
    # Activity Monitor - Surveillance système
    ("Why is my Mac running so slowly today?", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("Can you show me what's draining my battery?", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I think an app is frozen - help me check.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("Is my computer overheating right now?", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("Help me see which apps use the most memory.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("Can you monitor my network activity?", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("I want to check my Mac's overall health status.", "Activity Monitor", ["iStat Menus", "MenuMeters", "Stats"]),
    ("This application won't close - can you force quit it?", "Activity Monitor", ["Force Quit Applications"]),
    
    # Console - Diagnostic et débogage
    ("My app keeps crashing - can you check the logs?", "Console", ["Terminal", "VS Code"]),
    ("I want to see what errors occurred today.", "Console", ["Terminal", "VS Code"]),
    ("Help me troubleshoot this software issue.", "Console", ["Terminal", "VS Code", "Xcode"]),
    ("Can you investigate why my Mac is acting weird?", "Console", ["Terminal", "VS Code"]),
    ("I need to monitor system performance messages.", "Console", ["Terminal", "VS Code"]),
    ("Help me debug this application's behavior.", "Console", ["Terminal", "VS Code", "Xcode"]),
    ("Can you check for hardware-related errors?", "Console", ["Terminal", "VS Code"]),
    ("I want to see what's happening behind the scenes.", "Console", ["Terminal", "VS Code"]),
    
    # Maps - Navigation et localisation
    ("Where am I right now?", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("Can you find the nearest coffee shop?", "Maps", ["Google Maps", "Yelp", "Safari"]),
    ("Is there heavy traffic on my usual route?", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("Help me plan the fastest route to the airport.", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("I want to explore restaurants in this neighborhood.", "Maps", ["Google Maps", "Yelp", "Safari"]),
    ("Can you locate this address for me?", "Maps", ["Google Maps", "Safari"]),
    ("How long will it take to get there by car?", "Maps", ["Google Maps", "Waze", "Safari"]),
    ("I need subway directions to downtown.", "Maps", ["Google Maps", "Citymapper", "Safari"]),
]