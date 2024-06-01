# UI to easily use Suno's Bark TTS model

This is a program to generate speech from text using [Suno's Bark](https://github.com/suno-ai/bark) text-to-speech model. The UI is made with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

The Bark TTS model is confined to short audio duration of about 13-14 seconds. To circumvent this the program is concatenating audio segments with the help of [Pydub](https://github.com/jiaaro/pydub).
The audio segments and the merged audio file are both saved in the selected output directory. You can choose from 10 different voice presets to read the text. Eventhough the Bark TTS model supports other languages as well, I've chosen English for now. I might add other languages and an option to choose them in the UI later.

<u><b>Be advised</b></u>, additionally to all the used Python libraries you need to install [PyTorch](https://github.com/jiaaro/pydub) for this program to work. 
The program is using the full version of Bark and thus you will need a GPU with at least 12GB of VRAM for this to function properly. 
As described on Bark's GitHub page, to use a smaller version of the models, which should fit into 8GB VRAM, set the environment flag `SUNO_USE_SMALL_MODELS=True`.

### UI view
![image](https://github.com/aretaleks/bark-tts-ui-app/assets/31519197/cb4a4411-5a53-4e1b-b81b-b3d90c1b32ff)

### Generated files
![image](https://github.com/aretaleks/bark-tts-ui-app/assets/31519197/b6e1fe07-29d6-427c-9faf-528e75f197d0)
