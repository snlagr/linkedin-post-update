import requests, json, time

# this will be common for both fetching & editing
# may need to update after some time by capturing another manual request?
headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'csrf-token': 'enter your token here',
    'cookie': 'paste your cookies here',
}

# find this by manually & update for each post
threadUrn = 'urn:li:activity:xxxxxxxxxxxxxxxxxxx'
thread2 = 'urn:li:share:xxxxxxxxxxxxxxxxxx'

# remember to update that activity number as per the post
params = (
    ('count', '3'),
    ('q', 'reactionType'),
    ('sortOrder', 'REV_CHRON'),
    ('start', '0'),
    ('threadUrn', threadUrn),
)

prev_likes = 0

while True:
    # extract latest liked person's name
    # print("Finding new likes...")
    response = requests.get('https://www.linkedin.com/voyager/api/feed/reactions', headers=headers, params=params)
    res = json.loads(response.text)
    
    # these should be in a array, refactor later
    name1 = res['included'][3]['firstName'] + ' ' + res['included'][3]['lastName']
    name2 = res['included'][4]['firstName'] + ' ' + res['included'][4]['lastName']
    name3 = res['included'][5]['firstName'] + ' ' + res['included'][5]['lastName']

    profurn1 = res['included'][3]['entityUrn']
    profurn1 = "urn:li:fs_normalized_profile:" + profurn1[22:]
    profurn2 = res['included'][4]['entityUrn']
    profurn2 = "urn:li:fs_normalized_profile:" + profurn2[22:]
    profurn3 = res['included'][5]['entityUrn']
    profurn3 = "urn:li:fs_normalized_profile:" + profurn3[22:]

    start1, len1 = 19, len(name1)
    start2, len2 = start1+len(name1)+2, len(name2)
    start3, len3 = start2+len(name2)+3, len(name3)


    total_likes = res['data']['paging']['total']
    print("Latest names: " + name1, name2, name3, sep=", ")
    print("Total likes:", total_likes)

    # contruct post content
    postStr = "A huge shoutout to "+name1+", " +name2+ " & " +name3+ "!\\n\\nTotal number of reactions: "+str(total_likes)+" 🎉 \\n\\nTrying something new here, hopefully it will work 😅 \\n\\nThis post is alive 👻 and will show its gratitute to three most recent people who reacted. \\n\\n Want to try? ⌛ \\nLike the post and refresh it after few seconds. \\n\\n Details in the comment below 👇 "
    # print(postStr)

    
    if total_likes > prev_likes:   
        try:   
            # print("Updating the post...")
            data = '{"patch":{"$set":{"commentaryV2":{"text":"'+postStr+'","attributes":[{"type":"PROFILE_MENTION","start":'+str(start1)+',"length":'+str(len1)+',"normalizedProfileUrn":"'+profurn1+'","$type":"com.linkedin.voyager.common.TextAttribute"}, {"type":"PROFILE_MENTION","start":'+str(start2)+',"length":'+str(len2)+',"normalizedProfileUrn":"'+profurn2+'","$type":"com.linkedin.voyager.common.TextAttribute"}, {"type":"PROFILE_MENTION","start":'+str(start3)+',"length":'+str(len3)+',"normalizedProfileUrn":"'+profurn3+'","$type":"com.linkedin.voyager.common.TextAttribute"}],"$type":"com.linkedin.voyager.common.TextViewModel"}}}}'
            data = data.encode()
            response = requests.post('https://www.linkedin.com/voyager/api/contentcreation/normShares/'+thread2, headers=headers, data=data)
            response.raise_for_status()
            # print(response.text)
            # print("Post updated!")
        except:
            print("Some error occurred!")
    else:
        print("no new likes, skipping update")

    # so that api is not overused
    # print("Taking a 1 minute break...\n")
    time.sleep(60)
    print()
    prev_likes = total_likes
