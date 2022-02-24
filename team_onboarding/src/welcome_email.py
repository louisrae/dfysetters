"""This module generates an email that we can send to the new team member"""


def email_setup(df):
    """Generates the email to be sent

    Args:
        df (dataframe): Single row dataframe with the data of the employee who
        needs to be followed up with

    Returns:
        tuple: email address to send to, subject line of email, body of email
    """

    email_address = df["company_email"][0]

    slack_link = input("What is the manual invite link you generated? ")

    subject = "Congratulations!"

    body = f"""{df["full_name"][0]},

    Congratulations and welcome to Setters&Specialists! We've decided to bring you on board as our new {df["company_role"][0]}. We're excited to have you and can't wait for you to start!

    As discussed, here are the terms of your employment:

    Rate: {df["pay_per_client"][0]} USD per client (OTE: 3k)

    Hours: 9-5 CST but performance is more important

    Working days: Monday - Friday

    Before we move to the onboarding process, please complete the following right away:

    Join Our Asana Workspace (Link In Email)

    Join our Slack channel ({slack_link})

    Watch Asana Initial Video (In Onboarding Project in Asana)

    An Asana and Slack Invite have been sent to {df["company_email"][0]}, please confirm once you have this.

    We cannot move forward until the above 2 tasks are complete. :)

    We're looking at about three days for general onboarding. After that, you'll move to your department, where you'll start role-specific training.

    Please let me know if you have any questions.

    Again, Welcome to Setters&Specialists! :)

    Setters & Specialists Ltd"""

    return email_address, subject, body
