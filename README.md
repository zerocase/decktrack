# Deck | Track

**Note** : **Deck | Track** is currently in alpha and still being developed to incorporate new features and improve upon the existing ones.

- **Create & Manage Collections** - Whether you have purchased and downloaded an album from your favourite artist or a playlist on Spotify, **Deck | Track** works as a bridge between the many sources of music, allowing you to convert between them seamlessly.
- **Local Track Analysis** - You can analyse tracks that you have locally using algorithms similar to the analysis data you can get from the Spotify api.
- **Sorting** - Sort your tracks depending on different values that you have inferred from the analysis.

## What do you get from analysis?

### | Duration | Key | BPM | Loudness | Danceability | Energy (rms)|

## Getting Started

The current **Deck | Track** GUI looks like this:
![Pasted image 20230615224224](https://github.com/zerocase/decktrack/assets/32014360/aeefcd87-20b3-44d3-bcf5-b17588dbe757)

There are currently two main tabs.
- Collections List - is a list with all of the current Collections that are created and/or imported into **Deck | Track**.
- Tracks Table - is a table made of rows where each row corresponds to a specific track there you can view and sort the different tracks depending on what element you want to sort by.

### Adding a Collection

- You can add a collection by either clicking the **[ + ]** button or through the top menu by going to
**File** > **New** > **Collection by folder**.

- A new window will show up allowing you to browse and find the specific folder you're looking for.

![Pasted image 20230615225426](https://github.com/zerocase/decktrack/assets/32014360/f82dc5aa-2c19-47d5-bb23-5f2bd3ab625e)

- After you've selected the desired folder, click on **Ok**.
- Another window will popup asking if you want to analyse the tracks.

![Pasted image 20230615225656](https://github.com/zerocase/decktrack/assets/32014360/931e558c-6969-4345-ae58-2c5a74532f10)

- If you want to see the analysis data then you can click on **Yes**, however this will take some time depending on your computer's speed. You can also analyse Collections after you've added them to **Deck | Track**

**Note:** In the future you will be able to add playlists from most of the popular music streaming or downloading of tracks such as Bandcamp.

## Modify Menu

Clicking on the **Three Dots** next to the + button will show a menu with options.

- Clicking **Analyse** will start the analysis process for the selected collection.
- Clicking **Delete** will remove the collection and the analysed data.

![Pasted image 20230615230141](https://github.com/zerocase/decktrack/assets/32014360/a66593e0-bf2a-40e3-ad16-b9bbdfebc081)

You can also do these steps from the menu at the top.
- **File** > **Analyse**
- **File** > **Delete**
