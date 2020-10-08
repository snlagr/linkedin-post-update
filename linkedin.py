import requests, json, time

# this will be common for both fetching & editing
# may need to update after some time by capturing another manual request?
headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'csrf-token': 'ajax:6508858799033046130',
    'cookie': 'bcookie="v=2&d6f49f37-e92b-47ff-85c1-347e6cb73c60"; bscookie="v=1&20200701145032656ff920-baf6-41fe-8a60-81565fce7e23AQEKiAKRhpb18QWh8Q-oAVm025OOXUdq"; lissc=1; G_ENABLED_IDPS=google; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; g_state={"i_l":0}; liap=true; JSESSIONID="ajax:6508858799033046130"; spectroscopyId=fce90c96-c6d8-41df-8271-62f5a4196ac5; PLAY_LANG=en; _gcl_au=1.1.207071894.1599081027; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiIyZTQ5MzA5Ny00Y2I1LTQwYWYtYWQyYy0xNzBjMzU2M2ZkZWJ8MTU5NzA2NzExMyIsInJlY2VudGx5LXNlYXJjaGVkIjoiIiwicmVmZXJyYWwtdXJsIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJhaWQiOiIiLCJSTlQtaWQiOiJ8MCIsInJlY2VudGx5LXZpZXdlZCI6IiIsIkNQVC1pZCI6InDDk0BHdMKlXHUwMDFGVlwiwos2wrgqNWbDsiIsImZsb3dUcmFja2luZ0lkIjoiRVgvaVR2SGlUVHlCcisyaHNXZmdUZz09IiwiZXhwZXJpZW5jZSI6ImJyb3dzZSIsImlzX25hdGl2ZSI6ImZhbHNlIiwid2hpdGVsaXN0Ijoie30iLCJ0cmsiOiIifSwibmJmIjoxNjAyMTAyNjc1LCJpYXQiOjE2MDIxMDI2NzV9.5dB9Zs-rR6HfRfmuyQuD4DosNuhkjrAVQk18FM20vXw; li_at=AQEDASGHhFgBlbPUAAABdQTC4oIAAAF1KM9mglYAEPl7057xwHVEsOKeqtYhdKukZTBn2PgMDSMnhzroFF1e2b9BW1qqiXK9vMMJNARDI7955cl_0DN7p2kHlQyYKYpUmq7NIFFlzD2enAZLHVuhhDkd; lang=v=2&lang=en-us; lidc="b=OB68:s=O:r=O:g=2311:u=3:i=1602108717:t=1602153658:v=1:sig=AQFMaTogPg4aevbVkQAoz4MQRw-UFNFj"; transaction_state=AgFowyLXIXK2AAAAAXUFMFAFi7nlVlU5Sdhv69rrnp8EZoJF2sM4AfQ3R-FoTOOS07Fzuz4bljZ0_5OW28jfUtpkaWd2VFAq8afCB4fyGYF_IRQgwW20EIDfiFNqFGBievBZxZVUotSxqH-E8pzMnmJ_GEdIKF_a6pFxpdig24aXBjdAWB724sJeBaNCrZL2yYg_0ootPw; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-408604571%7CMCIDTS%7C18543%7CMCMID%7C10002714062377648578255546124531049272%7CMCOPTOUT-1602117065s%7CNONE%7CvVersion%7C4.6.0; UserMatchHistory=AQKWAycw1TNbVwAAAXUFOYz5ZlqT2HfkCIjuaE05xb5GPjzi_nHPVAQiX81aQbbVOeLXb_e6oSzxDsgOrX9oY7kH6sHyEC8p31K1PF4-o1-ZLaxWLsOwUJaJZrPNx1RhNZtDA35DbwxhGesyqV8h_m7fMSeS62_xkdOYOrT_WwDsW0jWJbzeUJ53h1Deu21cmDX6caDvNY6j9unqMjqyNyux64Z98aysD2DFeAzK9sM-',
}

# find this by manually & update for each post
threadUrn = 'urn:li:activity:6719956972214599680'
thread2 = 'urn:li:share:6719956971753230337'

# remember to update that activity number as per the post
params = (
    ('count', '3'),
    ('q', 'reactionType'),
    ('sortOrder', 'REV_CHRON'),
    ('start', '0'),
    ('threadUrn', threadUrn),
)

while True:
    # extract latest liked person's name
    print("Finding new likes...")
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
    print("Latest names: " + name1, name2, name3, sep=",")
    print("Total likes:", total_likes)

    # contruct post content
    postStr = "A huge shoutout to "+name1+", " +name2+ " & " +name3+ "!\\n\\nTotal number of likes: "+str(total_likes)+" \xF0\x9F\x8E\x89 \\n\\nTrying something new here, hopefully it will work \xF0\x9F\x98\x85 \\n\\nThis post is alive \xF0\x9F\x91\xBB and will show its gratitute to three most recent people who liked it. \\n\\n Want to try? \xE2\x8C\x9B \\nLike the post and refresh it after few seconds. \\n\\n Details in the comment below \xF0\x9F\x91\x87 "
    # print(postStr)

   
    try:   
        print("Updating the post...")
        data = '{"patch":{"$set":{"commentaryV2":{"text":"'+postStr+'","attributes":[{"type":"PROFILE_MENTION","start":'+str(start1)+',"length":'+str(len1)+',"normalizedProfileUrn":"'+profurn1+'","$type":"com.linkedin.voyager.common.TextAttribute"}, {"type":"PROFILE_MENTION","start":'+str(start2)+',"length":'+str(len2)+',"normalizedProfileUrn":"'+profurn2+'","$type":"com.linkedin.voyager.common.TextAttribute"}, {"type":"PROFILE_MENTION","start":'+str(start3)+',"length":'+str(len3)+',"normalizedProfileUrn":"'+profurn3+'","$type":"com.linkedin.voyager.common.TextAttribute"}],"$type":"com.linkedin.voyager.common.TextViewModel"}}}}'
        response = requests.post('https://www.linkedin.com/voyager/api/contentcreation/normShares/'+thread2, headers=headers, data=data)
        response.raise_for_status()
        # print(response.text)
        print("Post updated!")
    except:
        print("Some error occurred! Emoji in name?")


    # so that api is not overused
    print("Taking a 2 minute break...\n")
    time.sleep(120)