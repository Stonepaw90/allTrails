import requests
#import re
import pandas as food
import plotly.express as px
import streamlit as st
import time
from datetime import datetime, timedelta
from fake_useragent import UserAgent

def get_info_from_one_map(map_dict):
    id = map_dict["id"]
    name = map_dict["name"]
    time_created = map_dict["created_at"]
    ret_dict = {"ID" :id,
                "name": name,
                "time_created":time_created}

    if "location" in map_dict.keys()and map_dict["location"] is not None:
        location = (map_dict["location"]["longitude"], map_dict["location"]["latitude"])
        ret_dict["location"] = location
    if "activity" in map_dict.keys() and map_dict["activity"] is not None:
        type1 = map_dict["activity"]["name"]
        type2 = map_dict["activity"]["uid"]
        ret_dict["type1"] = type1
        ret_dict["type2"] = type2
    if "summaryStats" in map_dict.keys() and map_dict["summaryStats"] is not None:
        time_taken = map_dict["summaryStats"]["timeMoving"] #time in seconds
        distance = map_dict["summaryStats"]["distanceTotal"] #distance in meters
        miles = distance/(1000*1.60934)
        speed = map_dict["summaryStats"]["speedAverage"] #distance/Time in mps
        pace = map_dict["summaryStats"]["paceAverage"]  #Time/distance in seconds per meter
        #desired is mile pace - seconds per mile
        pace_spm = pace * 1000 * 1.60934 #pace in seconds per mile
        dm = divmod(pace_spm, 60)
        mile_pace_string = f"{round(dm[0])}:{round(dm[1])}"
        ret_dict["pace"] = pace_spm
        ret_dict["time_taken"] = time_taken
        ret_dict["miles"] = miles
        ret_dict["mile_pace_string"] = mile_pace_string

    for key in ["ID", "name", "time_created", "location", "type1", "type2","pace", "time_taken", "miles", "mile_pace_string"]:
        if key not in ret_dict.keys():
            ret_dict[key] = ""

    return ret_dict

def random_from_list(input_list):
    return(list(food.DataFrame(input_list).sample(1)[0])[0])
def get_df_from_users_requests_get(maps_list):
    json_dict = maps_list.json()
    list_of_maps = [get_info_from_one_map(map_dict) for map_dict in json_dict["maps"]]
    df = food.DataFrame(list_of_maps, columns = ["ID", "name", "time_created", "location", "type1", "type2", "pace", "time_taken", "miles", "mile_pace_string"])
    return(df)

def get_df_from_user_id(user_id = "30079005"):
    params = {
        'limit': '100',
        'presentation_type': 'track',
    }

    cookies = {
        'Path': '/',
        'osano_consentmanager_uuid': '97229f76-b17c-4443-8b79-1e136c234c5a',
        'osano_consentmanager': 'gsJg0C5oy315NAuJ0p6dUm4GQ4gQZ3p7yXlTMTXzmuNAOsYSDiGT7bwR53MeTJL4TU-r69PJ2ohH0uVOvvvpXiWoD3BEqawA4nooaovg9r50I5FuOZyzsojWqXtXcz70RxMcGqgSOVyPrnuctazA5XhIvtvAskW1ysQPPELsISVMUKxqkLPTWKtOncwGIYDq1JziF3mF3GZg9ShdhIObq7ATZmX5it6RjRG2y30NJaW0C5h_hDeQHBCw-XgVPWm5p2pdrjAerukK5rWsq8zshoghtJdWROOZv2Rs1Q==',
        'G_AUTHUSER_H': '0',
        '_auth_token': 'JCRjipmRVe_LnsE2DjyB',
        'amp_6ad463': '_iiIrY-6uNgzutBRK5r_b8.NDAwMzgyMTI=..1h9r2t1g2.1h9r2t1g4.a.6.g',
        '_ga_V6WJN779TY': 'GS1.1.1694199870.1.1.1694199875.0.0.0',
        '_alltrails_session': 'bFdNemI4TC8ybVN2QnBpQlJNVzFXRjFQd3BRK1A0QnMxUFhaVU5leWFYbk9VZTJGRU90b1h5WVBpZXovVTFJeTNKakNYYVc3MVFkeG5DUVBBRDhEZnhZTG1KL0p6TStUN3NhdlQ4M3RaM0g5UkkwT08vVnZCalR0MkdCVFFkN3dyWTlMbnlnY2pkWHh2bDg2Zi9mYVloejQzTFdmTzJkSllOZThPY2cxNjZpNFVCQlJCSDhiUjdVRUE5WjFIdzg3OHcyS2IyTWJFT3B5bGdkcGk0dHowdCthL3VXdzduZDQvSXY0cmZzNjdxV2ZxNU9vVzFFUUpMUlJIZSt0UGcvS2NMY0pqTWlwVGs2akFBNFBUWlJiNStPMm1WL21HeDB1eDdSaGQrdmZBcU5DRGlCeUExcWVseEZwTng4Z2huS25LYXNBUjVzT1RwZ1M0Mm1QZGxFb2Voci92VysvYUVJL3JMQnF0TWwrTmM3anZQbktSeS95dmZ6WldjYS8wdGdxbElLcXYxZ2Zkak5OSm1qNUpLcHBLcjlySUgxeVhrMWFIRG42M2V2TjRkeVhjamUxUnpHaWo5dlBTSkx0RStxTW1QcW1mOGVJei8rOVBsNEZWbytTVmhkdm5Zb2JFTzVkdStWN1daVkJIcXhYK29zODRZb3loMTRXdG16SUg0SFEtLW9xanhXZlZ1aVdCZGtEbWMreWhteEE9PQ%3D%3D--e78bbc93ee2c61de06c65d1eb066d8277768d3f0',
        'datadome': '5-d2Cx25gcX4MXFCOoCsWxUzTT-ZyMiBMf0QoFGHxJja1tY1FaGTSfQFNvvOKKg1uhN7r8GmYUwBi7IyYtdmMi2bKBWtHrao9TM_96kHKPaEA0oiQ0~7kccKPHuv6bh6',
    }
    refers = ["https://www.alltrails.com/members/bobthebuilder05/reviews", "https://www.alltrails.com/members/addie-brendel/completed",
              "https://www.alltrails.com/members/priscilla-anne-1", "https://www.alltrails.com/members/max-porter-3/photos",
              "https://www.alltrails.com/members/samuel-szabo/lists", "https://www.alltrails.com/members/felix-ackerman/recordings",
              "https://www.alltrails.com/members/sydney-cooney-1/stats/achievements", "https://www.alltrails.com/members/doug-davis-49/recordings",
              "https://www.alltrails.com/members/miranda-leigh-sannino/recordings", 'https://www.alltrails.com/members/drew-t-12/recordings']
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'Path=/; Path=/; osano_consentmanager_uuid=97229f76-b17c-4443-8b79-1e136c234c5a; osano_consentmanager=gsJg0C5oy315NAuJ0p6dUm4GQ4gQZ3p7yXlTMTXzmuNAOsYSDiGT7bwR53MeTJL4TU-r69PJ2ohH0uVOvvvpXiWoD3BEqawA4nooaovg9r50I5FuOZyzsojWqXtXcz70RxMcGqgSOVyPrnuctazA5XhIvtvAskW1ysQPPELsISVMUKxqkLPTWKtOncwGIYDq1JziF3mF3GZg9ShdhIObq7ATZmX5it6RjRG2y30NJaW0C5h_hDeQHBCw-XgVPWm5p2pdrjAerukK5rWsq8zshoghtJdWROOZv2Rs1Q==; Path=/; G_AUTHUSER_H=0; _auth_token=JCRjipmRVe_LnsE2DjyB; amp_6ad463=_iiIrY-6uNgzutBRK5r_b8.NDAwMzgyMTI=..1h9r2t1g2.1h9r2t1g4.a.6.g; _ga_V6WJN779TY=GS1.1.1694199870.1.1.1694199875.0.0.0; _alltrails_session=bFdNemI4TC8ybVN2QnBpQlJNVzFXRjFQd3BRK1A0QnMxUFhaVU5leWFYbk9VZTJGRU90b1h5WVBpZXovVTFJeTNKakNYYVc3MVFkeG5DUVBBRDhEZnhZTG1KL0p6TStUN3NhdlQ4M3RaM0g5UkkwT08vVnZCalR0MkdCVFFkN3dyWTlMbnlnY2pkWHh2bDg2Zi9mYVloejQzTFdmTzJkSllOZThPY2cxNjZpNFVCQlJCSDhiUjdVRUE5WjFIdzg3OHcyS2IyTWJFT3B5bGdkcGk0dHowdCthL3VXdzduZDQvSXY0cmZzNjdxV2ZxNU9vVzFFUUpMUlJIZSt0UGcvS2NMY0pqTWlwVGs2akFBNFBUWlJiNStPMm1WL21HeDB1eDdSaGQrdmZBcU5DRGlCeUExcWVseEZwTng4Z2huS25LYXNBUjVzT1RwZ1M0Mm1QZGxFb2Voci92VysvYUVJL3JMQnF0TWwrTmM3anZQbktSeS95dmZ6WldjYS8wdGdxbElLcXYxZ2Zkak5OSm1qNUpLcHBLcjlySUgxeVhrMWFIRG42M2V2TjRkeVhjamUxUnpHaWo5dlBTSkx0RStxTW1QcW1mOGVJei8rOVBsNEZWbytTVmhkdm5Zb2JFTzVkdStWN1daVkJIcXhYK29zODRZb3loMTRXdG16SUg0SFEtLW9xanhXZlZ1aVdCZGtEbWMreWhteEE9PQ%3D%3D--e78bbc93ee2c61de06c65d1eb066d8277768d3f0; datadome=5-d2Cx25gcX4MXFCOoCsWxUzTT-ZyMiBMf0QoFGHxJja1tY1FaGTSfQFNvvOKKg1uhN7r8GmYUwBi7IyYtdmMi2bKBWtHrao9TM_96kHKPaEA0oiQ0~7kccKPHuv6bh6',
        'If-None-Match': 'W/"f084e80dc858e9fafb25c376f371baa2"',
        'Referer': "NA",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': "NA",
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-AT-CALLER': 'Mugen',
        'X-AT-KEY': '3p0t5s6b5g4g0e8k3c1j3w7y5c3m4t8i',
        'X-CSRF-TOKEN': 'undefined',
        'X-Language-Locale': 'en-US',

    }

    attempts_made = 0
    while attempts_made < 3:
        headers["Referer"] = random_from_list(refers)
        headers["User-Agent"] = UserAgent().random
        maps_list = requests.get(
            #https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja
            f'https://www.alltrails.com/api/alltrails/users/{user_id}/maps',
            # 30079005 (drew) #18994746 (2 activity guy) #439118773
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False#,
            #proxies = {'http': 'http://95.154.198.201'}
                       #"https": 'https://95.154.198.201'} # https://free-proxy-list.net/
        )
        if maps_list.status_code != 403:
            df = get_df_from_users_requests_get(maps_list)
            return df
        attempts_made += 1
        st.write(f"Attempt #{attempts_made} Failure. Details:\nUser ID: {user_id}\n Referer: {headers['Referer']}\nUser Agent: {headers['User-Agent']}")
        time.sleep(random_from_list([0.5002, 1.0021, 3.0011, 6.013, 11.022]))
    st.error(PermissionError(f"Failure to access details for {user_id}."))
    exit()


def get_fig_from_id(id):
    df = get_df_from_user_id(id)
    df["date_string"] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y at %I:%M%p") for date in
                         df["time_created"]]
    df["is_weekend"] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%a") in ["Sat", "Sun"] for date in
                        df["time_created"]]
    df["datetime"] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for date in
                      df["time_created"]]

    fig = px.scatter(df,
                     x="miles", y="pace", color="is_weekend",  # color = "datetime",
                     custom_data=["date_string", "mile_pace_string", "time_taken"]
                     )
    fig.update_traces(
        hovertemplate='<b>Time of Hike</b>: %{customdata[0]}<br>' +
                      '<b>Pace</b>: %{customdata[1]}<br>' +
                      '<b>Time Taken</b>: %{customdata[2]}<br>' +
                      '<extra></extra>'
    )
    fig.update_layout(title="AllTrails Pace vs. Milage",
                      xaxis={'title': 'Miles'},
                      yaxis={'title': 'Pace (Seconds Per Mile)'},
                      )
    return fig

def get_fig_from_df(df):
    df["date_string"] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y at %I:%M%p") for date in
                         df["time_created"]]
    df["is_weekend"] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%a") in ["Sat", "Sun"] for date in
                        df["time_created"]]
    df["datetime"] = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for date in
                      df["time_created"]]
    #df["pace_datetime"] = [datetime.strptime(pace, "%Y-%m-%dT%H:%M:%SZ") for pace in df["pace"]]
    df["pace_datedelta"] = [timedelta(seconds = pace) for pace in df["pace"]]
    #pace_string = []
    #pace_datetime = []
    #for pace in df["pace"]:
    #    if pace > 3600:
    #        minutes, seconds = divmod(pace, 60)
    #        hours, minutes = divmod(minutes, 60)
    #        pace_string.append(f"{hours}:{minutes:02}:{seconds:02}")
    #        pace_datetime.append(f"{hours}:{minutes.2f}:{seconds.2f}")
    #    else
    #        minutes, seconds = divmod(pace, 60)
    #        pace_string.append(f"{minutes:02}:{seconds:02}")
    #pace_datetime = []

    fig = px.scatter(df,
                     x="miles", y=df["pace_datedelta"]+ food.to_datetime('1970/01/01'), color="is_weekend",  # color = "datetime",
                     custom_data=["date_string", "mile_pace_string", "time_taken"]
                     )
    fig.update_traces(
        hovertemplate='<b>Time of Hike</b>: %{customdata[0]}<br>' +
                      '<b>Pace</b>: %{customdata[1]}<br>' +
                      '<b>Time Taken</b>: %{customdata[2]}<br>' +
                      '<extra></extra>'
    )
    fig.update_layout(title="AllTrails Pace vs. Milage",
                      xaxis={'title': 'Miles'},
                      yaxis={'title': 'Pace (Seconds Per Mile)'},
                      yaxis_tickformat = "%H:%M:%S"
                      )
    return fig


def main():
    st.set_page_config(page_title="Alltrails Mileage and Pacing", layout="wide")
    st.title("AllTrails Mileage and Pacing")
    st.markdown("### Coded by Abraham Holleran :sunglasses:")

    activity_options = ["Hiking", "Mountain biking", "Running", "Road biking",
                        "Backpacking", "Walking", "OHV/Off-road driving", "Scenic driving",
                        "Bike Touring", "Snowshoeing", "Cross-country skiing",
                        "Skiing", "Paddle sports", "Camping", "Fishing", "Bird watching",
                        "Horseback riding", "Rock climbing", "Via ferrata"]
    user_list = ["38485383", "6597282", "69037412", "5624674", "61300094", "65720818", "19450700", "36307315", "49203513"] #"40038212",

    user_id = st.text_input("Enter the ID for the user to plot for.", value = random_from_list(user_list))
    user_activities = st.multiselect("Which activities are you interested in?", options = activity_options, default = activity_options)
    df = get_df_from_user_id(user_id)
    if(len(user_activities) > 0):
        #df1 = df[(df.type1 in user_activities) | (df.type2 in user_activities)]
        df1 = df.copy()[(df["type1"].isin(user_activities)) | (df["type2"].isin(user_activities))]

        fig = get_fig_from_df(df1)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Select an activity to plot your pace.")

if __name__ == "__main__":
    main()
