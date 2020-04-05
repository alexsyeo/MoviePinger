# MoviePinger

A simple script that will automatically send you an email containing information regarding upcoming movies, including popularity, release date, and plot overview. Currently, it is automated by running Task Scheduler on Windows. (Could be automated on Mac/Linux through Crontab.) Users can simply edit the batch file if running on Windows.

The program expects three command line arguments: SENDER EMAIL ADDRESS, RECEIVER EMAIL ADDRESS, SENDER EMAIL PASSWORD (in that order). A user can use the same email address for both sender and receiver if they wish.
