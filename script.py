#CONVERTIR UNE VIDEO EN FICHIER AUDIO

import os
import openai
from moviepy.editor import VideoFileClip

# récupère toutes les vidéos dans le fichier videos
videos = os.listdir('videos')
audios = os.listdir('audios')

# pour chaque vidéo, extraire l’audio et mettez l’audio dans le dossier audio du même nom
for video in videos:
    video_name = os.path.splitext(video)[0]

    if video_name + '.mp3' in audios:
        continue

    video_path = f'videos/{video}'
    audio_path = f'audios/{video_name}.mp3'
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

# obtenir le « Fichier texte manquant » en comparant le dossier audio avec le dossier de sortie
# chaque vidéo doit être transcrite et le résultat doit être mis dans le dossier de sortie du même nom
audio_to_transcribe = os.listdir('audios')
output = os.listdir('output')

# supprimer l’audio de audio_to_transcribe s’il se trouve déjà dans le dossier de sortie
for audio in audio_to_transcribe:
    txt_name = os.path.splitext(audio)[0] + '.txt'
    if txt_name in output:
        audio_to_transcribe.remove(audio)

print(audio_to_transcribe)


# Chargez votre clé API à partir d’une variable d’environnement ou d’un service de gestion de secrets
openai.api_key = "votre clé API"

def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
    return transcription['text']

for audio_file in audio_to_transcribe:
    print("En cours de transcription : ", audio_file)

    result = transcribe_audio(f'audios/{audio_file}')
    txt_name = os.path.splitext(audio_file)[0] + '.txt'

    with open(f'output/{txt_name}', 'w') as txt_file:
        txt_file.write(result)