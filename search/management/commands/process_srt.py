import os
import re
from django.core.management.base import BaseCommand
from search.srt_processing import srt_to_subtitles
from search.models import Show, Season, Episode

class Command(BaseCommand):
    help = "Process an SRT file and save subtitles to the database."

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help="Name of the .srt file (e.g., JohnOliver_S01E1.srt)")

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        show_title = "Last Week Tonight with John Oliver"  # Fixed title for this show
        srt_file_path = os.path.join('media', 'subtitles', filename)

        # Check if the file exists
        if not os.path.exists(srt_file_path):
            self.stderr.write(self.style.ERROR(f"File {srt_file_path} not found"))
            return

        # Extract season and episode numbers from filename (e.g., S01E1)
        match = re.search(r'S(\d{2})E(\d{1,2})', filename)
        if not match:
            self.stderr.write(self.style.ERROR("Filename must contain season and episode in the format SXXEXX"))
            return

        season_number = int(match.group(1))
        episode_number = int(match.group(2))

        # Get or create the show
        show, _ = Show.objects.get_or_create(title=show_title, release_date="2014-04-27")

        # Get or create the season
        season, _ = Season.objects.get_or_create(number=season_number, show=show)

        # Get or create the episode
        episode, _ = Episode.objects.get_or_create(
            title=f"Episode {episode_number}",
            season=season,
            show=show,
            release_date="2014-04-27"  # Replace with the correct date if available
        )

        # Process and save subtitles
        srt_to_subtitles(srt_file_path, episode.id)
        self.stdout.write(self.style.SUCCESS(f"Subtitles processed successfully for {filename}"))
