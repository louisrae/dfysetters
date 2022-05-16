### Other
SPECIALIST_NAME = "Tylee Evans Groll"
SCHEDULE_ONCE_HEADERS = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}
SCHEDULE_ONCE_URL = (
    "https://api.oncehub.com/v2/bookings?expand=booking_page&limit=100"
)

### Google Sheets
DAILY_KPIS_URL = "https://docs.google.com/spreadsheets/d/18AgIMFyPCOxHYQXRYJowihJd_i2kRMB9pzB5jdA3ZVc/edit#gid=1070219116"
MESSAGE_DATA_WORKBOOK = "https://docs.google.com/spreadsheets/d/1ilUCdcEP-TDUMrC8Alwp2x3Jq2LYfOzINFfF2MTY91k/edit#gid=1232583697"
LEVEL_10_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"
APPOINTMENTS_SET_URL = "https://docs.google.com/spreadsheets/d/191VOLxOdD-yDSUa4_qeHiDg2HoZ7cu0Ai3bSN9UkPQw/edit#gid=1189654778"
NEW_DAILY_KPIS_URL = "https://docs.google.com/spreadsheets/d/1DxaeFkk6A56X-DOoCKQWdYrBk4jOoNpX4nDsR5OXrc0/edit#gid=0"
EXPORTS_URL = "https://docs.google.com/spreadsheets/d/1Gp2o7KUmWMcd7zJTLreecyvFTMRQnIzJ7vekrGGRcJ8/edit#gid=771905595"
TOTALS_TRACKER_URL = "https://docs.google.com/spreadsheets/d/1V5F60V0QVR5EG2IRmRAqP9XhDnmiuvuXjaqQh_NveHI/edit#gid=0"


### Slack Channels
SETTERS_TEAM_ID = "C0199AXJC80"
CLIENT_REPORTS_ID = "C01GHC2Q3GC"
SETTERS_ID = "C02GCRKL19Q"
SPECIALISTS_ID = "C02LHKV5UKG"
LEVEL_5_ID = "C02SXKE5S6R"
SFU_ID = "C033T3PTU30"
PURPLE_ID = "C02SXVC9PE3"
GIRLS_ID = "C026GHAF3A5"
SCRUMTEAM_ID = "C01K8EK5VJ4"

### Credentials
GCAL_EMAIL_LOUISRAE = "louisrae@settersandspecialists.com"


### Checking Sales Data
MONTH_NUMBER_WEEK_AGO = 1
DAY_NUMBER_WEEK_AGO = 1

### Checking Close
APP_SET_SHEET_URL = "https://docs.google.com/spreadsheets/d/1hznTOKg-8MLcYrt0sW-Chy674JeosjSJyJo8_WbS-zE/edit#gid=790164004"
CLOSE_METRICS = [
    "calls.outbound.all.count",
    "sms.sent.all.count",
    "emails.sent.all.count",
    "emails.opened.all.count",
    "emails.sent.manual_with_reply.count",
    "sms.received.all.count",
    "leads.contacted.all.count",
]
### COLUMN NAMES

PERCENTAGE_COLUMNS = {
    "fb_group_columns": [
        {
            "column_name": "fb_group_reach_out_to_replies_pc",
            "small_metric": "fb_group_reach_outs",
            "large_metric": "fb_group_replies",
        },
        {
            "column_name": "fb_group_replies_to_tc_booked_pc",
            "small_metric": "fb_group_replies",
            "large_metric": "fb_group_tc_booked",
        },
        {
            "column_name": "fb_group_tc_scheduled_to_tc_taken_pc",
            "small_metric": "fb_group_tc_scheduled",
            "large_metric": "fb_group_tc_taken",
        },
        {
            "column_name": "fb_group_tc_taken_to_ss_booked_pc",
            "small_metric": "fb_group_tc_taken",
            "large_metric": "fb_group_ss_booked",
        },
    ],
    "ghl_columns": [
        {
            "column_name": "ghl_replies_to_tc_booked_pc",
            "small_metric": "ghl_replies",
            "large_metric": "ghl_tc_booked",
        },
        {
            "column_name": "ghl_tc_scheduled_to_tc_taken_pc",
            "small_metric": "ghl_tc_scheduled",
            "large_metric": "ghl_tc_taken",
        },
        {
            "column_name": "ghl_tc_taken_to_ss_booked_pc",
            "small_metric": "ghl_tc_taken",
            "large_metric": "ghl_ss_booked",
        },
    ],
    "email_columns": [
        {
            "column_name": "email_replies_to_tc_booked_pc",
            "small_metric": "email_replies",
            "large_metric": "email_tc_booked",
        },
        {
            "column_name": "email_tc_scheduled_to_tc_taken_pc",
            "small_metric": "email_tc_scheduled",
            "large_metric": "email_tc_taken",
        },
        {
            "column_name": "email_tc_taken_to_ss_booked_pc",
            "small_metric": "email_tc_taken",
            "large_metric": "email_ss_booked",
        },
    ],
    "fb_page_columns": [
        {
            "column_name": "fb_page_replies_to_tc_booked_pc",
            "small_metric": "fb_page_replies",
            "large_metric": "fb_page_tc_booked",
        },
        {
            "column_name": "fb_page_tc_scheduled_to_tc_taken_pc",
            "small_metric": "fb_page_tc_scheduled",
            "large_metric": "fb_page_tc_taken",
        },
        {
            "column_name": "fb_page_tc_taken_to_ss_booked_pc",
            "small_metric": "fb_page_tc_taken",
            "large_metric": "fb_page_ss_booked",
        },
    ],
    "inbound_triage_columns": [
        {
            "column_name": "inbound_triage_tc_scheduled_to_tc_taken_pc",
            "small_metric": "inbound_triage_tc_scheduled",
            "large_metric": "inbound_triage_tc_taken",
        },
        {
            "column_name": "inbound_triage_tc_taken_to_ss_booked_pc",
            "small_metric": "inbound_triage_tc_taken",
            "large_metric": "inbound_triage_ss_booked",
        },
    ],
    "outbound_dials_columns": [
        {
            "column_name": "outbound_dials_call_to_connection_pc",
            "small_metric": "outbound_dials_calls",
            "large_metric": "outbound_dials_connections",
        },
        {
            "column_name": "outbound_dials_connection_to_tc_booked_pc",
            "small_metric": "outbound_dials_connections",
            "large_metric": "outbound_dials_tc_booked",
        },
        {
            "column_name": "outbound_dials_connection_to_ss_booked_pc",
            "small_metric": "outbound_dials_connections",
            "large_metric": "outbound_dials_ss_booked",
        },
        {
            "column_name": "outbound_dials_tc_scheduled_to_tc_taken_pc",
            "small_metric": "outbound_dials_tc_scheduled",
            "large_metric": "outbound_dials_tc_taken",
        },
        {
            "column_name": "outbound_dials_tc_taken_to_ss_booked_pc",
            "small_metric": "outbound_dials_tc_taken",
            "large_metric": "outbound_dials_ss_booked",
        },
    ],
}


ORDERED_COLUMNS = [
    "fb_group_reach_outs",
    "fb_group_reach_out_to_replies_pc",
    "fb_group_replies",
    "fb_group_replies_to_tc_booked_pc",
    "fb_group_tc_booked",
    "fb_group_tc_scheduled",
    "fb_group_tc_scheduled_to_tc_taken_pc",
    "fb_group_tc_taken",
    "fb_group_tc_taken_to_ss_booked_pc",
    "fb_group_ss_booked",
    "ghl_replies",
    "ghl_replies_to_tc_booked_pc",
    "ghl_tc_booked",
    "ghl_tc_scheduled",
    "ghl_tc_scheduled_to_tc_taken_pc",
    "ghl_tc_taken",
    "ghl_tc_taken_to_ss_booked_pc",
    "ghl_ss_booked",
    "email_replies",
    "email_replies_to_tc_booked_pc",
    "email_tc_booked",
    "email_tc_scheduled",
    "email_tc_scheduled_to_tc_taken_pc",
    "email_tc_taken",
    "email_tc_taken_to_ss_booked_pc",
    "email_ss_booked",
    "fb_page_replies",
    "fb_page_replies_to_tc_booked_pc",
    "fb_page_tc_booked",
    "fb_page_tc_scheduled",
    "fb_page_tc_scheduled_to_tc_taken_pc",
    "fb_page_tc_taken",
    "fb_page_tc_taken_to_ss_booked_pc",
    "fb_page_ss_booked",
    "outbound_dials_calls",
    "outbound_dials_call_to_connection_pc",
    "outbound_dials_connections",
    "outbound_dials_connection_to_tc_booked_pc",
    "outbound_dials_tc_booked",
    "outbound_dials_tc_scheduled",
    "outbound_dials_tc_scheduled_to_tc_taken_pc",
    "outbound_dials_tc_taken",
    "outbound_dials_tc_taken_to_ss_booked_pc",
    "outbound_dials_ss_booked",
    "outbound_dials_connection_to_ss_booked_pc",
    "inbound_triage_tc_scheduled",
    "inbound_triage_tc_scheduled_to_tc_taken_pc",
    "inbound_triage_tc_taken",
    "inbound_triage_tc_taken_to_ss_booked_pc",
    "inbound_triage_ss_booked",
]

### COLUMNS WITH A1 NOTATION
PERCENT_COLUMNS = [
    "C2:C",
    "E2:E",
    "H2:H",
    "J2:J",
    "M2:M",
    "P2:P",
    "R2:R",
    "U2:U",
    "X2:X",
    "Z2:Z",
    "AC2:AC",
    "AF2:AF",
    "AH2:AH",
    "AK2:AK",
    "AM2:AM",
    "AP2:AP",
    "AR2:AR",
    "AT2:AT",
    "AV2:AV",
    "AX2:AX",
]

NON_PERCENT_COLUMNS = [
    "b1:b",
    "d1:D",
    "f1:f",
    "g1:g",
    "i1:i",
    "k1:k",
    "l1:l",
    "n1:n",
    "o1:o",
    "q1:q",
    "s1:s",
    "t1:t",
    "v1:v",
    "w1:w",
    "y1:y",
    "aa1:aa",
    "ab1:ab",
    "ad1:ad",
    "ae1:ae",
    "ag1:ag",
    "ai1:ai",
    "aj1:aj",
    "al1:al",
    "an1:an",
    "ao1:ao",
    "aq1:aq",
    "as1:as",
    "au1:au",
    "aw1:aw",
    "ay1:ay",
    "az1:az",
    "ba1:ba",
]

HEADER_COLUMNS = "A1:BA1"
WHOLE_SHEET = "A1:BA"
DATE = "A2:A"

FACEBOOK_END_COLUMN = "K1:K"
GHL_END_COLUMN = "S1:S"
EMAIL_END_COLUMN = "AA1:AA"
FB_PAGE_END_COLUMN = "AI1:AI"
OUTBOUND_END_COLUMN = "AT1:AT"
INBOUND_END_COLUMN = "AY1:AY"

ALL_END_COLUMNS = [
    FACEBOOK_END_COLUMN,
    GHL_END_COLUMN,
    EMAIL_END_COLUMN,
    FB_PAGE_END_COLUMN,
    OUTBOUND_END_COLUMN,
    INBOUND_END_COLUMN,
]

FB_TITLES = "B1:K1"
GHL_TITLES = "L1:S1"
EMAIL_TITLES = "T1:AA1"
FB_PAGE_TITLES = "AB1:AI1"
OUTBOUND_DIALS_TITLES = "AJ1:AT1"
INBOUND_TRIAGE_TITLES = "AU1:AY1"

### Databases
PATH_TO_DATABASE_FILE = "/Library/PostgreSQL/14/bin/Database/"
