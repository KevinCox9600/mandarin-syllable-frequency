from bs4 import BeautifulSoup
import pickle
import requests

def scrape_data():
    def is_valid_row(row):
        return str(row)[0] in '0123456789'

    use_tone = True

    URL_SYLLABLE_TONE = 'https://lingua.mtsu.edu/chinese-computing/phonology/syllabletone.php'
    URL_SYLLABLE = 'https://lingua.mtsu.edu/chinese-computing/phonology/syllable.php'
    FILENAME_SYLLABLE_TONE = 'syllable_tone.pkl'
    FILENAME_SYLLABLE = 'syllable.pkl'

    SYLLABLE_INDEX = 1
    FREQ_INDEX = 2

    url = URL_SYLLABLE_TONE if use_tone else URL_SYLLABLE
    filename = FILENAME_SYLLABLE_TONE if use_tone else FILENAME_SYLLABLE

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("pre") 
        syllable_to_freq = {}
        for row in table.children:
            if is_valid_row(row):
                split_row = row.split('\t')
                syllable = split_row[SYLLABLE_INDEX]
                freq = split_row[FREQ_INDEX]

                syllable_to_freq[syllable] = int(freq)
    
    with open(filename, 'wb') as f: 
        pickle.dump(syllable_to_freq, f) 



def main():
    scrape_data()

if __name__ == '__main__':
    main()