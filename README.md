## Tunisian Dialect Text-To-Speech

This project project was developed with the purpose of bridging the gap between high-resource and low-resource languages. Our main focus in creating this dataset is to work on a mono-speaker Tunisian dialect Text-to-Speech model. 

This repository contains all the scraping and pre-processing scripts for Tunisian TTS dataset. It contains also the two approaches described in the paper (from scratch and transfer learning). 


You can test our models in this [Huggingface space](https://huggingface.co/spaces/Elyadata/TunArTTS). Or you can train your models following the scripts provided in this repo.

### Steps : 
- First of all, you have to install the requirements : \
     `pip install -r requirements.txt`

- Then, You have to create the dataset following the scripts provided in `dataset_recreation`\
- Finally, you have to train the model either from scratch or using transfer learning technique as described in `espnet_experiments`.


If you use TunArTTS in your research, please cite it using the following BibTeX entry:

@inproceedings{TunArTTS,
    title = "TunArTTS: Tunisian Arabic Text-To-Speech Corpus",
    author = "Imen, Laouirine and Rami Kammoun  and Fethi BOUGARES",
    booktitle = "THE 2024 JOINT INTERNATIONAL CONFERENCE ON COMPUTATIONAL LINGUISTICS, LANGUAGE RESOURCES AND EVALUATION",
    month = mai,
    year = "2024",
    address = "TORINO, ITALIA",
    publisher = "European Language Resources Association",
    }
