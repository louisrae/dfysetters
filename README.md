<div align="center">
  <h3 align="center">Done For You Setters</h3>
  <p align="center">Back end code base for a sales-as-a-service business</p>
</div>

## About The Project

This project was created for the Done For You Setters team. It supports our switch from using humans to set, to using software. We are in the very early stages of the project, and we are focused primarily on tracking team numbers, along with standardising onboarding for both team and clients. We think that software is crucial to be able to scale our setting agency

Here's why:
* The quantity of high quality setters in the indsutry is low, meaning we are bottlenecked by talent
* A lot of the chat process for setters is repetitive, meaning once we have decided a good reply, we have to continue to make that decision every day
* Code is more reliable than humans, giving us consistency when tracking our numbers

### Built With

* [pandas](https://pandas.pydata.org)
* [gspread](https://docs.gspread.org/en/v5.2.0/)
* [pytest](https://docs.pytest.org/en/7.0.x/)

## Features

* Count how many facebook messages we missed in a given time frame
* Rank the team based on their key metrics
* Pull TC Booked Data for each client
* Pull TC Scheduled Data for each client
* Onboard new team members with one script

### Prerequisites

These are the things you need to use the software and how to install them. All of our software right now is DFY Setters specific, meaning you will need the below accounts for it to work correctly

* settersandspecialists.com G Suite Account
* Access to the CoachingSales.com Slack workspace

### Installation

1. `git clone https://github.com/louisrae/dfysetters`

2. `cd dfysetters`

3. `virtualenv venv`

4. `. venv/bin/activate`

5. `pip3 install -r requirements.txt`


## Usage

Rank all team members by metric

`leaderboard = Leaderboard(level_10_sheet)`

`weekly_totals = leaderboard.getWeekTotalFromLevel10()`

`rank_team_members = leaderboard.getSortedTCandSSNumbersForTeamMembers(role_list, weekly_totals)`

Invites team member to Slack channels based on pod

`team_member = get_row_of_database_based_on_name()` 

`user_id, channels = slack_data_setup(team_member)`

`client.conversations_invite(channel=channel, users=user_id)`

For more examples, please refer to the [Documentation](https://github.com/louisrae/dfysetters)

## Roadmap

- [] Release on PyPi
- [] Daily usage inside of the settersandspecialists organization
- [] Move client trackers to databases

See the [open issues](https://github.com/louisrae/dfysetters/issues) for a full list of proposed features (and known issues).


## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Louis-Rae - louisrae@settersandspecialists.com - Project Link: [https://github.com/louisrae/dfysetters_to_repo](https://github.com/louisrae/dfysetters)

## Acknowledgments

* [Shivam - For helping me write this](https://github.com/er1shivam)