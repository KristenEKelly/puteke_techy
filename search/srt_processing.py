import pysrt
from .models import Subtitle, Episode
from django.contrib.postgres.search import SearchVector

def srt_to_subtitles(srt_file_path, episode_id):
    """
    Process an .srt file and save each subtitle entry to the Subtitle model
    for a specific episode, then update the search vector.
    """
    # Load the SRT file using pysrt
    subs = pysrt.open(srt_file_path)

    # Get the episode instance
    episode = Episode.objects.get(id=episode_id)

    # List to hold subtitle instances
    subtitle_instances = []

    # Loop through each subtitle entry and prepare for database insertion
    for sub in subs:
        subtitle_instance = Subtitle(
            episode=episode,
            language='en',  # You can customize this as needed
            text=sub.text
        )
        subtitle_instances.append(subtitle_instance)

    # Bulk create subtitle entries
    Subtitle.objects.bulk_create(subtitle_instances)

    # Update search vector for each subtitle entry
    Subtitle.objects.filter(episode=episode).update(search_vector=SearchVector('text'))

    print(f"Successfully processed and saved subtitles for episode {episode_id}")
