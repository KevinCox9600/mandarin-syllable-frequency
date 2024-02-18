from bs4 import BeautifulSoup
import pickle
import requests

USE_TONE = True

URL_SYLLABLE_TONE = 'https://lingua.mtsu.edu/chinese-computing/phonology/syllabletone.php'
URL_SYLLABLE = 'https://lingua.mtsu.edu/chinese-computing/phonology/syllable.php'
FILENAME_SYLLABLE_TONE = 'syllable_tone.pkl'
FILENAME_SYLLABLE = 'syllable.pkl'

filename = FILENAME_SYLLABLE_TONE if USE_TONE else FILENAME_SYLLABLE

def scrape_data():
    """Scrape data from website table."""
    def is_valid_row(row):
        return str(row)[0] in '0123456789'

    SYLLABLE_INDEX = 1
    FREQ_INDEX = 2

    url = URL_SYLLABLE_TONE if USE_TONE else URL_SYLLABLE

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("pre") 
        syllable_to_count = {}
        for row in table.children:
            if is_valid_row(row):
                split_row = row.split('\t')
                syllable = split_row[SYLLABLE_INDEX]
                freq = split_row[FREQ_INDEX]

                syllable_to_count[syllable] = int(freq)
    
    with open(filename, 'wb') as f: 
        pickle.dump(syllable_to_count, f) 

def analyze_data():
    """Generate sorted list of frequencies by syllable."""
    with open(filename, 'rb') as f:
        syllable_to_count = pickle.load(f)
        
        total = 0
        for count in syllable_to_count.values():
            total += count

        syllable_to_freq = {}
        for syllable, count in syllable_to_count.items():
            syllable_to_freq[syllable] = count / total
        
        items = syllable_to_freq.items()
        sorted_freqs = sorted(items, key=lambda x: x[1], reverse=True)

        return sorted_freqs


def display_data():
    pass


def main():
    analyze_data()

if __name__ == '__main__':
    main()